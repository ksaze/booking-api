from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class BookingBase(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class BookingOut(BookingBase):
    id: int
    booked_at: datetime


class BookingCreate(BookingBase):
    pass


class Booking(BookingBase):
    id: int
    user_id: int
    booked_at: datetime
