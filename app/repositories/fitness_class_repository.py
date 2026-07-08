from datetime import datetime, UTC
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.fitness_class import FitnessClass
from app.schemas.fitness_class import (
    FitnessClassCreate,
    FitnessClassEdit,
    FitnessClassOut,
)
from app.utils.time import to_ist


def get_fitness_class(db: Session, class_id: int) -> Optional[FitnessClass]:
    return db.query(FitnessClass).filter(FitnessClass.id == class_id).first()


def get_upcoming_classes(
    db: Session, skip: int = 0, limit: int = 100, upcoming_only: bool = True
) -> List[FitnessClass]:
    query = db.query(FitnessClass).filter(FitnessClass.is_active == True)  # noqa: E712
    if upcoming_only:
        query = query.filter(FitnessClass.date_time >= datetime.now())
    return query.order_by(FitnessClass.date_time.asc()).offset(skip).limit(limit).all()


def create_fitness_class(db: Session, obj_in: FitnessClassCreate) -> FitnessClass:
    ist_datetime = to_ist(obj_in.date_time)

    db_obj = FitnessClass(
        name=obj_in.name,
        instructor=obj_in.instructor,
        date_time=ist_datetime,
        total_slots=obj_in.available_slots,
        available_slots=obj_in.available_slots,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_fitness_class(
    db: Session, db_obj: FitnessClass, obj_in: FitnessClassEdit
) -> FitnessClass:
    update_data = obj_in.dict(exclude_unset=True)
    if "date_time" in update_data:
        db_obj.date_time = update_data.pop("date_time")
    if "available_slots" in update_data:
        db_obj.available_slots = update_data.pop("available_slots")
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def deactivate_fitness_class(db: Session, db_obj: FitnessClass) -> FitnessClass:
    db_obj.is_active = False
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def has_available_slots(fitness_class: FitnessClass) -> bool:
    return fitness_class.available_slots > 0


def decrement_available_slots(db: Session, db_obj: FitnessClass) -> FitnessClass:
    """Caller is responsible for checking has_available_slots() first."""
    db_obj.available_slots -= 1
    db.add(db_obj)
    return db_obj


def serialize_class(
    fitness_class: FitnessClass,
    timezone: str | None = None,
) -> FitnessClassOut:
    return FitnessClassOut(
        id=fitness_class.id,
        name=fitness_class.name,
        instructor=fitness_class.instructor,
        available_slots=fitness_class.available_slots,
        date_time=fitness_class.date_time.astimezone(UTC),
    )
