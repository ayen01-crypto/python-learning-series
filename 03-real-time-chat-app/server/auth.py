"""
Authentication Manager
This module handles user authentication for the chat application.
"""

import secrets
import hashlib
import time
from typing import Optional, Dict
from server.models import User
from server.database import DatabaseManager


class AuthManager:
    """Manages user authentication."""

    def __init__(self):
        self.db_manager = DatabaseManager()
        self.tokens: Dict[str, Dict[str, str]] = {}  # token -> {user_id, expires}
        self.token_expiry = 3600  # 1 hour

    def hash_password(self, password: str, salt: str = None) -> tuple:
        """Hash a password with a salt."""
        if not salt:
            salt = secrets.token_hex(16)
        
        # Combine password and salt
        salted_password = password + salt
        
        # Hash the salted password
        hashed = hashlib.sha256(salted_password.encode()).hexdigest()
        
        return hashed, salt

    def verify_password(self, password: str, hashed: str, salt: str) -> bool:
        """Verify a password against its hash."""
        new_hash, _ = self.hash_password(password, salt)
        return secrets.compare_digest(new_hash, hashed)

    def generate_token(self, user_id: str) -> str:
        """Generate an authentication token for a user."""
        token = secrets.token_urlsafe(32)
        
        # Store token with expiration
        self.tokens[token] = {
            "user_id": user_id,
            "expires": time.time() + self.token_expiry
        }
        
        return token

    def validate_token(self, token: str) -> Optional[str]:
        """Validate a token and return the user ID if valid."""
        if token not in self.tokens:
            return None
        
        token_data = self.tokens[token]
        
        # Check if token has expired
        if time.time() > token_data["expires"]:
            # Remove expired token
            del self.tokens[token]
            return None
        
        return token_data["user_id"]

    def invalidate_token(self, token: str) -> bool:
        """Invalidate a token."""
        if token in self.tokens:
            del self.tokens[token]
            return True
        return False

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password."""
        user = self.db_manager.get_user_by_username(username)
        if not user:
            return None
        
        if self.verify_password(password, user.password_hash, user.password_salt):
            return user
        
        return None

    def register_user(self, username: str, email: str, password: str) -> Optional[User]:
        """Register a new user."""
        # Check if user already exists
        if self.db_manager.get_user_by_username(username):
            return None
        
        if self.db_manager.get_user_by_email(email):
            return None
        
        # Create user
        user = User(username=username, email=email, password=password)
        
        # Save user to database
        self.db_manager.save_user(user)
        
        return user

    def logout_user(self, token: str) -> bool:
        """Logout a user by invalidating their token."""
        return self.invalidate_token(token)


# Convenience function
def create_auth_manager() -> AuthManager:
    """Create an authentication manager instance."""
    return AuthManager()