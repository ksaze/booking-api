"""
Business logic for booking management.

Allows users to book classes and check their bookings using JWT Token based
authentication.
"""

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
    """Raised when trying to book a class which doesn't exist"""


class ClassFullError(Exception):
    """Raised when trying to book a class which has no remaining slots"""


class DuplicateBookingError(Exception):
    """Raised when trying to book a class the user has already booked"""


def book(
    db: Session,
    user_id: int,
    booking_in: BookingCreate,
) -> BookingOut:
    """
    Allows an authenticated user to book a class

    Args:
        db: Database session
        user_id: User to create booking for
        booking_in: Booking information

    Raises:
       ClassNotFoundError: No class with the provided class.id exists
       ClassFullError: Class has no remaining slots available
       DuplicateBookingError: User already has a booking for the given class

    Returns:
        BookingOut object containing booking information
    """

    fitness_class = get_class_for_booking(
        db,
        booking_in.class_id,
    )

    if fitness_class is None:
        raise ClassNotFoundError()

    # Priority given to already booked exception over class full
    if has_existing_booking(
        db,
        class_id=booking_in.class_id,
        user_id=user_id,
    ):
        raise DuplicateBookingError()

    if fitness_class.available_slots <= 0:
        raise ClassFullError()

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
    """
    Lists all classes booked by an authenticated user

    Args:
        db: Database session
        user_id: User to list bookings for

    Returns:
        List of BookingOut objects containing booking information
    """
    bookings = get_user_bookings(db, user_id)

    return [BookingOut.model_validate(booking) for booking in bookings]
