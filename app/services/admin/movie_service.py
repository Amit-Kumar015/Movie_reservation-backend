import logging
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.movie import Movie

logger = logging.getLogger(__name__)

_UNSET = object()

class MovieNotFoundError(Exception):
  pass

class MovieAlreadyExistsError(Exception):
  pass

def create_movie(db: Session, title: str, description: str, duration: int, poster_url: str, genre_id: UUID | None = None) -> Movie:
  try:
    movie = db.query(Movie).filter(Movie.title == title).first()
    if movie:
      raise MovieAlreadyExistsError(f"Movie with title {title} already exists")
    new_movie = Movie(
      title=title,
      description=description,
      duration=duration,
      poster_url=poster_url,
      genre_id=genre_id
    )
    
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie
  except MovieAlreadyExistsError:
    raise
  except SQLAlchemyError as e:
    db.rollback()
    logger.error("Database error occurred while creating movie: %s", str(e))
    raise
  except Exception as e:
    db.rollback()
    logger.error("Unexpected error occurred while creating movie: %s", str(e))
    raise
    
def update_movie(db: Session, movie_id: UUID, title: str | None = None, description: str | None = None, duration: int | None = None, poster_url: str | None = None, genre_id: UUID | None = _UNSET) -> Movie:
  try:
    movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
    
    if not movie:
      raise MovieNotFoundError(f"Movie with id {movie_id} not found")
    if title is not None:
      movie.title = title
    if description is not None:
      movie.description = description
    if duration is not None:
      movie.duration = duration
    if poster_url is not None:
      movie.poster_url = poster_url
    if genre_id is not _UNSET:
      movie.genre_id = genre_id

    db.commit()
    db.refresh(movie)
    return movie
  except MovieNotFoundError:
    raise
  except SQLAlchemyError as e:
    db.rollback()
    logger.error("Database error occurred while updating movie: %s", str(e))
    raise
  except Exception as e:
    db.rollback()
    logger.error("Unexpected error occurred while updating movie: %s", str(e))
    raise
  
def delete_movie(db: Session, movie_id: UUID):
  try:
    movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
    if not movie:
      raise MovieNotFoundError(f"Movie with id {movie_id} not found")
    
    db.delete(movie)
    db.commit()
  except MovieNotFoundError:
    raise
  except SQLAlchemyError as e:
    db.rollback()
    logger.error("Database error occurred while deleting movie: %s", str(e))
    raise
  except Exception as e:
    db.rollback()
    logger.error("Unexpected error occurred while deleting movie: %s", str(e))
    raise