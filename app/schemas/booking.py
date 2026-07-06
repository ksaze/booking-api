from datetime import datetime
from typing import Union, TYPE_CHECKING
from pydantic import BaseModel, EmailStr, ConfigDict
import typing as t

# FitnessClass and User both import Booking directly
# so Booking must not import them back at module level - that would be
# circular. We only need them for type-checking; the string forward refs
# below are resolved once by schemas/__init__.py after every model loads.
if TYPE_CHECKING:
    from .fitness_class import FitnessClass
    from .user import User


class BookingBase(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr
    model_config = ConfigDict()


class BookingOut(BookingBase):
    pass


class BookingCreate(BookingBase):
    pass


class BookingEdit(BookingBase):
    class_id: t.Optional[int] = None
    client_name: t.Optional[str] = None
    client_email: t.Optional[EmailStr] = None
    model_config = ConfigDict(model_config=ConfigDict(from_attributes=True))


class Booking(BookingBase):
    id: int
    user_id: int
    booked_at: datetime
    is_active: bool
    fitness_class: Union["FitnessClass", None] = None
    user: Union["User", None] = None
    model_config = ConfigDict(model_config=ConfigDict(from_attributes=True))
