from datetime import datetime

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


class FitnessClass(FitnessClassBase):
    id: int


class FitnessClassOut(FitnessClassBase):
    id: int
    name: str
    date_time: datetime = Field(
        serialization_alias="dateTime",
    )
    instructor: str
    available_slots: int = Field(
        serialization_alias="availableSlots",
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        serialize_by_alias=True,
    )
