import redis
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Movie Reservation System"
    DATABASE_URL: str
    
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_DB: int = Field(default=0)
    
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    
settings = Settings()

redis_client = redis.Redis(
  host=settings.REDIS_HOST,
  port=settings.REDIS_PORT,
  db=settings.REDIS_DB,
  decode_responses=True
)