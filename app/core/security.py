from datetime import UTC, datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.core.config import settings
from app.schemas.token import TokenPayload

password_hash = PasswordHash.recommended()


class TokenError(Exception):
    """Raised when a token is invalid, expired, or of the wrong type."""


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def _create_token(subject: str, expires_delta: timedelta, token_type: str) -> str:
    expire = datetime.now(UTC) + expires_delta
    payload = {
        "sub": subject,
        "exp": expire,
        "type": token_type,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    return _create_token(
        subject,
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "access",
    )


def refresh_access_token(refresh_token: str) -> str:
    payload = decode_token(
        refresh_token,
        expected_type="refresh",
    )

    return create_access_token(payload.sub)


def create_refresh_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    return _create_token(
        subject,
        expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        "refresh",
    )


def decode_token(
    token: str,
    expected_type: str = "access",
) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError as exc:
        raise TokenError("Could not validate token") from exc

    try:
        token_payload = TokenPayload.model_validate(payload)
    except Exception as exc:
        raise TokenError("Malformed token payload") from exc

    if token_payload.type != expected_type:
        raise TokenError(f"Expected a {expected_type} token")

    return token_payload
