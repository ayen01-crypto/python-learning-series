"""
Framework Tests
This module contains tests for the web framework components.
"""

import unittest
import sys
import os

# Add the framework to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from framework import HTTPRequest, HTTPResponse, Route, Application
from http import HTTPMethods
from templating import Template


class TestHTTPRequest(unittest.TestCase):
    """Test HTTPRequest class."""

    def test_request_creation(self):
        """Test creating an HTTP request."""
        request = HTTPRequest(
            method=HTTPMethods.GET,
            path="/test",
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(request.method, HTTPMethods.GET)
        self.assertEqual(request.path, "/test")
        self.assertEqual(request.headers["Content-Type"], "application/json")
        self.assertEqual(request.body, "")


class TestHTTPResponse(unittest.TestCase):
    """Test HTTPResponse class."""

    def test_response_creation(self):
        """Test creating an HTTP response."""
        response = HTTPResponse(
            body="Hello, World!",
            status_code=200,
            headers={"Content-Type": "text/plain"}
        )
        
        self.assertEqual(response.body, "Hello, World!")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/plain")


class TestRoute(unittest.TestCase):
    """Test Route class."""

    def test_route_matching(self):
        """Test route matching."""
        def handler(request):
            return "OK"
        
        route = Route("/users/{user_id}", handler, [HTTPMethods.GET])
        
        # Test exact match
        params = route.matches("/users/123", HTTPMethods.GET)
        self.assertIsNotNone(params)
        self.assertEqual(params["user_id"], "123")
        
        # Test method mismatch
        params = route.matches("/users/123", HTTPMethods.POST)
        self.assertIsNone(params)
        
        # Test path mismatch
        params = route.matches("/users", HTTPMethods.GET)
        self.assertIsNone(params)


class TestTemplate(unittest.TestCase):
    """Test Template class."""

    def test_template_rendering(self):
        """Test template rendering."""
        template_str = "Hello, {{ name }}!"
        template = Template(template_str)
        
        result = template.render({"name": "World"})
        self.assertEqual(result, "Hello, World!")


class TestApplication(unittest.TestCase):
    """Test Application class."""

    def test_singleton_pattern(self):
        """Test that Application follows singleton pattern."""
        app1 = Application()
        app2 = Application()
        
        self.assertIs(app1, app2)

    def test_route_registration(self):
        """Test route registration."""
        app = Application()
        
        def handler(request):
            return "OK"
        
        app.add_route("/test", handler, [HTTPMethods.GET])
        
        self.assertEqual(len(app.routes), 1)
        self.assertEqual(app.routes[0].path, "/test")


if __name__ == "__main__":
    unittest.main()