from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
import typing as t


class BookingBase(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr
    model_config = ConfigDict()


class BookingOut(BookingBase):
    id: int
    booked_at: datetime
    class_id: int
    client_name: str
    client_email: str


class BookingCreate(BookingBase):
    pass


class BookingEdit(BookingBase):
    class_id: t.Optional[int] = None
    client_name: t.Optional[str] = None
    client_email: t.Optional[EmailStr] = None
    model_config = ConfigDict(from_attributes=True)


class Booking(BookingBase):
    id: int
    user_id: int
    booked_at: datetime
    is_active: bool
