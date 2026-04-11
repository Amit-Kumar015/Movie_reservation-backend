from pydantic import BaseModel
from uuid import UUID

class CreateGenreRequest(BaseModel):
  genre_type: str

class GenreResponse(BaseModel):
  genre_id: UUID
  genre_type: str

  class Config:
    from_attributes = True