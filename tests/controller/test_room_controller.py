import pytest
from flask import Flask
from unittest.mock import MagicMock
from src.controllers.room_controller import RoomController


@pytest.fixture
def mock_service():
    return MagicMock()

@pytest.fixture
def app(mock_service):
    app = Flask(__name__)
    controller = RoomController(mock_service)
    app.register_blueprint(controller.blueprint)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_all_rooms(client, mock_service):
    mock_service.get_all_rooms.return_value = [MagicMock(to_dict=lambda: {"id": "1", "name": "RoomA"})]
    response = client.get('/rooms/')
    assert response.status_code == 200
    assert response.get_json() == [{"id": "1", "name": "RoomA"}]

def test_get_room_by_id_found(client, mock_service):
    mock_service.get_room_by_id.return_value = MagicMock(to_dict=lambda: {"id": "1", "name": "RoomA"})
    response = client.get('/rooms/1')
    assert response.status_code == 200
    assert response.get_json() == {"id": "1", "name": "RoomA"}

def test_get_room_by_id_not_found(client, mock_service):
    mock_service.get_room_by_id.return_value = None
    response = client.get('/rooms/999')
    assert response.status_code == 404

def test_create_room(client, mock_service):
    mock_service.create_room.return_value = MagicMock(to_dict=lambda: {"id": "2", "name": "RoomB"})
    response = client.post('/rooms/', json={"name": "RoomB"})
    assert response.status_code == 201
    assert response.get_json() == {"id": "2", "name": "RoomB"}

def test_update_room_found(client, mock_service):
    mock_service.update_room.return_value = MagicMock(to_dict=lambda: {"id": "1", "name": "RoomA-updated"})
    response = client.put('/rooms/1', json={"name": "RoomA-updated"})
    assert response.status_code == 200
    assert response.get_json() == {"id": "1", "name": "RoomA-updated"}

def test_update_room_not_found(client, mock_service):
    mock_service.update_room.return_value = None
    response = client.put('/rooms/999', json={"name": "DoesNotExist"})
    assert response.status_code == 404

def test_delete_room_found(client, mock_service):
    mock_service.delete_room.return_value = MagicMock(to_dict=lambda: {"id": "1", "name": "RoomA"})
    response = client.delete('/rooms/1')
    assert response.status_code == 200
    assert response.get_json() == {"id": "1", "name": "RoomA"}

def test_delete_room_not_found(client, mock_service):
    mock_service.delete_room.return_value = None
    response = client.delete('/rooms/999')
    assert response.status_code == 404