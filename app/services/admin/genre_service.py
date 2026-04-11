import logging
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.genre import Genre

logger = logging.getLogger(__name__)

class GenreNotFoundError(Exception):
  pass

class GenreAlreadyExistsError(Exception):
  pass

def create_genre(db: Session, genre_type: str) -> Genre:
  try:
    genre = db.query(Genre).filter(Genre.genre_type == genre_type).first()
    if genre:
      raise GenreAlreadyExistsError(f"Genre with type '{genre_type}' already exists")
    new_genre = Genre(genre_type=genre_type)
    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)
    return new_genre
  except GenreAlreadyExistsError:
    raise
  except SQLAlchemyError as e:
    logger.error(f"Error creating genre: {e}")
    db.rollback()
    raise
  except Exception as e:
    logger.error(f"Unexpected error creating genre: {e}")
    db.rollback()
    raise
  
def update_genre(db: Session, genre_id: UUID, genre_type: str) -> Genre:
  try:
    genre = db.query(Genre).filter(Genre.genre_id == genre_id).first()
    if not genre:
      raise GenreNotFoundError(f"Genre with id {genre_id} not found")
    genre.genre_type = genre_type
    db.commit()
    db.refresh(genre)
    return genre
  except GenreNotFoundError:  
    raise 
  except SQLAlchemyError as e:
    logger.error(f"Error updating genre: {e}")
    db.rollback()
    raise
  except Exception as e:
    logger.error(f"Unexpected error updating genre: {e}")
    db.rollback()
    raise
  
def delete_genre(db: Session, genre_id: UUID):
  try:
    genre = db.query(Genre).filter(Genre.genre_id == genre_id).first()
    if not genre:
      raise GenreNotFoundError(f"Genre with id {genre_id} not found")
    db.delete(genre)
    db.commit()
  except GenreNotFoundError:  
    raise 
  except SQLAlchemyError as e:
    logger.error(f"Error deleting genre: {e}")
    db.rollback()
    raise
  except Exception as e:
    logger.error(f"Unexpected error deleting genre: {e}")
    db.rollback()
    raise