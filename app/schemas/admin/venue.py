from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class CreateVenueRequest(BaseModel):
  name: str
  location: str
  
class UpdateVenueRequest(BaseModel):
  name: Optional[str] = None
  location: Optional[str] = None
  
class VenueResponse(BaseModel):
  venue_id: UUID
  name: str
  location: str
  
  class Config:
    from_attributes = True