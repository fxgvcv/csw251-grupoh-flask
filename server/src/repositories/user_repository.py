from sqlalchemy.orm import Session
from src.repositories.interfaces.user_repository import InterfaceUserRepository
from src.models.user_model import User
from typing import List

class UserRepository(InterfaceUserRepository):
    def __init__(self, session: Session):
        self.session = session
        self.model = User

    def get_user_by_id(self, user_id: str) -> User:
        """Retrieve a user by their ID."""
        return self.session.query(self.model).filter_by(id=user_id).first()

    def get_all_users(self) -> List[User]:
        """Retrieve all users."""
        return self.session.query(self.model).all()

    def get_user_by_username(self, username: str) -> User:
        """Retrieve a user by their username."""
        return self.session.query(self.model).filter_by(username=username).first()

    def create_user(self, user_data: dict) -> User:
        """Add a new user."""
        new_user = self.model(**user_data)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def update_user(self, user_id: str, user_data: dict) -> User:
        """Update an existing user."""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        for key, value in user_data.items():
            setattr(user, key, value)
        self.session.commit()
        return user

    def delete_user(self, user_id: str) -> User:
        """Delete a user by their ID."""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        self.session.delete(user)
        self.session.commit()
        return user
