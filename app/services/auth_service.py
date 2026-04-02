import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token, decode_token

logger = logging.getLogger(__name__)

class UserAlreadyExistsException(Exception):
  pass

class InvalidCredentialsError(Exception):
  pass

class InvalidTokenError(Exception):
  pass

def signup(db: Session, name: str, email: str, password: str):    
    try:  
      existing_user = db.query(User).filter(User.email == email).first()
      if existing_user:
          raise UserAlreadyExistsException("Email already registered")

      new_user = User(
          name=name, 
          email=email,
          password=hash_password(password)
      )
      db.add(new_user)
      db.commit()
      db.refresh(new_user)

      return new_user
    except UserAlreadyExistsException:
      raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"DB error during signup: {e}")
        raise 
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error during signup: {e}")
        raise

def login(db: Session, email: str, password: str):
    try:
      user = db.query(User).filter(User.email == email).first()
      if not user or not verify_password(password, user.password):
          raise InvalidCredentialsError("Invalid email or password")
      
      token = create_access_token({"id": user.user_id, "name": user.name, "role": user.role})

      return {"access_token": token, "token_type": "bearer"}
    
    except InvalidCredentialsError:
      raise
    except SQLAlchemyError as e:
        logger.error(f"DB error during login: {e}")
        raise
    except Exception as e:
      logger.error(f"Unexpected error during login: {e}")
      raise

def get_current_user(db: Session, token: str):
    try:
      payload = decode_token(token)
      user_id = payload.get("id")
      if not user_id:
          raise InvalidTokenError("Token payload missing user id")

      user = db.query(User).filter(User.user_id == user_id).first()
      
      if not user:
          raise InvalidTokenError("User no longer exists")
      
      return user
    
    except InvalidTokenError:
      raise
    except SQLAlchemyError as e:
        logger.error(f"DB error during get_current_user: {e}")
        raise
    except Exception as e:
      logger.error(f"Unexpected error during get_current_user: {e}")
      raise 

