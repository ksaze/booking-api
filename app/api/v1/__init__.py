from fastapi import APIRouter

from .auth import router as auth_router
from .fitness_class import router as class_router
from .booking import router as booking_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(class_router)
router.include_router(booking_router)
