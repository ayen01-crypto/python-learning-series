"""
Query Building and Execution
This module defines the QuerySet class for building and executing database queries.
"""

from typing import List, Optional, Any, Dict
import sqlite3
from .database import Database
from .exceptions import DoesNotExist, MultipleObjectsReturned


class QuerySet:
    """QuerySet for building and executing database queries."""
    
    def __init__(self, model_class: Any, database: Database = None):
        self.model_class = model_class
        self.database = database
        self._filters = {}
        self._excludes = {}
        self._order_by = []
        self._limit = None
        self._offset = None
    
    def filter(self, **kwargs) -> 'QuerySet':
        """Add filter conditions to the query."""
        new_queryset = self._clone()
        new_queryset._filters.update(kwargs)
        return new_queryset
    
    def exclude(self, **kwargs) -> 'QuerySet':
        """Add exclude conditions to the query."""
        new_queryset = self._clone()
        new_queryset._excludes.update(kwargs)
        return new_queryset
    
    def order_by(self, *fields) -> 'QuerySet':
        """Add ordering to the query."""
        new_queryset = self._clone()
        new_queryset._order_by.extend(fields)
        return new_queryset
    
    def limit(self, limit: int) -> 'QuerySet':
        """Limit the number of results."""
        new_queryset = self._clone()
        new_queryset._limit = limit
        return new_queryset
    
    def offset(self, offset: int) -> 'QuerySet':
        """Offset the results."""
        new_queryset = self._clone()
        new_queryset._offset = offset
        return new_queryset
    
    def all(self) -> 'QuerySet':
        """Get all instances (default behavior)."""
        return self._clone()
    
    def get(self, **kwargs) -> Any:
        """Get a single instance."""
        if kwargs:
            queryset = self.filter(**kwargs)
        else:
            queryset = self
        
        results = queryset._fetch_results()
        
        if len(results) == 0:
            raise DoesNotExist(f"{self.model_class.__name__} matching query does not exist.")
        elif len(results) > 1:
            raise MultipleObjectsReturned(f"get() returned more than one {self.model_class.__name__} -- it returned {len(results)}!")
        
        return results[0]
    
    def first(self) -> Optional[Any]:
        """Get the first instance."""
        results = self.limit(1)._fetch_results()
        return results[0] if results else None
    
    def last(self) -> Optional[Any]:
        """Get the last instance."""
        # Order by id descending and get first
        queryset = self.order_by('-id').limit(1)
        results = queryset._fetch_results()
        return results[0] if results else None
    
    def count(self) -> int:
        """Count the number of instances."""
        table_name = self.model_class.Meta.table_name
        query = f"SELECT COUNT(*) FROM {table_name}"
        params = []
        
        # Add WHERE clause for filters
        where_clause, where_params = self._build_where_clause()
        if where_clause:
            query += f" WHERE {where_clause}"
            params.extend(where_params)
        
        cursor = self.database.execute(query, params)
        row = cursor.fetchone()
        return row[0] if row else 0
    
    def exists(self) -> bool:
        """Check if any instances exist."""
        return self.count() > 0
    
    def delete(self) -> int:
        """Delete all instances matching the query."""
        table_name = self.model_class.Meta.table_name
        query = f"DELETE FROM {table_name}"
        params = []
        
        # Add WHERE clause for filters
        where_clause, where_params = self._build_where_clause()
        if where_clause:
            query += f" WHERE {where_clause}"
            params.extend(where_params)
        
        cursor = self.database.execute(query, params)
        return cursor.rowcount
    
    def update(self, **kwargs) -> int:
        """Update all instances matching the query."""
        table_name = self.model_class.Meta.table_name
        
        # Build SET clause
        set_clause = ', '.join([f"{field} = ?" for field in kwargs.keys()])
        params = list(kwargs.values())
        
        query = f"UPDATE {table_name} SET {set_clause}"
        
        # Add WHERE clause for filters
        where_clause, where_params = self._build_where_clause()
        if where_clause:
            query += f" WHERE {where_clause}"
            params.extend(where_params)
        
        cursor = self.database.execute(query, params)
        return cursor.rowcount
    
    def _fetch_results(self) -> List[Any]:
        """Fetch results from the database."""
        table_name = self.model_class.Meta.table_name
        
        # Build SELECT query
        query = f"SELECT * FROM {table_name}"
        params = []
        
        # Add WHERE clause for filters
        where_clause, where_params = self._build_where_clause()
        if where_clause:
            query += f" WHERE {where_clause}"
            params.extend(where_params)
        
        # Add ORDER BY clause
        if self._order_by:
            order_fields = []
            for field in self._order_by:
                if field.startswith('-'):
                    order_fields.append(f"{field[1:]} DESC")
                else:
                    order_fields.append(f"{field} ASC")
            query += f" ORDER BY {', '.join(order_fields)}"
        
        # Add LIMIT and OFFSET
        if self._limit is not None:
            query += f" LIMIT {self._limit}"
            if self._offset is not None:
                query += f" OFFSET {self._offset}"
        
        # Execute query
        cursor = self.database.execute(query, params)
        rows = cursor.fetchall()
        
        # Convert rows to model instances
        instances = []
        for row in rows:
            # Convert row to dictionary
            if isinstance(row, sqlite3.Row):
                data = dict(row)
            else:
                # Get column names
                columns = [description[0] for description in cursor.description]
                data = dict(zip(columns, row))
            
            # Create model instance
            instance = self.model_class(**data)
            instance._is_saved = True
            instances.append(instance)
        
        return instances
    
    def _build_where_clause(self) -> tuple:
        """Build WHERE clause and parameters."""
        conditions = []
        params = []
        
        # Add filter conditions
        for field, value in self._filters.items():
            if '__' in field:
                field_name, lookup = field.split('__', 1)
                if lookup == 'exact':
                    conditions.append(f"{field_name} = ?")
                elif lookup == 'iexact':
                    conditions.append(f"LOWER({field_name}) = LOWER(?)")
                elif lookup == 'contains':
                    conditions.append(f"{field_name} LIKE ?")
                    params.append(f"%{value}%")
                    continue
                elif lookup == 'icontains':
                    conditions.append(f"LOWER({field_name}) LIKE LOWER(?)")
                    params.append(f"%{value}%")
                    continue
                elif lookup == 'startswith':
                    conditions.append(f"{field_name} LIKE ?")
                    params.append(f"{value}%")
                    continue
                elif lookup == 'endswith':
                    conditions.append(f"{field_name} LIKE ?")
                    params.append(f"%{value}")
                    continue
                elif lookup == 'gt':
                    conditions.append(f"{field_name} > ?")
                elif lookup == 'gte':
                    conditions.append(f"{field_name} >= ?")
                elif lookup == 'lt':
                    conditions.append(f"{field_name} < ?")
                elif lookup == 'lte':
                    conditions.append(f"{field_name} <= ?")
                elif lookup == 'in':
                    placeholders = ','.join(['?' for _ in value])
                    conditions.append(f"{field_name} IN ({placeholders})")
                    params.extend(value)
                    continue
                else:
                    conditions.append(f"{field_name} = ?")
            else:
                field_name = field
                conditions.append(f"{field_name} = ?")
            
            params.append(value)
        
        # Add exclude conditions
        for field, value in self._excludes.items():
            if '__' in field:
                field_name, lookup = field.split('__', 1)
                if lookup == 'exact':
                    conditions.append(f"{field_name} != ?")
                elif lookup == 'gt':
                    conditions.append(f"{field_name} <= ?")
                elif lookup == 'gte':
                    conditions.append(f"{field_name} < ?")
                elif lookup == 'lt':
                    conditions.append(f"{field_name} >= ?")
                elif lookup == 'lte':
                    conditions.append(f"{field_name} > ?")
                else:
                    conditions.append(f"{field_name} != ?")
            else:
                field_name = field
                conditions.append(f"{field_name} != ?")
            
            params.append(value)
        
        where_clause = ' AND '.join(conditions) if conditions else ''
        return where_clause, params
    
    def _clone(self) -> 'QuerySet':
        """Create a copy of this QuerySet."""
        clone = QuerySet(self.model_class, self.database)
        clone._filters = self._filters.copy()
        clone._excludes = self._excludes.copy()
        clone._order_by = self._order_by.copy()
        clone._limit = self._limit
        clone._offset = self._offset
        return clone
    
    def __iter__(self):
        """Make QuerySet iterable."""
        results = self._fetch_results()
        return iter(results)
    
    def __len__(self):
        """Return count of results."""
        return self.count()
    
    def __getitem__(self, key):
        """Support indexing."""
        if isinstance(key, slice):
            # Handle slicing
            queryset = self._clone()
            if key.start is not None:
                queryset = queryset.offset(key.start)
            if key.stop is not None:
                queryset = queryset.limit(key.stop - (key.start or 0))
            return queryset._fetch_results()
        else:
            # Handle single item access
            queryset = self.offset(key).limit(1)
            results = queryset._fetch_results()
            if not results:
                raise IndexError("QuerySet index out of range")
            return results[0]