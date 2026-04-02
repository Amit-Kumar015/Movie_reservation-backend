import logging
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta

from app.models.showtime import Showtime
from app.models.screen import Screen

logger = logging.getLogger(__name__)

class ShowtimeNotFoundError(Exception):
  pass

def get_showtimes_by_movie(db: Session, movie_id: UUID, date: datetime | None = None) -> list[Showtime]:
  try:
    showtimes = db.query(Showtime).options(joinedload(Showtime.screen).joinedload(Screen.seats), joinedload(Showtime.reservation_seats)).filter(Showtime.movie_id == movie_id)
    if date:
      start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
      end_of_day = start_of_day + timedelta(days=1)
      showtimes = showtimes.filter(Showtime.start_time >= start_of_day, Showtime.start_time < end_of_day)
    showtimes = showtimes.order_by(Showtime.start_time.asc()).all()
    if not showtimes:
      raise ShowtimeNotFoundError(f"No showtimes found for movie {movie_id}")
    return showtimes
  except SQLAlchemyError as e:
    logger.error("Database error occurred while fetching showtime by ID: %s", str(e))
    raise
  except Exception as e:
    logger.error("Unexpected error occurred while fetching showtime by ID: %s", str(e))
    raise
  
def get_showtime_by_id(db: Session, showtime_id: UUID) -> Showtime:
  try:
    showtime = db.query(Showtime).options(joinedload(Showtime.screen).joinedload(Screen.seats), joinedload(Showtime.reservation_seats)).filter(Showtime.showtime_id == showtime_id).first()
    if not showtime:
      raise ShowtimeNotFoundError(f"Showtime with ID {showtime_id} not found")
    return showtime
  except SQLAlchemyError as e:
    logger.error("Database error occurred while fetching showtime by ID: %s", str(e))
    raise
  except Exception as e:
    logger.error("Unexpected error occurred while fetching showtime by ID: %s", str(e))
    raise
   