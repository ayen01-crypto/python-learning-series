"""
Data Models
This module defines the data models for the chat application.
"""

import uuid
from datetime import datetime
import hashlib
import secrets
from typing import Optional, Set


class User:
    """Represents a user in the chat application."""

    def __init__(self, username: str = "", email: str = "", password: str = "", 
                 id: Optional[str] = None, password_hash: Optional[str] = None, password_salt: Optional[str] = None,
                 created_at: Optional[str] = None):
        self.id: str = id or str(uuid.uuid4())
        self.username: str = username
        self.email: str = email
        self.created_at: str = created_at or datetime.now().isoformat()
        
        # Handle password hashing
        if password:
            self.password_salt = secrets.token_hex(16)
            self.password_hash = self._hash_password(password, self.password_salt)
        else:
            self.password_hash = password_hash or ""
            self.password_salt = password_salt or ""

    def _hash_password(self, password: str, salt: str) -> str:
        """Hash a password with salt."""
        salted_password = password + salt
        return hashlib.sha256(salted_password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        """Verify a password against the hash."""
        if not self.password_salt or not self.password_hash:
            return False
        hashed = self._hash_password(password, self.password_salt)
        return secrets.compare_digest(hashed, self.password_hash)


class ChatRoom:
    """Represents a chat room."""

    def __init__(self, name: str, description: str = "", id: Optional[str] = None, created_at: Optional[str] = None):
        self.id: str = id or str(uuid.uuid4())
        self.name: str = name
        self.description: str = description
        self.created_at: str = created_at or datetime.now().isoformat()
        self.users: Set[str] = set()  # Users currently in the room


class Message:
    """Represents a chat message."""

    def __init__(self, room_id: str, user_id: str, content: str, 
                 id: Optional[str] = None, timestamp: Optional[str] = None):
        self.id: str = id or str(uuid.uuid4())
        self.room_id: str = room_id
        self.user_id: str = user_id
        self.content: str = content
        self.timestamp: str = timestamp or datetime.now().isoformat()


class FileAttachment:
    """Represents a file attachment."""

    def __init__(self, message_id: str, file_name: str, file_path: str, 
                 file_size: int, mime_type: str, id: Optional[str] = None):
        self.id: str = id or str(uuid.uuid4())
        self.message_id: str = message_id
        self.file_name: str = file_name
        self.file_path: str = file_path
        self.file_size: int = file_size
        self.mime_type: str = mime_type
        self.uploaded_at: str = datetime.now().isoformat()


class Reaction:
    """Represents a reaction to a message."""

    def __init__(self, message_id: str, user_id: str, reaction_type: str, id: Optional[str] = None):
        self.id: str = id or str(uuid.uuid4())
        self.message_id: str = message_id
        self.user_id: str = user_id
        self.reaction_type: str = reaction_type
        self.created_at: str = datetime.now().isoformat()