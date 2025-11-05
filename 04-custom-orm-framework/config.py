"""
Configuration Module
This module handles configuration for the ORM framework.
"""

import os


class Config:
    """ORM Framework Configuration."""

    def __init__(self):
        # Database configuration
        self.DATABASE_URL = os.environ.get('ORM_DATABASE_URL', 'sqlite:///default.db')
        
        # Connection pooling
        self.CONNECTION_POOL_SIZE = int(os.environ.get('ORM_CONNECTION_POOL_SIZE', 5))
        self.CONNECTION_TIMEOUT = int(os.environ.get('ORM_CONNECTION_TIMEOUT', 30))
        
        # Query configuration
        self.DEFAULT_QUERY_LIMIT = int(os.environ.get('ORM_DEFAULT_QUERY_LIMIT', 1000))
        
        # Caching
        self.ENABLE_QUERY_CACHE = os.environ.get('ORM_ENABLE_QUERY_CACHE', 'false').lower() == 'true'
        self.QUERY_CACHE_SIZE = int(os.environ.get('ORM_QUERY_CACHE_SIZE', 100))
        
        # Logging
        self.LOG_LEVEL = os.environ.get('ORM_LOG_LEVEL', 'INFO')
        self.LOG_FILE = os.environ.get('ORM_LOG_FILE', 'orm.log')
        
        # Validation
        self.STRICT_VALIDATION = os.environ.get('ORM_STRICT_VALIDATION', 'true').lower() == 'true'
        
        # Performance
        self.BATCH_SIZE = int(os.environ.get('ORM_BATCH_SIZE', 100))


# Global configuration instance
config = Config()