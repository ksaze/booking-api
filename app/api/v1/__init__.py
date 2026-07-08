"""
API routes definition package

This package is resposible for:
- Defining api routes using FastAPI.
- Converting service exceptions into HTTPExceptions

Check swagger documentation at http://127.0.0.1:8000/docs for detailed
documentation of every route.
"""

from fastapi import APIRouter

from .auth import router as auth_router
from .fitness_class import router as class_router
from .booking import router as booking_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(class_router)
router.include_router(booking_router)
