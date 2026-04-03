from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
import logging
from uuid import UUID

from app.models.seat import Seat
from app.models.screen import Screen
from app.models.showtime import Showtime

logger = logging.getLogger(__name__)

class SeatNotFoundError(Exception):
  pass

def get_seats_by_showtime_id(db: Session, showtime_id: UUID) -> list[Seat]:
  try:
    showtime = db.query(Showtime).options(joinedload(Showtime.screen).joinedload(Screen.seats), joinedload(Showtime.reservations_seats)).filter(Showtime.showtime_id == showtime_id).first()
    if not showtime:
      raise SeatNotFoundError(f"No showtime found with ID {showtime_id}")
    seats = showtime.screen.seats
    booked_seats_ids = {
      rs.seat_id for rs in showtime.reservations_seats if rs.status == "BOOKED"
    }
    return [
      {
        "seat_id": seat.seat_id,
        "row": seat.row,
        "col": seat.col,
        "is_available": seat.seat_id not in booked_seats_ids
      }
      for seat in seats
    ]
  except SQLAlchemyError as e:
    logger.error(f"Error occurred while fetching seats for showtime {showtime_id}: {e}")
    raise
  except Exception as e:
    logger.error(f"Unexpected error occurred while fetching seats for showtime {showtime_id}: {e}")
    raise