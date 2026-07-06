from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from db.models import FitnessClass
from schemas import FitnessClassCreate, FitnessClassEdit


def get_fitness_class(db: Session, class_id: int) -> Optional[FitnessClass]:
    return db.query(FitnessClass).filter(FitnessClass.id == class_id).first()


def get_fitness_classes(
    db: Session, skip: int = 0, limit: int = 100, upcoming_only: bool = True
) -> List[FitnessClass]:
    query = db.query(FitnessClass).filter(FitnessClass.is_active == True)  # noqa: E712
    if upcoming_only:
        query = query.filter(FitnessClass.date_time >= datetime.now())
    return query.order_by(FitnessClass.date_time.asc()).offset(skip).limit(limit).all()


def create_fitness_class(db: Session, obj_in: FitnessClassCreate) -> FitnessClass:
    db_obj = FitnessClass(
        name=obj_in.name,
        instructor=obj_in.instructor,
        date_time=obj_in.dateTime,
        total_slots=obj_in.availableSlots,
        available_slots=obj_in.availableSlots,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_fitness_class(
    db: Session, db_obj: FitnessClass, obj_in: FitnessClassEdit
) -> FitnessClass:
    update_data = obj_in.dict(exclude_unset=True)
    if "dateTime" in update_data:
        db_obj.date_time = update_data.pop("dateTime")
    if "availableSlots" in update_data:
        db_obj.available_slots = update_data.pop("availableSlots")
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
