from src.services.interfaces.room_service import InterfaceRoomService
from src.repositories.interfaces.room_repository import InterfaceRoomRepository

class RoomService(InterfaceRoomService):
    def __init__(self, room_repository: InterfaceRoomRepository):
        self.room_repository = room_repository

    def get_room_by_id(self, room_id: str):
        return self.room_repository.get_room_by_id(room_id)

    def get_all_rooms(self):
        return self.room_repository.get_all_rooms()

    def create_room(self, room_data: dict):
        return self.room_repository.create_room(room_data)

    def update_room(self, room_id: str, room_data: dict):
        return self.room_repository.update_room(room_id, room_data)

    def delete_room(self, room_id: str):
        return self.room_repository.delete_room(room_id)