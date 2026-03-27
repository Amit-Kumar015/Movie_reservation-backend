from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base

class Genre(Base):
    __tablename__ = "genres"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    movies = relationship("Movie", back_populates="genre", passive_deletes=True)

