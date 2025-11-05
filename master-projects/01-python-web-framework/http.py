"""
HTTP Components Module
This module provides HTTP-related utilities and constants for the web framework.
"""

from enum import Enum
from typing import Dict, Any


class HTTPStatus(Enum):
    """HTTP status codes."""
    OK = (200, "OK")
    CREATED = (201, "Created")
    ACCEPTED = (202, "Accepted")
    NO_CONTENT = (204, "No Content")
    MOVED_PERMANENTLY = (301, "Moved Permanently")
    FOUND = (302, "Found")
    NOT_MODIFIED = (304, "Not Modified")
    BAD_REQUEST = (400, "Bad Request")
    UNAUTHORIZED = (401, "Unauthorized")
    FORBIDDEN = (403, "Forbidden")
    NOT_FOUND = (404, "Not Found")
    METHOD_NOT_ALLOWED = (405, "Method Not Allowed")
    INTERNAL_SERVER_ERROR = (500, "Internal Server Error")
    NOT_IMPLEMENTED = (501, "Not Implemented")
    BAD_GATEWAY = (502, "Bad Gateway")
    SERVICE_UNAVAILABLE = (503, "Service Unavailable")


class HTTPHeaders:
    """Common HTTP headers."""
    CONTENT_TYPE = "Content-Type"
    CONTENT_LENGTH = "Content-Length"
    USER_AGENT = "User-Agent"
    ACCEPT = "Accept"
    AUTHORIZATION = "Authorization"
    COOKIE = "Cookie"
    SET_COOKIE = "Set-Cookie"
    LOCATION = "Location"
    CACHE_CONTROL = "Cache-Control"
    ETAG = "ETag"
    LAST_MODIFIED = "Last-Modified"


class HTTPMethods:
    """HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class Cookie:
    """Represents an HTTP cookie."""

    def __init__(self, name: str, value: str, **kwargs):
        self.name = name
        self.value = value
        self.expires = kwargs.get('expires')
        self.max_age = kwargs.get('max_age')
        self.domain = kwargs.get('domain')
        self.path = kwargs.get('path', '/')
        self.secure = kwargs.get('secure', False)
        self.http_only = kwargs.get('http_only', False)

    def to_header_string(self) -> str:
        """Convert cookie to HTTP header string."""
        cookie_str = f"{self.name}={self.value}"
        
        if self.expires:
            cookie_str += f"; Expires={self.expires}"
        if self.max_age:
            cookie_str += f"; Max-Age={self.max_age}"
        if self.domain:
            cookie_str += f"; Domain={self.domain}"
        if self.path:
            cookie_str += f"; Path={self.path}"
        if self.secure:
            cookie_str += "; Secure"
        if self.http_only:
            cookie_str += "; HttpOnly"
            
        return cookie_str


class HTTPParser:
    """Utility class for parsing HTTP requests and responses."""

    @staticmethod
    def parse_request_line(request_line: str) -> tuple:
        """Parse an HTTP request line."""
        parts = request_line.strip().split()
        if len(parts) != 3:
            raise ValueError("Invalid request line")
        return parts[0], parts[1], parts[2]  # method, path, version

    @staticmethod
    def parse_headers(header_lines: list) -> Dict[str, str]:
        """Parse HTTP headers."""
        headers = {}
        for line in header_lines:
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
        return headers

    @staticmethod
    def parse_cookies(cookie_header: str) -> Dict[str, str]:
        """Parse cookies from Cookie header."""
        cookies = {}
        if cookie_header:
            cookie_pairs = cookie_header.split(';')
            for pair in cookie_pairs:
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    cookies[key.strip()] = value.strip()
        return cookies


class MIMEType:
    """Common MIME types."""
    TEXT_HTML = "text/html"
    TEXT_PLAIN = "text/plain"
    TEXT_CSS = "text/css"
    APPLICATION_JSON = "application/json"
    APPLICATION_XML = "application/xml"
    APPLICATION_JAVASCRIPT = "application/javascript"
    IMAGE_PNG = "image/png"
    IMAGE_JPEG = "image/jpeg"
    IMAGE_GIF = "image/gif"


# Common HTTP status messages
STATUS_MESSAGES = {
    200: "OK",
    201: "Created",
    202: "Accepted",
    204: "No Content",
    301: "Moved Permanently",
    302: "Found",
    304: "Not Modified",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
}