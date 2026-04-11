import logging
from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.showtime import Showtime
from app.models.movie import Movie
from app.models.screen import Screen

logger = logging.getLogger(__name__)

class MovieNotFoundError(Exception):
  pass

class ShowtimeNotFoundError(Exception):
  pass

class ScreenNotFoundError(Exception):
  pass

def create_showtime(db: Session, screen_id: UUID, movie_id: UUID, start_time: datetime, price: float) -> Showtime:
  try:
    movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
    if not movie:
      raise MovieNotFoundError(f"Movie with ID {movie_id} not found")
    
    screen = db.query(Screen).filter(Screen.screen_id == screen_id).first()
    if not screen:
      raise ScreenNotFoundError(f"Screen with ID {screen_id} not found")
    
    new_showtime = Showtime(
      screen_id=screen_id,
      movie_id=movie_id,
      start_time=start_time,
      end_time=start_time + timedelta(minutes=movie.duration),
      price=price,
    )
    db.add(new_showtime)
    db.commit()
    db.refresh(new_showtime)
    return new_showtime
  except MovieNotFoundError:
    raise
  except ScreenNotFoundError:
    raise
  except SQLAlchemyError as e:
    logger.error(f"Database error while creating showtime for screen {screen_id} and movie {movie_id}: {str(e)}")
    db.rollback()
    raise
  except Exception as e:
    logger.error(f"Unexpected error while creating showtime for screen {screen_id} and movie {movie_id}: {str(e)}")
    db.rollback()
    raise

def delete_showtime(db: Session, showtime_id: UUID) -> None:
  try:
    showtime = db.query(Showtime).filter(Showtime.showtime_id == showtime_id).first()
    if not showtime:
      raise ShowtimeNotFoundError(f"Showtime with ID {showtime_id} not found")
    
    db.delete(showtime)
    db.commit()
  except ShowtimeNotFoundError:
    raise
  except SQLAlchemyError as e:
    logger.error(f"Database error while deleting showtime {showtime_id}: {str(e)}")
    db.rollback()
    raise
  except Exception as e:
    logger.error(f"Unexpected error while deleting showtime {showtime_id}: {str(e)}")
    db.rollback()
    raise