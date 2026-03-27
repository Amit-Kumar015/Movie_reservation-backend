from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.core.security import hash_password, verify_password, create_accesse_token, decode_token

def signup(db: Session, name: str, email: str, password: str):    
    try:  
      existing_user = db.query(User).filter(User.email == email).first()
      if existing_user:
          raise HTTPException(status_code=400, detail="User already exists")

      new_user = User(
          name=name, 
          email=email,
          password=hash_password(password)
      )
      db.add(new_user)
      db.commit()
      db.refresh(new_user)

      return {"message": "User created successfully"}
    except HTTPException as e:
        raise e
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

def login(db: Session, email: str, password: str):
    try:
      user = db.query(User).filter(User.email == email).first()
      if not user:
          raise HTTPException(status_code=400, detail="Invalid email or password")

      if not verify_password(password, user.password):
          raise HTTPException(status_code=400, detail="Invalid email or password")
      
      token = create_accesse_token({"id": user.id, "name": user.name, "role": user.role})

      return {"access_token": token, "token_type": "bearer"}
    
    except HTTPException as e:
      raise e
    except Exception:
      raise HTTPException(status_code=500, detail="Internal server error")

def get_current_user(db: Session, token: str):
    try:
      payload = decode_token(token)
      id = payload.get("id")
      if not id:
          raise HTTPException(status_code=401, detail="Invalid token")

      user = db.query(User).filter(User.id == id).first()
      
      if not user:
          raise HTTPException(status_code=401, detail="Invalid token")
      
      return {
          "id": user.id,
          "name": user.name,
          "email": user.email,
          "role": user.role,
      }
    except HTTPException as e:
      raise e 
    except Exception:
      raise HTTPException(status_code=500, detail="Internal server error")

