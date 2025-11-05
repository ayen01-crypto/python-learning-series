"""
Custom ORM Framework
This is a custom Object-Relational Mapping framework built from scratch.
"""

from .base import Model
from . import fields
from .database import Database
from .manager import Manager
from .query import QuerySet
from .exceptions import ORMException, ValidationError

__version__ = "1.0.0"
__author__ = "Python Learning Series"

__all__ = [
    "Model",
    "fields",
    "Database",
    "Manager",
    "QuerySet",
    "ORMException",
    "ValidationError"
]