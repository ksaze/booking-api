from typing import Union
from pydantic import BaseModel, EmailStr
from .booking import Booking
import typing as t


class UserBase(BaseModel):
    email: EmailStr
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None

    class Config:
        orm_mode = True


class UserOut(UserBase):
    pass


class UserCreate(UserBase):
    password: str


class UserEdit(UserBase):
    email: t.Optional[EmailStr] = None
    first_name: t.Optional[str] = None
    last_name: t.Optional[str] = None
    password: t.Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    is_active: bool
    bookings: t.List[Booking] = None

    class Config:
        orm_mode = True
