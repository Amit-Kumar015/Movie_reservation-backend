from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import get_db
from app.services.admin.genre_service import create_genre, update_genre, delete_genre, GenreNotFoundError, GenreAlreadyExistsError
from app.schemas.admin.genre import CreateGenreRequest, GenreResponse

router = APIRouter(prefix="/admin/genres", tags=["Admin Genres"])

@router.post('/', response_model=GenreResponse)
def create_genre_endpoint(request: CreateGenreRequest, db: Session = Depends(get_db)):
  try:
    genre = create_genre(db, request.genre_type)
    return genre
  except GenreAlreadyExistsError as e:
    raise HTTPException(status_code=400, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")
  
@router.put('/{genre_id}', response_model=GenreResponse)
def update_genre_endpoint(genre_id: UUID, request: CreateGenreRequest, db: Session = Depends(get_db)):
  try:
    genre = update_genre(db, genre_id, request.genre_type)
    return genre
  except GenreNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")
  
@router.delete('/{genre_id}')
def delete_genre_endpoint(genre_id: UUID, db: Session = Depends(get_db)):
  try:
    delete_genre(db, genre_id)
    return {"detail": "Genre deleted successfully"}
  except GenreNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")