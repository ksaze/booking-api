from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .booking import Booking


class UserBase(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserOut(UserBase):
    pass


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class User(UserBase):
    id: int
    bookings: list[Booking] = []

    model_config = ConfigDict(from_attributes=True)
