"""
Database Manager
This module handles database operations for the chat application.
"""

import sqlite3
import os
import hashlib
import secrets
import sys
from typing import List, Optional
from datetime import datetime

# Add parent directory to path to import models
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Local imports (using relative imports would be better in a package)
try:
    from server.models import User, ChatRoom, Message
except ImportError:
    # Fallback if relative imports don't work
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from server.models import User, ChatRoom, Message


class DatabaseManager:
    """Manages database operations for the chat application."""

    def __init__(self, db_path: str = "database/chat.db"):
        self.db_path = db_path
        # Create database directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True)

    def initialize_database(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                password_salt TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Create rooms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Create messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                room_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (room_id) REFERENCES rooms (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create default room if it doesn't exist
        cursor.execute('SELECT COUNT(*) FROM rooms')
        if cursor.fetchone()[0] == 0:
            default_room = ChatRoom(name="General", description="General chat room")
            cursor.execute('''
                INSERT INTO rooms (id, name, description, created_at)
                VALUES (?, ?, ?, ?)
            ''', (default_room.id, default_room.name, default_room.description, default_room.created_at))
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")

    def save_user(self, user: User):
        """Save a user to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users (id, username, email, password_hash, password_salt, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user.id, user.username, user.email, user.password_hash, user.password_salt, user.created_at))
        
        conn.commit()
        conn.close()

    def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                password_salt=row[4],
                created_at=row[5]
            )
        return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                password_salt=row[4],
                created_at=row[5]
            )
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                password_salt=row[4],
                created_at=row[5]
            )
        return None

    def get_all_users(self) -> List[User]:
        """Get all users."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        
        conn.close()
        
        return [
            User(
                id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                password_salt=row[4],
                created_at=row[5]
            ) for row in rows
        ]

    def save_room(self, room: ChatRoom):
        """Save a chat room to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO rooms (id, name, description, created_at)
            VALUES (?, ?, ?, ?)
        ''', (room.id, room.name, room.description, room.created_at))
        
        conn.commit()
        conn.close()

    def get_room(self, room_id: str) -> Optional[ChatRoom]:
        """Get a chat room by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM rooms WHERE id = ?', (room_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return ChatRoom(
                id=row[0],
                name=row[1],
                description=row[2],
                created_at=row[3]
            )
        return None

    def get_all_rooms(self) -> List[ChatRoom]:
        """Get all chat rooms."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM rooms')
        rows = cursor.fetchall()
        
        conn.close()
        
        return [
            ChatRoom(
                id=row[0],
                name=row[1],
                description=row[2],
                created_at=row[3]
            ) for row in rows
        ]

    def save_message(self, message: Message):
        """Save a message to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO messages (id, room_id, user_id, content, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (message.id, message.room_id, message.user_id, message.content, message.timestamp))
        
        conn.commit()
        conn.close()

    def get_messages_for_room(self, room_id: str, limit: int = 100) -> List[Message]:
        """Get messages for a specific room."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM messages 
            WHERE room_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (room_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Message(
                id=row[0],
                room_id=row[1],
                user_id=row[2],
                content=row[3],
                timestamp=row[4]
            ) for row in rows
        ]

    def get_recent_messages(self, limit: int = 50) -> List[Message]:
        """Get recent messages from all rooms."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM messages 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Message(
                id=row[0],
                room_id=row[1],
                user_id=row[2],
                content=row[3],
                timestamp=row[4]
            ) for row in rows
        ]


# Convenience function
def create_database_manager(db_path: str = "database/chat.db") -> DatabaseManager:
    """Create a database manager instance."""
    return DatabaseManager(db_path)