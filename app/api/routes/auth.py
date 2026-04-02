from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import get_db
from app.services.auth_service import signup, login, get_current_user, UserAlreadyExistsException, InvalidCredentialsError, InvalidTokenError
from app.schemas.auth import SignUpRequest, LoginRequest, UserResponse, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])
bearer_scheme = HTTPBearer()

@router.post("/signup", response_model=UserResponse, status_code=201)
def signup_user_endpoint(request: SignUpRequest, db: Session = Depends(get_db)):
  try:
    return signup(db, request.name, request.email, request.password)
  except UserAlreadyExistsException as e:
    raise HTTPException(status_code=400, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/login", response_model=TokenResponse)
def login_user_endpoint(request: LoginRequest, db: Session = Depends(get_db)):
  try:
    return login(db, request.email, request.password)
  except InvalidCredentialsError as e:
    raise HTTPException(status_code=401, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/me", response_model=UserResponse)
def get_user_endpoint(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
  try:
    return get_current_user(db, credentials.credentials)
  except InvalidTokenError as e:
    raise HTTPException(status_code=401, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")
  
