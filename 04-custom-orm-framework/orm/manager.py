"""
Model Manager
This module defines the Manager class for handling model operations.
"""

from typing import List, Optional, Any
from .query import QuerySet
from .database import Database
from .exceptions import ORMException


class Manager:
    """Manager for model operations."""
    
    def __init__(self, model_class: Any):
        self.model_class = model_class
        self.database = None
    
    def set_database(self, database: Database):
        """Set the database connection."""
        self.database = database
        # Also set it on the model class
        self.model_class.set_database(database)
    
    def get_queryset(self) -> QuerySet:
        """Get a QuerySet for this model."""
        if self.database is None:
            # Try to get database from model class
            self.database = getattr(self.model_class, '_database', None)
            if self.database is None:
                raise ORMException("No database connection available")
        return QuerySet(self.model_class, self.database)
    
    def all(self) -> QuerySet:
        """Get all instances of the model."""
        return self.get_queryset().all()
    
    def filter(self, **kwargs) -> QuerySet:
        """Filter instances of the model."""
        return self.get_queryset().filter(**kwargs)
    
    def exclude(self, **kwargs) -> QuerySet:
        """Exclude instances of the model."""
        return self.get_queryset().exclude(**kwargs)
    
    def get(self, **kwargs) -> Any:
        """Get a single instance of the model."""
        return self.get_queryset().get(**kwargs)
    
    def first(self) -> Optional[Any]:
        """Get the first instance of the model."""
        return self.get_queryset().first()
    
    def last(self) -> Optional[Any]:
        """Get the last instance of the model."""
        return self.get_queryset().last()
    
    def count(self) -> int:
        """Count instances of the model."""
        return self.get_queryset().count()
    
    def exists(self) -> bool:
        """Check if any instances of the model exist."""
        return self.get_queryset().exists()
    
    def create(self, **kwargs) -> Any:
        """Create and save a new instance of the model."""
        instance = self.model_class(**kwargs)
        instance.save(self.database)
        return instance
    
    def bulk_create(self, instances: List[Any]) -> List[Any]:
        """Create multiple instances of the model."""
        if not instances:
            return []
        
        # For simplicity, we'll save each instance individually
        # In a real implementation, you'd use bulk insert
        for instance in instances:
            instance.save(self.database)
        
        return instances
    
    def delete(self, **kwargs) -> int:
        """Delete instances of the model."""
        queryset = self.get_queryset().filter(**kwargs)
        count = queryset.count()
        queryset.delete()
        return count
    
    def update(self, **kwargs) -> int:
        """Update instances of the model."""
        queryset = self.get_queryset()
        return queryset.update(**kwargs)


# Convenience function
def create_manager(model_class: Any) -> Manager:
    """Create a manager for a model class."""
    return Manager(model_class)