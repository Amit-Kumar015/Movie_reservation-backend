from uuid import UUID
from pydantic import BaseModel, field_validator
from typing import Any, Optional
from datetime import datetime

class SearchMovieRequest(BaseModel):
  title: Optional[str] = None
  genre: Optional[str] = None
  page: int = 1
  page_size: int = 10
  
class MovieResponse(BaseModel):
  movie_id: UUID
  title: str
  description: Optional[str] = None
  duration: int
  poster_url: str
  genre: Optional[str] = None
  created_at: datetime
  
  class Config:
    from_attributes = True
    
  @field_validator("genre", mode="before")
  @classmethod
  def serialize_genre_object(cls, value: Any) -> Optional[str]:
      if value is None:
          return None
        
      if hasattr(value, "name"):
          return value.name
      return str(value)
  
  
class PaginatedMovieResponse(BaseModel):
  total: int
  page: int
  page_size: int
  movies: list[MovieResponse]
  