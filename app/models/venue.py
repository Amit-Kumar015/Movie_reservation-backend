from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy import relationship
import uuid

from app.db.database import Base

class Venue(Base):
    __tablename__ = "venues"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    screens = relationship("Screen", back_populates="venue", passive_deletes=True)

    __table_args__ = (
        Index("idx_venue_name_location", "name", "location")
    )