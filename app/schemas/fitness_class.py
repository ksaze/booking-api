from datetime import datetime
import typing as t

from pydantic import BaseModel, ConfigDict, Field


class FitnessClassBase(BaseModel):
    name: str
    date_time: datetime = Field(
        validation_alias="dateTime",
        serialization_alias="dateTime",
    )
    instructor: str
    available_slots: int = Field(
        validation_alias="availableSlots",
        serialization_alias="availableSlots",
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        validate_by_name=True,
        validate_by_alias=True,
        serialize_by_alias=True,
    )


class FitnessClassCreate(FitnessClassBase):
    pass


class FitnessClassEdit(BaseModel):
    name: t.Optional[str] = None
    date_time: t.Optional[datetime] = Field(
        default=None,
        validation_alias="dateTime",
        serialization_alias="dateTime",
    )
    instructor: t.Optional[str] = None
    available_slots: t.Optional[int] = Field(
        default=None,
        validation_alias="availableSlots",
        serialization_alias="availableSlots",
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        validate_by_name=True,
        validate_by_alias=True,
        serialize_by_alias=True,
    )


class FitnessClass(FitnessClassBase):
    id: int
    is_active: bool


class FitnessClassOut(BaseModel):
    id: int
    name: str
    date_time: datetime = Field(
        serialization_alias="dateTime",
    )
    instructor: str
    available_slots: int = Field(
        serialization_alias="availableSlots",
    )
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        serialize_by_alias=True,
    )
