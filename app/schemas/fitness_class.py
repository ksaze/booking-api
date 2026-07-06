from datetime import datetime
from pydantic import BaseModel, ConfigDict
from .booking import Booking
import typing as t


class FitnessClassBase(BaseModel):
    name: str
    dateTime: datetime
    instructor: str
    availableSlots: int
    model_config = ConfigDict()


class FitnessClassOut(FitnessClassBase):
    pass


class FitnessClassCreate(FitnessClassBase):
    pass


class FitnessClassEdit(FitnessClassBase):
    name: t.Optional[str] = None
    dateTime: t.Optional[datetime] = None
    instructor: t.Optional[str] = None
    availableSlots: t.Optional[int] = None
    model_config = ConfigDict()


class FitnessClass(FitnessClassBase):
    id: int
    is_active: bool
    bookings: t.List[Booking] = None
    model_config = ConfigDict()
