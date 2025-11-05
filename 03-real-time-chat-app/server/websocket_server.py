"""
WebSocket Server
This module implements the WebSocket server for real-time chat functionality.
"""

import asyncio
import websockets
import json
import uuid
from typing import Dict, Set, Any
from datetime import datetime
from server.models import User, Message, ChatRoom
from server.database import DatabaseManager
from server.auth import AuthManager


class WebSocketServer:
    """WebSocket server for real-time chat."""

    def __init__(self, host: str = "localhost", port: int = 8081):
        self.host = host
        self.port = port
        self.clients: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.users: Dict[str, User] = {}
        self.rooms: Dict[str, ChatRoom] = {}
        self.db_manager = DatabaseManager()
        self.auth_manager = AuthManager()
        self.running = False

    async def register_client(self, websocket: websockets.WebSocketServerProtocol, user_id: str):
        """Register a new client connection."""
        self.clients[user_id] = websocket
        print(f"Client {user_id} connected")

    async def unregister_client(self, user_id: str):
        """Unregister a client connection."""
        if user_id in self.clients:
            del self.clients[user_id]
            print(f"Client {user_id} disconnected")

    async def handle_message(self, websocket: websockets.WebSocketServerProtocol, message: str):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(message)
            action = data.get("action")
            
            if action == "authenticate":
                await self.handle_authentication(websocket, data)
            elif action == "join_room":
                await self.handle_join_room(websocket, data)
            elif action == "leave_room":
                await self.handle_leave_room(websocket, data)
            elif action == "send_message":
                await self.handle_send_message(websocket, data)
            elif action == "typing_start":
                await self.handle_typing_start(websocket, data)
            elif action == "typing_stop":
                await self.handle_typing_stop(websocket, data)
            elif action == "reaction":
                await self.handle_reaction(websocket, data)
            else:
                await websocket.send(json.dumps({
                    "action": "error",
                    "message": f"Unknown action: {action}"
                }))
                
        except json.JSONDecodeError:
            await websocket.send(json.dumps({
                "action": "error",
                "message": "Invalid JSON format"
            }))
        except Exception as e:
            print(f"Error handling message: {e}")
            await websocket.send(json.dumps({
                "action": "error",
                "message": "Internal server error"
            }))

    async def handle_authentication(self, websocket: websockets.WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle user authentication."""
        token = data.get("token")
        if not token:
            await websocket.send(json.dumps({
                "action": "auth_error",
                "message": "Authentication token required"
            }))
            return
        
        # Validate token
        user_id = self.auth_manager.validate_token(token)
        if not user_id:
            await websocket.send(json.dumps({
                "action": "auth_error",
                "message": "Invalid authentication token"
            }))
            return
        
        # Register client
        await self.register_client(websocket, user_id)
        
        # Get user info
        user = self.db_manager.get_user(user_id)
        if user:
            self.users[user_id] = user
            await websocket.send(json.dumps({
                "action": "auth_success",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }))

    async def handle_join_room(self, websocket: websockets.WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle user joining a chat room."""
        user_id = self.get_user_id_from_websocket(websocket)
        if not user_id:
            await websocket.send(json.dumps({
                "action": "error",
                "message": "Not authenticated"
            }))
            return
        
        room_id = data.get("room_id")
        if not room_id:
            await websocket.send(json.dumps({
                "action": "error",
                "message": "Room ID required"
            }))
            return
        
        # Add user to room
        if room_id not in self.rooms:
            room = self.db_manager.get_room(room_id)
            if not room:
                await websocket.send(json.dumps({
                    "action": "error",
                    "message": "Room not found"
                }))
                return
            self.rooms[room_id] = room
        
        # Add user to room's user list
        if not hasattr(self.rooms[room_id], 'users'):
            self.rooms[room_id].users = set()
        self.rooms[room_id].users.add(user_id)
        
        # Notify other users in the room
        await self.broadcast_to_room(room_id, {
            "action": "user_joined",
            "user_id": user_id,
            "username": self.users[user_id].username if user_id in self.users else "Unknown"
        }, exclude_user=user_id)
        
        # Send room info to user
        await websocket.send(json.dumps({
            "action": "room_joined",
            "room_id": room_id,
            "room_name": self.rooms[room_id].name
        }))

    async def handle_leave_room(self, websocket: websockets.WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle user leaving a chat room."""
        user_id = self.get_user_id_from_websocket(websocket)
        if not user_id:
            return
        
        room_id = data.get("room_id")
        if not room_id or room_id not in self.rooms:
            return
        
        # Remove user from room
        if hasattr(self.rooms[room_id], 'users') and user_id in self.rooms[room_id].users:
            self.rooms[room_id].users.remove(user_id)
        
        # Notify other users in the room
        await self.broadcast_to_room(room_id, {
            "action": "user_left",
            "user_id": user_id,
            "username": self.users[user_id].username if user_id in self.users else "Unknown"
        }, exclude_user=user_id)

    async def handle_send_message(self, websocket: websockets.WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle sending a chat message."""
        user_id = self.get_user_id_from_websocket(websocket)
        if not user_id:
            await websocket.send(json.dumps({
                "action": "error",
                "message": "Not authenticated"
            }))
            return
        
        room_id = data.get("room_id")
        content = data.get("content")
        
        if not room_id or not content:
            await websocket.send(json.dumps({
                "action": "error",
                "message": "Room ID and content required"
            }))
            return
        
        # Create message
        message = Message(
            id=str(uuid.uuid4()),
            room_id=room_id,
            user_id=user_id,
            content=content,
            timestamp=datetime.now().isoformat()
        )
        
        # Save message to database
        self.db_manager.save_message(message)
        
        # Broadcast message to room
        await self.broadcast_to_room(room_id, {
            "action": "new_message",
            "message": {
                "id": message.id,
                "room_id": message.room_id,
                "user_id": message.user_id,
                "username": self.users[user_id].username if user_id in self.users else "Unknown",
                "content": message.content,
                "timestamp": message.timestamp
            }
        })

    async def handle_typing_start(self, websocket: websockets.WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle typing start notification."""
        user_id = self.get_user_id_from_websocket(websocket)
        if not user_id:
            return
        
        room_id = data.get("room_id")
        if not room_id:
            return
        
        # Broadcast typing start to room
        await self.broadcast_to_room(room_id, {
            "action": "typing_start",
            "user_id": user_id,
            "username": self.users[user_id].username if user_id in self.users else "Unknown"
        }, exclude_user=user_id)

    async def handle_typing_stop(self, websocket: websockets.WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle typing stop notification."""
        user_id = self.get_user_id_from_websocket(websocket)
        if not user_id:
            return
        
        room_id = data.get("room_id")
        if not room_id:
            return
        
        # Broadcast typing stop to room
        await self.broadcast_to_room(room_id, {
            "action": "typing_stop",
            "user_id": user_id,
            "username": self.users[user_id].username if user_id in self.users else "Unknown"
        }, exclude_user=user_id)

    async def handle_reaction(self, websocket: websockets.WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle message reaction."""
        user_id = self.get_user_id_from_websocket(websocket)
        if not user_id:
            await websocket.send(json.dumps({
                "action": "error",
                "message": "Not authenticated"
            }))
            return
        
        message_id = data.get("message_id")
        reaction = data.get("reaction")
        
        if not message_id or not reaction:
            await websocket.send(json.dumps({
                "action": "error",
                "message": "Message ID and reaction required"
            }))
            return
        
        # Save reaction to database (simplified)
        # In a real implementation, you'd update the message with the reaction
        
        # Broadcast reaction to room
        # For simplicity, we'll assume the message is in the first room we find
        room_id = None
        for rid, room in self.rooms.items():
            if hasattr(room, 'users') and user_id in room.users:
                room_id = rid
                break
        
        if room_id:
            await self.broadcast_to_room(room_id, {
                "action": "reaction",
                "message_id": message_id,
                "user_id": user_id,
                "reaction": reaction
            })

    def get_user_id_from_websocket(self, websocket: websockets.WebSocketServerProtocol) -> str:
        """Get user ID from WebSocket connection."""
        for user_id, ws in self.clients.items():
            if ws == websocket:
                return user_id
        return None

    async def broadcast_to_room(self, room_id: str, message: Dict[str, Any], exclude_user: str = None):
        """Broadcast message to all users in a room."""
        if room_id not in self.rooms or not hasattr(self.rooms[room_id], 'users'):
            return
        
        # Get connected users in the room
        connected_users = set(self.clients.keys()) & self.rooms[room_id].users
        
        # Send message to each user
        for user_id in connected_users:
            if user_id == exclude_user:
                continue
            
            try:
                await self.clients[user_id].send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                await self.unregister_client(user_id)

    async def handle_client(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Handle individual client connections."""
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            user_id = self.get_user_id_from_websocket(websocket)
            if user_id:
                await self.unregister_client(user_id)
        except Exception as e:
            print(f"Error handling client: {e}")
            user_id = self.get_user_id_from_websocket(websocket)
            if user_id:
                await self.unregister_client(user_id)

    async def start_server(self):
        """Start the WebSocket server."""
        self.running = True
        server = await websockets.serve(self.handle_client, self.host, self.port)
        print(f"WebSocket server started on ws://{self.host}:{self.port}")
        
        try:
            await server.wait_closed()
        except asyncio.CancelledError:
            pass
        finally:
            self.running = False

    def stop_server(self):
        """Stop the WebSocket server."""
        self.running = False
        print("WebSocket server stopped")


# Convenience function
def create_websocket_server(host: str = "localhost", port: int = 8081) -> WebSocketServer:
    """Create a WebSocket server instance."""
    return WebSocketServer(host, port)