from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class CreateMovieRequest(BaseModel):
  title: str
  description: str
  duration: int
  poster_url: str
  genre_id: UUID
  
class MovieResponse(BaseModel):
  movie_id: UUID
  title: str
  description: Optional[str]
  duration: int
  poster_url: str
  genre_id: Optional[UUID]
  
  class Config:
    from_attributes = True
    
class UpdateMovieRequest(BaseModel):
  title: Optional[str] = None
  description: Optional[str] = None
  duration: Optional[int] = None
  poster_url: Optional[str] = None
  genre_id: Optional[UUID] = None
  
  
  

