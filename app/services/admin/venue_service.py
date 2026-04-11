import logging
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.venue import Venue

logger = logging.getLogger(__name__) 

class VenueNotFoundError(Exception):
  pass 

class VenueAlreadyExistsError(Exception):
  pass

def create_venue(db: Session, name: str, location: str) -> Venue:
  try:
    venue = db.query(Venue).filter_by(name=name, location=location).first()
    if venue:
      raise VenueAlreadyExistsError(f"Venue with name {name} and location {location} already exists")
    
    new_venue = Venue(name=name, location=location)
    db.add(new_venue)
    db.commit()
    db.refresh(new_venue)
    return new_venue
  except VenueAlreadyExistsError as e:
    logger.warning(str(e))
    raise 
  except SQLAlchemyError as e:
    logger.error(f"Database error while creating venue: {str(e)}")
    db.rollback()
    raise
  except Exception as e:
    logger.error(f"Unexpected error while creating venue: {str(e)}")
    db.rollback()
    raise
  
def update_venue(db: Session, venue_id: UUID, name: str | None = None, location: str | None = None) -> Venue:
  try:
    venue = db.query(Venue).filter_by(venue_id=venue_id).first()
    if not venue:
      raise VenueNotFoundError(f"Venue with id {venue_id} not found")
    
    if name:
      venue.name = name
    if location:
      venue.location = location
    
    db.commit()
    db.refresh(venue)
    return venue
  except VenueNotFoundError as e:
    logger.warning(str(e))
    raise 
  except SQLAlchemyError as e:
    logger.error(f"Database error while updating venue: {str(e)}")
    db.rollback()
    raise
  except Exception as e:
    logger.error(f"Unexpected error while updating venue: {str(e)}")
    db.rollback()
    raise
  
def delete_venue(db: Session, venue_id: UUID) -> None:
  try:
    venue = db.query(Venue).filter_by(venue_id=venue_id).first()
    if not venue:
      raise VenueNotFoundError(f"Venue with id {venue_id} not found")
    db.delete(venue)
    db.commit()
  except VenueNotFoundError as e:
    logger.warning(str(e))
    raise
  except SQLAlchemyError as e:
    logger.error(f"Database error while deleting venue: {str(e)}")
    db.rollback()
    raise
  except Exception as e:
    logger.error(f"Unexpected error while deleting venue: {str(e)}")
    db.rollback()
    raise