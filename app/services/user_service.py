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
    pass


class InvalidCredentialsError(Exception):
    pass


class InvalidRefreshTokenError(Exception):
    pass


def signup(db: Session, user_in: UserCreate):
    if get_user_by_email(db, user_in.email):
        raise UserAlreadyExistsError()

    return create_user(db, user_in)


def login(
    db: Session,
    *,
    email: str,
    password: str,
) -> Token:
    user = authenticate_user(db, email, password)

    if user is None:
        raise InvalidCredentialsError()

    return Token(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


def refresh(refresh_token: str) -> Token:
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
