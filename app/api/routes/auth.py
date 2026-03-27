from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.auth_service import signup, login, get_current_user
from app.schemas.auth import SignUpRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])
bearer_scheme = HTTPBearer()

@router.post("/signup")
def signup_user(request: SignUpRequest, db: Session = Depends(get_db)):
  return signup(db, request.name, request.email, request.password)

@router.post("/login")
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
  return login(db, request.email, request.password)

@router.get("/me")
def get_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
  return get_current_user(db, credentials.credentials)
  
