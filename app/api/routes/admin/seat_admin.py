from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import get_db
from app.services.admin.seat_service import create_seats_for_screen, delete_seat_for_screen, ScreenNotFoundError, SeatNotFoundError
from app.schemas.admin.seat import CreateSeatRequest, SeatResponse

router = APIRouter(prefix="/admin/seats", tags=["Admin Seats"])

@router.post('/', response_model=list[SeatResponse])
def create_seats_for_screen_endpoint(request: CreateSeatRequest, db: Session = Depends(get_db)):
  try:
    seats = create_seats_for_screen(db, request.screen_id, request.row, request.col)
    return seats
  except ScreenNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")
  
@router.delete('/{seat_id}')
def delete_seat_for_screen_endpoint(seat_id: UUID, db: Session = Depends(get_db)):
  try:
    delete_seat_for_screen(db, seat_id)
    return {"detail": "Seat deleted successfully"}
  except SeatNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")