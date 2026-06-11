from fastapi import APIRouter, HTTPException, Depends
from app.api.deps import get_authenticated_user
from app.models.user import User
from app.services.queue_service import QueueService

router = APIRouter(tags=['Queue'])

@router.post("/showtimes/{showtime_id}/queue/join")
def join_queue(showtime_id: str, current_user: User = Depends(get_authenticated_user)):
  return QueueService.join_waiting_room(showtime_id, current_user.user_id)

@router.get("/showtimes/{showtime_id}/queue/status")
def get_queue_status(showtime_id: str, current_user: User = Depends(get_authenticated_user)):
  status_data = QueueService.check_queue_status(showtime_id, current_user.user_id)
  
  if status_data["status"] == "not_in_queue":
    raise HTTPException(status_code=404, detail="User is not in the queue for this showtime.")
  
  return status_data
