from datetime import datetime
from typing import List
from sqlalchemy.orm import Session

from app.models.fitness_class import FitnessClass
from app.schemas.fitness_class import (
    FitnessClassCreate,
)
from app.utils.time import to_ist


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
