from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.core.auth import (
    get_current_active_user,
    get_current_superuser,
    get_current_user,
)
from app.core.security import TokenError, TokenPayload


def test_get_current_user_success(monkeypatch):
    user = SimpleNamespace(
        id=1,
        is_active=True,
        is_superuser=False,
    )

    monkeypatch.setattr(
        "app.core.auth.decode_token",
        lambda *_args, **_kwargs: TokenPayload(
            sub="1",
            exp=0,
            type="access",
        ),
    )

    monkeypatch.setattr(
        "app.core.auth.get_user",
        lambda *_args, **_kwargs: user,
    )

    assert get_current_user(token="token", db=object()) is user


def test_get_current_user_invalid_token(monkeypatch):
    monkeypatch.setattr(
        "app.core.auth.decode_token",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(TokenError()),
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(token="token", db=object())

    assert exc.value.status_code == 401


def test_get_current_user_missing_sub(monkeypatch):
    monkeypatch.setattr(
        "app.core.auth.decode_token",
        lambda *_args, **_kwargs: TokenPayload(
            sub="",
            exp=0,
            type="access",
        ),
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(token="token", db=object())

    assert exc.value.status_code == 401


def test_get_current_user_user_not_found(monkeypatch):
    monkeypatch.setattr(
        "app.core.auth.decode_token",
        lambda *_args, **_kwargs: TokenPayload(
            sub="1",
            exp=0,
            type="access",
        ),
    )

    monkeypatch.setattr(
        "app.core.auth.get_user",
        lambda *_args, **_kwargs: None,
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(token="token", db=object())

    assert exc.value.status_code == 401


def test_get_current_active_user_success():
    user = SimpleNamespace(is_active=True)

    assert get_current_active_user(user) is user


def test_get_current_active_user_inactive():
    with pytest.raises(HTTPException) as exc:
        get_current_active_user(SimpleNamespace(is_active=False))

    assert exc.value.status_code == 400


def test_get_current_superuser_success():
    user = SimpleNamespace(is_superuser=True)

    assert get_current_superuser(user) is user


def test_get_current_superuser_forbidden():
    with pytest.raises(HTTPException) as exc:
        get_current_superuser(SimpleNamespace(is_superuser=False))

    assert exc.value.status_code == 403
