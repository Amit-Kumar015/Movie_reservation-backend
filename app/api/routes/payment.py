import logging

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.enum import ReservationSeatStatus, ReservationStatus
from app.models.reservation import Reservation
from app.models.reservation_seat import ReservationSeat

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/payments', tags=['Payments'])

@router.post("/webhook", status_code=status.HTTP_200_OK)
def payment_webhook(payload: dict, db: Session = Depends(get_db)):
  reservation_id_str = payload.get("metadata", {}).get("reservation_id")
  
  if not reservation_id_str:
    raise HTTPException(status_code=400, detail="Missing reservation_id in payload metadata.")
  
  try:
    reservation_id = UUID(reservation_id_str)
    reservation = db.query(Reservation).filter(Reservation.reservation_id == reservation_id).with_for_update().first()

    if not reservation:
      raise HTTPException(status_code=404, detail="Reservation not found.")

    if reservation.status == ReservationStatus.CANCELLED:
      logger.warning(f"Payment received for already EXPIRED reservation {reservation_id}. Triggering refund process.")
      return {"status": "error", "message": "Reservation expired. Processing autonomous customer refund."}

    if reservation and reservation.status == ReservationStatus.PENDING:
      reservation.status = ReservationStatus.CONFIRMED
      
      seats = db.query(ReservationSeat).filter(ReservationSeat.reservation_id == reservation_id).with_for_update().all()
      
      for seat in seats:
        seat.status = ReservationSeatStatus.BOOKED

      db.commit()
      logger.info(f"Payment verification successful. Booking {reservation_id} finalized permanently.")
      return {"status": "Success, booking secured permanently!"}

    return {"status": "ignored", "message": f"Reservation already processed with status: {reservation.status}"}
  except ValueError:
      raise HTTPException(status_code=400, detail="Invalid reservation UUID format structured.")
  except Exception as e:
      db.rollback()
      logger.error(f"Critical execution error processing payment verification webhook: {e}")
      raise HTTPException(status_code=500, detail="Internal processing error occurred.")