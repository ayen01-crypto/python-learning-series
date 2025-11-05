"""
Configuration Module
This module handles configuration for the chat application.
"""

import os


class Config:
    """Application configuration."""

    def __init__(self):
        # Server configuration
        self.HOST = os.environ.get('CHAT_HOST', 'localhost')
        self.WEBSOCKET_PORT = int(os.environ.get('CHAT_WEBSOCKET_PORT', 8081))
        self.HTTP_PORT = int(os.environ.get('CHAT_HTTP_PORT', 8080))
        
        # Database configuration
        self.DATABASE_PATH = os.environ.get('CHAT_DATABASE_PATH', 'database/chat.db')
        
        # Security configuration
        self.SECRET_KEY = os.environ.get('CHAT_SECRET_KEY', 'your-secret-key-here')
        self.TOKEN_EXPIRY = int(os.environ.get('CHAT_TOKEN_EXPIRY', 3600))  # 1 hour
        
        # WebSocket configuration
        self.WEBSOCKET_PING_INTERVAL = int(os.environ.get('CHAT_WEBSOCKET_PING_INTERVAL', 30))
        self.WEBSOCKET_PING_TIMEOUT = int(os.environ.get('CHAT_WEBSOCKET_PING_TIMEOUT', 10))
        
        # Message configuration
        self.MAX_MESSAGE_LENGTH = int(os.environ.get('CHAT_MAX_MESSAGE_LENGTH', 1000))
        self.MESSAGE_HISTORY_LIMIT = int(os.environ.get('CHAT_MESSAGE_HISTORY_LIMIT', 100))
        
        # Room configuration
        self.DEFAULT_ROOM_NAME = os.environ.get('CHAT_DEFAULT_ROOM_NAME', 'General')
        self.MAX_ROOMS = int(os.environ.get('CHAT_MAX_ROOMS', 100))
        
        # User configuration
        self.MAX_USERNAME_LENGTH = int(os.environ.get('CHAT_MAX_USERNAME_LENGTH', 50))
        self.MAX_USERS_PER_ROOM = int(os.environ.get('CHAT_MAX_USERS_PER_ROOM', 1000))


# Global configuration instance
config = Config()