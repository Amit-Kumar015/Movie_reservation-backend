from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import get_db
from app.services.admin.showtime_service import create_showtime, delete_showtime, MovieNotFoundError, ShowtimeNotFoundError, ScreenNotFoundError
from app.schemas.admin.showtime import CreateShowtimeRequest, ShowtimeResponse

router = APIRouter(prefix="/admin/showtimes", tags=["Admin Showtimes"])

@router.post('/', response_model=ShowtimeResponse)
def create_showtime_endpoint(request: CreateShowtimeRequest, db: Session = Depends(get_db)):
  try:
    showtime = create_showtime(db, request.screen_id, request.movie_id, request.start_time, request.price)
    return showtime
  except MovieNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except ScreenNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")
  
@router.delete('/{showtime_id}')
def delete_showtime_endpoint(showtime_id: UUID, db: Session = Depends(get_db)):
  try:
    delete_showtime(db, showtime_id)
    return {"detail": "Showtime deleted successfully"}
  except ShowtimeNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")