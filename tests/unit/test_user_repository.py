from types import SimpleNamespace
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from app.repositories.user_repository import authenticate_user


def test_authenticate_user_success(monkeypatch):
    db = MagicMock(spec=Session)

    user = SimpleNamespace(
        email="alice@example.com",
        hashed_password="hashed",
    )

    monkeypatch.setattr(
        "app.repositories.user_repository.get_user_by_email",
        lambda *_: user,
    )

    monkeypatch.setattr(
        "app.repositories.user_repository.verify_password",
        lambda *_: True,
    )

    assert authenticate_user(db, "alice@example.com", "password") == user


def test_authenticate_user_wrong_password(monkeypatch):
    db = MagicMock(spec=Session)

    user = SimpleNamespace(hashed_password="hashed")

    monkeypatch.setattr(
        "app.repositories.user_repository.get_user_by_email",
        lambda *_: user,
    )

    monkeypatch.setattr(
        "app.repositories.user_repository.verify_password",
        lambda *_: False,
    )

    assert authenticate_user(db, "alice@example.com", "wrong") is None


def test_authenticate_user_missing_user(monkeypatch):
    db = MagicMock(spec=Session)

    monkeypatch.setattr(
        "app.repositories.user_repository.get_user_by_email",
        lambda *_: None,
    )

    assert authenticate_user(db, "missing@example.com", "pw") is None
