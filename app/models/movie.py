from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy import relationship
import uuid

from app.db.database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    duration = Column(Integer, nullable=False)
    posterUrl = Column(String, nullable=False)
    genre_id = Column(String, ForeignKey("genres.id"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    genre = relationship("Genre", back_populates="movies", passive_deletes=True)
    showtimes = relationship("Showtime", back_populates="movie", passive_deletes=True)