"""
Mini Project: API Framework

A lightweight API framework using decorators for routing, validation, and middleware.
"""

import json
import functools
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime


# ============================================
# API Framework Core
# ============================================

class APIError(Exception):
    """Base exception for API errors."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class Request:
    """Represents an HTTP request."""
    def __init__(self, method: str, path: str, headers: Dict[str, str] = None, 
                 body: str = None, params: Dict[str, str] = None):
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.body = body
        self.params = params or {}
        self.timestamp = datetime.now()


class Response:
    """Represents an HTTP response."""
    def __init__(self, data: Any = None, status_code: int = 200, 
                 headers: Dict[str, str] = None):
        self.data = data
        self.status_code = status_code
        self.headers = headers or {"Content-Type": "application/json"}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "data": self.data,
            "status_code": self.status_code,
            "headers": self.headers,
            "timestamp": self.timestamp.isoformat()
        }


# ============================================
# Decorators
# ============================================

class APIDecorators:
    """Collection of API decorators."""
    
    @staticmethod
    def route(path: str, methods: List[str] = None):
        """Route decorator for mapping URLs to functions."""
        if methods is None:
            methods = ["GET"]
        
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            
            # Store route information
            wrapper._route = {
                "path": path,
                "methods": methods
            }
            return wrapper
        return decorator
    
    @staticmethod
    def validate_params(**param_rules):
        """Validate request parameters."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(request: Request, *args, **kwargs):
                # Validate required parameters
                for param_name, rules in param_rules.items():
                    required = rules.get("required", False)
                    param_type = rules.get("type", str)
                    
                    if required and param_name not in request.params:
                        raise APIError(f"Missing required parameter: {param_name}", 400)
                    
                    if param_name in request.params:
                        try:
                            # Convert parameter to specified type
                            converted_value = param_type(request.params[param_name])
                            request.params[param_name] = converted_value
                        except (ValueError, TypeError):
                            raise APIError(
                                f"Invalid type for parameter {param_name}. Expected {param_type.__name__}", 
                                400
                            )
                
                return func(request, *args, **kwargs)
            return wrapper
        return decorator
    
    @staticmethod
    def authenticate(required: bool = True):
        """Authentication decorator."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(request: Request, *args, **kwargs):
                if required:
                    auth_header = request.headers.get("Authorization")
                    if not auth_header or not auth_header.startswith("Bearer "):
                        raise APIError("Authentication required", 401)
                    
                    token = auth_header.split(" ")[1]
                    if token != "secret-token":
                        raise APIError("Invalid token", 401)
                
                return func(request, *args, **kwargs)
            return wrapper
        return decorator
    
    @staticmethod
    def rate_limit(max_requests: int = 100, window_seconds: int = 60):
        """Rate limiting decorator."""
        request_counts = {}
        
        def decorator(func):
            @functools.wraps(func)
            def wrapper(request: Request, *args, **kwargs):
                client_ip = request.headers.get("X-Forwarded-For", "127.0.0.1")
                current_time = datetime.now().timestamp()
                
                # Clean old entries
                expired_keys = [
                    key for key, (count, timestamp) in request_counts.items()
                    if current_time - timestamp > window_seconds
                ]
                for key in expired_keys:
                    del request_counts[key]
                
                # Check rate limit
                key = f"{client_ip}:{request.path}"
                count, last_time = request_counts.get(key, (0, current_time))
                
                if count >= max_requests:
                    raise APIError("Rate limit exceeded", 429)
                
                request_counts[key] = (count + 1, current_time)
                return func(request, *args, **kwargs)
            return wrapper
        return decorator
    
    @staticmethod
    def cache(expiry_seconds: int = 300):
        """Caching decorator."""
        cache_storage = {}
        
        def decorator(func):
            @functools.wraps(func)
            def wrapper(request: Request, *args, **kwargs):
                cache_key = f"{request.method}:{request.path}:{hash(str(request.params))}"
                current_time = datetime.now().timestamp()
                
                # Check cache
                if cache_key in cache_storage:
                    cached_data, expiry_time = cache_storage[cache_key]
                    if current_time < expiry_time:
                        return Response(cached_data, 200)
                
                # Execute function and cache result
                result = func(request, *args, **kwargs)
                if isinstance(result, Response) and result.status_code == 200:
                    expiry_time = current_time + expiry_seconds
                    cache_storage[cache_key] = (result.data, expiry_time)
                
                return result
            return wrapper
        return decorator


# ============================================
# API Router
# ============================================

class APIRouter:
    """Main API router that handles routing and middleware."""
    
    def __init__(self):
        self.routes: Dict[str, Dict[str, Callable]] = {}
        self.middleware: List[Callable] = []
        self.decorators = APIDecorators()
    
    def add_route(self, path: str, method: str, handler: Callable):
        """Add a route manually."""
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method] = handler
    
    def register_routes(self, module):
        """Automatically register routes from a module."""
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if callable(attr) and hasattr(attr, '_route'):
                route_info = attr._route
                for method in route_info['methods']:
                    self.add_route(route_info['path'], method, attr)
    
    def add_middleware(self, middleware: Callable):
        """Add middleware to the pipeline."""
        self.middleware.append(middleware)
    
    def handle_request(self, request: Request) -> Response:
        """Handle an incoming request."""
        try:
            # Find route handler
            if request.path not in self.routes:
                raise APIError("Route not found", 404)
            
            if request.method not in self.routes[request.path]:
                raise APIError("Method not allowed", 405)
            
            handler = self.routes[request.path][request.method]
            
            # Apply middleware
            for middleware in self.middleware:
                request = middleware(request)
                if not isinstance(request, Request):
                    return request  # Middleware returned a response
            
            # Execute handler
            result = handler(request)
            
            # Convert to Response if needed
            if not isinstance(result, Response):
                result = Response(result)
            
            return result
            
        except APIError as e:
            return Response({"error": e.message}, e.status_code)
        except Exception as e:
            return Response({"error": "Internal server error"}, 500)


# ============================================
# Sample API Endpoints
# ============================================

# Create global router instance
router = APIRouter()

@router.decorators.route("/users", ["GET"])
@router.decorators.authenticate(required=False)
@router.decorators.rate_limit(max_requests=1000)
@router.decorators.cache(expiry_seconds=60)
@router.decorators.validate_params(page={"type": int, "required": False, "default": 1})
def get_users(request: Request):
    """Get list of users."""
    page = request.params.get("page", 1)
    
    # Simulate database query
    users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    ]
    
    return {
        "users": users,
        "page": page,
        "total": len(users)
    }

@router.decorators.route("/users/<int:user_id>", ["GET"])
@router.decorators.authenticate()
def get_user(request: Request, user_id: int):
    """Get a specific user."""
    # Simulate database lookup
    if user_id == 1:
        return {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com",
            "created_at": "2023-01-01T00:00:00Z"
        }
    else:
        raise APIError("User not found", 404)

@router.decorators.route("/users", ["POST"])
@router.decorators.authenticate()
@router.decorators.validate_params(
    name={"type": str, "required": True},
    email={"type": str, "required": True}
)
def create_user(request: Request):
    """Create a new user."""
    name = request.params.get("name")
    email = request.params.get("email")
    
    # Simulate user creation
    new_user = {
        "id": 999,
        "name": name,
        "email": email,
        "created_at": datetime.now().isoformat()
    }
    
    return Response(new_user, 201)

@router.decorators.route("/health", ["GET"])
@router.decorators.rate_limit(max_requests=10000)  # High rate limit for health checks
def health_check(request: Request):
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


# ============================================
# Middleware
# ============================================

def logging_middleware(request: Request) -> Request:
    """Log incoming requests."""
    print(f"[{datetime.now().isoformat()}] {request.method} {request.path}")
    return request

def cors_middleware(request: Request) -> Request:
    """Add CORS headers."""
    request.headers["Access-Control-Allow-Origin"] = "*"
    return request

# Register middleware
router.add_middleware(logging_middleware)
router.add_middleware(cors_middleware)

# Register routes
router.register_routes(__import__(__name__))


# ============================================
# API Server
# ============================================

class APIServer:
    """Simple API server."""
    
    def __init__(self, router: APIRouter):
        self.router = router
    
    def serve(self, request: Request) -> Dict[str, Any]:
        """Serve a request and return JSON response."""
        response = self.router.handle_request(request)
        return response.to_dict()
    
    def get_routes(self) -> List[str]:
        """Get all registered routes."""
        routes = []
        for path, methods in self.router.routes.items():
            for method in methods:
                routes.append(f"{method} {path}")
        return sorted(routes)


# ============================================
# User Interface
# ============================================

def print_header(text: str):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70)


def print_menu():
    """Display main menu."""
    print("\n" + "-" * 70)
    print("\n📋 MAIN MENU:")
    print("1.  List Routes")
    print("2.  Make GET Request")
    print("3.  Make POST Request")
    print("4.  Health Check")
    print("5.  Test Authentication")
    print("6.  Test Rate Limiting")
    print("7.  Test Validation")
    print("8.  Load Sample Data")
    print("9.  Exit")


def list_routes_interactive(server: APIServer):
    """List all available routes."""
    print_header("🛣️  AVAILABLE ROUTES")
    
    routes = server.get_routes()
    if not routes:
        print("❌ No routes found!")
        return
    
    print(f"Found {len(routes)} route(s):\n")
    for route in routes:
        print(f"  📍 {route}")


def make_get_request_interactive(server: APIServer):
    """Make a GET request."""
    print_header("📥 GET REQUEST")
    
    path = input("Path (default: /users): ").strip() or "/users"
    
    # Build request
    request = Request("GET", path)
    
    # Add authentication if needed
    if "user" in path:
        request.headers["Authorization"] = "Bearer secret-token"
    
    # Add parameters
    params_input = input("Query parameters (key=value&key2=value2): ").strip()
    if params_input:
        params = {}
        for param in params_input.split("&"):
            if "=" in param:
                key, value = param.split("=", 1)
                params[key] = value
        request.params = params
    
    # Make request
    response = server.serve(request)
    
    print(f"\n📤 RESPONSE:")
    print(f"Status: {response['status_code']}")
    print(f"Headers: {response['headers']}")
    print(f"Data: {json.dumps(response['data'], indent=2)}")


def make_post_request_interactive(server: APIServer):
    """Make a POST request."""
    print_header("📤 POST REQUEST")
    
    path = input("Path (default: /users): ").strip() or "/users"
    
    # Build request
    request = Request("POST", path)
    request.headers["Authorization"] = "Bearer secret-token"
    
    # Add parameters
    print("Enter parameters (press Enter twice to finish):")
    params = {}
    while True:
        param_input = input("parameter=value: ").strip()
        if not param_input:
            break
        if "=" in param_input:
            key, value = param_input.split("=", 1)
            params[key] = value
    
    request.params = params
    
    # Make request
    response = server.serve(request)
    
    print(f"\n📤 RESPONSE:")
    print(f"Status: {response['status_code']}")
    print(f"Headers: {response['headers']}")
    print(f"Data: {json.dumps(response['data'], indent=2)}")


def health_check_interactive(server: APIServer):
    """Perform health check."""
    print_header("❤️  HEALTH CHECK")
    
    request = Request("GET", "/health")
    response = server.serve(request)
    
    print(f"Status: {response['status_code']}")
    print(f"Data: {json.dumps(response['data'], indent=2)}")


def test_authentication_interactive(server: APIServer):
    """Test authentication."""
    print_header("🔐 AUTHENTICATION TEST")
    
    # Test without auth (should fail for protected routes)
    print("Testing without authentication:")
    request = Request("GET", "/users/1")
    response = server.serve(request)
    print(f"Status: {response['status_code']}")
    print(f"Error: {response['data'].get('error', 'None')}")
    
    print("\nTesting with authentication:")
    request = Request("GET", "/users/1")
    request.headers["Authorization"] = "Bearer secret-token"
    response = server.serve(request)
    print(f"Status: {response['status_code']}")
    if response['status_code'] == 200:
        print(f"User data: {json.dumps(response['data'], indent=2)}")
    else:
        print(f"Error: {response['data'].get('error', 'None')}")


def test_rate_limiting_interactive(server: APIServer):
    """Test rate limiting."""
    print_header("🚦 RATE LIMITING TEST")
    
    request = Request("GET", "/health")
    
    print("Making 5 rapid requests to test rate limiting...")
    for i in range(5):
        response = server.serve(request)
        print(f"Request {i+1}: Status {response['status_code']}")
        if response['status_code'] != 200:
            print(f"  Error: {response['data'].get('error', 'None')}")
        time.sleep(0.1)  # Small delay


def test_validation_interactive(server: APIServer):
    """Test parameter validation."""
    print_header("✅ VALIDATION TEST")
    
    # Test with valid parameters
    print("Testing with valid parameters:")
    request = Request("POST", "/users")
    request.headers["Authorization"] = "Bearer secret-token"
    request.params = {"name": "Test User", "email": "test@example.com"}
    response = server.serve(request)
    print(f"Status: {response['status_code']}")
    if response['status_code'] == 201:
        print(f"Created user: {json.dumps(response['data'], indent=2)}")
    
    # Test with invalid parameters
    print("\nTesting with missing required parameters:")
    request = Request("POST", "/users")
    request.headers["Authorization"] = "Bearer secret-token"
    request.params = {"name": "Test User"}  # Missing email
    response = server.serve(request)
    print(f"Status: {response['status_code']}")
    print(f"Error: {response['data'].get('error', 'None')}")
    
    # Test with invalid parameter types
    print("\nTesting with invalid parameter types:")
    request = Request("GET", "/users")
    request.params = {"page": "invalid"}  # Should be integer
    response = server.serve(request)
    print(f"Status: {response['status_code']}")
    print(f"Error: {response['data'].get('error', 'None')}")


def load_sample_data(server: APIServer):
    """Load sample data."""
    print_header("📊 SAMPLE DATA")
    
    print("✅ API Framework is ready!")
    print("   • 4 endpoints registered")
    print("   • Authentication system")
    print("   • Rate limiting")
    print("   • Parameter validation")
    print("   • Caching")
    print("   • Middleware support")


# ============================================
# Main Application
# ============================================

def main():
    """Main application loop."""
    server = APIServer(router)
    
    print("=" * 70)
    print("🌐  API FRAMEWORK  🌐".center(70))
    print("=" * 70)
    print("Lightweight API framework using decorators!")
    
    while True:
        print_menu()
        choice = input("\nYour choice: ").strip()
        
        if choice == '1':
            list_routes_interactive(server)
        elif choice == '2':
            make_get_request_interactive(server)
        elif choice == '3':
            make_post_request_interactive(server)
        elif choice == '4':
            health_check_interactive(server)
        elif choice == '5':
            test_authentication_interactive(server)
        elif choice == '6':
            test_rate_limiting_interactive(server)
        elif choice == '7':
            test_validation_interactive(server)
        elif choice == '8':
            load_sample_data(server)
        elif choice == '9':
            print("\n👋 Thank you for using the API Framework!")
            print("=" * 70 + "\n")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    import time
    main()
