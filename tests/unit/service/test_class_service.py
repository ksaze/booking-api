from datetime import UTC, datetime, timedelta

import pytest
from unittest.mock import Mock

from app.schemas.fitness_class import (
    FitnessClass,
    FitnessClassCreate,
    FitnessClassOut,
)
from app.services.fitness_class_service import (
    InvalidClassDateError,
    InvalidSlotCountError,
    create_class,
    list_upcoming,
)
from app.utils.time import to_ist


def make_class():
    return FitnessClass(
        id=1,
        name="Yoga",
        instructor="Alice",
        date_time=to_ist(datetime.now(UTC) + timedelta(days=1)),
        available_slots=20,
        is_active=True,
        bookings=[],
    )


def test_create_success(db, monkeypatch):
    fitness_class = make_class()

    repo = Mock(return_value=fitness_class)

    monkeypatch.setattr(
        "app.services.fitness_class_service.create_fitness_class",
        repo,
    )

    payload = FitnessClassCreate(
        name="Yoga",
        instructor="Alice",
        date_time=datetime.now(UTC) + timedelta(days=1),
        available_slots=20,
    )

    result = create_class(db, payload)

    repo.assert_called_once()
    assert result == FitnessClassOut.model_validate(fitness_class)


def test_create_invalid_slot_count(db):
    payload = FitnessClassCreate(
        name="Yoga",
        instructor="Alice",
        date_time=datetime.now(UTC) + timedelta(days=1),
        available_slots=0,
    )

    with pytest.raises(InvalidSlotCountError):
        create_class(db, payload)


def test_create_past_date(db):
    payload = FitnessClassCreate(
        name="Yoga",
        instructor="Alice",
        date_time=datetime.now(UTC) - timedelta(minutes=1),
        available_slots=10,
    )

    with pytest.raises(InvalidClassDateError):
        create_class(db, payload)


def test_create_converts_datetime_to_ist(db, monkeypatch):
    fitness_class = make_class()

    captured = {}

    def fake_create(_, class_in):
        captured["date_time"] = class_in.date_time
        return fitness_class

    monkeypatch.setattr(
        "app.services.fitness_class_service.create_fitness_class",
        fake_create,
    )

    utc_time = datetime.now(UTC) + timedelta(days=1)
    expected = to_ist(utc_time)

    payload = FitnessClassCreate(
        name="Yoga",
        instructor="Alice",
        date_time=utc_time,
        available_slots=10,
    )

    create_class(db, payload)

    assert captured["date_time"].tzinfo == expected.tzinfo
    assert captured["date_time"] == expected


def test_list_upcoming(db, monkeypatch):
    classes = [make_class(), make_class()]

    repo = Mock(return_value=classes)

    monkeypatch.setattr(
        "app.services.fitness_class_service.get_upcoming_classes",
        repo,
    )

    result = list_upcoming(db)

    repo.assert_called_once_with(db)
    assert len(result) == 2
    assert all(isinstance(cls, FitnessClassOut) for cls in result)


def test_list_upcoming_empty(db, monkeypatch):
    monkeypatch.setattr(
        "app.services.fitness_class_service.get_upcoming_classes",
        Mock(return_value=[]),
    )

    assert list_upcoming(db) == []
