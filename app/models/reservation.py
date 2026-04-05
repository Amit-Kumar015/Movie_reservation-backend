from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.database import Base
from app.models.enum import ReservationStatus

class Reservation(Base):
    __tablename__ = "reservations"

    reservation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    showtime_id = Column(UUID(as_uuid=True), ForeignKey("showtimes.showtime_id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(Enum(ReservationStatus), nullable=False, default=ReservationStatus.PENDING)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="reservations", passive_deletes=True)
    showtime = relationship("Showtime", back_populates="reservations", passive_deletes=True)
    reservation_seats = relationship("ReservationSeat", back_populates="reservation", passive_deletes=True)