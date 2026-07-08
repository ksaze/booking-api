from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.booking import Booking
from app.models.fitness_class import FitnessClass
from app.schemas.booking import BookingCreate


def get_user_bookings(
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


def get_class_for_booking(
    db: Session,
    class_id: int,
) -> Optional[FitnessClass]:
    return (
        db.query(FitnessClass)
        .filter(FitnessClass.id == class_id)
        .with_for_update()
        .first()
    )


def has_existing_booking(
    db: Session,
    *,
    class_id: int,
    user_id: int,
) -> bool:
    return (
        db.query(Booking)
        .filter(
            Booking.class_id == class_id,
            Booking.user_id == user_id,
            Booking.is_active,
        )
        .first()
        is not None
    )


def create_booking(
    db: Session,
    *,
    user_id: int,
    booking_in: BookingCreate,
    fitness_class: FitnessClass,
) -> Booking:
    """
    Books a slot for the given user, guarding against overbooking and
    duplicate bookings (same email, same class).

    Raises ClassNotFoundError / ClassFullError / DuplicateBookingError on
    failure; the caller (route handler) maps these to HTTP status codes.
    """
    booking = Booking(
        class_id=booking_in.class_id,
        user_id=user_id,
        client_name=booking_in.client_name,
        client_email=booking_in.client_email,
    )

    fitness_class.available_slots -= 1

    db.add(booking)
    db.add(fitness_class)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(booking)
    return booking
