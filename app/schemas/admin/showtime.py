from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class CreateShowtimeRequest(BaseModel):
  screen_id: UUID
  movie_id: UUID
  start_time: datetime
  price: float
  
class ShowtimeResponse(BaseModel):
  showtime_id: UUID
  screen_id: UUID
  movie_id: UUID
  start_time: datetime
  end_time: datetime
  price: float
  
  class Config:
    from_attributes = True