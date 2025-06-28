from src.services.interfaces.building_service import InterfaceBuildingService
from src.repositories.interfaces.building_repository import InterfaceBuildingRepository

class BuildingService(InterfaceBuildingService):
    def __init__(self, building_repository: InterfaceBuildingRepository):
        self.building_repository = building_repository

    def get_building_by_id(self, building_id: str):
        return self.building_repository.get_building_by_id(building_id)

    def get_all_buildings(self):
        return self.building_repository.get_all_buildings()

    def create_building(self, building_data: dict):
        return self.building_repository.create_building(building_data)

    def update_building(self, building_id: str, building_data: dict):
        return self.building_repository.update_building(building_id, building_data)

    def delete_building(self, building_id: str):
        return self.building_repository.delete_building(building_id)