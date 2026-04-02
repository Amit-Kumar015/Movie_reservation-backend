from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class ShowtimeResponse(BaseModel):
  showtime_id: UUID
  movie_id: UUID
  screen_id: UUID
  start_time: datetime
  end_time: datetime
  price: float
  total_seats: int
  available_seats: int
  
  class Config:
    from_attributes = True
    
class ShowtimeListResponse(BaseModel):
  date: Optional[datetime] = None
  showtimes: list[ShowtimeResponse]
  