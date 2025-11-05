"""
Migration System
This module provides a simple migration system for the ORM framework.
"""

import os
import json
import sqlite3
from typing import List, Dict, Any, Tuple
from orm.database import Database


class Migration:
    """Represents a single migration."""
    
    def __init__(self, name: str, operations: List[Dict[str, Any]]):
        self.name = name
        self.operations = operations
        self.applied = False


class MigrationSystem:
    """Manages database migrations."""
    
    def __init__(self, database: Database, migrations_dir: str = "migrations"):
        self.database = database
        self.migrations_dir = migrations_dir
        self.migrations: List[Migration] = []
        self._ensure_migrations_table()
    
    def _ensure_migrations_table(self):
        """Ensure the migrations table exists."""
        query = """
        CREATE TABLE IF NOT EXISTS orm_migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.database.execute(query)
    
    def create_migration(self, name: str, operations: List[Dict[str, Any]]) -> str:
        """Create a new migration file."""
        # Create migrations directory if it doesn't exist
        os.makedirs(self.migrations_dir, exist_ok=True)
        
        # Create migration file
        filename = f"{len(self.migrations) + 1:04d}_{name}.json"
        filepath = os.path.join(self.migrations_dir, filename)
        
        migration_data = {
            "name": name,
            "operations": operations
        }
        
        with open(filepath, 'w') as f:
            json.dump(migration_data, f, indent=2)
        
        # Add to migrations list
        migration = Migration(name, operations)
        self.migrations.append(migration)
        
        return filepath
    
    def load_migrations(self):
        """Load migrations from files."""
        if not os.path.exists(self.migrations_dir):
            return
        
        # Load migration files
        for filename in sorted(os.listdir(self.migrations_dir)):
            if filename.endswith('.json'):
                filepath = os.path.join(self.migrations_dir, filename)
                with open(filepath, 'r') as f:
                    migration_data = json.load(f)
                
                migration = Migration(
                    migration_data['name'],
                    migration_data['operations']
                )
                self.migrations.append(migration)
    
    def get_applied_migrations(self) -> List[str]:
        """Get list of applied migrations."""
        query = "SELECT name FROM orm_migrations ORDER BY id"
        cursor = self.database.execute(query)
        return [row[0] for row in cursor.fetchall()]
    
    def apply_migration(self, migration: Migration):
        """Apply a single migration."""
        # Start transaction
        with self.database.transaction():
            # Apply operations
            for operation in migration.operations:
                self._apply_operation(operation)
            
            # Record migration as applied
            query = "INSERT INTO orm_migrations (name) VALUES (?)"
            self.database.execute(query, (migration.name,))
        
        migration.applied = True
    
    def _apply_operation(self, operation: Dict[str, Any]):
        """Apply a single operation."""
        op_type = operation.get('type')
        
        if op_type == 'sql':
            # Execute raw SQL
            sql = operation.get('sql')
            if sql:
                self.database.execute(sql)
        elif op_type == 'create_table':
            # Create table (simplified)
            table_name = operation.get('table')
            columns = operation.get('columns', [])
            if table_name and columns:
                column_defs = []
                for col in columns:
                    col_def = f"{col['name']} {col['type']}"
                    if col.get('nullable', True) is False:
                        col_def += " NOT NULL"
                    if col.get('primary_key', False):
                        col_def += " PRIMARY KEY"
                    column_defs.append(col_def)
                
                query = f"CREATE TABLE {table_name} ({', '.join(column_defs)})"
                self.database.execute(query)
        elif op_type == 'add_column':
            # Add column to table
            table_name = operation.get('table')
            column = operation.get('column')
            if table_name and column:
                query = f"ALTER TABLE {table_name} ADD COLUMN {column['name']} {column['type']}"
                if column.get('nullable', True) is False:
                    query += " NOT NULL"
                self.database.execute(query)
    
    def migrate(self):
        """Apply all unapplied migrations."""
        # Load migrations
        self.load_migrations()
        
        # Get applied migrations
        applied = set(self.get_applied_migrations())
        
        # Apply unapplied migrations
        for migration in self.migrations:
            if migration.name not in applied:
                print(f"Applying migration: {migration.name}")
                self.apply_migration(migration)
        
        print("Migrations completed successfully")


# Convenience functions
def create_migration_system(database: Database, migrations_dir: str = "migrations") -> MigrationSystem:
    """Create a migration system."""
    return MigrationSystem(database, migrations_dir)


def run_migrations(database: Database, migrations_dir: str = "migrations"):
    """Run all pending migrations."""
    migration_system = MigrationSystem(database, migrations_dir)
    migration_system.migrate()