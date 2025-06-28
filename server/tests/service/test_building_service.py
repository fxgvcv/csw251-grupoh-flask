import pytest
from unittest.mock import MagicMock
from src.services.building_service import BuildingService


@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def service(mock_repository):
    return BuildingService(mock_repository)

def test_get_building_by_id_found(service, mock_repository):
    mock_building = MagicMock()
    mock_repository.get_building_by_id.return_value = mock_building
    result = service.get_building_by_id("1")
    assert result == mock_building
    mock_repository.get_building_by_id.assert_called_once_with("1")

def test_get_building_by_id_not_found(service, mock_repository):
    mock_repository.get_building_by_id.return_value = None
    result = service.get_building_by_id("999")
    assert result is None
    mock_repository.get_building_by_id.assert_called_once_with("999")

def test_get_all_buildings(service, mock_repository):
    mock_buildings = [MagicMock(), MagicMock()]
    mock_repository.get_all_buildings.return_value = mock_buildings
    result = service.get_all_buildings()
    assert result == mock_buildings
    mock_repository.get_all_buildings.assert_called_once()

def test_create_building(service, mock_repository):
    building_data = {"name": "BuildingA"}
    mock_building = MagicMock()
    mock_repository.create_building.return_value = mock_building
    result = service.create_building(building_data)
    assert result == mock_building
    mock_repository.create_building.assert_called_once_with(building_data)

def test_update_building_found(service, mock_repository):
    building_data = {"name": "Updated"}
    mock_building = MagicMock()
    mock_repository.update_building.return_value = mock_building
    result = service.update_building("1", building_data)
    assert result == mock_building
    mock_repository.update_building.assert_called_once_with("1", building_data)

def test_update_building_not_found(service, mock_repository):
    building_data = {"name": "DoesNotExist"}
    mock_repository.update_building.return_value = None
    result = service.update_building("999", building_data)
    assert result is None
    mock_repository.update_building.assert_called_once_with("999", building_data)

def test_delete_building_found(service, mock_repository):
    mock_building = MagicMock()
    mock_repository.delete_building.return_value = mock_building
    result = service.delete_building("1")
    assert result == mock_building
    mock_repository.delete_building.assert_called_once_with("1")

def test_delete_building_not_found(service, mock_repository):
    mock_repository.delete_building.return_value = None
    result = service.delete_building("999")
    assert result is None
    mock_repository.delete_building.assert_called_once_with("999")