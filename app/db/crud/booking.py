from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from db.models import Booking, FitnessClass
from schemas import BookingCreate
from crud.fitness_class import has_available_slots, decrement_available_slots


class ClassNotFoundError(Exception):
    pass


class ClassFullError(Exception):
    pass


class DuplicateBookingError(Exception):
    pass


def get_booking(db: Session, booking_id: int) -> Optional[Booking]:
    return db.query(Booking).filter(Booking.id == booking_id).first()


def get_bookings_by_user(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[Booking]:
    return (
        db.query(Booking)
        .filter(Booking.user_id == user_id)
        .order_by(Booking.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_bookings_for_class(db: Session, class_id: int) -> List[Booking]:
    return db.query(Booking).filter(Booking.class_id == class_id).all()


def create_booking(db: Session, obj_in: BookingCreate, user_id: int) -> Booking:
    """
    Books a slot for the given user, guarding against overbooking and
    duplicate bookings (same email, same class).

    Raises ClassNotFoundError / ClassFullError / DuplicateBookingError on
    failure; the caller (route handler) maps these to HTTP status codes.
    """
    # Row lock on the class so two concurrent requests for the last slot
    # can't both pass the availability check (no-op on SQLite, real lock
    # on Postgres/MySQL).
    fitness_class = (
        db.query(FitnessClass)
        .filter(FitnessClass.id == obj_in.class_id)
        .with_for_update()
        .first()
    )
    if fitness_class is None:
        raise ClassNotFoundError(f"Class {obj_in.class_id} not found")

    if not has_available_slots(fitness_class):
        raise ClassFullError(f"Class {obj_in.class_id} has no available slots")

    db_obj = Booking(
        class_id=obj_in.class_id,
        user_id=user_id,
        client_name=obj_in.client_name,
        client_email=obj_in.client_email,
    )
    db.add(db_obj)
    decrement_available_slots(db, fitness_class)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateBookingError(
            f"{obj_in.client_email} has already booked class {obj_in.class_id}"
        )

    db.refresh(db_obj)
    return db_obj


def cancel_booking(db: Session, db_obj: Booking) -> Booking:
    """Marks a booking inactive and returns the slot to the class."""
    if db_obj.is_active:
        db_obj.fitness_class.available_slots += 1
        db.add(db_obj.fitness_class)
    db_obj.is_active = False
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
