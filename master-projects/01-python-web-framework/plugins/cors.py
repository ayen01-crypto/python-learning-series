"""
CORS Plugin
This plugin handles Cross-Origin Resource Sharing for the web framework.
"""

from typing import List
from framework import Middleware, HTTPRequest, HTTPResponse


class CORSPlugin(Middleware):
    """Middleware for handling Cross-Origin Resource Sharing."""

    def __init__(self, origins: List[str] = None, allow_credentials: bool = False, 
                 allow_methods: List[str] = None, allow_headers: List[str] = None):
        self.origins = origins or ["*"]
        self.allow_credentials = allow_credentials
        self.allow_methods = allow_methods or ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        self.allow_headers = allow_headers or ["*"]

    def process_request(self, request: HTTPRequest) -> None:
        """Process CORS preflight requests."""
        if request.method == "OPTIONS":
            origin = request.headers.get("Origin")
            if origin and (origin in self.origins or "*" in self.origins):
                # Handle preflight request by setting appropriate headers
                pass

    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        """Add CORS headers to responses."""
        origin = request.headers.get("Origin")
        
        if origin and (origin in self.origins or "*" in self.origins):
            # Set allowed origin
            if "*" in self.origins and not self.allow_credentials:
                response.headers["Access-Control-Allow-Origin"] = "*"
            else:
                response.headers["Access-Control-Allow-Origin"] = origin
            
            # Set allowed methods
            response.headers["Access-Control-Allow-Methods"] = ", ".join(self.allow_methods)
            
            # Set allowed headers
            if "*" in self.allow_headers:
                # If Access-Control-Request-Headers is present, echo it back
                request_headers = request.headers.get("Access-Control-Request-Headers")
                if request_headers:
                    response.headers["Access-Control-Allow-Headers"] = request_headers
                else:
                    response.headers["Access-Control-Allow-Headers"] = "*"
            else:
                response.headers["Access-Control-Allow-Headers"] = ", ".join(self.allow_headers)
            
            # Set credentials
            if self.allow_credentials:
                response.headers["Access-Control-Allow-Credentials"] = "true"
                
            # Set max age
            response.headers["Access-Control-Max-Age"] = "86400"  # 24 hours
            
        return response


# Convenience function
def setup_cors(app, origins: List[str] = None, allow_credentials: bool = False,
               allow_methods: List[str] = None, allow_headers: List[str] = None):
    """Setup CORS middleware."""
    cors_middleware = CORSPlugin(origins, allow_credentials, allow_methods, allow_headers)
    app.add_middleware(cors_middleware)