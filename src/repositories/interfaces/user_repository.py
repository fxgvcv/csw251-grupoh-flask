from abc import ABC, abstractmethod
from typing import List
from src.models.user_model import User

class InterfaceUserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User:
        """Retrieve a user by their ID."""
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        """Retrieve all users."""
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> User:
        """Retrieve a user by their username."""
        pass

    @abstractmethod
    def create_user(self, user_data: dict) -> User:
        """Add a new user."""
        pass

    @abstractmethod
    def update_user(self, user_id: str, user_data: dict) -> User:
        """Update an existing user."""
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> User:
        """Delete a user by their ID."""
        pass