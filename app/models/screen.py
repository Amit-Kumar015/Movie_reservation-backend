from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy import relationship
import uuid

from app.db.database import Base

class Screen(Base):
    __tablename__ = "screens"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    venue_id = Column(String, ForeignKey("venues.id"), ondelete="CASCADE", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    venue = relationship("Venue", back_populates="screens", passive_deletes=True)
    showtimes = relationship("Showtime", back_populates="screen", passive_deletes=True)
    seats = relationship("Seat", back_populates="screen", passive_deletes=True)

    __table_args__ = (
        UniqueConstraint("name", "venue_id", name="uq_screen_name_venue")
    )