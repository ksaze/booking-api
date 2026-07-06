from .booking import Booking, BookingOut, BookingCreate, BookingEdit
from .fitness_class import (
    FitnessClass,
    FitnessClassOut,
    FitnessClassCreate,
    FitnessClassEdit,
)
from .user import User, UserOut, UserCreate, UserEdit

Booking.update_forward_refs(FitnessClass=FitnessClass, User=User)

__all__ = [
    "Booking",
    "BookingOut",
    "BookingCreate",
    "BookingEdit",
    "FitnessClass",
    "FitnessClassOut",
    "FitnessClassCreate",
    "FitnessClassEdit",
    "User",
    "UserOut",
    "UserCreate",
    "UserEdit",
]
