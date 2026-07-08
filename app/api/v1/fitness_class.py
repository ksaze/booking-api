from fastapi import APIRouter, Depends, status, HTTPException

from app.db.session import get_db
from app.core.auth import get_current_user

from app.schemas.fitness_class import (
    FitnessClassCreate,
    FitnessClassOut,
)
from app.schemas.error_response import ErrorResponse
from app.services.fitness_class_service import (
    create_class,
    list_upcoming,
    InvalidClassDateError,
    InvalidSlotCountError,
)

router = APIRouter(tags=["Fitness Classes"])


@router.post(
    "/classes",
    response_model=FitnessClassOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Invalid class date or slot count",
        },
        401: {"model": ErrorResponse, "description": "Unauthorised"},
    },
)
def create(
    payload: FitnessClassCreate,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        return create_class(db, payload)
    except InvalidClassDateError:
        raise HTTPException(
            status_code=400, detail="Class cannot be scheduled in the past."
        )
    except InvalidSlotCountError:
        raise HTTPException(
            status_code=400, detail="Available slots must be greater than zero"
        )


@router.get(
    "/classes",
    response_model=list[FitnessClassOut],
)
def list_classes(
    db=Depends(get_db),
):
    return list_upcoming(db)
