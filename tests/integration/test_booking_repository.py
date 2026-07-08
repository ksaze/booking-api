from datetime import UTC, datetime, timedelta

from app.repositories.booking_repository import (
    cancel_booking,
    create_booking,
    get_class_for_booking,
    get_user_bookings,
)
from app.repositories.fitness_class_repository import create_fitness_class
from app.repositories.user_repository import create_user
from app.schemas.booking import BookingCreate
from app.schemas.fitness_class import FitnessClassCreate
from app.schemas.user import UserCreate


def create_fixture(db):
    user = create_user(
        db,
        UserCreate(
            name="abc",
            email="user@test.com",
            password="secret01",
        ),
    )

    fitness_class = create_fitness_class(
        db,
        FitnessClassCreate(
            name="Yoga",
            instructor="Alice",
            date_time=datetime.now(UTC) + timedelta(days=1),
            available_slots=1,
        ),
    )

    return user, fitness_class


def test_create_booking_decrements_slots(db):
    user, cls = create_fixture(db)

    booking = create_booking(
        db=db,
        user_id=user.id,
        booking_in=BookingCreate(
            class_id=cls.id,
            client_name="Bob",
            client_email="bob@test.com",
        ),
        fitness_class=cls,
    )

    assert booking.id is not None

    db.refresh(cls)

    assert cls.available_slots == 0


def test_get_class_for_booking(db):
    _, cls = create_fixture(db)

    result = get_class_for_booking(db, cls.id)

    assert result is not None
    assert result.id == cls.id


def test_get_user_bookings(db):
    user, cls = create_fixture(db)

    booking = create_booking(
        db=db,
        user_id=user.id,
        booking_in=BookingCreate(
            class_id=cls.id,
            client_name="Bob",
            client_email="bob@test.com",
        ),
        fitness_class=cls,
    )

    bookings = get_user_bookings(db, user.id)

    assert bookings == [booking]


def test_cancel_booking_restores_slot(db):
    user, cls = create_fixture(db)

    booking = create_booking(
        db=db,
        user_id=user.id,
        booking_in=BookingCreate(
            class_id=cls.id,
            client_name="Bob",
            client_email="bob@test.com",
        ),
        fitness_class=cls,
    )

    cancel_booking(db, booking)

    db.refresh(cls)

    assert cls.available_slots == 1
    assert booking.is_active is False
