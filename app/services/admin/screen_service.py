import logging
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.screen import Screen
from app.services.admin.seat_service import create_seats_for_screen

logger = logging.getLogger(__name__)

class ScreenNotFoundError(Exception):
  pass

class ScreenAlreadyExistsError(Exception):
  pass

def create_screen(db: Session, name: str, venue_id: UUID, row: str, col: str) -> Screen:
  try:
    screen = db.query(Screen).filter_by(name=name, venue_id=venue_id).first()
    if screen:
      raise ScreenAlreadyExistsError(f"Screen with name {name} already exists in venue {venue_id}")
    
    new_screen = Screen(name=name, venue_id=venue_id)
    db.add(new_screen)
    db.flush()
    
    seats = create_seats_for_screen(db, new_screen.screen_id, row, col)
    seat_labels = [f"{seat.row}{seat.col}" for seat in seats]
    
    db.commit()
    db.refresh(new_screen)
    return {"screen_id": new_screen.screen_id, "name": new_screen.name, "venue": new_screen.venue.name, "seats": seat_labels}
  except ScreenAlreadyExistsError as e:
    logger.warning(str(e))
    raise
  except SQLAlchemyError as e:
    logger.error(f"Database error while creating screen: {str(e)}")
    db.rollback()
    raise
  except Exception as e:
    logger.error(f"Unexpected error while creating screen: {str(e)}")
    db.rollback()
    raise
  
def update_screen(db: Session, screen_id: UUID, name: str | None = None, venue_id: UUID | None = None) -> Screen:
  try:
    screen = db.query(Screen).filter(Screen.screen_id == screen_id).first()
    if not screen:
      raise ScreenNotFoundError(f"Screen with ID {screen_id} not found")

    if name is not None:
      screen.name = name
    if venue_id is not None:
      screen.venue_id = venue_id

    db.commit()
    db.refresh(screen)
    return {"screen_id": screen.screen_id, "name": screen.name, "venue": screen.venue.name}
  except ScreenNotFoundError as e:
    logger.warning(str(e))
    raise
  except SQLAlchemyError as e:
    logger.error(f"Database error while updating screen: {str(e)}")
    db.rollback()
    raise
  except Exception as e:
    logger.error(f"Unexpected error while updating screen: {str(e)}")
    db.rollback()
    raise
  
def delete_screen(db: Session, screen_id: UUID) -> None:
  try:
    screen = db.query(Screen).filter(Screen.screen_id == screen_id).first()
    if not screen:
      raise ScreenNotFoundError(f"Screen with ID {screen_id} not found")
    
    db.delete(screen)
    db.commit()
  except ScreenNotFoundError as e:
    logger.warning(str(e))
    raise
  except SQLAlchemyError as e:
    logger.error(f"Database error while deleting screen: {str(e)}")
    db.rollback()
    raise
  except Exception as e:
    logger.error(f"Unexpected error while deleting screen: {str(e)}")
    db.rollback()
    raise
