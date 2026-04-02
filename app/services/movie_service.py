import logging
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.movie import Movie

logger = logging.getLogger(__name__)

class MovieNotFoundError(Exception):
  pass

def get_movies(db: Session, page: int = 1, page_size: int = 10):
  try:
    offset = (page - 1) * page_size
    total = db.query(Movie).count()
    movies = db.query(Movie).order_by(Movie.created_at.desc()).offset(offset).limit(page_size).all()
    return {"total": total, "page": page, "page_size": page_size, "movies": movies}
  except SQLAlchemyError as e:
    logger.error("Database error occurred while fetching movies: %s", str(e))
    raise 
  except Exception as e:
    logger.error("Unexpected error occurred while fetching movies: %s", str(e))
    raise 

def get_latest_movies(db:Session):
  try:
    movies = db.query(Movie).order_by(Movie.created_at.desc()).limit(10).all()
    return movies
  
  except SQLAlchemyError as e:
    logger.error("Database error occurred while fetching latest movies: %s", str(e))
    raise
  except Exception as e:
    logger.error("Unexpected error occurred while fetching latest movies: %s", str(e))
    raise
  
def get_search_movies(db:Session, title: str | None = None, genre: str | None = None, page:int = 1, page_size: int = 10):
  try:
    offset = (page - 1) * page_size
    query = db.query(Movie)
    if title:
      query = query.filter(Movie.title.ilike(f"%{title}%"))
    if genre:
      query = query.filter(Movie.genre.ilike(f"%{genre}%"))
    total = query.count()
    movies = query.order_by(Movie.created_at.desc()).offset(offset).limit(page_size).all()
    return {"total": total, "page": page, "page_size": page_size, "movies": movies}
  except SQLAlchemyError as e:
    logger.error("Database error occurred while fetching search movies: %s", str(e))
    raise
  except Exception as e:
    logger.error("Unexpected error occurred while fetching search movies: %s", str(e))
    raise
  
def get_movie_by_id(db: Session, movie_id: UUID) -> Movie:
  try:
    movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
    if not movie:
      raise MovieNotFoundError(f"Movie with ID {movie_id} not found")
    return movie
  except SQLAlchemyError as e:
    logger.error("Database error occurred while fetching movie by ID: %s", str(e))
    raise
  except Exception as e:
    logger.error("Unexpected error occurred while fetching movie by ID: %s", str(e))
    raise