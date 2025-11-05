"""
Helper Functions
This module contains various helper functions for the web framework.
"""

import json
import hashlib
import secrets
import re
from typing import Dict, Any, Optional
from framework import HTTPResponse


def json_response(data: Dict[str, Any], status_code: int = 200) -> HTTPResponse:
    """Create a JSON response."""
    return HTTPResponse(
        body=json.dumps(data),
        status_code=status_code,
        headers={"Content-Type": "application/json"}
    )


def redirect(url: str, status_code: int = 302) -> HTTPResponse:
    """Create a redirect response."""
    return HTTPResponse(
        body="",
        status_code=status_code,
        headers={"Location": url}
    )


def generate_csrf_token() -> str:
    """Generate a CSRF token."""
    return secrets.token_urlsafe(32)


def verify_csrf_token(token: str, expected: str) -> bool:
    """Verify a CSRF token."""
    return secrets.compare_digest(token, expected)


def hash_password(password: str, salt: Optional[str] = None) -> tuple:
    """Hash a password with a salt."""
    if not salt:
        salt = secrets.token_hex(16)
    
    # Combine password and salt
    salted_password = password + salt
    
    # Hash the salted password
    hashed = hashlib.sha256(salted_password.encode()).hexdigest()
    
    return hashed, salt


def verify_password(password: str, hashed: str, salt: str) -> bool:
    """Verify a password against its hash."""
    new_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(new_hash, hashed)


def validate_email(email: str) -> bool:
    """Validate an email address."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple:
    """
    Validate a password.
    Returns (is_valid, error_message).
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, ""


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    # Convert to lowercase
    text = text.lower()
    
    # Replace spaces and special characters with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)
    
    # Remove leading and trailing hyphens
    text = text.strip('-')
    
    return text


def format_bytes(bytes_size: int) -> str:
    """Format bytes into human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size = int(bytes_size / 1024.0)
    return f"{bytes_size:.1f} PB"


def get_client_ip(request) -> str:
    """Get client IP address from request."""
    # Check for X-Forwarded-For header (load balancers/proxies)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Get the first IP in the list
        return forwarded_for.split(',')[0].strip()
    
    # Check for X-Real-IP header
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fall back to remote address (if available)
    # Note: This depends on the server implementation
    return getattr(request, 'client_ip', '127.0.0.1')


def is_ajax_request(request) -> bool:
    """Check if request is an AJAX request."""
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def get_user_agent(request) -> str:
    """Get user agent string from request."""
    return request.headers.get("User-Agent", "")


def is_mobile_user_agent(user_agent: str) -> bool:
    """Check if user agent is from a mobile device."""
    mobile_patterns = [
        r'Mobile', r'Android', r'iPhone', r'iPad', r'iPod',
        r'BlackBerry', r'Windows Phone', r'Opera Mini'
    ]
    
    for pattern in mobile_patterns:
        if re.search(pattern, user_agent, re.IGNORECASE):
            return True
    
    return False


# Convenience aliases
jsonify = json_response