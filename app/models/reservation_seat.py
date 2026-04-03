from sqlalchemy import Column, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.database import Base
from app.models.enum import ReservationSeatStatus

class ReservationSeat(Base):
    __tablename__ = "reservation_seats"

    reservation_seat_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    reservation_id = Column(UUID(as_uuid=True), ForeignKey("reservations.reservation_id", ondelete="CASCADE"), nullable=False, index=True)
    seat_id = Column(UUID(as_uuid=True), ForeignKey("seats.seat_id", ondelete="CASCADE"), nullable=False, index=True)
    showtime_id = Column(UUID(as_uuid=True), ForeignKey("showtimes.showtime_id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(Enum(ReservationSeatStatus), nullable=False, default=ReservationSeatStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    reservation = relationship("Reservation", back_populates="reservation_seats", passive_deletes=True)
    seat = relationship("Seat", back_populates="reservation_seats", passive_deletes=True)
    showtimes = relationship("Showtime", back_populates="reservation_seats", passive_deletes=True)

    __table_args__ = (
        UniqueConstraint("seat_id", "showtime_id", name="uq_reservation_seat_seat_showtime"),
    )