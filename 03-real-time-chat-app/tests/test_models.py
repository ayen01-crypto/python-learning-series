"""
Tests for Data Models
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from server.models import User, ChatRoom, Message


class TestUser(unittest.TestCase):
    """Test User model."""

    def test_user_creation(self):
        """Test creating a user."""
        user = User(username="testuser", email="test@example.com", password="password123")
        
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertIsNotNone(user.password_hash)
        self.assertIsNotNone(user.password_salt)
        self.assertIsNotNone(user.created_at)

    def test_user_password_verification(self):
        """Test user password verification."""
        user = User(username="testuser", email="test@example.com", password="password123")
        
        self.assertTrue(user.verify_password("password123"))
        self.assertFalse(user.verify_password("wrongpassword"))


class TestChatRoom(unittest.TestCase):
    """Test ChatRoom model."""

    def test_room_creation(self):
        """Test creating a chat room."""
        room = ChatRoom(name="Test Room", description="A test chat room")
        
        self.assertIsNotNone(room.id)
        self.assertEqual(room.name, "Test Room")
        self.assertEqual(room.description, "A test chat room")
        self.assertIsNotNone(room.created_at)
        self.assertIsInstance(room.users, set)


class TestMessage(unittest.TestCase):
    """Test Message model."""

    def test_message_creation(self):
        """Test creating a message."""
        message = Message(room_id="room123", user_id="user123", content="Hello, world!")
        
        self.assertIsNotNone(message.id)
        self.assertEqual(message.room_id, "room123")
        self.assertEqual(message.user_id, "user123")
        self.assertEqual(message.content, "Hello, world!")
        self.assertIsNotNone(message.timestamp)


if __name__ == '__main__':
    unittest.main()