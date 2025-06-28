import pytest
from flask import Flask
from unittest.mock import MagicMock
from src.controllers.user_controller import UserController

@pytest.fixture
def mock_service():
    return MagicMock()

@pytest.fixture
def app(mock_service):
    app = Flask(__name__)
    controller = UserController(mock_service)
    app.register_blueprint(controller.blueprint)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_all_users(client, mock_service):
    mock_service.get_all_users.return_value = [
        MagicMock(to_dict=lambda: {"id": "1", "username": "user1", "email": "user1@test.com", "password": "hashed"}),
        MagicMock(to_dict=lambda: {"id": "2", "username": "user2", "email": "user2@test.com", "password": "hashed"})
    ]
    response = client.get('/users/')
    assert response.status_code == 200
    result = response.get_json()
    assert len(result) == 2
    assert result[0] == {"id": "1", "username": "user1", "email": "user1@test.com"}
    assert result[1] == {"id": "2", "username": "user2", "email": "user2@test.com"}

def test_get_user_by_id_found(client, mock_service):
    mock_service.get_user.return_value = MagicMock(
        to_dict=lambda: {"id": "1", "username": "user1", "email": "user1@test.com", "password": "hashed"}
    )
    response = client.get('/users/1')
    assert response.status_code == 200
    assert response.get_json() == {"id": "1", "username": "user1", "email": "user1@test.com"}

def test_get_user_by_id_not_found(client, mock_service):
    mock_service.get_user.return_value = None
    response = client.get('/users/999')
    assert response.status_code == 404

def test_create_user_success(client, mock_service):
    mock_service.create_user.return_value = MagicMock(
        to_dict=lambda: {"id": "1", "username": "newuser", "email": "new@test.com", "password": "hashed"}
    )
    response = client.post('/users/', json={
        "username": "newuser",
        "email": "new@test.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.get_json() == {"id": "1", "username": "newuser", "email": "new@test.com"}

def test_create_user_missing_fields(client, mock_service):
    response = client.post('/users/', json={"username": "newuser"})
    assert response.status_code == 400

def test_create_user_no_data(client, mock_service):
    response = client.post('/users/', json={})
    assert response.status_code == 400

def test_update_user_found(client, mock_service):
    mock_service.update_user.return_value = MagicMock(
        to_dict=lambda: {"id": "1", "username": "updated_user", "email": "updated@test.com", "password": "hashed"}
    )
    response = client.put('/users/1', json={"username": "updated_user"})
    assert response.status_code == 200
    assert response.get_json() == {"id": "1", "username": "updated_user", "email": "updated@test.com"}

def test_update_user_not_found(client, mock_service):
    mock_service.update_user.return_value = None
    response = client.put('/users/999', json={"username": "updated_user"})
    assert response.status_code == 404

def test_delete_user_found(client, mock_service):
    mock_service.delete_user.return_value = MagicMock(
        to_dict=lambda: {"id": "1", "username": "user1", "email": "user1@test.com", "password": "hashed"}
    )
    response = client.delete('/users/1')
    assert response.status_code == 200
    assert response.get_json() == {"id": "1", "username": "user1", "email": "user1@test.com"}

def test_delete_user_not_found(client, mock_service):
    mock_service.delete_user.return_value = None
    response = client.delete('/users/999')
    assert response.status_code == 404

def test_get_user_by_username_found(client, mock_service):
    mock_service.get_user_by_username.return_value = MagicMock(
        to_dict=lambda: {"id": "1", "username": "testuser", "email": "test@test.com", "password": "hashed"}
    )
    response = client.get('/users/username/testuser')
    assert response.status_code == 200
    assert response.get_json() == {"id": "1", "username": "testuser", "email": "test@test.com"}

def test_get_user_by_username_not_found(client, mock_service):
    mock_service.get_user_by_username.return_value = None
    response = client.get('/users/username/nonexistent')
    assert response.status_code == 404

def test_authenticate_user_success(client, mock_service):
    mock_service.authenticate.return_value = MagicMock(
        to_dict=lambda: {"id": "1", "username": "testuser", "email": "test@test.com", "password": "hashed"}
    )
    response = client.post('/users/authenticate', json={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    result = response.get_json()
    assert result["message"] == "Authentication successful"
    assert result["user"] == {"id": "1", "username": "testuser", "email": "test@test.com"}

def test_authenticate_user_invalid_credentials(client, mock_service):
    mock_service.authenticate.return_value = None
    response = client.post('/users/authenticate', json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_authenticate_user_missing_fields(client, mock_service):
    response = client.post('/users/authenticate', json={"username": "testuser"})
    assert response.status_code == 400

def test_authenticate_user_no_data(client, mock_service):
    response = client.post('/users/authenticate', json={})
    assert response.status_code == 400
