"""
Database seed generation script

Generates classes, users and bookings using the service module

Usage:
- Clear any existing .db sqlite file
- python -m scripts.seed
"""

from datetime import UTC, datetime, timedelta

from app.db.session import SessionLocal
from app.models.user import User
from app.models.fitness_class import FitnessClass
from app.services.user_service import signup
from app.services.fitness_class_service import create_class
from app.services.booking_service import book
from app.schemas.user import UserCreate
from app.schemas.fitness_class import FitnessClassCreate
from app.schemas.booking import BookingCreate


def main():
    db = SessionLocal()

    try:
        # Start fresh
        db.query(FitnessClass).delete()
        db.query(User).delete()
        db.commit()

        # Users
        alice = signup(
            db,
            UserCreate(
                name="Alice",
                email="alice@example.com",
                password="password123",
            ),
        )

        bob = signup(
            db,
            UserCreate(
                name="Bob",
                email="bob@example.com",
                password="password123",
            ),
        )

        # Classes
        yoga = create_class(
            db,
            FitnessClassCreate(
                name="Morning Yoga",
                instructor="John Doe",
                date_time=datetime.now(UTC) + timedelta(days=1),
                available_slots=20,
            ),
        )

        hiit = create_class(
            db,
            FitnessClassCreate(
                name="HIIT Blast",
                instructor="Jane Smith",
                date_time=datetime.now(UTC) + timedelta(days=2),
                available_slots=15,
            ),
        )

        pilates = create_class(
            db,
            FitnessClassCreate(
                name="Pilates",
                instructor="Emily Brown",
                date_time=datetime.now(UTC) + timedelta(days=3),
                available_slots=12,
            ),
        )

        # Bookings
        book(
            db,
            alice.id,
            BookingCreate(
                class_id=yoga.id,
                client_name="Alice",
                client_email="alice@example.com",
            ),
        )

        book(
            db,
            bob.id,
            BookingCreate(
                class_id=hiit.id,
                client_name="Bob",
                client_email="bob@example.com",
            ),
        )

        print("Database seeded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    main()
