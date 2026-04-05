import logging
from sqlalchemy.orm import Session, joinedload
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.enum import ReservationSeatStatus, ReservationStatus
from app.models.reservation import Reservation
from app.models.reservation_seat import ReservationSeat
from app.models.showtime import Showtime
from app.models.screen import Screen

logger = logging.getLogger(__name__)

class ReservationError(Exception):
    pass

class SeatNotAvailableError(Exception):
    pass
  
class ShowtimeNotFoundError(Exception):
    pass
  
class ReservationNotFoundError(Exception):
    pass

def create_reservation(db: Session, user_id: UUID, showtime_id: UUID, seat_ids: list[UUID]) -> Reservation:
  try:
    showtime = db.query(Showtime).options(joinedload(Showtime.screen).joinedload(Screen.seats), joinedload(Showtime.reservation_seats)).filter(Showtime.showtime_id == showtime_id).first()
    if not showtime:
        raise ShowtimeNotFoundError("Showtime not found")
    
    booked_seat_ids = {
      rs.seat_id
      for rs in showtime.reservation_seats
      if rs.status in [ReservationSeatStatus.BOOKED, ReservationSeatStatus.PENDING]
    }
    
    unavailable_seats = [sid for sid in seat_ids if sid in booked_seat_ids]
    if unavailable_seats:
        raise SeatNotAvailableError(f"Seats not available: {unavailable_seats}")
      
    total_price = showtime.price * len(seat_ids)
    
    reservation = Reservation(user_id=user_id, showtime_id=showtime_id, total_price=total_price)
    db.add(reservation)
    db.flush()
    
    for seat_id in seat_ids:
      reservation_seat = ReservationSeat(reservation_id = reservation.reservation_id, seat_id = seat_id, showtime_id = showtime_id, status=ReservationSeatStatus.CONFIRMED)
      db.add(reservation_seat)
      
    db.commit()
    db.refresh(reservation)
    return reservation
  except (ShowtimeNotFoundError, SeatNotAvailableError) as e:
    raise
  except IntegrityError as e:
    db.rollback()
    logger.error("Double booking attempt for showtime %s", showtime_id)
    raise SeatNotAvailableError("One or more seats were just taken. Please try again.")
  except SQLAlchemyError as e:
    db.rollback()
    logger.error(f"DB error during reservation creation: {e}")
    raise
  except Exception as e:
    db.rollback()
    logger.error(f"Unexpected error during reservation creation: {e}")
    raise
  
def get_all_reservations_by_user(db: Session, user_id: UUID) -> list[Reservation]:
  try:
    return db.query(Reservation).options(joinedload(Reservation.reservation_seats)).filter(Reservation.user_id == user_id).all()
  except SQLAlchemyError as e:
    logger.error(f"DB error during fetching reservations: {e}")
    raise
  except Exception as e:
    logger.error(f"Unexpected error during fetching reservations: {e}")
    raise
  
def get_reservation_by_id(db: Session, reservation_id: UUID, user_id: UUID, is_admin: bool = False) -> Reservation:
  try:
    reservation = db.query(Reservation).options(joinedload(Reservation.reservation_seats)).filter(Reservation.reservation_id == reservation_id)
    
    if not is_admin:
      query = db.query(Reservation).filter(Reservation.user_id == user_id)
      
    reservation = query.first()
    if not reservation:
        raise ReservationNotFoundError("Reservation not found")
    return reservation
  except ReservationNotFoundError:
    raise
  except SQLAlchemyError as e:
    logger.error(f"DB error during fetching reservation {reservation_id}: {e}")
    raise
  except Exception as e:
    logger.error(f"Unexpected error during fetching reservation {reservation_id}: {e}")
    raise
  
def cancel_reservation(db: Session, reservation_id: UUID, user_id: UUID) -> Reservation:
  try:
    reservation = db.query(Reservation).options(joinedload(Reservation.reservation_seats)).filter(Reservation.reservation_id == reservation_id, Reservation.user_id == user_id).first()
    if not reservation:
        raise ReservationNotFoundError("Reservation not found")
      
    reservation.status = ReservationStatus.CANCELLED
    for rs in reservation.reservation_seats:
      rs.status = ReservationSeatStatus.CANCELLED
    
    db.commit()
    return reservation
  except ReservationNotFoundError:
    raise
  except SQLAlchemyError as e:
    db.rollback()
    logger.error(f"DB error during cancelling reservation {reservation_id}: {e}")
    raise
  except Exception as e:
    db.rollback()
    logger.error(f"Unexpected error during cancelling reservation {reservation_id}: {e}")
    raise