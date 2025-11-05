"""
Middleware Module
This module implements various middleware components for the web framework.
"""

import json
import time
import uuid
from typing import Dict, Any
from framework import Middleware, HTTPRequest, HTTPResponse
from http import HTTPHeaders, HTTPMethods


class LoggingMiddleware(Middleware):
    """Middleware for logging requests and responses."""

    def process_request(self, request: HTTPRequest) -> None:
        """Log incoming requests."""
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {request.method} {request.path}")
        print(f"Headers: {request.headers}")

    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        """Log outgoing responses."""
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {response.status_code} {request.path}")
        return response


class CORSMiddleware(Middleware):
    """Middleware for handling Cross-Origin Resource Sharing."""

    def __init__(self, origins: list = None, allow_credentials: bool = False):
        self.origins = origins or ["*"]
        self.allow_credentials = allow_credentials

    def process_request(self, request: HTTPRequest) -> None:
        """Process CORS preflight requests."""
        if request.method == "OPTIONS":
            origin = request.headers.get("Origin")
            if origin and (origin in self.origins or "*" in self.origins):
                # Handle preflight request
                pass

    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        """Add CORS headers to responses."""
        origin = request.headers.get("Origin")
        if origin and (origin in self.origins or "*" in self.origins):
            response.headers["Access-Control-Allow-Origin"] = origin if origin in self.origins else "*"
            
            if "Access-Control-Request-Method" in request.headers:
                response.headers["Access-Control-Allow-Methods"] = request.headers["Access-Control-Request-Method"]
            
            if "Access-Control-Request-Headers" in request.headers:
                response.headers["Access-Control-Allow-Headers"] = request.headers["Access-Control-Request-Headers"]
            
            if self.allow_credentials:
                response.headers["Access-Control-Allow-Credentials"] = "true"
                
            response.headers["Access-Control-Max-Age"] = "86400"  # 24 hours
            
        return response


class JSONMiddleware(Middleware):
    """Middleware for handling JSON requests and responses."""

    def process_request(self, request: HTTPRequest) -> None:
        """Parse JSON request body."""
        content_type = request.headers.get("Content-Type", "")
        if "application/json" in content_type and request.body:
            try:
                request.json = json.loads(request.body)
            except json.JSONDecodeError:
                request.json = {}

    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        """Convert dict responses to JSON."""
        if isinstance(response.body, dict):
            response.body = json.dumps(response.body)
            response.headers["Content-Type"] = "application/json"
        return response


class AuthenticationMiddleware(Middleware):
    """Middleware for handling authentication."""

    def __init__(self, user_provider=None):
        self.user_provider = user_provider
        self.excluded_paths = ["/login", "/register", "/static/"]

    def process_request(self, request: HTTPRequest) -> HTTPResponse:
        """Check authentication for protected routes."""
        # Skip authentication for excluded paths
        for path in self.excluded_paths:
            if request.path.startswith(path):
                return None

        # Check for authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return HTTPResponse(
                '{"error": "Missing authorization header"}',
                status_code=401,
                headers={"Content-Type": "application/json"}
            )

        # Parse token
        if not auth_header.startswith("Bearer "):
            return HTTPResponse(
                '{"error": "Invalid authorization header"}',
                status_code=401,
                headers={"Content-Type": "application/json"}
            )

        token = auth_header[7:]  # Remove "Bearer " prefix
        
        # Validate token (simplified)
        if self.user_provider:
            user = self.user_provider.get_user_from_token(token)
            if user:
                request.user = user
            else:
                return HTTPResponse(
                    '{"error": "Invalid token"}',
                    status_code=401,
                    headers={"Content-Type": "application/json"}
                )
        
        return None


class SessionMiddleware(Middleware):
    """Middleware for handling sessions."""

    def __init__(self, session_store=None):
        self.session_store = session_store or InMemorySessionStore()

    def process_request(self, request: HTTPRequest) -> None:
        """Load session data."""
        session_id = self._get_session_id(request)
        if session_id:
            request.session = self.session_store.get_session(session_id)
        else:
            request.session = None

    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        """Save session data."""
        if hasattr(request, 'session') and request.session:
            session_id = self._get_session_id(request)
            if not session_id:
                session_id = str(uuid.uuid4())
                response.cookies["session_id"] = session_id
            
            self.session_store.save_session(session_id, request.session)
            
        return response

    def _get_session_id(self, request: HTTPRequest) -> str:
        """Extract session ID from request."""
        # Check cookies first
        cookie_header = request.headers.get("Cookie", "")
        if "session_id=" in cookie_header:
            # Simple cookie parsing
            parts = cookie_header.split(";")
            for part in parts:
                if "session_id=" in part:
                    return part.split("=")[1].strip()
        
        # Check query parameters
        if "session_id" in request.query_params:
            return request.query_params["session_id"][0]
            
        return None


class InMemorySessionStore:
    """Simple in-memory session store."""

    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.expirations: Dict[str, float] = {}

    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get session data by ID."""
        if session_id in self.sessions:
            # Check expiration
            if session_id in self.expirations:
                if time.time() > self.expirations[session_id]:
                    # Session expired
                    del self.sessions[session_id]
                    del self.expirations[session_id]
                    return {}
            return self.sessions[session_id]
        return {}

    def save_session(self, session_id: str, session_data: Dict[str, Any]) -> None:
        """Save session data."""
        self.sessions[session_id] = session_data
        # Set expiration (1 hour)
        self.expirations[session_id] = time.time() + 3600

    def delete_session(self, session_id: str) -> None:
        """Delete a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
        if session_id in self.expirations:
            del self.expirations[session_id]


class ErrorHandlingMiddleware(Middleware):
    """Middleware for handling errors gracefully."""

    def __init__(self, debug: bool = False):
        self.debug = debug

    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        """Handle errors in responses."""
        if response.status_code >= 400:
            if not self.debug:
                # Don't expose internal errors in production
                if response.status_code == 500:
                    response.body = '{"error": "Internal server error"}'
                    response.headers["Content-Type"] = "application/json"
            else:
                # In debug mode, include error details
                pass
                
        return response


class CompressionMiddleware(Middleware):
    """Middleware for compressing responses."""

    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        """Compress response body if requested."""
        accept_encoding = request.headers.get("Accept-Encoding", "")
        
        # Check if client accepts gzip
        if "gzip" in accept_encoding and isinstance(response.body, str):
            import gzip
            import io
            
            # Only compress if body is large enough
            if len(response.body) > 1024:
                try:
                    # Compress the response
                    out = io.BytesIO()
                    with gzip.GzipFile(fileobj=out, mode='w') as f:
                        f.write(response.body.encode('utf-8'))
                    
                    compressed = out.getvalue()
                    
                    # Only use compression if it actually reduces size
                    if len(compressed) < len(response.body):
                        response.body = compressed.decode('latin1')  # Store as string
                        response.headers["Content-Encoding"] = "gzip"
                except Exception:
                    # If compression fails, return original response
                    pass
                    
        return response


# Convenience function to create middleware stack
def create_default_middleware_stack(debug: bool = False) -> list:
    """Create a default middleware stack."""
    return [
        LoggingMiddleware(),
        JSONMiddleware(),
        CORSMiddleware(),
        ErrorHandlingMiddleware(debug),
        SessionMiddleware(),
    ]