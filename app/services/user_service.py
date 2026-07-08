"""
Business logic for user management and authentication.

Provides user registeration, login, and token refresh functionality.
"""

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
)
from app.core.auth import decode_token
from app.repositories.user_repository import (
    authenticate_user,
    create_user,
    get_user_by_email,
)
from app.schemas.token import Token
from app.schemas.user import UserCreate


class UserAlreadyExistsError(Exception):
    """
    Raised when trying to create a user with an email which already exists
    in database
    """


class InvalidCredentialsError(Exception):
    """Raised when either email isn't registered or provided password isn't valid"""


class InvalidRefreshTokenError(Exception):
    """Raised when trying to refresh with a JWT refresh token which isn't valid"""


def signup(db: Session, user_in: UserCreate):
    """
    Creates a new user.

    Args:
        db: Database session
        user_in: User information

    Raises:
        UserAlreadyExistsError: A user with the given email already exists.
    """
    if get_user_by_email(db, user_in.email):
        raise UserAlreadyExistsError()

    return create_user(db, user_in)


def login(
    db: Session,
    *,
    email: str,
    password: str,
) -> Token:
    """
    Authenticates using email and password.

    Args:
        db: Database sessoin
        email: Email address
        password: Associated password

    Raises:
        InvalidCredentialsError: No user with the given email exists or
        provided pass word is invalid.

    Returns:
        Token object with JWT access token and refresh tokens for authenticating
        further requests and refreshing authentication token.
    """
    user = authenticate_user(db, email, password)

    if user is None:
        raise InvalidCredentialsError()

    return Token(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


def refresh(refresh_token: str) -> Token:
    """
    Refreshes access token's validity

    Args:
        refresh_token: JWT refresh_token generated at log in

    Raises:
        InvalidRefreshTokenError

    Returns:
        Token object with JWT access and refresh tokens
    """
    payload = decode_token(
        refresh_token,
        expected_type="refresh",
    )

    user_id = int(payload["sub"])

    if user_id is None:
        raise InvalidRefreshTokenError()

    return Token(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )
