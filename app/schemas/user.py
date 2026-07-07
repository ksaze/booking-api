from pydantic import BaseModel, ConfigDict, EmailStr, Field
import typing as t

from .booking import Booking


class UserBase(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserOut(UserBase):
    pass


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserEdit(BaseModel):
    name: t.Optional[str] = Field(default=None, min_length=2)
    email: t.Optional[EmailStr] = None
    password: t.Optional[str] = Field(default=None, min_length=8)

    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    id: int
    is_active: bool
    bookings: list[Booking] = []

    model_config = ConfigDict(from_attributes=True)
