from pydantic import BaseModel
from typing import Optional

class RoomDTO(BaseModel):
    id: Optional[int] = None
    name: str
    capacity: int
    location: Optional[str] = None