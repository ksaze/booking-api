from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut
from app.schemas.error_response import ErrorResponse
from app.schemas.token import LoginRequest, Token
from app.services.user_service import (
    signup,
    login,
    refresh,
    UserAlreadyExistsError,
    InvalidRefreshTokenError,
    InvalidCredentialsError,
)

router = APIRouter(tags=["Authentication"])


@router.post(
    "/signup",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": ErrorResponse, "description": "Email already registered"}
    },
)
def signup_user(
    payload: UserCreate,
    db=Depends(get_db),
):
    try:
        return signup(db, payload)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="User registered with the given email already exists.",
        )


@router.post(
    "/login",
    response_model=Token,
)
def login_user(
    payload: LoginRequest,
    db=Depends(get_db),
    responses={
        400: {"model": ErrorResponse, "description": "Invalid login credentials"}
    },
):
    try:
        return login(
            db,
            email=payload.email,
            password=payload.password,
        )
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password",
        )


security = HTTPBearer()


@router.post(
    "/refresh",
    response_model=Token,
)
def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    responses={400: {"model": ErrorResponse, "description": "Invalid refresh token"}},
):
    try:
        return refresh(credentials.credentials)
    except InvalidRefreshTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
        )
