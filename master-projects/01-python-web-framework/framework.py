"""
Core Framework Module
This module implements the main application class and core components of our lightweight web framework.
"""

import json
import re
import threading
from typing import Dict, List, Callable, Any, Optional, Tuple
from urllib.parse import parse_qs, urlparse
import traceback


class SingletonMeta(type):
    """Thread-safe Singleton metaclass."""
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class HTTPRequest:
    """Represents an HTTP request."""

    def __init__(self, method: str, path: str, headers: Dict[str, str], body: str = ""):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
        self.params = {}
        self.query_params = {}
        self.session = None
        self.user = None
        
        # Parse query parameters
        parsed_url = urlparse(path)
        self.query_params = parse_qs(parsed_url.query)


class HTTPResponse:
    """Represents an HTTP response."""

    def __init__(self, body: str = "", status_code: int = 200, headers: Dict[str, str] = None):
        self.body = body
        self.status_code = status_code
        self.headers = headers or {}
        self.cookies = {}


class Route:
    """Represents a route definition."""

    def __init__(self, path: str, handler: Callable, methods: List[str] = None):
        self.path = path
        self.handler = handler
        self.methods = methods or ["GET"]
        # Convert path to regex for parameter matching
        self.regex = self._path_to_regex(path)
        self.param_names = self._extract_param_names(path)

    def _path_to_regex(self, path: str) -> str:
        """Convert a path with parameters to a regex pattern."""
        # Replace {param} with regex capturing group
        pattern = re.sub(r'\{([^}]+)\}', r'(?P<\1>[^/]+)', path)
        # Escape other regex special characters
        pattern = re.sub(r'([\.\\\+\*\?\[\^\]\$\(\)\{\}\|\-])', r'\\\1', pattern)
        return f'^{pattern}$'

    def _extract_param_names(self, path: str) -> List[str]:
        """Extract parameter names from path."""
        return re.findall(r'\{([^}]+)\}', path)

    def matches(self, path: str, method: str) -> Optional[Dict[str, str]]:
        """Check if this route matches the given path and method."""
        if method not in self.methods:
            return None
            
        match = re.match(self.regex, path)
        if match:
            return match.groupdict()
        return None


class Middleware:
    """Base middleware class."""

    def process_request(self, request: HTTPRequest) -> Optional[HTTPResponse]:
        """Process the request before it reaches the handler."""
        return None

    def process_response(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        """Process the response before it's sent."""
        return response


class Application(metaclass=SingletonMeta):
    """Main application class implementing the web framework."""

    def __init__(self):
        self.routes: List[Route] = []
        self.middlewares: List[Middleware] = []
        self.error_handlers: Dict[int, Callable] = {}
        self.template_engine = None
        self.static_files_dir = "static"
        self.debug = False

    def route(self, path: str, methods: List[str] = None):
        """Decorator for registering routes."""
        def decorator(handler: Callable):
            self.add_route(path, handler, methods)
            return handler
        return decorator

    def add_route(self, path: str, handler: Callable, methods: List[str] = None):
        """Add a route to the application."""
        route = Route(path, handler, methods)
        self.routes.append(route)

    def add_middleware(self, middleware: Middleware):
        """Add middleware to the application."""
        self.middlewares.append(middleware)

    def errorhandler(self, status_code: int):
        """Decorator for registering error handlers."""
        def decorator(handler: Callable):
            self.error_handlers[status_code] = handler
            return handler
        return decorator

    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        """Handle an incoming HTTP request."""
        try:
            # Process request through middlewares
            for middleware in self.middlewares:
                response = middleware.process_request(request)
                if response:
                    return self._apply_response_middlewares(request, response)

            # Find matching route
            handler, params = self._find_handler(request)
            if not handler:
                return self._handle_error(404, request)

            # Set parameters in request
            request.params = params

            # Call the handler
            try:
                result = handler(request)
            except Exception as e:
                if self.debug:
                    traceback.print_exc()
                return self._handle_error(500, request)

            # Convert result to response if needed
            if isinstance(result, HTTPResponse):
                response = result
            elif isinstance(result, str):
                response = HTTPResponse(result)
            elif isinstance(result, dict):
                response = HTTPResponse(
                    json.dumps(result),
                    headers={"Content-Type": "application/json"}
                )
            else:
                response = HTTPResponse(str(result))

        except Exception as e:
            if self.debug:
                traceback.print_exc()
            return self._handle_error(500, request)

        return self._apply_response_middlewares(request, response)

    def _find_handler(self, request: HTTPRequest) -> Tuple[Optional[Callable], Dict[str, str]]:
        """Find the appropriate handler for a request."""
        for route in self.routes:
            params = route.matches(request.path, request.method)
            if params is not None:
                return route.handler, params
        return None, {}

    def _apply_response_middlewares(self, request: HTTPRequest, response: HTTPResponse) -> HTTPResponse:
        """Apply response middlewares."""
        for middleware in reversed(self.middlewares):
            response = middleware.process_response(request, response)
        return response

    def _handle_error(self, status_code: int, request: HTTPRequest) -> HTTPResponse:
        """Handle an error by calling the appropriate error handler."""
        if status_code in self.error_handlers:
            handler = self.error_handlers[status_code]
            try:
                result = handler(request)
                if isinstance(result, HTTPResponse):
                    return result
                else:
                    return HTTPResponse(str(result), status_code=status_code)
            except Exception:
                pass  # Fall through to default error handling

        # Default error responses
        error_messages = {
            404: "Not Found",
            500: "Internal Server Error"
        }
        
        return HTTPResponse(
            f"<h1>{status_code} {error_messages.get(status_code, 'Error')}</h1>",
            status_code=status_code
        )

    def run(self, host: str = "localhost", port: int = 8000):
        """Run the development server."""
        from http.server import HTTPServer, BaseHTTPRequestHandler
        
        class RequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self._handle_request("GET")
                
            def do_POST(self):
                self._handle_request("POST")
                
            def do_PUT(self):
                self._handle_request("PUT")
                
            def do_DELETE(self):
                self._handle_request("DELETE")
                
            def _handle_request(self, method):
                # Read request body
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ""
                
                # Create request object
                request = HTTPRequest(
                    method=method,
                    path=self.path,
                    headers=dict(self.headers),
                    body=body
                )
                
                # Handle request
                response = self.application.handle_request(request)
                
                # Send response
                self.send_response(response.status_code)
                for header, value in response.headers.items():
                    self.send_header(header, value)
                for cookie, value in response.cookies.items():
                    self.send_header('Set-Cookie', f'{cookie}={value}')
                self.end_headers()
                self.wfile.write(response.body.encode('utf-8'))
        
        # Attach application to handler
        RequestHandler.application = self
        
        # Start server
        server = HTTPServer((host, port), RequestHandler)
        print(f"Starting server on http://{host}:{port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            server.shutdown()


# Global application instance
app = Application()


# Convenience decorators
def route(path: str, methods: List[str] = None):
    """Decorator for registering routes."""
    return app.route(path, methods)


def errorhandler(status_code: int):
    """Decorator for registering error handlers."""
    return app.errorhandler(status_code)