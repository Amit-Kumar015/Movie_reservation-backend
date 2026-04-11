import logging
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.screen import Screen
from app.models.seat import Seat

logger = logging.getLogger(__name__)

class ScreenNotFoundError(Exception):
  pass

class SeatNotFoundError(Exception):
  pass

def create_seats_for_screen(db: Session, screen_id: UUID, row: str, col: str) -> list[Seat]:
  try:
    screen = db.query(Screen).filter_by(screen_id=screen_id).first()
    if not screen:
      raise ScreenNotFoundError("Screen with the given ID was not found.")

    db.query(Seat).filter(Seat.screen_id == screen_id).delete(synchronize_session=False)

    seats = []
    for r in range(int(row)):
      for c in range(int(col)):
        new_seat = Seat(screen_id=screen_id, row=chr(65 + r), col=str(c + 1))
        seats.append(new_seat)
        
    db.add_all(seats)
    db.flush()
    db.commit()
    for seat in seats:
      db.refresh(seat)
    return seats
  except ScreenNotFoundError:
    raise
  except SQLAlchemyError as e:
    logger.error(f"Database error while creating seats for screen {screen_id}: {str(e)}")
    db.rollback()
    raise
  except Exception as e:
    logger.error(f"Unexpected error while creating seats for screen {screen_id}: {str(e)}")
    db.rollback()
    raise
  
def delete_seat_for_screen(db: Session, seat_id: UUID) -> None:
  try:
    seat = db.query(Seat).filter_by(seat_id=seat_id).first()
    if not seat:
      raise SeatNotFoundError(f"Seat with id {seat_id} not found")
    
    db.delete(seat)
    db.commit()
  except SeatNotFoundError:
    raise
  except SQLAlchemyError as e:
    logger.error(f"Database error while deleting seat {seat_id}: {str(e)}")
    db.rollback()
    raise
  except Exception as e:
    logger.error(f"Unexpected error while deleting seat {seat_id}: {str(e)}")
    db.rollback()
    raise
      