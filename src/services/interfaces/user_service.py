from abc import ABC, abstractmethod
from typing import Optional, List
from src.models.user_model import User

class InterfaceUserService(ABC):
    @abstractmethod
    def create_user(self, user_data: dict) -> User:
        """Create a new user."""
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> Optional[User]:
        """Retrieve a user by their ID."""
        pass

    @abstractmethod
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user by username and password."""
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by their username."""
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        """Retrieve all users."""
        pass

    @abstractmethod
    def update_user(self, user_id: str, user_data: dict) -> Optional[User]:
        """Update an existing user."""
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> Optional[User]:
        """Delete a user by their ID."""
        pass