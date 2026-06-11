import logging

from celery import Celery
from app.core.config import settings
from app.api.deps import get_db
from app.models.reservation import Reservation
from app.models.reservation_seat import ReservationSeat
from app.models.enum import ReservationStatus, ReservationSeatStatus
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(name="tasks.expire_reservation_timeout")
def expire_reservation_timeout(reservation_id: str):
  db = get_db()
  try:
    reservation = db.query(Reservation).filter(Reservation.reservation_id == reservation_id).with_for_update().first()
    
    if reservation.status == ReservationStatus.PENDING:
      reservation.status = ReservationStatus.CANCELLED
      
      seats = db.query(ReservationSeat).filter(ReservationSeat.reservation_id == reservation_id).all()
      for seat in seats:
        seat.status = ReservationSeatStatus.CANCELLED
        
      db.commit()
      logger.info(f"Reservation {reservation_id} expired. Seats released back to inventory.")
      return f"Reservation {reservation_id} expired successfully."
    
    return f"Reservation {reservation_id} was already processed (Status: {reservation.status})."
  except Exception as e:
    db.rollback()
    logger.error(f"Error handling timeout for reservation {reservation_id}: {e}")
    return
  