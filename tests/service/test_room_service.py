import pytest
from unittest.mock import MagicMock
from src.services.room_service import RoomService

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def service(mock_repository):
    return RoomService(mock_repository)

def test_get_room_by_id_found(service, mock_repository):
    mock_room = MagicMock()
    mock_repository.get_room_by_id.return_value = mock_room
    result = service.get_room_by_id("1")
    assert result == mock_room
    mock_repository.get_room_by_id.assert_called_once_with("1")

def test_get_room_by_id_not_found(service, mock_repository):
    mock_repository.get_room_by_id.return_value = None
    result = service.get_room_by_id("999")
    assert result is None
    mock_repository.get_room_by_id.assert_called_once_with("999")

def test_get_all_rooms(service, mock_repository):
    mock_rooms = [MagicMock(), MagicMock()]
    mock_repository.get_all_rooms.return_value = mock_rooms
    result = service.get_all_rooms()
    assert result == mock_rooms
    mock_repository.get_all_rooms.assert_called_once()

def test_create_room(service, mock_repository):
    room_data = {"name": "RoomA"}
    mock_room = MagicMock()
    mock_repository.create_room_.return_value = mock_room
    result = service.create_room(room_data)
    assert result == mock_room
    mock_repository.create_room_.assert_called_once_with(room_data)

def test_update_room_found(service, mock_repository):
    room_data = {"name": "Updated"}
    mock_room = MagicMock()
    mock_repository.update_room.return_value = mock_room
    result = service.update_room("1", room_data)
    assert result == mock_room
    mock_repository.update_room.assert_called_once_with("1", room_data)

def test_update_room_not_found(service, mock_repository):
    room_data = {"name": "DoesNotExist"}
    mock_repository.update_room.return_value = None
    result = service.update_room("999", room_data)
    assert result is None
    mock_repository.update_room.assert_called_once_with("999", room_data)

def test_delete_room_found(service, mock_repository):
    mock_room = MagicMock()
    mock_repository.delete_room.return_value = mock_room
    result = service.delete_room("1")
    assert result == mock_room
    mock_repository.delete_room.assert_called_once_with("1")

def test_delete_room_not_found(service, mock_repository):
    mock_repository.delete_room.return_value = None
    result = service.delete_room("999")
    assert result is None
    mock_repository.delete_room.assert_called_once_with("999")