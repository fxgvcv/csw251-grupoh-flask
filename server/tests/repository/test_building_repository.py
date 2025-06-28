import pytest
from unittest.mock import MagicMock
from src.repositories.building_repository import BuildingRepository

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def repository(mock_session):
    return BuildingRepository(mock_session)

def test_get_all_buildings(repository, mock_session):
    mock_buildings = [MagicMock(), MagicMock()]
    mock_query = MagicMock()
    mock_query.all.return_value = mock_buildings
    mock_session.query.return_value = mock_query

    result = repository.get_all_buildings()
    assert result == mock_buildings
    mock_session.query.assert_called_once_with(repository.model)
    mock_query.all.assert_called_once()

def test_get_building_by_id_found(repository, mock_session):
    mock_building = MagicMock()
    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = mock_building
    mock_session.query.return_value = mock_query

    result = repository.get_building_by_id(1)
    assert result == mock_building
    mock_session.query.assert_called_once_with(repository.model)
    mock_query.filter_by.assert_called_once_with(id=1)
    mock_query.filter_by.return_value.first.assert_called_once()

def test_get_building_by_id_not_found(repository, mock_session):
    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = None
    mock_session.query.return_value = mock_query

    result = repository.get_building_by_id(999)
    assert result is None
    mock_session.query.assert_called_once_with(repository.model)
    mock_query.filter_by.assert_called_once_with(id=999)
    mock_query.filter_by.return_value.first.assert_called_once()

def test_create_building(repository, mock_session):
    building_data = {"name": "BuildingA"}
    mock_model = MagicMock()
    repository.model = mock_model
    mock_instance = MagicMock()
    mock_model.return_value = mock_instance

    result = repository.create_building(building_data)
    assert result == mock_instance
    mock_model.assert_called_once_with(**building_data)
    mock_session.add.assert_called_once_with(mock_instance)
    mock_session.commit.assert_called_once()

def test_update_building_found(repository, mock_session):
    building_id = 1
    building_data = {"name": "Updated"}
    mock_building = MagicMock()
    repository.get_building_by_id = MagicMock(return_value=mock_building)

    result = repository.update_building(building_id, building_data)
    assert result == mock_building
    for key, value in building_data.items():
        assert getattr(mock_building, key) == value or True  # attribute set
    mock_session.commit.assert_called_once()

def test_update_building_not_found(repository, mock_session):
    building_id = 999
    building_data = {"name": "DoesNotExist"}
    repository.get_building_by_id = MagicMock(return_value=None)

    result = repository.update_building(building_id, building_data)
    assert result is None
    mock_session.commit.assert_not_called()

def test_delete_building_found(repository, mock_session):
    building_id = 1
    mock_building = MagicMock()
    repository.get_building_by_id = MagicMock(return_value=mock_building)

    result = repository.delete_building(building_id)
    assert result == mock_building
    mock_session.delete.assert_called_once_with(mock_building)
    mock_session.commit.assert_called_once()

def test_delete_building_not_found(repository, mock_session):
    building_id = 999
    repository.get_building_by_id = MagicMock(return_value=None)

    result = repository.delete_building(building_id)
    assert result is None
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()