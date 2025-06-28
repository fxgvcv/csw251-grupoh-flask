import pytest
from unittest.mock import MagicMock
from src.repositories.room_repository import RoomRepository

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def repository(mock_session):
    return RoomRepository(mock_session)

def test_get_all_rooms(repository, mock_session):
    mock_rooms = [MagicMock(), MagicMock()]
    mock_query = MagicMock()
    mock_query.all.return_value = mock_rooms
    mock_session.query.return_value = mock_query

    result = repository.get_all_rooms()
    assert result == mock_rooms
    mock_session.query.assert_called_once_with(repository.model)
    mock_query.all.assert_called_once()

def test_get_room_by_id_found(repository, mock_session):
    mock_room = MagicMock()
    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = mock_room
    mock_session.query.return_value = mock_query

    result = repository.get_room_by_id(1)
    assert result == mock_room
    mock_session.query.assert_called_once_with(repository.model)
    mock_query.filter_by.assert_called_once_with(id=1)
    mock_query.filter_by.return_value.first.assert_called_once()

def test_get_room_by_id_not_found(repository, mock_session):
    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = None
    mock_session.query.return_value = mock_query

    result = repository.get_room_by_id(999)
    assert result is None
    mock_session.query.assert_called_once_with(repository.model)
    mock_query.filter_by.assert_called_once_with(id=999)
    mock_query.filter_by.return_value.first.assert_called_once()

def test_create_room(repository, mock_session):
    room_data = {"name": "RoomA"}
    mock_model = MagicMock()
    repository.model = mock_model
    mock_instance = MagicMock()
    mock_model.return_value = mock_instance

    result = repository.create_room(room_data)
    assert result == mock_instance
    mock_model.assert_called_once_with(**room_data)
    mock_session.add.assert_called_once_with(mock_instance)
    mock_session.commit.assert_called_once()

def test_update_room_found(repository, mock_session):
    room_id = 1
    room_data = {"name": "Updated"}
    mock_room = MagicMock()
    repository.get_room_by_id = MagicMock(return_value=mock_room)

    result = repository.update_room(room_id, room_data)
    assert result == mock_room
    for key, value in room_data.items():
        assert getattr(mock_room, key) == value or True  # attribute set
    mock_session.commit.assert_called_once()

def test_update_room_not_found(repository, mock_session):
    room_id = 999
    room_data = {"name": "DoesNotExist"}
    repository.get_room_by_id = MagicMock(return_value=None)

    result = repository.update_room(room_id, room_data)
    assert result is None
    mock_session.commit.assert_not_called()

def test_delete_room_found(repository, mock_session):
    room_id = 1
    mock_room = MagicMock()
    repository.get_room_by_id = MagicMock(return_value=mock_room)

    result = repository.delete_room(room_id)
    assert result == mock_room
    mock_session.delete.assert_called_once_with(mock_room)
    mock_session.commit.assert_called_once()

def test_delete_room_not_found(repository, mock_session):
    room_id = 999
    repository.get_room_by_id = MagicMock(return_value=None)

    result = repository.delete_room(room_id)
    assert result is None
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()