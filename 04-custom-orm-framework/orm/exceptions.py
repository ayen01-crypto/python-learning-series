"""
Custom Exceptions
This module defines custom exceptions for the ORM framework.
"""


class ORMException(Exception):
    """Base exception for ORM-related errors."""
    pass


class ValidationError(ORMException):
    """Exception raised for validation errors."""
    pass


class DoesNotExist(ORMException):
    """Exception raised when an object does not exist."""
    pass


class MultipleObjectsReturned(ORMException):
    """Exception raised when multiple objects are returned but only one was expected."""
    pass


class DatabaseError(ORMException):
    """Exception raised for database-related errors."""
    pass


class FieldError(ORMException):
    """Exception raised for field-related errors."""
    pass


class ImproperlyConfigured(ORMException):
    """Exception raised when the ORM is improperly configured."""
    pass