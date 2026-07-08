from datetime import datetime, timedelta, UTC

from app.repositories.fitness_class_repository import (
    create_fitness_class,
    get_upcoming_classes,
)

from app.schemas.fitness_class import FitnessClassCreate


def test_create_class(db):
    cls = create_fitness_class(
        db,
        FitnessClassCreate(
            name="Yoga",
            instructor="Alice",
            date_time=datetime.now(UTC) + timedelta(days=1),
            available_slots=15,
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
            date_time=datetime.now(UTC) + timedelta(days=2),
            available_slots=10,
        ),
    )

    classes = get_upcoming_classes(db)

    assert len(classes) == 1
