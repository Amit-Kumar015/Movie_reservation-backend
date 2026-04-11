from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ScreenCreateRequest(BaseModel):
    name: str
    venue_id: UUID
    row: str
    col: str
    
class ScreenCreateResponse(BaseModel):
    screen_id: UUID
    name: str
    venue: str
    seats: list[str]
    
    class Config:
      from_attributes = True

class ScreenUpdateRequest(BaseModel):
    name: Optional[str] = None
    venue_id: Optional[UUID] = None

class ScreenResponse(BaseModel):
    screen_id: UUID
    name: str
    venue: str
    
    class Config:
      from_attributes = True