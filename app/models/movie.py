from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.database import Base

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    title = Column(String, nullable=False, index=True)
    description = Column(String(300), nullable=True)
    duration = Column(Integer, nullable=False)
    poster_url = Column(String, nullable=False)
    genre_id = Column(UUID(as_uuid=True), ForeignKey("genres.genre_id"), ondelete="SET NULL", nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
      CheckConstraint("duration > 0", name="check_movie_duration_positive"),
    )

    genre = relationship("Genre", back_populates="movies", passive_deletes=True)
    showtimes = relationship("Showtime", back_populates="movie", passive_deletes=True)