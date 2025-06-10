from src.utils.shared.db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    building_id = Column(Integer, nullable=False)
    capacity = Column(Integer, ForeignKey('buildings.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'building_id': self.building_id,
            'capacity': self.capacity
        }