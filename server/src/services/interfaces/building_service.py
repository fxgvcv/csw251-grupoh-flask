from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.building_model import Building

class InterfaceBuildingService(ABC):
    @abstractmethod
    def get_building_by_id(self, building_id: str) -> Optional[Building]:
        """Retrieve a building by its ID."""
        pass

    @abstractmethod
    def get_all_buildings(self) -> List[Building]:
        """Retrieve all buildings."""
        pass

    @abstractmethod
    def create_building(self, building_data: dict) -> Building:
        """Create a new building."""
        pass

    @abstractmethod
    def update_building(self, building_id: str, building_data: dict) -> Optional[Building]:
        """Update an existing building."""
        pass

    @abstractmethod
    def delete_building(self, building_id: str) -> Optional[Building]:
        """Delete a building by its ID."""
        pass