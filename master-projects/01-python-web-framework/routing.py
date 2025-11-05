"""
Routing System Module
This module implements the routing system for the web framework.
"""

import re
from typing import Dict, List, Callable, Optional, Any
from framework import Route


class Router:
    """Manages application routes."""

    def __init__(self):
        self.routes: List[Route] = []
        self.route_tree = {}

    def add_route(self, path: str, handler: Callable, methods: List[str] = None):
        """Add a route to the router."""
        route = Route(path, handler, methods)
        self.routes.append(route)
        self._build_route_tree(route)

    def _build_route_tree(self, route: Route):
        """Build a tree structure for efficient route matching."""
        parts = route.path.strip('/').split('/')
        current = self.route_tree
        
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Store route info at the leaf
        if '__routes__' not in current:
            current['__routes__'] = []
        current['__routes__'].append(route)

    def find_route(self, path: str, method: str) -> tuple[Optional[Callable], Dict[str, str]]:
        """Find a matching route for the given path and method."""
        # First try exact matching
        for route in self.routes:
            params = route.matches(path, method)
            if params is not None:
                return route.handler, params
        
        # If no exact match, try tree-based matching for parameterized routes
        return self._match_route_tree(path, method)

    def _match_route_tree(self, path: str, method: str) -> tuple[Optional[Callable], Dict[str, str]]:
        """Match route using tree structure."""
        parts = path.strip('/').split('/')
        current = self.route_tree
        params = {}
        
        for i, part in enumerate(parts):
            if part in current:
                current = current[part]
            else:
                # Check for parameterized segments
                found = False
                for key, subtree in current.items():
                    if key.startswith('{') and key.endswith('}'):
                        param_name = key[1:-1]
                        params[param_name] = part
                        current = subtree
                        found = True
                        break
                
                if not found:
                    return None, {}
        
        # Check if we have routes at this node
        if '__routes__' in current:
            for route in current['__routes__']:
                if method in route.methods:
                    return route.handler, params
        
        return None, {}


class URLBuilder:
    """Utility for building URLs from route patterns."""

    @staticmethod
    def build_url(route_path: str, **kwargs) -> str:
        """Build a URL by substituting parameters in the route path."""
        url = route_path
        for key, value in kwargs.items():
            url = url.replace(f'{{{key}}}', str(value))
        return url

    @staticmethod
    def build_query_string(params: Dict[str, Any]) -> str:
        """Build a query string from parameters."""
        if not params:
            return ""
        
        query_parts = []
        for key, value in params.items():
            if isinstance(value, list):
                for item in value:
                    query_parts.append(f"{key}={item}")
            else:
                query_parts.append(f"{key}={value}")
        
        return "?" + "&".join(query_parts)


class RouteGroup:
    """Group related routes together with common prefixes."""

    def __init__(self, prefix: str = "", middleware: List[Callable] = None):
        self.prefix = prefix
        self.middleware = middleware or []
        self.routes: List[Route] = []

    def route(self, path: str, methods: List[str] = None):
        """Decorator for adding routes to the group."""
        def decorator(handler: Callable):
            full_path = self.prefix + path
            route = Route(full_path, handler, methods)
            self.routes.append(route)
            return handler
        return decorator

    def get_routes(self) -> List[Route]:
        """Get all routes in the group."""
        return self.routes


# Convenience functions
def url_for(route_path: str, **kwargs) -> str:
    """Build a URL for a route."""
    return URLBuilder.build_url(route_path, **kwargs)