from types import SimpleNamespace
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from app.repositories.fitness_class_repository import (
    has_available_slots,
    decrement_available_slots,
)


def test_has_available_slots_true():
    cls = SimpleNamespace(available_slots=3)

    assert has_available_slots(cls)


def test_has_available_slots_false():
    cls = SimpleNamespace(available_slots=0)

    assert not has_available_slots(cls)


def test_decrement_available_slots():
    db = MagicMock(spec=Session)

    cls = SimpleNamespace(available_slots=4)

    decrement_available_slots(db, cls)

    assert cls.available_slots == 3
    db.add.assert_called_once_with(cls)
