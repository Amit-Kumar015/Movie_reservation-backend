from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import get_db
from app.services.admin.screen_service import create_screen, update_screen, delete_screen, ScreenNotFoundError, ScreenAlreadyExistsError
from app.schemas.admin.screen import ScreenCreateRequest, ScreenCreateResponse, ScreenUpdateRequest, ScreenResponse

router = APIRouter(prefix="/admin/screens", tags=["Admin Screens"])

@router.post('/', response_model=ScreenCreateResponse)
def create_screen_endpoint(request: ScreenCreateRequest, db: Session = Depends(get_db)):
  try:
    return create_screen(db, request.name, request.venue_id, request.row, request.col)
  except ScreenAlreadyExistsError as e:
    raise HTTPException(status_code=400, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")
  
@router.put('/{screen_id}', response_model=ScreenResponse)
def update_screen_endpoint(screen_id: UUID, request: ScreenUpdateRequest, db: Session = Depends(get_db)):
  try:
    return update_screen(db, screen_id, request.name, request.venue_id)
  except ScreenNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")
  
@router.delete('/{screen_id}')
def delete_screen_endpoint(screen_id: UUID, db: Session = Depends(get_db)):
  try:
    delete_screen(db, screen_id)
    return {"detail": "Screen deleted successfully"}
  except ScreenNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except SQLAlchemyError:
    raise HTTPException(status_code=500, detail="Database error")
  except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")