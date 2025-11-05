"""
Lesson 13: Context Managers
Comprehensive Examples
"""

import time
import os
import tempfile
from contextlib import contextmanager, closing, suppress
from typing import Any, Generator


# ============================================
# 1. Basic Context Manager Protocol
# ============================================

print("=== BASIC CONTEXT MANAGER PROTOCOL ===\n")

class SimpleContextManager:
    """Simple context manager demonstrating the protocol."""
    
    def __enter__(self):
        print("Entering context")
        return "Context data"
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting context")
        if exc_type:
            print(f"Exception occurred: {exc_type.__name__}: {exc_val}")
        return False  # Don't suppress exceptions

# Using the context manager
print("Using simple context manager:")
with SimpleContextManager() as data:
    print(f"Inside context: {data}")

# With exception handling
print("\nWith exception:")
try:
    with SimpleContextManager() as data:
        print(f"Inside context: {data}")
        raise ValueError("Test exception")
except ValueError as e:
    print(f"Caught exception: {e}")


# ============================================
# 2. File Context Manager
# ============================================

print("\n" + "="*60)
print("=== FILE CONTEXT MANAGER ===\n")

class FileManager:
    """Context manager for file operations."""
    
    def __init__(self, filename: str, mode: str = 'r'):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        print(f"Opening file: {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            print(f"Closing file: {self.filename}")
            self.file.close()
        if exc_type:
            print(f"File operation error: {exc_type.__name__}: {exc_val}")
        return False

# Create a test file
with open("test.txt", "w") as f:
    f.write("Hello, Context Managers!")

# Use custom file manager
print("Using custom file manager:")
with FileManager("test.txt", "r") as f:
    content = f.read()
    print(f"File content: {content}")


# ============================================
# 3. Database Connection Context Manager
# ============================================

print("\n" + "="*60)
print("=== DATABASE CONNECTION ===\n")

class DatabaseConnection:
    """Simulated database connection context manager."""
    
    def __init__(self, host: str, port: int = 5432):
        self.host = host
        self.port = port
        self.connection = None
        self.transaction_active = False
    
    def __enter__(self):
        print(f"Connecting to database at {self.host}:{self.port}")
        self.connection = f"Connection to {self.host}"
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.transaction_active:
            if exc_type:
                print("Rolling back transaction due to error")
                self.rollback()
            else:
                print("Committing transaction")
                self.commit()
        
        print(f"Closing database connection to {self.host}")
        self.connection = None
        return False
    
    def execute(self, query: str):
        """Execute a database query."""
        if not self.connection:
            raise RuntimeError("Not connected to database")
        print(f"Executing: {query}")
        return f"Results for: {query}"
    
    def begin_transaction(self):
        """Begin a database transaction."""
        self.transaction_active = True
        print("Transaction started")
    
    def commit(self):
        """Commit the transaction."""
        self.transaction_active = False
        print("Transaction committed")
    
    def rollback(self):
        """Rollback the transaction."""
        self.transaction_active = False
        print("Transaction rolled back")

# Using database context manager
print("Using database context manager:")
with DatabaseConnection("localhost") as db:
    db.begin_transaction()
    result1 = db.execute("SELECT * FROM users")
    result2 = db.execute("UPDATE users SET name='John' WHERE id=1")
    # Transaction will be committed automatically


# ============================================
# 4. Contextlib Decorator
# ============================================

print("\n" + "="*60)
print("=== CONTEXTLIB DECORATOR ===\n")

from contextlib import contextmanager

@contextmanager
def timer_context():
    """Context manager that times execution."""
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f"Execution time: {end - start:.4f} seconds")

@contextmanager
def temporary_file(filename: str, content: str = ""):
    """Context manager for temporary files."""
    try:
        with open(filename, "w") as f:
            f.write(content)
        print(f"Created temporary file: {filename}")
        yield filename
    finally:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Removed temporary file: {filename}")

# Using timer context manager
print("Using timer context manager:")
with timer_context():
    time.sleep(0.1)
    print("Doing some work...")

# Using temporary file context manager
print("\nUsing temporary file context manager:")
with temporary_file("temp.txt", "Hello, World!") as filename:
    with open(filename, "r") as f:
        content = f.read()
        print(f"File content: {content}")


# ============================================
# 5. Advanced Context Managers
# ============================================

print("\n" + "="*60)
print("=== ADVANCED CONTEXT MANAGERS ===\n")

@contextmanager
def error_handler(*exception_types):
    """Context manager that handles specific exceptions."""
    try:
        yield
    except exception_types as e:
        print(f"Caught handled exception: {type(e).__name__}: {e}")
    except Exception as e:
        print(f"Caught unhandled exception: {type(e).__name__}: {e}")
        raise

@contextmanager
def change_directory(new_dir: str):
    """Context manager that changes directory temporarily."""
    old_dir = os.getcwd()
    try:
        os.chdir(new_dir)
        print(f"Changed to directory: {new_dir}")
        yield new_dir
    finally:
        os.chdir(old_dir)
        print(f"Returned to directory: {old_dir}")

# Using error handler
print("Using error handler:")
with error_handler(ValueError, TypeError):
    raise ValueError("This will be handled")

