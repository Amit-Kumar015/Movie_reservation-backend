from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.reservation import ReservationRequest, ReservationResponse, ReservationListResponse
from app.services.reservation import cancel_reservation, create_reservation, ReservationNotFoundError, SeatNotAvailableError, ShowtimeNotFoundError, get_all_reservations_by_user, get_reservation_by_id, ReservationError
from app.api.deps import get_authenticated_user, get_db
from app.models.user import User

router = APIRouter(prefix='/reservations', tags=['Reservations'])

@router.post('/', response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def make_reservation(request: ReservationRequest, db: Session = Depends(get_db), current_user: User = Depends(get_authenticated_user)):
  try:
    reservation = create_reservation(db, current_user.user_id, request.showtime_id, request.seat_ids)
    return reservation
  except SeatNotAvailableError as e:
    raise HTTPException(status_code=409, detail=str(e))
  except ShowtimeNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error occurred")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")
  
@router.get('/my', response_model=ReservationListResponse)
def get_users_reservations(db: Session = Depends(get_db), current_user: User = Depends(get_authenticated_user)):
  try:
    reservations = get_all_reservations_by_user(db, current_user.user_id)
    return ReservationListResponse(reservations=reservations)
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error occurred")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")
  
@router.get('/{reservation_id}', response_model=ReservationResponse)
def reservation_by_id(reservation_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_authenticated_user)):
  try:
    reservation = get_reservation_by_id(db, reservation_id, current_user.user_id)
    return reservation
  except ReservationNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error occurred")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")
  
@router.delete('/{reservation_id}', response_model=ReservationResponse)
def cancel_reservation_by_id(reservation_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_authenticated_user)):
  try:
    reservation = cancel_reservation(db, reservation_id, current_user.user_id)
    return reservation
  except ReservationNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except ReservationError as e:
        raise HTTPException(status_code=400, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error occurred")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")