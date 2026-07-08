from datetime import UTC, datetime

import pytest
from sqlalchemy.exc import IntegrityError
from unittest.mock import Mock

from app.schemas.booking import BookingCreate, BookingOut
from app.services.booking_service import (
    book,
    list_user_bookings,
    ClassNotFoundError,
    ClassFullError,
    DuplicateBookingError,
)


def make_booking():
    return BookingOut(
        id=1,
        class_id=1,
        client_name="Alice",
        client_email="alice@example.com",
        booked_at=datetime.now(UTC),
    )


def test_book_success(db, monkeypatch):
    booking = make_booking()

    monkeypatch.setattr(
        "app.services.booking_service.get_class_for_booking",
        Mock(return_value=Mock(available_slots=5)),
    )

    monkeypatch.setattr(
        "app.services.booking_service.has_existing_booking",
        Mock(return_value=False),
    )

    repo = Mock(return_value=booking)

    monkeypatch.setattr(
        "app.services.booking_service.create_booking",
        repo,
    )

    payload = BookingCreate(
        class_id=1,
        client_name="Alice",
        client_email="alice@example.com",
    )

    result = book(db, 1, payload)

    repo.assert_called_once()
    assert result == booking


def test_book_class_not_found(db, monkeypatch):
    monkeypatch.setattr(
        "app.services.booking_service.get_class_for_booking",
        Mock(return_value=None),
    )

    payload = BookingCreate(
        class_id=1,
        client_name="Alice",
        client_email="alice@example.com",
    )

    with pytest.raises(ClassNotFoundError):
        book(db, 1, payload)


def test_book_class_full(db, monkeypatch):
    monkeypatch.setattr(
        "app.services.booking_service.get_class_for_booking",
        Mock(return_value=Mock(available_slots=0)),
    )

    payload = BookingCreate(
        class_id=1,
        client_name="Alice",
        client_email="alice@example.com",
    )

    with pytest.raises(ClassFullError):
        book(db, 1, payload)


def test_book_duplicate_existing(db, monkeypatch):
    monkeypatch.setattr(
        "app.services.booking_service.get_class_for_booking",
        Mock(return_value=Mock(available_slots=5)),
    )

    monkeypatch.setattr(
        "app.services.booking_service.has_existing_booking",
        Mock(return_value=True),
    )

    payload = BookingCreate(
        class_id=1,
        client_name="Alice",
        client_email="alice@example.com",
    )

    with pytest.raises(DuplicateBookingError):
        book(db, 1, payload)


def test_book_duplicate_integrity_error(db, monkeypatch):
    monkeypatch.setattr(
        "app.services.booking_service.get_class_for_booking",
        Mock(return_value=Mock(available_slots=5)),
    )

    monkeypatch.setattr(
        "app.services.booking_service.has_existing_booking",
        Mock(return_value=False),
    )

    monkeypatch.setattr(
        "app.services.booking_service.create_booking",
        Mock(side_effect=IntegrityError("", "", "")),
    )

    payload = BookingCreate(
        class_id=1,
        client_name="Alice",
        client_email="alice@example.com",
    )

    with pytest.raises(DuplicateBookingError):
        book(db, 1, payload)


def test_list_user_bookings(db, monkeypatch):
    bookings = [make_booking(), make_booking()]

    repo = Mock(return_value=bookings)

    monkeypatch.setattr(
        "app.services.booking_service.get_user_bookings",
        repo,
    )

    result = list_user_bookings(db, 1)

    repo.assert_called_once_with(db, 1)
    assert result == bookings


def test_list_user_bookings_empty(db, monkeypatch):
    monkeypatch.setattr(
        "app.services.booking_service.get_user_bookings",
        Mock(return_value=[]),
    )

    assert list_user_bookings(db, 1) == []
