from sqlalchemy.orm import Session
from src.repositories.interfaces.building_repository import InterfaceBuildingRepository
from src.models.building_model import Building
from typing import List, Optional

class BuildingRepository(InterfaceBuildingRepository):
    def __init__(self, session: Session):
        self.session = session
        self.model = Building

    def get_all_buildings(self) -> List[Building]:
        return self.session.query(self.model).all()

    def get_building_by_id(self, building_id: int) -> Optional[Building]:
        return self.session.query(self.model).filter_by(id=building_id).first()

    def create_building(self, building_data) -> Building:
        new_building = self.model(**building_data)
        self.session.add(new_building)
        self.session.commit()
        return new_building

    def update_building(self, building_id: int, building_data) -> Building:
        building = self.get_building_by_id(building_id)
        if not building:
            return None
        for key, value in building_data.items():
            setattr(building, key, value)
        self.session.commit()
        return building

    def delete_building(self, building_id: int) -> Building:
        building = self.get_building_by_id(building_id)
        if not building:
            return None
        self.session.delete(building)
        self.session.commit()
        return building