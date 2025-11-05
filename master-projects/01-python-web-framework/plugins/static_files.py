"""
Static Files Plugin
This plugin serves static files like CSS, JavaScript, and images.
"""

import os
import mimetypes
from typing import Optional
from framework import Middleware, HTTPRequest, HTTPResponse


class StaticFilesPlugin(Middleware):
    """Middleware for serving static files."""

    def __init__(self, static_dir: str = "static", url_prefix: str = "/static/"):
        self.static_dir = static_dir
        self.url_prefix = url_prefix
        # Ensure static directory exists
        os.makedirs(static_dir, exist_ok=True)

    def process_request(self, request: HTTPRequest) -> Optional[HTTPResponse]:
        """Serve static files if the request matches."""
        if not request.path.startswith(self.url_prefix):
            return None

        # Extract file path
        file_path = request.path[len(self.url_prefix):]
        full_path = os.path.join(self.static_dir, file_path)

        # Security check: prevent directory traversal
        if ".." in file_path:
            return HTTPResponse("Forbidden", status_code=403)

        # Check if file exists
        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            return None  # Let the main app handle 404

        # Determine content type
        content_type, _ = mimetypes.guess_type(full_path)
        if not content_type:
            content_type = "application/octet-stream"

        # Read and serve file
        try:
            with open(full_path, 'rb') as f:
                content = f.read()
            
            # Convert bytes to string for text files, keep as bytes for binary files
            if content_type.startswith('text/'):
                body_content = content.decode('utf-8')
            else:
                # For binary files, we need to handle this differently
                # In a real implementation, we'd need to modify HTTPResponse to handle bytes
                body_content = content.decode('utf-8', errors='ignore')  # Simplified for this example
            
            return HTTPResponse(
                body=body_content,
                headers={"Content-Type": content_type}
            )
        except Exception as e:
            return HTTPResponse(f"Error reading file: {str(e)}", status_code=500)


# Convenience function
def setup_static_files(app, static_dir: str = "static", url_prefix: str = "/static/"):
    """Setup static files middleware."""
    static_middleware = StaticFilesPlugin(static_dir, url_prefix)
    app.add_middleware(static_middleware)