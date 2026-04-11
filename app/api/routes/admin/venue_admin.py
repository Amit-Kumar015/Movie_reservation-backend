from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import get_db
from app.services.admin.venue_service import VenueNotFoundError, create_venue, update_venue, delete_venue, VenueAlreadyExistsError
from app.schemas.admin.venue import CreateVenueRequest, UpdateVenueRequest, VenueResponse

router = APIRouter(prefix='/admin/venues', tags=['Admin Venues'])

@router.post('/', response_model=VenueResponse)
def create_venue_endpoint(request: CreateVenueRequest, db: Session = Depends(get_db)):
  try:
    venue = create_venue(db, request.name, request.location)
    return venue
  except VenueAlreadyExistsError as e:
    raise HTTPException(status_code=400, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")
  
@router.put('/{venue_id}', response_model=VenueResponse)
def update_venue_endpoint(venue_id: UUID, request: UpdateVenueRequest, db: Session = Depends(get_db)):
  try:
    venue = update_venue(db, venue_id, request.name, request.location)
    return venue
  except VenueNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")
  
@router.delete('/{venue_id}')
def delete_venue_endpoint(venue_id: UUID, db: Session = Depends(get_db)):
  try:    
    delete_venue(db, venue_id)
    return {"detail": "Venue deleted successfully"}
  except VenueNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")
  