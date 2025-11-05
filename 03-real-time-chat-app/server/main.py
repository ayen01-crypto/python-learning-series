"""
Main Server Entry Point
This script starts both the WebSocket server and HTTP server for the chat application.
"""

import asyncio
import threading
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.websocket_server import WebSocketServer
from server.http_server import HTTPServer
from server.database import DatabaseManager


def start_http_server():
    """Start the HTTP server in a separate thread."""
    http_server = HTTPServer()
    http_server.run()


def main():
    """Main function to start both servers."""
    print("=== Real-time Chat Application ===")
    
    # Initialize database
    db_manager = DatabaseManager()
    db_manager.initialize_database()
    print("Database initialized")
    
    # Start HTTP server in a separate thread
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()
    print("HTTP server started on http://localhost:8080")
    
    # Start WebSocket server in main thread
    websocket_server = WebSocketServer()
    print("WebSocket server starting on ws://localhost:8081")
    
    try:
        asyncio.run(websocket_server.start_server())
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        websocket_server.stop_server()
        print("Servers stopped")


if __name__ == "__main__":
    main()