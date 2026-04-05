from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.database import Base

class Seat(Base):
    __tablename__ = "seats"

    seat_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    screen_id = Column(UUID(as_uuid=True), ForeignKey("screens.screen_id", ondelete="CASCADE"), nullable=False, index=True)
    row = Column(String, nullable=False)
    col = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    screen = relationship("Screen", back_populates="seats", passive_deletes=True)
    reservation_seats = relationship("ReservationSeat", back_populates="seat", passive_deletes=True)

    __table_args__ = (
        UniqueConstraint("screen_id", "row", "col", name="uq_seat_screen_row_col"),
    )