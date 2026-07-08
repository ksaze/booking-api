from types import SimpleNamespace

import pytest

from app.core.security import TokenError
from app.schemas.token import Token
from app.schemas.user import UserCreate
from app.services.user_service import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    login,
    signup,
    refresh,
)


def test_signup_success(mocker, db):
    user_in = UserCreate(
        name="Alice",
        email="alice@example.com",
        password="password123",
    )

    user = SimpleNamespace(id=1)

    mocker.patch(
        "app.services.user_service.get_user_by_email",
        return_value=None,
    )

    create_user = mocker.patch(
        "app.services.user_service.create_user",
        return_value=user,
    )

    result = signup(db, user_in)

    create_user.assert_called_once_with(db, user_in)
    assert result is user


def test_signup_existing_user(mocker, db):
    user_in = UserCreate(
        name="Alice",
        email="alice@example.com",
        password="password123",
    )

    mocker.patch(
        "app.services.user_service.get_user_by_email",
        return_value=SimpleNamespace(id=1),
    )

    with pytest.raises(UserAlreadyExistsError):
        signup(db, user_in)


def test_login_success(mocker, db):
    user = SimpleNamespace(id=42)

    mocker.patch(
        "app.services.user_service.authenticate_user",
        return_value=user,
    )

    create_access = mocker.patch(
        "app.services.user_service.create_access_token",
        return_value="access-token",
    )

    create_refresh = mocker.patch(
        "app.services.user_service.create_refresh_token",
        return_value="refresh-token",
    )

    token = login(
        db,
        email="alice@example.com",
        password="password123",
    )

    assert isinstance(token, Token)
    assert token.access_token == "access-token"
    assert token.refresh_token == "refresh-token"
    assert token.token_type == "bearer"

    create_access.assert_called_once_with("42")
    create_refresh.assert_called_once_with("42")


def test_login_invalid_credentials(mocker, db):
    mocker.patch(
        "app.services.user_service.authenticate_user",
        return_value=None,
    )

    with pytest.raises(InvalidCredentialsError):
        login(
            db,
            email="alice@example.com",
            password="wrong-password",
        )


def test_refresh_success(mocker):
    payload = SimpleNamespace(sub="42")

    decode = mocker.patch(
        "app.services.user_service.decode_token",
        return_value=payload,
    )

    access = mocker.patch(
        "app.services.user_service.create_access_token",
        return_value="new-access",
    )

    refresh_token = mocker.patch(
        "app.services.user_service.create_refresh_token",
        return_value="new-refresh",
    )

    token = refresh("old-refresh-token")

    decode.assert_called_once_with(
        "old-refresh-token",
        expected_type="refresh",
    )

    access.assert_called_once_with("42")
    refresh_token.assert_called_once_with("42")

    assert token == Token(
        access_token="new-access",
        refresh_token="new-refresh",
        token_type="bearer",
    )


def test_refresh_invalid_token(mocker):
    mocker.patch(
        "app.services.user_service.decode_token",
        side_effect=TokenError(),
    )

    with pytest.raises(TokenError):
        refresh("invalid-token")
