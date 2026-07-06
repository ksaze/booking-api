from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
)

from sqlalchemy.orm import relationship
from app.db.session import Base


class FitnessClass(Base):
    __tablename__ = "fitness_classes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, index=True)
    instructor = Column(String, nullable=False)
    date_time = Column(DateTime, nullable=False, index=True)
    total_slots = Column(Integer, nullable=False)
    available_slots = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # foreignKey relations
    bookings = relationship("Booking", back_populates="fitness_class")
