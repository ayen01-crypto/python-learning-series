"""
Session Management Module
This module implements session handling for the web framework.
"""

import json
import time
import uuid
import hashlib
import os
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class Session(ABC):
    """Abstract base class for session implementations."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.data: Dict[str, Any] = {}
        self.created_at = time.time()
        self.last_accessed = self.created_at

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the session."""
        self.last_accessed = time.time()
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a value in the session."""
        self.data[key] = value
        self.last_accessed = time.time()

    def delete(self, key: str) -> None:
        """Delete a key from the session."""
        if key in self.data:
            del self.data[key]
        self.last_accessed = time.time()

    def clear(self) -> None:
        """Clear all session data."""
        self.data.clear()
        self.last_accessed = time.time()

    def keys(self) -> list:
        """Get all session keys."""
        return list(self.data.keys())

    def values(self) -> list:
        """Get all session values."""
        return list(self.data.values())

    def items(self) -> list:
        """Get all session key-value pairs."""
        return list(self.data.items())

    @abstractmethod
    def save(self) -> None:
        """Save the session data."""
        pass

    @abstractmethod
    def load(self) -> None:
        """Load the session data."""
        pass

    @abstractmethod
    def destroy(self) -> None:
        """Destroy the session."""
        pass


class InMemorySession(Session):
    """In-memory session implementation."""

    _storage: Dict[str, Dict[str, Any]] = {}
    _metadata: Dict[str, Dict[str, float]] = {}

    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.load()

    def save(self) -> None:
        """Save session to in-memory storage."""
        InMemorySession._storage[self.session_id] = self.data.copy()
        InMemorySession._metadata[self.session_id] = {
            'created_at': self.created_at,
            'last_accessed': self.last_accessed
        }

    def load(self) -> None:
        """Load session from in-memory storage."""
        if self.session_id in InMemorySession._storage:
            self.data = InMemorySession._storage[self.session_id].copy()
            metadata = InMemorySession._metadata[self.session_id]
            self.created_at = metadata['created_at']
            self.last_accessed = metadata['last_accessed']

    def destroy(self) -> None:
        """Destroy the session."""
        if self.session_id in InMemorySession._storage:
            del InMemorySession._storage[self.session_id]
        if self.session_id in InMemorySession._metadata:
            del InMemorySession._metadata[self.session_id]


class FileSession(Session):
    """File-based session implementation."""

    def __init__(self, session_id: str, storage_path: str = "sessions"):
        self.storage_path = storage_path
        # Create storage directory if it doesn't exist
        os.makedirs(storage_path, exist_ok=True)
        super().__init__(session_id)
        self.load()

    def _get_session_file_path(self) -> str:
        """Get the file path for this session."""
        # Use a hash of the session ID to avoid filesystem issues
        session_hash = hashlib.md5(self.session_id.encode()).hexdigest()
        return os.path.join(self.storage_path, f"session_{session_hash}.json")

    def save(self) -> None:
        """Save session to file."""
        session_data = {
            'session_id': self.session_id,
            'data': self.data,
            'created_at': self.created_at,
            'last_accessed': self.last_accessed
        }
        
        try:
            with open(self._get_session_file_path(), 'w') as f:
                json.dump(session_data, f)
        except Exception as e:
            print(f"Warning: Failed to save session: {e}")

    def load(self) -> None:
        """Load session from file."""
        try:
            with open(self._get_session_file_path(), 'r') as f:
                session_data = json.load(f)
                self.data = session_data.get('data', {})
                self.created_at = session_data.get('created_at', self.created_at)
                self.last_accessed = session_data.get('last_accessed', self.last_accessed)
        except FileNotFoundError:
            # Session file doesn't exist, start with empty session
            pass
        except Exception as e:
            print(f"Warning: Failed to load session: {e}")

    def destroy(self) -> None:
        """Destroy the session file."""
        try:
            os.remove(self._get_session_file_path())
        except FileNotFoundError:
            # File already deleted
            pass
        except Exception as e:
            print(f"Warning: Failed to destroy session: {e}")


class SessionManager:
    """Manages sessions across the application."""

    def __init__(self, session_class: type = InMemorySession, **kwargs):
        self.session_class = session_class
        self.session_kwargs = kwargs
        self.sessions: Dict[str, Session] = {}

    def create_session(self) -> Session:
        """Create a new session."""
        session_id = str(uuid.uuid4())
        session = self.session_class(session_id, **self.session_kwargs)
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get an existing session."""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            # Check if session has expired (1 hour default)
            if time.time() - session.last_accessed > 3600:
                self.destroy_session(session_id)
                return None
            return session
        
        # Try to load session
        try:
            session = self.session_class(session_id, **self.session_kwargs)
            if session.data:  # If session has data
                # Check expiration
                if time.time() - session.last_accessed <= 3600:
                    self.sessions[session_id] = session
                    return session
                else:
                    session.destroy()
        except Exception:
            pass
            
        return None

    def destroy_session(self, session_id: str) -> None:
        """Destroy a session."""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.destroy()
            del self.sessions[session_id]

    def cleanup_expired_sessions(self) -> None:
        """Remove expired sessions."""
        current_time = time.time()
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if current_time - session.last_accessed > 3600:  # 1 hour
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.destroy_session(session_id)


class SecureSession(InMemorySession):
    """Session with encryption support."""

    def __init__(self, session_id: str, secret_key: str = None):
        self.secret_key = secret_key or "default_secret_key"
        super().__init__(session_id)

    def _encrypt_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt session data."""
        # Simple XOR encryption for demonstration (not for production use)
        encrypted = {}
        for key, value in data.items():
            if isinstance(value, str):
                encrypted[key] = ''.join(chr(ord(c) ^ ord(self.secret_key[i % len(self.secret_key)])) 
                                       for i, c in enumerate(value))
            else:
                encrypted[key] = value  # Non-string values are not encrypted
        return encrypted

    def _decrypt_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Decrypt session data."""
        # Simple XOR decryption
        decrypted = {}
        for key, value in data.items():
            if isinstance(value, str):
                decrypted[key] = ''.join(chr(ord(c) ^ ord(self.secret_key[i % len(self.secret_key)])) 
                                       for i, c in enumerate(value))
            else:
                decrypted[key] = value
        return decrypted

    def save(self) -> None:
        """Save encrypted session data."""
        encrypted_data = self._encrypt_data(self.data)
        # Store encrypted data temporarily
        original_data = self.data.copy()
        self.data = encrypted_data
        super().save()
        # Restore original data
        self.data = original_data

    def load(self) -> None:
        """Load and decrypt session data."""
        super().load()
        if self.data:
            self.data = self._decrypt_data(self.data)


# Global session manager
session_manager = SessionManager()


# Convenience functions
def create_session() -> Session:
    """Create a new session."""
    return session_manager.create_session()


def get_session(session_id: str) -> Optional[Session]:
    """Get an existing session."""
    return session_manager.get_session(session_id)


def destroy_session(session_id: str) -> None:
    """Destroy a session."""
    session_manager.destroy_session(session_id)