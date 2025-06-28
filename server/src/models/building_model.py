from src.utils.shared.db.base import Base
from sqlalchemy import Column, Integer, String

class Building(Base):
    __tablename__ = 'buildings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }