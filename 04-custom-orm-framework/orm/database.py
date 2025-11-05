"""
Database Connection and Management
This module handles database connections and operations for the ORM framework.
"""

import sqlite3
import threading
from typing import Optional, Any, List
from contextlib import contextmanager
from .exceptions import ORMException


class Database:
    """Database connection manager."""
    
    def __init__(self, database_url: str = "sqlite:///default.db"):
        self.database_url = database_url
        self.connection = None
        self._lock = threading.Lock()
        self._parse_database_url()
    
    def _parse_database_url(self):
        """Parse the database URL."""
        if self.database_url.startswith("sqlite:///"):
            self.db_type = "sqlite"
            self.db_name = self.database_url[10:]  # Remove "sqlite:///"
        else:
            raise ORMException(f"Unsupported database type: {self.database_url}")
    
    def connect(self):
        """Establish database connection."""
        with self._lock:
            if self.connection is None:
                if self.db_type == "sqlite":
                    self.connection = sqlite3.connect(self.db_name, check_same_thread=False)
                    self.connection.row_factory = sqlite3.Row  # Enable named access to columns
                else:
                    raise ORMException(f"Unsupported database type: {self.db_type}")
    
    def disconnect(self):
        """Close database connection."""
        with self._lock:
            if self.connection:
                self.connection.close()
                self.connection = None
    
    def execute(self, query: str, params: Optional[tuple] = None):
        """Execute a SQL query."""
        if self.connection is None:
            self.connect()
        
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        except Exception as e:
            self.connection.rollback()
            raise ORMException(f"Database error: {e}")
    
    def execute_many(self, query: str, params_list: List[tuple]):
        """Execute a SQL query with multiple parameter sets."""
        if self.connection is None:
            self.connect()
        
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, params_list)
            self.connection.commit()
            return cursor
        except Exception as e:
            self.connection.rollback()
            raise ORMException(f"Database error: {e}")
    
    def fetch_all(self, query: str, params: Optional[tuple] = None):
        """Fetch all rows from a query."""
        cursor = self.execute(query, params)
        return cursor.fetchall()
    
    def fetch_one(self, query: str, params: Optional[tuple] = None):
        """Fetch one row from a query."""
        cursor = self.execute(query, params)
        return cursor.fetchone()
    
    @contextmanager
    def transaction(self):
        """Context manager for database transactions."""
        if self.connection is None:
            self.connect()
        
        old_autocommit = self.connection.isolation_level
        self.connection.isolation_level = None  # Autocommit mode off
        try:
            self.execute("BEGIN")
            yield self
            self.execute("COMMIT")
        except Exception as e:
            self.execute("ROLLBACK")
            raise e
        finally:
            self.connection.isolation_level = old_autocommit
    
    def create_tables(self, models: List[Any]):
        """Create tables for the given models."""
        for model in models:
            self.create_table(model)
    
    def create_table(self, model: Any):
        """Create table for a model."""
        if not hasattr(model, '_fields'):
            raise ORMException(f"Model {model.__name__} is not a valid ORM model")
        
        table_name = model.Meta.table_name
        fields = model._fields
        
        # Build CREATE TABLE statement
        columns = []
        for field_name, field in fields.items():
            column_def = self._get_column_definition(field_name, field)
            columns.append(column_def)
        
        # Add primary key if not specified
        if 'id' not in fields:
            columns.insert(0, "id INTEGER PRIMARY KEY AUTOINCREMENT")
        
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.execute(query)
    
    def _get_column_definition(self, field_name: str, field) -> str:
        """Get SQL column definition for a field."""
        column_parts = [field_name]
        
        # Field type
        if isinstance(field, (IntegerField, AutoField, ForeignKey)):
            column_parts.append("INTEGER")
        elif isinstance(field, (FloatField,)):
            column_parts.append("REAL")
        elif isinstance(field, (BooleanField,)):
            column_parts.append("BOOLEAN")
        else:
            column_parts.append("TEXT")
        
        # Constraints
        if field.required:
            column_parts.append("NOT NULL")
        
        if field.unique:
            column_parts.append("UNIQUE")
        
        if hasattr(field, 'default') and field.default is not None:
            if isinstance(field.default, str):
                column_parts.append(f"DEFAULT '{field.default}'")
            else:
                column_parts.append(f"DEFAULT {field.default}")
        
        return " ".join(column_parts)
    
    def drop_tables(self, models: List[Any]):
        """Drop tables for the given models."""
        for model in models:
            self.drop_table(model)
    
    def drop_table(self, model: Any):
        """Drop table for a model."""
        table_name = model.Meta.table_name
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.execute(query)


# Global database instance
_default_database = None


def get_database() -> Database:
    """Get the default database instance."""
    global _default_database
    if _default_database is None:
        _default_database = Database()
    return _default_database


def set_database(database: Database):
    """Set the default database instance."""
    global _default_database
    _default_database = database