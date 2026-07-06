from datetime import datetime, timedelta

from app.repositories.fitness_class_repository import (
    create_fitness_class,
    get_fitness_classes,
)

from app.schemas.fitness_class import FitnessClassCreate


def test_create_class(db):
    cls = create_fitness_class(
        db,
        FitnessClassCreate(
            name="Yoga",
            instructor="Alice",
            dateTime=datetime.now() + timedelta(days=1),
            availableSlots=15,
        ),
    )

    assert cls.id is not None
    assert cls.available_slots == 15
    assert cls.total_slots == 15


def test_get_upcoming_classes(db):
    create_fitness_class(
        db,
        FitnessClassCreate(
            name="Yoga",
            instructor="Alice",
            dateTime=datetime.now() + timedelta(days=2),
            availableSlots=10,
        ),
    )

    classes = get_fitness_classes(db)

    assert len(classes) == 1
