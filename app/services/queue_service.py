import time
import secrets
from app.core.config import redis_client

class QueueService:
    @staticmethod
    def join_waiting_room(showtime_id: str, user_id: str) -> dict:
        queue_key = f"showtime_queue:{showtime_id}"
        current_time = time.time()

        redis_client.zadd(queue_key, {str(user_id): current_time}, nx=True)
        position = redis_client.zrank(queue_key, str(user_id))

        return {"status": "queued", "position": position + 1}

    @staticmethod
    def check_queue_status(
        showtime_id: str, user_id: str, active_limit: int = 50
    ) -> dict:
        queue_key = f"showtime_queue:{showtime_id}"
        token_key = f"auth_token:showtime:{showtime_id}:user:{user_id}"

        existing_token = redis_client.get(token_key)
        if existing_token:
            return {"status": "allowed", "session_token": existing_token}
          
        position = redis_client.zrank(queue_key, str(user_id))
        if position is None:
            return {"status": "not_in_queue"}

        if position < active_limit:
            session_token = secrets.token_hex(16)
            
            redis_client.setex(token_key, 600, session_token)
            redis_client.zrem(queue_key, str(user_id))
            return {
                "status": "allowed",
                "message": "Proceed to seat selection and payment.",
                "session_token": session_token,
            }

        people_ahead = position - active_limit + 1
        return {
            "status": "waiting",
            "people_ahead": people_ahead,
            "estimated_wait_minutes": round((people_ahead * 20) / 60, 1),
        }
        
    @staticmethod
    def verify_session_token(showtime_id: str, user_id: str, token: str) -> bool:
        token_key = f"auth_token:showtime:{showtime_id}:user:{user_id}"
        stored_token = redis_client.get(token_key)
        return stored_token == token

    @staticmethod
    def leave_waiting_room(showtime_id: str, user_id: str) -> dict:
        queue_key = f"showtime_queue:{showtime_id}"
        redis_client.zrem(queue_key, str(user_id))
        return {"status": "removed"} 