from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import get_db
from app.models.movie import Movie
from app.services.admin.movie_service import create_movie, update_movie, delete_movie, MovieNotFoundError, MovieAlreadyExistsError
from app.schemas.admin.movie import CreateMovieRequest, UpdateMovieRequest, MovieResponse

router = APIRouter(prefix="/admin/movies", tags=["Admin Movies"])

@router.post('/', response_model=MovieResponse)
def create_movie_endpoint(request: CreateMovieRequest, db: Session = Depends(get_db)):
  try:
    movie = create_movie(db, request.title, request.description, request.duration, request.poster_url, request.genre_id)
    return movie
  except MovieAlreadyExistsError as e:
    raise HTTPException(status_code=400, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")
  
@router.put('/{movie_id}', response_model=MovieResponse)
def update_movie_endpoint(movie_id: UUID, request: UpdateMovieRequest, db: Session = Depends(get_db)):
  try:
    movie = update_movie(db, movie_id, request.title, request.description, request.duration, request.poster_url, request.genre_id)
    return movie
  except MovieNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")
  
@router.delete('/{movie_id}', status_code=204)
def delete_movie_endpoint(movie_id: UUID, db: Session = Depends(get_db)):
  try:
    delete_movie(db, movie_id)
  except MovieNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")