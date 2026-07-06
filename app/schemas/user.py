from typing import Union
from pydantic import BaseModel, EmailStr, ConfigDict
from .booking import Booking
import typing as t


class UserBase(BaseModel):
    email: EmailStr
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    model_config = ConfigDict(model_config=ConfigDict(from_attributes=True))


class UserOut(UserBase):
    pass


class UserCreate(UserBase):
    password: str


class UserEdit(UserBase):
    email: t.Optional[EmailStr] = None
    first_name: t.Optional[str] = None
    last_name: t.Optional[str] = None
    password: t.Optional[str] = None
    model_config = ConfigDict(model_config=ConfigDict(from_attributes=True))


class User(UserBase):
    id: int
    is_active: bool
    bookings: t.List[Booking] = None
    model_config = ConfigDict(model_config=ConfigDict(from_attributes=True))
