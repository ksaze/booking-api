from datetime import timedelta

import pytest
from jose import jwt

from app.core.config import settings
from app.core.security import (
    TokenError,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_hash_password():
    password = "super-secret"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)


def test_verify_password_invalid():
    hashed = hash_password("correct-password")

    assert not verify_password("wrong-password", hashed)


def test_create_and_decode_access_token():
    token = create_access_token("123")

    payload = decode_token(token)

    assert payload.sub == "123"
    assert payload.type == "access"


def test_create_and_decode_refresh_token():
    token = create_refresh_token("456")

    payload = decode_token(token, expected_type="refresh")

    assert payload.sub == "456"
    assert payload.type == "refresh"


def test_decode_wrong_token_type():
    token = create_refresh_token("123")

    with pytest.raises(TokenError):
        decode_token(token)


def test_decode_invalid_signature():
    bad_token = jwt.encode(
        {
            "sub": "123",
            "type": "access",
        },
        "wrong-secret",
        algorithm=settings.ALGORITHM,
    )

    with pytest.raises(TokenError):
        decode_token(bad_token)


def test_decode_expired_token():
    token = create_access_token(
        "123",
        expires_delta=timedelta(seconds=-1),
    )

    with pytest.raises(TokenError):
        decode_token(token)
