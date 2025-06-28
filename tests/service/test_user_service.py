import pytest
from unittest.mock import MagicMock, patch
from src.services.user_service import UserService


@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def service(mock_repository):
    return UserService(mock_repository)

def test_get_user_found(service, mock_repository):
    mock_user = MagicMock()
    mock_repository.get_user_by_id.return_value = mock_user
    result = service.get_user("1")
    assert result == mock_user
    mock_repository.get_user_by_id.assert_called_once_with("1")

def test_get_user_not_found(service, mock_repository):
    mock_repository.get_user_by_id.return_value = None
    result = service.get_user("999")
    assert result is None
    mock_repository.get_user_by_id.assert_called_once_with("999")

def test_get_all_users(service, mock_repository):
    mock_users = [MagicMock(), MagicMock()]
    mock_repository.get_all_users.return_value = mock_users
    result = service.get_all_users()
    assert result == mock_users
    mock_repository.get_all_users.assert_called_once()

def test_get_user_by_username_found(service, mock_repository):
    mock_user = MagicMock()
    mock_user.username = "testuser"
    mock_repository.get_all_users.return_value = [mock_user]
    
    result = service.get_user_by_username("testuser")
    assert result == mock_user
    mock_repository.get_all_users.assert_called_once()

def test_get_user_by_username_not_found(service, mock_repository):
    mock_user = MagicMock()
    mock_user.username = "otheruser"
    mock_repository.get_all_users.return_value = [mock_user]
    
    result = service.get_user_by_username("testuser")
    assert result is None
    mock_repository.get_all_users.assert_called_once()

@patch('src.services.user_service.hashlib.sha256')
def test_create_user_with_password(mock_sha256, service, mock_repository):
    mock_hash = MagicMock()
    mock_hash.hexdigest.return_value = "hashed_password"
    mock_sha256.return_value = mock_hash
    
    user_data = {"username": "newuser", "email": "new@test.com", "password": "plaintext"}
    mock_user = MagicMock()
    mock_repository.create_user.return_value = mock_user
    
    result = service.create_user(user_data)
    
    assert result == mock_user
    expected_data = {"username": "newuser", "email": "new@test.com", "password": "hashed_password"}
    mock_repository.create_user.assert_called_once_with(expected_data)
    mock_sha256.assert_called_once_with("plaintext".encode())

def test_create_user_without_password(service, mock_repository):
    user_data = {"username": "newuser", "email": "new@test.com"}
    mock_user = MagicMock()
    mock_repository.create_user.return_value = mock_user
    
    result = service.create_user(user_data)
    
    assert result == mock_user
    mock_repository.create_user.assert_called_once_with(user_data)

@patch('src.services.user_service.hashlib.sha256')
def test_update_user_with_password(mock_sha256, service, mock_repository):
    mock_hash = MagicMock()
    mock_hash.hexdigest.return_value = "hashed_password"
    mock_sha256.return_value = mock_hash
    
    user_data = {"email": "updated@test.com", "password": "newpassword"}
    mock_user = MagicMock()
    mock_repository.update_user.return_value = mock_user
    
    result = service.update_user("1", user_data)
    
    assert result == mock_user
    expected_data = {"email": "updated@test.com", "password": "hashed_password"}
    mock_repository.update_user.assert_called_once_with("1", expected_data)
    mock_sha256.assert_called_once_with("newpassword".encode())

def test_update_user_without_password(service, mock_repository):
    user_data = {"email": "updated@test.com"}
    mock_user = MagicMock()
    mock_repository.update_user.return_value = mock_user
    
    result = service.update_user("1", user_data)
    
    assert result == mock_user
    mock_repository.update_user.assert_called_once_with("1", user_data)

def test_update_user_not_found(service, mock_repository):
    user_data = {"email": "updated@test.com"}
    mock_repository.update_user.return_value = None
    
    result = service.update_user("999", user_data)
    
    assert result is None
    mock_repository.update_user.assert_called_once_with("999", user_data)

def test_delete_user_found(service, mock_repository):
    mock_user = MagicMock()
    mock_repository.delete_user.return_value = mock_user
    
    result = service.delete_user("1")
    
    assert result == mock_user
    mock_repository.delete_user.assert_called_once_with("1")

def test_delete_user_not_found(service, mock_repository):
    mock_repository.delete_user.return_value = None
    
    result = service.delete_user("999")
    
    assert result is None
    mock_repository.delete_user.assert_called_once_with("999")

@patch('src.services.user_service.hashlib.sha256')
def test_authenticate_success(mock_sha256, service, mock_repository):
    # Setup password hashing mock
    mock_hash = MagicMock()
    mock_hash.hexdigest.return_value = "hashed_password"
    mock_sha256.return_value = mock_hash
    
    # Setup user mock
    mock_user = MagicMock()
    mock_user.username = "testuser"
    mock_user.password = "hashed_password"
    mock_repository.get_all_users.return_value = [mock_user]
    
    result = service.authenticate("testuser", "plaintext")
    
    assert result == mock_user
    mock_repository.get_all_users.assert_called_once()
    mock_sha256.assert_called_once_with("plaintext".encode())

@patch('src.services.user_service.hashlib.sha256')
def test_authenticate_wrong_password(mock_sha256, service, mock_repository):
    # Setup password hashing mock
    mock_hash = MagicMock()
    mock_hash.hexdigest.return_value = "wrong_hash"
    mock_sha256.return_value = mock_hash
    
    # Setup user mock
    mock_user = MagicMock()
    mock_user.username = "testuser"
    mock_user.password = "correct_hash"
    mock_repository.get_all_users.return_value = [mock_user]
    
    result = service.authenticate("testuser", "wrongpassword")
    
    assert result is None
    mock_repository.get_all_users.assert_called_once()
    mock_sha256.assert_called_once_with("wrongpassword".encode())

def test_authenticate_user_not_found(service, mock_repository):
    mock_user = MagicMock()
    mock_user.username = "otheruser"
    mock_repository.get_all_users.return_value = [mock_user]
    
    result = service.authenticate("testuser", "password")
    
    assert result is None
    mock_repository.get_all_users.assert_called_once()

@patch('src.services.user_service.hashlib.sha256')
def test_hash_password(mock_sha256, service):
    mock_hash = MagicMock()
    mock_hash.hexdigest.return_value = "hashed_result"
    mock_sha256.return_value = mock_hash
    
    result = service._hash_password("plaintext")
    
    assert result == "hashed_result"
    mock_sha256.assert_called_once_with("plaintext".encode())
    mock_hash.hexdigest.assert_called_once()

@patch('src.services.user_service.hashlib.sha256')
def test_verify_password_correct(mock_sha256, service):
    mock_hash = MagicMock()
    mock_hash.hexdigest.return_value = "hashed_password"
    mock_sha256.return_value = mock_hash
    
    result = service._verify_password("plaintext", "hashed_password")
    
    assert result is True
    mock_sha256.assert_called_once_with("plaintext".encode())

@patch('src.services.user_service.hashlib.sha256')
def test_verify_password_incorrect(mock_sha256, service):
    mock_hash = MagicMock()
    mock_hash.hexdigest.return_value = "different_hash"
    mock_sha256.return_value = mock_hash
    
    result = service._verify_password("plaintext", "correct_hash")
    
    assert result is False
    mock_sha256.assert_called_once_with("plaintext".encode())
