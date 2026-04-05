from app.db.database import SessionLocal
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.auth_service import get_current_user, InvalidTokenError

bearer_scheme = HTTPBearer()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
    
def get_authenticated_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)) -> User:
  try:
    return get_current_user(db, credentials.credentials)
  except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=str(e))
  except Exception:
      raise HTTPException(status_code=401, detail="Authentication failed")
    
def get_admin_user(current_user: User = Depends(get_authenticated_user)) -> User:
  if not current_user.is_admin:
    raise HTTPException(status_code=403, detail="Admin privileges required")
  return current_user