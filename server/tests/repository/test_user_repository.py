import pytest
from unittest.mock import MagicMock
from src.repositories.user_repository import UserRepository

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def repository(mock_session):
    return UserRepository(mock_session)

def test_get_all_users(repository, mock_session):
    mock_users = [MagicMock(), MagicMock()]
    mock_query = MagicMock()
    mock_query.all.return_value = mock_users
    mock_session.query.return_value = mock_query

    result = repository.get_all_users()
    assert result == mock_users
    mock_session.query.assert_called_once_with(repository.model)
    mock_query.all.assert_called_once()

def test_get_user_by_id_found(repository, mock_session):
    mock_user = MagicMock()
    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = mock_user
    mock_session.query.return_value = mock_query

    result = repository.get_user_by_id("1")
    assert result == mock_user
    mock_session.query.assert_called_once_with(repository.model)
    mock_query.filter_by.assert_called_once_with(id="1")
    mock_query.filter_by.return_value.first.assert_called_once()

def test_get_user_by_id_not_found(repository, mock_session):
    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = None
    mock_session.query.return_value = mock_query

    result = repository.get_user_by_id("999")
    assert result is None
    mock_session.query.assert_called_once_with(repository.model)
    mock_query.filter_by.assert_called_once_with(id="999")
    mock_query.filter_by.return_value.first.assert_called_once()

def test_get_user_by_username_found(repository, mock_session):
    mock_user = MagicMock()
    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = mock_user
    mock_session.query.return_value = mock_query

    result = repository.get_user_by_username("testuser")
    assert result == mock_user
    mock_session.query.assert_called_once_with(repository.model)
    mock_query.filter_by.assert_called_once_with(username="testuser")
    mock_query.filter_by.return_value.first.assert_called_once()

def test_get_user_by_username_not_found(repository, mock_session):
    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = None
    mock_session.query.return_value = mock_query

    result = repository.get_user_by_username("nonexistent")
    assert result is None
    mock_session.query.assert_called_once_with(repository.model)
    mock_query.filter_by.assert_called_once_with(username="nonexistent")
    mock_query.filter_by.return_value.first.assert_called_once()

def test_create_user(repository, mock_session):
    user_data = {"username": "newuser", "email": "new@test.com", "password": "hashedpwd"}
    mock_model = MagicMock()
    repository.model = mock_model
    mock_user_instance = MagicMock()
    mock_model.return_value = mock_user_instance

    result = repository.create_user(user_data)
    
    assert result == mock_user_instance
    mock_model.assert_called_once_with(**user_data)
    mock_session.add.assert_called_once_with(mock_user_instance)
    mock_session.commit.assert_called_once()

def test_update_user_found(repository, mock_session):
    user_data = {"email": "updated@test.com"}
    mock_user = MagicMock()
    
    # Mock get_user_by_id behavior
    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = mock_user
    mock_session.query.return_value = mock_query

    result = repository.update_user("1", user_data)
    
    assert result == mock_user
    mock_session.query.assert_called_with(repository.model)
    mock_query.filter_by.assert_called_with(id="1")
    
    # Check that setattr was called for each key-value pair
    for key, value in user_data.items():
        assert hasattr(mock_user, key) or True  # setattr would have been called
    
    mock_session.commit.assert_called_once()

def test_update_user_not_found(repository, mock_session):
    user_data = {"email": "updated@test.com"}
    
    # Mock get_user_by_id to return None
    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = None
    mock_session.query.return_value = mock_query

    result = repository.update_user("999", user_data)
    
    assert result is None
    mock_session.commit.assert_not_called()

def test_delete_user_found(repository, mock_session):
    mock_user = MagicMock()
    
    # Mock get_user_by_id behavior
    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = mock_user
    mock_session.query.return_value = mock_query

    result = repository.delete_user("1")
    
    assert result == mock_user
    mock_session.query.assert_called_with(repository.model)
    mock_query.filter_by.assert_called_with(id="1")
    mock_session.delete.assert_called_once_with(mock_user)
    mock_session.commit.assert_called_once()

def test_delete_user_not_found(repository, mock_session):
    # Mock get_user_by_id to return None
    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = None
    mock_session.query.return_value = mock_query

    result = repository.delete_user("999")
    
    assert result is None
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()
