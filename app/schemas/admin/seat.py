from pydantic import BaseModel
from uuid import UUID

class CreateSeatRequest(BaseModel):
  screen_id: UUID
  row: str
  col: str

class SeatResponse(BaseModel):
  seat_id: UUID
  screen_id: UUID
  row: str
  col: str
  
  class Config:
    from_attributes = True