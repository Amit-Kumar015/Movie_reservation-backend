from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.database import Base

class Genre(Base):
    __tablename__ = "genres"

    genre_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    type = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    movies = relationship("Movie", back_populates="genre", passive_deletes=True)

