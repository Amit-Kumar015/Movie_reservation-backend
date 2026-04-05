from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from app.api.deps import get_db
from app.services.showtime_service import get_showtimes_by_movie, get_showtime_by_id, ShowtimeNotFoundError
from app.schemas.showtime import ShowtimeResponse, ShowtimeListResponse

router = APIRouter(prefix='/showtimes', tags=['Showtimes'])

@router.get('/movie/{movie_id}', response_model=ShowtimeListResponse)
def get_showtimes_by_movie_endpoint(movie_id: UUID, date: Optional[datetime] = Query(default=None), db : Session = Depends(get_db)):
  try:
    showtimes = get_showtimes_by_movie(db, movie_id, date)
    return ShowtimeListResponse(date=date, showtimes=showtimes)
  except ShowtimeNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")
  
@router.get('/{showtime_id}', response_model=ShowtimeResponse)
def get_showtime_by_id_endpoint(showtime_id: UUID, db : Session = Depends(get_db)):
  try:
    return get_showtime_by_id(db, showtime_id)
  except ShowtimeNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")