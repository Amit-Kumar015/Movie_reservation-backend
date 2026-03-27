from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base

class Seat(Base):
    __tablename__ = "seats"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    screen_id = Column(String, ForeignKey("screens.id"), ondelete="CASCADE", nullable=False, index=True)
    row = Column(String, nullable=False)
    col = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    screen = relationship("Screen", back_populates="seats", passive_deletes=True)
    reservation_seats = relationship("ReservationSeat", back_populates="seat", passive_deletes=True)

    __table_args__ = (
        UniqueConstraint("screen_id", "row", "col", name="uq_seat_screen_row_col"),
    )