from pydantic import BaseModel
from uuid import UUID

class SeatResponse(BaseModel):
  seat_id: UUID
  row: str
  col: str
  is_available: bool
  
  class Config:
    from_attributes = True
    
class SeatListResponse(BaseModel):
  seats: list[SeatResponse]