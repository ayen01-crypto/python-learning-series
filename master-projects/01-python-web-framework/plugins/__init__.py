"""
Plugins Package
This package contains built-in plugins for the web framework.
"""

from .static_files import StaticFilesPlugin
from .cors import CORSPlugin

__all__ = ['StaticFilesPlugin', 'CORSPlugin']