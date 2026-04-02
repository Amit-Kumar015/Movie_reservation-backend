from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.database import Base

class Screen(Base):
    __tablename__ = "screens"

    screen_id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    name = Column(String(50), nullable=False)
    venue_id = Column(UUID(as_uuid=True), ForeignKey("venues.venue_id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    venue = relationship("Venue", back_populates="screens", passive_deletes=True)
    showtimes = relationship("Showtime", back_populates="screen", passive_deletes=True)
    seats = relationship("Seat", back_populates="screen", passive_deletes=True)

    __table_args__ = (
        UniqueConstraint("name", "venue_id", name="uq_screen_name_venue"),
    )