# Using change directory (if possible)
print("\nUsing change directory:")
try:
    with change_directory(os.path.expanduser("~")):
        print(f"Current directory: {os.getcwd()}")
except Exception as e:
    print(f"Could not change directory: {e}")


# ============================================
# 6. Contextlib Utilities
# ============================================

print("\n" + "="*60)
print("=== CONTEXTLIB UTILITIES ===\n")

# suppress - suppress specific exceptions
print("Using suppress:")
with suppress(FileNotFoundError):
    with open("nonexistent.txt", "r") as f:
        content = f.read()
    print("This won't be printed")

# closing - ensure close() is called
from urllib.request import urlopen

print("\nUsing closing:")
# Note: This is a simplified example
class MockResource:
    def __init__(self, name):
        self.name = name
    
    def close(self):
        print(f"Closing resource: {self.name}")

with closing(MockResource("test_resource")) as resource:
    print(f"Using resource: {resource.name}")


# ============================================
# 7. Nested Context Managers
# ============================================

print("\n" + "="*60)
print("=== NESTED CONTEXT MANAGERS ===\n")

# Multiple context managers
print("Multiple context managers:")
with timer_context(), temporary_file("nested.txt", "Nested test"):
    with open("nested.txt", "r") as f:
        content = f.read()
        print(f"Content: {content}")

# Context manager that manages other context managers
class ContextManagerStack:
    """Stack of context managers."""
    
    def __init__(self):
        self.managers = []
    
    def add(self, manager):
        self.managers.append(manager)
        return self
    
    def __enter__(self):
        self.entered = []
        for manager in self.managers:
            entered = manager.__enter__()
            self.entered.append((manager, entered))
        return self.entered
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Exit in reverse order
        for manager, _ in reversed(self.entered):
            manager.__exit__(exc_type, exc_val, exc_tb)
        return False

# Using context manager stack
print("\nUsing context manager stack:")
stack = ContextManagerStack()
stack.add(temporary_file("stack1.txt", "File 1"))
stack.add(temporary_file("stack2.txt", "File 2"))

with stack as files:
    for manager, filename in files:
        with open(filename, "r") as f:
            print(f"{filename}: {f.read()}")


# ============================================
# 8. Exception Handling in Context Managers
# ============================================

print("\n" + "="*60)
print("=== EXCEPTION HANDLING ===\n")

class ExceptionHandlingContext:
    """Context manager that demonstrates exception handling."""
    
    def __enter__(self):
        print("Entering context")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting context")
        if exc_type:
            print(f"Exception type: {exc_type}")
            print(f"Exception value: {exc_val}")
            print(f"Traceback: {exc_tb}")
            
            # Handle specific exceptions
            if exc_type == ValueError:
                print("Handling ValueError - suppressing it")
                return True  # Suppress the exception
            elif exc_type == TypeError:
                print("Handling TypeError - letting it propagate")
                return False  # Don't suppress
        return False

# Test exception suppression
print("Testing exception suppression:")
with ExceptionHandlingContext():
    raise ValueError("This will be suppressed")

# Test exception propagation
print("\nTesting exception propagation:")
try:
    with ExceptionHandlingContext():
        raise TypeError("This will be propagated")
except TypeError as e:
    print(f"Caught propagated exception: {e}")


# ============================================
# 9. Practical Examples
# ============================================

print("\n" + "="*60)
print("=== PRACTICAL EXAMPLES ===\n")

@contextmanager
def database_transaction(db_connection):
    """Context manager for database transactions."""
    print("Starting transaction")
    transaction_id = "TXN12345"
    try:
        yield transaction_id
        print(f"Committing transaction {transaction_id}")
    except Exception as e:
        print(f"Rolling back transaction {transaction_id} due to: {e}")
        raise

@contextmanager
def performance_monitor(operation_name: str):
    """Context manager that monitors performance."""
    start_time = time.time()
    start_memory = 0  # In real implementation, you'd measure memory
    
    print(f"Starting operation: {operation_name}")
    try:
        yield
    finally:
        end_time = time.time()
        end_memory = 0  # In real implementation, you'd measure memory
        print(f"Operation '{operation_name}' completed in {end_time - start_time:.4f} seconds")

# Using practical examples
print("Using database transaction:")
with DatabaseConnection("localhost") as db:
    with database_transaction(db) as txn_id:
        result1 = db.execute("INSERT INTO users (name) VALUES ('Alice')")
        result2 = db.execute("INSERT INTO users (name) VALUES ('Bob')")
        print(f"Transaction {txn_id} completed successfully")

print("\nUsing performance monitor:")
with performance_monitor("data_processing"):
    time.sleep(0.2)
    print("Processing data...")


# ============================================
# Practice Exercise
# ============================================

print("\n" + "="*60)
print("🎯 PRACTICE EXERCISE")
print("="*60)
print("""
Try these exercises:

1. Create a thread lock context manager
2. Build a configuration file context manager
3. Implement a retry context manager with exponential backoff
4. Make a temporary directory context manager
5. Create a logging context manager that adds context to log messages
""")

# Clean up test files
test_files = ["test.txt", "temp.txt", "nested.txt", "stack1.txt", "stack2.txt"]
for filename in test_files:
    if os.path.exists(filename):
        os.remove(filename)
        print(f"🧹 Cleaned up {filename}")
