from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.repositories.booking_repository import (
    cancel_booking,
    ClassFullError,
)


def test_cancel_booking_returns_slot():
    db = MagicMock(spec=Session)

    fitness_class = SimpleNamespace(available_slots=2)

    booking = SimpleNamespace(
        is_active=True,
        fitness_class=fitness_class,
    )

    cancel_booking(db, booking)

    assert fitness_class.available_slots == 3
    assert booking.is_active is False

    db.add.assert_any_call(fitness_class)
    db.add.assert_any_call(booking)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(booking)


def test_cancel_booking_inactive_booking():
    db = MagicMock(spec=Session)

    fitness_class = SimpleNamespace(available_slots=5)

    booking = SimpleNamespace(
        is_active=False,
        fitness_class=fitness_class,
    )

    cancel_booking(db, booking)

    assert fitness_class.available_slots == 5

    db.add.assert_any_call(booking)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(booking)


def test_class_full_exception():
    with pytest.raises(ClassFullError):
        raise ClassFullError()
