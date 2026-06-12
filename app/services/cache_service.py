import json
from typing import Any, Optional
from app.core.config import redis_client

class CacheService:
  @staticmethod
  def get(key: str) -> Optional[Any]:
    cached_data = redis_client.get(key)
    if cached_data:
      return json.loads(cached_data)
    return None
  
  @staticmethod
  def set(key: str, value: Any, ttl_seconds: int = 300):
    serialized_value = json.dumps(value)
    redis_client.setex(key, ttl_seconds, serialized_value)
    
  @staticmethod
  def invalidate(key: str):
    redis_client.delete(key)