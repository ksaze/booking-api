from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.db.session import Base


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        UniqueConstraint("class_id", "client_email", name="uq_booking_class_email"),
    )
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # foreignKey relations
    class_id = Column(Integer, ForeignKey("fitness_classes.id"), nullable=False)
    fitness_class = relationship("FitnessClass", back_populates="bookings")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="bookings")
