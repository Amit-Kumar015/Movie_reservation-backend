from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import get_db
from app.services.seat_service import get_seats_by_showtime_id, SeatNotFoundError
from app.schemas.seats import SeatListResponse

router = APIRouter(prefix='/seats', tags=['Seats'])

@router.get('/showtime/{showtime_id}', response_model=SeatListResponse)
def get_seats_by_showtime_id_endpoints(showtime_id: UUID, db: Session = Depends(get_db)):
  try:
    seats = get_seats_by_showtime_id(db, showtime_id)
    return SeatListResponse(seats=seats)
  except SeatNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error occurred")
  except Exception:
    raise HTTPException(status_code=500, detail="An unexpected error occurred")