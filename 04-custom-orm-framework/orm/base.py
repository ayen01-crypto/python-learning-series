"""
Base Model Class
This module defines the base Model class and its metaclass for the ORM framework.
"""

import sqlite3
import json
from typing import Dict, Any, Optional, List
from .manager import Manager
from .fields import Field
from .database import Database
from .exceptions import ValidationError


class ModelMeta(type):
    """Metaclass for Model classes."""
    
    def __new__(cls, name, bases, attrs):
        # Skip for the base Model class
        if name == 'Model':
            return super().__new__(cls, name, bases, attrs)
        
        # Collect fields
        fields = {}
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                fields[key] = value
                attrs.pop(key)
        
        # Create the class
        new_class = super().__new__(cls, name, bases, attrs)
        
        # Add fields to the class
        new_class._fields = fields
        
        # Create default manager
        if not hasattr(new_class, 'objects'):
            new_class.objects = Manager(new_class)
        
        # Set table name
        if not hasattr(new_class, 'Meta'):
            class Meta:
                table_name = name.lower()
            new_class.Meta = Meta
        elif not hasattr(new_class.Meta, 'table_name'):
            new_class.Meta.table_name = name.lower()
        
        return new_class


class Model(metaclass=ModelMeta):
    """Base class for all ORM models."""
    
    def __init__(self, **kwargs):
        # Set field values
        for field_name, field in self._fields.items():
            if field_name in kwargs:
                setattr(self, field_name, kwargs[field_name])
            else:
                setattr(self, field_name, field.default)
        
        # Set non-field attributes
        for key, value in kwargs.items():
            if key not in self._fields:
                setattr(self, key, value)
        
        self._is_saved = False
    
    def __setattr__(self, name, value):
        # Validate field values
        if name in getattr(self, '_fields', {}):
            field = self._fields[name]
            try:
                validated_value = field.validate(value)
                super().__setattr__(name, validated_value)
            except ValidationError as e:
                raise ValidationError(f"Invalid value for field '{name}': {e}")
        else:
            super().__setattr__(name, value)
    
    def __repr__(self):
        attrs = []
        for field_name in self._fields:
            if hasattr(self, field_name):
                attrs.append(f"{field_name}={getattr(self, field_name)!r}")
        return f"<{self.__class__.__name__}({', '.join(attrs)})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary."""
        data = {}
        for field_name in self._fields:
            if hasattr(self, field_name):
                data[field_name] = getattr(self, field_name)
        return data
    
    def save(self, db: Database = None):
        """Save the model instance to the database."""
        if db is None:
            # Try to get database from manager
            db = getattr(self.__class__, '_database', None)
            if db is None:
                raise ValueError("No database connection provided")
        
        # Validate all fields
        self.full_clean()
        
        # Prepare data for saving
        data = self.to_dict()
        table_name = self.Meta.table_name
        
        if self._is_saved:
            # Update existing record
            set_clause = ', '.join([f"{field} = ?" for field in data.keys() if field != 'id'])
            values = [data[field] for field in data.keys() if field != 'id']
            if 'id' in data:
                values.append(data['id'])
                query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
            else:
                query = f"UPDATE {table_name} SET {set_clause}"
        else:
            # Insert new record
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            values = list(data.values())
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # Execute query
        cursor = db.execute(query, values)
        
        # Set ID if it's an insert operation
        if not self._is_saved and hasattr(self, '_fields') and 'id' in self._fields:
            if not hasattr(self, 'id') or self.id is None:
                self.id = cursor.lastrowid
        
        self._is_saved = True
        return self
    
    def delete(self, db: Database = None):
        """Delete the model instance from the database."""
        if db is None:
            db = getattr(self.__class__, '_database', None)
            if db is None:
                raise ValueError("No database connection provided")
        
        if not self._is_saved or not hasattr(self, 'id'):
            raise ValueError("Cannot delete unsaved instance")
        
        table_name = self.Meta.table_name
        query = f"DELETE FROM {table_name} WHERE id = ?"
        db.execute(query, [self.id])
        self._is_saved = False
    
    def refresh(self, db: Database = None):
        """Refresh the model instance from the database."""
        if db is None:
            db = getattr(self.__class__, '_database', None)
            if db is None:
                raise ValueError("No database connection provided")
        
        if not self._is_saved or not hasattr(self, 'id'):
            raise ValueError("Cannot refresh unsaved instance")
        
        table_name = self.Meta.table_name
        query = f"SELECT * FROM {table_name} WHERE id = ?"
        cursor = db.execute(query, [self.id])
        row = cursor.fetchone()
        
        if row:
            # Update instance with database values
            for field_name, value in zip([description[0] for description in cursor.description], row):
                if field_name in self._fields:
                    setattr(self, field_name, value)
        
        return self
    
    def full_clean(self):
        """Validate all fields."""
        for field_name, field in self._fields.items():
            if hasattr(self, field_name):
                value = getattr(self, field_name)
                field.validate(value)
    
    @classmethod
    def set_database(cls, db: Database):
        """Set the database connection for this model."""
        cls._database = db