from sqlalchemy.orm import Session
from src.repositories.interfaces.room_repository import InterfaceRoomRepository
from src.models.room_model import Room
from typing import List, Optional

class RoomRepository(InterfaceRoomRepository):
    def __init__(self, session: Session):
        self.session = session
        self.model = Room

    def get_all_rooms(self) -> List[Room]:
        return self.session.query(self.model).all()

    def get_room_by_id(self, room_id: int) -> Optional[Room]:
        return self.session.query(self.model).filter_by(id=room_id).first()

    def create_room(self, room_data: dict) -> Room:
        new_room = self.model(**room_data)
        self.session.add(new_room)
        self.session.commit()
        return new_room

    def update_room(self, room_id: int, room_data: dict) -> Room:
        room = self.get_room_by_id(room_id)
        if not room:
            return None
        for key, value in room_data.items():
            setattr(room, key, value)
        self.session.commit()
        return room

    def delete_room(self, room_id: int) -> Room:
        room = self.get_room_by_id(room_id)
        if not room:
            return None
        self.session.delete(room)
        self.session.commit()
        return room