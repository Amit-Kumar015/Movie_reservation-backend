from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy import relationship
import uuid

from app.db.database import Base

class ReservationSeat(Base):
    __tablename__ = "reservation_seats"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    reservation_id = Column(String, ForeignKey("reservations.id"), ondelete="CASCADE", index=True)
    seat_id = Column(String, ForeignKey("seats.id"), ondelete="CASCADE", index=True)
    showtime_id = Column(String, ForeignKey("showtimes.id"), ondelete="CASCADE", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    reservation = relationship("Reservation", back_populates="reservation_seats", passive_deletes=True)
    seat = relationship("Seat", back_populates="reservation_seats", passive_deletes=True)
    showtimes = relationship("Showtime", back_populates="reservation_seats", passive_deletes=True)

    __table_args__ = (
        UniqueConstraint("seat_id", "showtime_id", name="uq_reservation_seat_seat_showtime"),
    )