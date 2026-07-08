from app.repositories.user_repository import (
    create_user,
    authenticate_user,
)

from app.schemas.user import UserCreate


def test_create_user_hashes_password(db):
    user = create_user(
        db,
        UserCreate(
            name="abc",
            email="alice@example.com",
            password="password123",
        ),
    )

    assert user.id is not None
    assert user.email == "alice@example.com"

    assert user.hashed_password != "password123"


def test_authenticate_user_success(db):
    create_user(
        db,
        UserCreate(
            name="abc",
            email="alice@example.com",
            password="secret01",
        ),
    )

    user = authenticate_user(
        db,
        "alice@example.com",
        "secret01",
    )

    assert user is not None


def test_authenticate_user_bad_password(db):
    create_user(
        db,
        UserCreate(
            name="alice",
            email="alice@example.com",
            password="secret01",
        ),
    )

    assert (
        authenticate_user(
            db,
            "alice@example.com",
            "wrong01",
        )
        is None
    )
