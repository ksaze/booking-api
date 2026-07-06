from datetime import datetime
from pydantic import BaseModel
from .booking import Booking
import typing as t


class FitnessClassBase(BaseModel):
    name: str
    dateTime: datetime
    instructor: str
    availableSlots: int

    class Config:
        orm_mode = True


class FitnessClassOut(FitnessClassBase):
    pass


class FitnessClassCreate(FitnessClassBase):
    pass


class FitnessClassEdit(FitnessClassBase):
    name: t.Optional[str] = None
    dateTime: t.Optional[datetime] = None
    instructor: t.Optional[str] = None
    availableSlots: t.Optional[int] = None

    class Config:
        orm_mode = True


class FitnessClass(FitnessClassBase):
    id: int
    is_active: bool
    bookings: t.List[Booking] = None

    class Config:
        orm_mode = True
