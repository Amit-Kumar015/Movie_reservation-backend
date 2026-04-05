from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class ReservationRequest(BaseModel):
  showtime_id: UUID
  seat_ids: list[UUID] = Field(min_length=1, max_length=10)
  
class ReservationSeatsResponse(BaseModel):
  reservation_seat_id: UUID
  seat_id: UUID
  status: str
  
  class Config:
    from_attributes = True
  
class ReservationResponse(BaseModel):
  reservation_id: UUID
  user_id: UUID
  showtime_id: UUID
  total_price: float
  status: str
  created_at: datetime
  reservation_seats: list[ReservationSeatsResponse]
  
  class Config:
    from_attributes = True
    
class ReservationListResponse(BaseModel):
  reservations: list[ReservationResponse]