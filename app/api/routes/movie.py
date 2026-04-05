from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import get_db
from app.services.movie_service import get_movies, get_latest_movies, get_search_movies, get_movie_by_id, MovieNotFoundError
from app.schemas.movie import MovieResponse, PaginatedMovieResponse

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get('/', response_model=PaginatedMovieResponse)
def get_movies_endpoint(page: int = Query(default=1, ge=1), page_size: int = Query(default=10), db: Session = Depends(get_db)):
    return get_movies(db, page, page_size)

@router.get('/latest', response_model=list[MovieResponse])
def get_latest_movies_endpoint(db: Session = Depends(get_db)):
    return get_latest_movies(db)
  
@router.get('/search', response_model=PaginatedMovieResponse)
def get_search_movies_endpoint(title: str = Query(default=None), genre: str = Query(default=None), page: int = Query(default=1, ge=1), page_size: int = Query(default=10), db: Session = Depends(get_db)):
  return get_search_movies(db, title, genre, page, page_size)

@router.get('/{movie_id}', response_model=MovieResponse)
def get_movie_by_id_endpoint(movie_id: UUID, db: Session = Depends(get_db)):
  try:
    return get_movie_by_id(db, movie_id)
  except MovieNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")