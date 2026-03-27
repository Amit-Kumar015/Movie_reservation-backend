from pydantic import BaseModel
from typing import List

class BookSeatsRequest(BaseModel):
    showTimeId: str
    seatIds: List[str]