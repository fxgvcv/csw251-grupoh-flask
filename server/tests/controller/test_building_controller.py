import pytest
from flask import Flask
from unittest.mock import MagicMock
from src.controllers.building_controller import BuildingController

@pytest.fixture
def mock_service():
    return MagicMock()

@pytest.fixture
def app(mock_service):
    app = Flask(__name__)
    controller = BuildingController(mock_service)
    app.register_blueprint(controller.blueprint)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_all_buildings(client, mock_service):
    mock_service.get_all_buildings.return_value = [MagicMock(to_dict=lambda: {"id": "1", "name": "A"})]
    response = client.get('/buildings/')
    assert response.status_code == 200
    assert response.get_json() == [{"id": "1", "name": "A"}]

def test_get_building_by_id_found(client, mock_service):
    mock_service.get_building_by_id.return_value = MagicMock(to_dict=lambda: {"id": "1", "name": "A"})
    response = client.get('/buildings/1')
    assert response.status_code == 200
    assert response.get_json() == {"id": "1", "name": "A"}

def test_get_building_by_id_not_found(client, mock_service):
    mock_service.get_building_by_id.return_value = None
    response = client.get('/buildings/999')
    assert response.status_code == 404

def test_create_building(client, mock_service):
    mock_service.create_building.return_value = MagicMock(to_dict=lambda: {"id": "2", "name": "B"})
    response = client.post('/buildings/', json={"name": "B"})
    assert response.status_code == 201
    assert response.get_json() == {"id": "2", "name": "B"}

def test_update_building_found(client, mock_service):
    mock_service.update_building.return_value = MagicMock(to_dict=lambda: {"id": "1", "name": "A-updated"})
    response = client.put('/buildings/1', json={"name": "A-updated"})
    assert response.status_code == 200
    assert response.get_json() == {"id": "1", "name": "A-updated"}

def test_update_building_not_found(client, mock_service):
    mock_service.update_building.return_value = None
    response = client.put('/buildings/999', json={"name": "DoesNotExist"})
    assert response.status_code == 404

def test_delete_building_found(client, mock_service):
    mock_service.delete_building.return_value = MagicMock(to_dict=lambda: {"id": "1", "name": "A"})
    response = client.delete('/buildings/1')
    assert response.status_code == 200
    assert response.get_json() == {"id": "1", "name": "A"}

def test_delete_building_not_found(client, mock_service):
    mock_service.delete_building.return_value = None
    response = client.delete('/buildings/999')
    assert response.status_code == 404