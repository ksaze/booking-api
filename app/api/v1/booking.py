from fastapi import APIRouter, Depends, status, HTTPException

from app.db.session import get_db
from app.core.auth import get_current_user

from app.schemas.booking import (
    BookingCreate,
    BookingOut,
)
from app.schemas.error_response import ErrorResponse
from app.services.booking_service import (
    book,
    list_user_bookings,
    ClassNotFoundError,
    ClassFullError,
    DuplicateBookingError,
)

router = APIRouter(tags=["Bookings"])


@router.post(
    "/book",
    response_model=BookingOut,
    status_code=status.HTTP_201_CREATED,
)
def create_booking(
    payload: BookingCreate,
    db=Depends(get_db),
    user=Depends(get_current_user),
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Class full",
        },
        401: {"model": ErrorResponse, "description": "Unauthorised"},
        404: {"model": ErrorResponse, "description": "Class not found"},
        409: {"model": ErrorResponse, "description": "Duplicate booking"},
    },
):
    try:
        return book(
            db,
            user.id,
            payload,
        )
    except ClassNotFoundError:
        raise HTTPException(
            status_code=404, detail="No class with the provided id exists"
        )
    except ClassFullError:
        raise HTTPException(
            status_code=401, detail="Provided class has no remaining slots available."
        )
    except DuplicateBookingError:
        raise HTTPException(
            status_code=400, detail="Booking for the given class already exists."
        )


@router.get(
    "/bookings",
    response_model=list[BookingOut],
)
def get_bookings(
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    return list_user_bookings(
        db,
        user.id,
    )
