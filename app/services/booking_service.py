from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.booking_repository import (
    create_booking,
    get_class_for_booking,
    get_user_bookings,
    has_existing_booking,
)
from app.schemas.booking import BookingCreate, BookingOut


class ClassNotFoundError(Exception):
    pass


class ClassFullError(Exception):
    pass


class DuplicateBookingError(Exception):
    pass


def book(
    db: Session,
    user_id: int,
    booking_in: BookingCreate,
) -> BookingOut:
    fitness_class = get_class_for_booking(
        db,
        booking_in.class_id,
    )

    if fitness_class is None:
        raise ClassNotFoundError()

    if fitness_class.available_slots <= 0:
        raise ClassFullError()

    if has_existing_booking(
        db,
        class_id=booking_in.class_id,
        user_id=user_id,
    ):
        raise DuplicateBookingError()

    try:
        booking = create_booking(
            db=db,
            user_id=user_id,
            booking_in=booking_in,
            fitness_class=fitness_class,
        )
    except IntegrityError:
        # In case another request races us and the unique constraint wins.
        raise DuplicateBookingError()

    return BookingOut.model_validate(booking)


def list_user_bookings(
    db: Session,
    user_id: int,
) -> list[BookingOut]:
    bookings = get_user_bookings(db, user_id)

    return [BookingOut.model_validate(booking) for booking in bookings]
