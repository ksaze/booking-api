from datetime import datetime, timedelta

import pytest

from app.repositories.user_repository import create_user
from app.repositories.fitness_class_repository import create_fitness_class
from app.repositories.booking_repository import (
    create_booking,
    cancel_booking,
    ClassFullError,
)

from app.schemas.user import UserCreate
from app.schemas.booking import BookingCreate
from app.schemas.fitness_class import FitnessClassCreate


def create_fixture(db):
    user = create_user(
        db,
        UserCreate(
            email="user@test.com",
            password="secret",
        ),
    )

    fitness_class = create_fitness_class(
        db,
        FitnessClassCreate(
            name="Yoga",
            instructor="Alice",
            dateTime=datetime.now() + timedelta(days=1),
            availableSlots=1,
        ),
    )

    return user, fitness_class


def test_create_booking_decrements_slots(db):
    user, cls = create_fixture(db)

    booking = create_booking(
        db,
        BookingCreate(
            class_id=cls.id,
            client_name="Bob",
            client_email="bob@test.com",
        ),
        user.id,
    )

    assert booking.id is not None

    db.refresh(cls)

    assert cls.available_slots == 0


def test_booking_full_class_raises(db):
    user, cls = create_fixture(db)

    create_booking(
        db,
        BookingCreate(
            class_id=cls.id,
            client_name="Bob",
            client_email="bob@test.com",
        ),
        user.id,
    )

    with pytest.raises(ClassFullError):
        create_booking(
            db,
            BookingCreate(
                class_id=cls.id,
                client_name="Jane",
                client_email="jane@test.com",
            ),
            user.id,
        )


def test_cancel_booking_restores_slot(db):
    user, cls = create_fixture(db)

    booking = create_booking(
        db,
        BookingCreate(
            class_id=cls.id,
            client_name="Bob",
            client_email="bob@test.com",
        ),
        user.id,
    )

    cancel_booking(db, booking)

    db.refresh(cls)

    assert cls.available_slots == 1
    assert booking.is_active is False
