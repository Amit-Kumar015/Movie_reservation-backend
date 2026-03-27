from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base
from app.models.enum import ReservationStatus

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), ondelete="CASCADE", nullable=False, index=True)
    showtime_id = Column(String, ForeignKey("showtimes.id"), ondelete="CASCADE", nullable=False, index=True)
    status = Column(Enum(ReservationStatus), nullable=False, default=ReservationStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="reservations", passive_deletes=True)
    showtime = relationship("Showtime", back_populates="reservations", passive_deletes=True)
    reservation_seats = relationship("ReservationSeat", back_populates="reservation", passive_deletes=True)