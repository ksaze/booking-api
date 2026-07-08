"""
Business logic for fitness class management.

Handles class creation and listing upcoming classes, while normalising
timezone to IST for the database and back to UTC ISO 8601
"""

from sqlalchemy.orm import Session

from app.repositories.fitness_class_repository import (
    create_fitness_class,
    get_upcoming_classes,
)
from app.schemas.fitness_class import FitnessClassCreate, FitnessClassOut
from app.utils.time import ist_now, to_ist


class InvalidClassDateError(Exception):
    """Raised when attempting to create a class in the past."""


class InvalidSlotCountError(Exception):
    """Raised when there are no available slots."""


def create_class(
    db: Session,
    class_in: FitnessClassCreate,
) -> FitnessClassOut:
    """
    Creates a new fitness class

    Args:
        db: Database session
        class_in: Class information

    Raises:
        InvalidClassDateError: Class created for a datetime in the past
        InvalidSlotCountError: Numbers of slots are less than or equal to zero

    Returns:
        FitnessClassOut object containing information about the created class
    """
    if class_in.available_slots <= 0:
        raise InvalidSlotCountError()

    ist_time = to_ist(class_in.date_time)

    if ist_time <= ist_now():
        raise InvalidClassDateError()

    class_in = class_in.model_copy(update={"date_time": ist_time})

    return FitnessClassOut.model_validate(create_fitness_class(db, class_in))


def list_upcoming(
    db: Session,
) -> list[FitnessClassOut]:
    """
    Lists all upcoming fitness classes

    Args:
        db: Database session

    Returns:
        List of FitnessClassOut objects
    """
    classes = get_upcoming_classes(db)
    return [FitnessClassOut.model_validate(cls) for cls in classes]
