"""
Demo Script for Real-time Chat Application
This script demonstrates how to use the chat application components.
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from server.models import User, ChatRoom, Message
from server.database import DatabaseManager
from server.auth import AuthManager


def demo_user_operations():
    """Demonstrate user operations."""
    print("=== User Operations Demo ===")
    
    # Create database manager
    db_manager = DatabaseManager()
    db_manager.initialize_database()
    
    # Create auth manager
    auth_manager = AuthManager()
    
    # Register a new user
    print("1. Registering a new user...")
    user = auth_manager.register_user("alice", "alice@example.com", "password123")
    if user:
        print(f"   User registered: {user.username} ({user.email})")
    else:
        print("   Failed to register user")
    
    # Try to register the same user again (should fail)
    print("2. Trying to register the same user again...")
    user2 = auth_manager.register_user("alice", "alice2@example.com", "password456")
    if user2:
        print("   User registered again (unexpected)")
    else:
        print("   Registration failed as expected (username already exists)")
    
    # Authenticate user
    print("3. Authenticating user...")
    authenticated_user = auth_manager.authenticate_user("alice", "password123")
    if authenticated_user:
        print(f"   User authenticated: {authenticated_user.username}")
    else:
        print("   Authentication failed")
    
    # Try wrong password
    print("4. Trying wrong password...")
    wrong_auth = auth_manager.authenticate_user("alice", "wrongpassword")
    if wrong_auth:
        print("   Authentication succeeded (unexpected)")
    else:
        print("   Authentication failed as expected (wrong password)")


def demo_room_operations():
    """Demonstrate room operations."""
    print("\n=== Room Operations Demo ===")
    
    # Create database manager
    db_manager = DatabaseManager()
    
    # Create a chat room
    print("1. Creating a chat room...")
    room = ChatRoom(name="Python Developers", description="Discussion about Python programming")
    db_manager.save_room(room)
    print(f"   Room created: {room.name}")
    
    # Get all rooms
    print("2. Getting all rooms...")
    rooms = db_manager.get_all_rooms()
    for r in rooms:
        print(f"   Room: {r.name} - {r.description}")


def demo_message_operations():
    """Demonstrate message operations."""
    print("\n=== Message Operations Demo ===")
    
    # Create database manager
    db_manager = DatabaseManager()
    
    # Get user and room
    user = db_manager.get_user_by_username("alice")
    rooms = db_manager.get_all_rooms()
    
    if user and rooms:
        room = rooms[0]  # Get the first room
        
        # Create a message
        print("1. Creating a message...")
        message = Message(
            room_id=room.id,
            user_id=user.id,
            content="Hello, this is a test message!"
        )
        db_manager.save_message(message)
        print(f"   Message sent by {user.username}: {message.content}")
        
        # Get messages for room
        print("2. Getting messages for room...")
        messages = db_manager.get_messages_for_room(room.id)
        for msg in messages:
            user = db_manager.get_user(msg.user_id)
            username = user.username if user else "Unknown"
            print(f"   [{msg.timestamp}] {username}: {msg.content}")


def main():
    """Main demo function."""
    print("Real-time Chat Application Demo")
    print("=" * 40)
    
    demo_user_operations()
    demo_room_operations()
    demo_message_operations()
    
    print("\n=== Demo Completed ===")
    print("To run the full chat application:")
    print("1. Run 'python server/main.py'")
    print("2. Open your browser to http://localhost:8080")
    print("3. Register a new account or login with existing credentials")


if __name__ == "__main__":
    main()