from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base

class Showtime(Base):
    __tablename__ = "showtimes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    movie_id = Column(String, ForeignKey("movies.id"), ondelete="CASCADE", nullable=False, index=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    price = Column(Integer, nullable=False)
    screen_id = Column(String, ForeignKey("screens.id"), ondelete="CASCADE", nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    movie = relationship("Movie", back_populates="showtimes", passive_deletes=True)
    screen = relationship("Screen", back_populates="showtimes", passive_deletes=True)
    reservations = relationship("Reservation", back_populates="showtime", passive_deletes=True)
    reservation_seats = relationship("ReservationSeat", back_populates="showtime", passive_deletes=True)