from pydantic import BaseModel, EmailStr, Field
from enum import Enum

from sqlalchemy import UUID

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class SignUpRequest(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)
    
class UserResponse(BaseModel):
  user_id: UUID
  name: str
  email: str
  role: UserRole
  
  class Config:
    from_attributes = True
    
class TokenResponse(BaseModel):
  access_token: str
  token_type: str
