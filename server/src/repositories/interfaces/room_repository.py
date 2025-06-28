from abc import ABC, abstractmethod
from typing import List
from src.models.room_model import Room

class InterfaceRoomRepository(ABC):
    @abstractmethod
    def get_room_by_id(self, room_id: str) -> Room:
        """Retrieve a room by its ID."""
        pass

    @abstractmethod
    def get_all_rooms(self) -> List[Room]:
        """Retrieve all rooms."""
        pass

    @abstractmethod
    def create_room(self, room_data: dict) -> Room:
        """Add a new room."""
        pass

    @abstractmethod
    def update_room(self, room_id: str, room_data: dict) -> Room:
        """Update an existing room."""
        pass

    @abstractmethod
    def delete_room(self, room_id: str) -> Room:
        """Delete a room by its ID."""
        pass