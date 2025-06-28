from abc import ABC, abstractmethod
from typing import Optional, List
import hashlib
from src.services.interfaces.user_service import InterfaceUserService
from src.repositories.interfaces.user_repository import InterfaceUserRepository
from src.models.user_model import User


class UserService(InterfaceUserService):
    def __init__(self, user_repository: InterfaceUserRepository):
        self.user_repository = user_repository

    def create_user(self, user_data: dict) -> User:
        """Create a new user."""
        # Hash the password before storing
        if 'password' in user_data:
            user_data['password'] = self._hash_password(user_data['password'])
        
        return self.user_repository.create_user(user_data)

    def get_user(self, user_id: str) -> Optional[User]:
        """Retrieve a user by their ID."""
        return self.user_repository.get_user_by_id(user_id)

    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user by username and password."""
        user = self.get_user_by_username(username)
        
        if user and self._verify_password(password, user.password):
            return user
        return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by their username."""
        all_users = self.user_repository.get_all_users()
        return next((u for u in all_users if u.username == username), None)

    def get_all_users(self) -> List[User]:
        """Retrieve all users."""
        return self.user_repository.get_all_users()

    def update_user(self, user_id: str, user_data: dict) -> Optional[User]:
        """Update an existing user."""
        # Hash password if it's being updated
        if 'password' in user_data:
            user_data['password'] = self._hash_password(user_data['password'])
        
        return self.user_repository.update_user(user_id, user_data)

    def delete_user(self, user_id: str) -> Optional[User]:
        """Delete a user by their ID."""
        return self.user_repository.delete_user(user_id)

    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return self._hash_password(password) == hashed_password
