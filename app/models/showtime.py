from sqlalchemy import Column, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.database import Base

class Showtime(Base):
    __tablename__ = "showtimes"

    showtime_id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    movie_id = Column(UUID(as_uuid=True), ForeignKey("movies.movie_id"), ondelete="CASCADE", nullable=False, index=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    price = Column(Float, nullable=False)
    screen_id = Column(UUID(as_uuid=True), ForeignKey("screens.screen_id"), ondelete="CASCADE", nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    movie = relationship("Movie", back_populates="showtimes", passive_deletes=True)
    screen = relationship("Screen", back_populates="showtimes", passive_deletes=True)
    reservations = relationship("Reservation", back_populates="showtime", passive_deletes=True)
    reservation_seats = relationship("ReservationSeat", back_populates="showtime", passive_deletes=True)
    
    @property
    def total_seats(self):
      return len(self.screen.seats)
    
    @property
    def available_seats(self):
      booked = sum(1 for rs in self.reservation_seats if rs.status == "BOOKED")
      return self.total_seats - booked