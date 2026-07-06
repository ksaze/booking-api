from app.repositories.user_repository import (
    create_user,
    authenticate_user,
    update_user,
)

from app.schemas.user import UserCreate, UserEdit


def test_create_user_hashes_password(db):
    user = create_user(
        db,
        UserCreate(
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
            email="alice@example.com",
            password="secret",
        ),
    )

    user = authenticate_user(
        db,
        "alice@example.com",
        "secret",
    )

    assert user is not None


def test_authenticate_user_bad_password(db):
    create_user(
        db,
        UserCreate(
            email="alice@example.com",
            password="secret",
        ),
    )

    assert (
        authenticate_user(
            db,
            "alice@example.com",
            "wrong",
        )
        is None
    )


def test_update_password(db):
    user = create_user(
        db,
        UserCreate(
            email="alice@example.com",
            password="oldpass",
        ),
    )

    old_hash = user.hashed_password

    user = update_user(
        db,
        user,
        UserEdit(password="newpass"),
    )

    assert user.hashed_password != old_hash
