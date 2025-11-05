"""
HTTP Server
This module implements the HTTP server for serving static files and REST API endpoints.
"""

import json
import os
from flask import Flask, request, jsonify, send_from_directory
from server.database import DatabaseManager
from server.auth import AuthManager
from server.models import User, ChatRoom, Message


class HTTPServer:
    """HTTP server for REST API and static file serving."""

    def __init__(self, host: str = "localhost", port: int = 8080):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.db_manager = DatabaseManager()
        self.auth_manager = AuthManager()
        self._setup_routes()

    def _setup_routes(self):
        """Setup HTTP routes."""
        
        # Serve static files
        @self.app.route('/')
        def index():
            return send_from_directory('client', 'index.html')
        
        @self.app.route('/<path:filename>')
        def static_files(filename):
            return send_from_directory('client', filename)
        
        # API routes
        @self.app.route('/api/users', methods=['GET'])
        def get_users():
            """Get list of all users."""
            try:
                users = self.db_manager.get_all_users()
                return jsonify([{
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at
                } for user in users])
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/users', methods=['POST'])
        def register_user():
            """Register a new user."""
            try:
                data = request.get_json()
                username = data.get('username')
                email = data.get('email')
                password = data.get('password')
                
                if not username or not email or not password:
                    return jsonify({'error': 'Username, email, and password are required'}), 400
                
                # Check if user already exists
                if self.db_manager.get_user_by_username(username):
                    return jsonify({'error': 'Username already exists'}), 400
                
                if self.db_manager.get_user_by_email(email):
                    return jsonify({'error': 'Email already exists'}), 400
                
                # Create user
                user = User(username=username, email=email, password=password)
                self.db_manager.save_user(user)
                
                return jsonify({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at
                }), 201
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/login', methods=['POST'])
        def login():
            """User login."""
            try:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')
                
                if not username or not password:
                    return jsonify({'error': 'Username and password are required'}), 400
                
                # Authenticate user
                user = self.db_manager.get_user_by_username(username)
                if not user or not self.auth_manager.verify_password(password, user.password_hash, user.password_salt):
                    return jsonify({'error': 'Invalid username or password'}), 401
                
                # Generate token
                token = self.auth_manager.generate_token(user.id)
                
                return jsonify({
                    'token': token,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/rooms', methods=['GET'])
        def get_rooms():
            """Get list of all chat rooms."""
            try:
                rooms = self.db_manager.get_all_rooms()
                return jsonify([{
                    'id': room.id,
                    'name': room.name,
                    'description': room.description,
                    'created_at': room.created_at
                } for room in rooms])
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/rooms', methods=['POST'])
        def create_room():
            """Create a new chat room."""
            try:
                # Check authentication
                auth_header = request.headers.get('Authorization')
                if not auth_header or not auth_header.startswith('Bearer '):
                    return jsonify({'error': 'Authentication required'}), 401
                
                token = auth_header[7:]  # Remove 'Bearer ' prefix
                user_id = self.auth_manager.validate_token(token)
                if not user_id:
                    return jsonify({'error': 'Invalid token'}), 401
                
                data = request.get_json()
                name = data.get('name')
                description = data.get('description')
                
                if not name:
                    return jsonify({'error': 'Room name is required'}), 400
                
                # Create room
                room = ChatRoom(name=name, description=description)
                self.db_manager.save_room(room)
                
                return jsonify({
                    'id': room.id,
                    'name': room.name,
                    'description': room.description,
                    'created_at': room.created_at
                }), 201
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/rooms/<room_id>', methods=['GET'])
        def get_room(room_id):
            """Get room details."""
            try:
                room = self.db_manager.get_room(room_id)
                if not room:
                    return jsonify({'error': 'Room not found'}), 404
                
                return jsonify({
                    'id': room.id,
                    'name': room.name,
                    'description': room.description,
                    'created_at': room.created_at
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/messages', methods=['POST'])
        def send_message():
            """Send a message."""
            try:
                # Check authentication
                auth_header = request.headers.get('Authorization')
                if not auth_header or not auth_header.startswith('Bearer '):
                    return jsonify({'error': 'Authentication required'}), 401
                
                token = auth_header[7:]  # Remove 'Bearer ' prefix
                user_id = self.auth_manager.validate_token(token)
                if not user_id:
                    return jsonify({'error': 'Invalid token'}), 401
                
                data = request.get_json()
                room_id = data.get('room_id')
                content = data.get('content')
                
                if not room_id or not content:
                    return jsonify({'error': 'Room ID and content are required'}), 400
                
                # Create message
                from datetime import datetime
                message = Message(
                    room_id=room_id,
                    user_id=user_id,
                    content=content,
                    timestamp=datetime.now().isoformat()
                )
                self.db_manager.save_message(message)
                
                return jsonify({
                    'id': message.id,
                    'room_id': message.room_id,
                    'user_id': message.user_id,
                    'content': message.content,
                    'timestamp': message.timestamp
                }), 201
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/messages/<room_id>', methods=['GET'])
        def get_messages(room_id):
            """Get message history for a room."""
            try:
                # Check authentication
                auth_header = request.headers.get('Authorization')
                if not auth_header or not auth_header.startswith('Bearer '):
                    return jsonify({'error': 'Authentication required'}), 401
                
                token = auth_header[7:]  # Remove 'Bearer ' prefix
                user_id = self.auth_manager.validate_token(token)
                if not user_id:
                    return jsonify({'error': 'Invalid token'}), 401
                
                # Get messages
                messages = self.db_manager.get_messages_for_room(room_id)
                
                return jsonify([{
                    'id': msg.id,
                    'room_id': msg.room_id,
                    'user_id': msg.user_id,
                    'content': msg.content,
                    'timestamp': msg.timestamp
                } for msg in messages])
            except Exception as e:
                return jsonify({'error': str(e)}), 500

    def run(self, debug: bool = False):
        """Run the HTTP server."""
        self.app.run(host=self.host, port=self.port, debug=debug)


# Convenience function
def create_http_server(host: str = "localhost", port: int = 8080) -> HTTPServer:
    """Create an HTTP server instance."""
    return HTTPServer(host, port)