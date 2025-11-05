"""
Mini Project: Resource Manager

A comprehensive resource management system using context managers for efficient resource handling.
"""

import os
import time
import threading
import tempfile
from typing import Dict, List, Any, Optional
from contextlib import contextmanager
from datetime import datetime


# ============================================
# Resource Manager Core
# ============================================

class ResourceManager:
    """Central resource management system."""
    
    def __init__(self):
        self.resources: Dict[str, Any] = {}
        self.lock = threading.RLock()
        self.resource_history: List[Dict[str, Any]] = []
    
    def register_resource(self, name: str, resource: Any) -> bool:
        """Register a resource with the manager."""
        with self.lock:
            if name in self.resources:
                return False
            self.resources[name] = resource
            self._log_action("register", name, type(resource).__name__)
            return True
    
    def get_resource(self, name: str) -> Optional[Any]:
        """Get a registered resource."""
        with self.lock:
            return self.resources.get(name)
    
    def unregister_resource(self, name: str) -> bool:
        """Unregister a resource."""
        with self.lock:
            if name in self.resources:
                resource = self.resources.pop(name)
                self._log_action("unregister", name, type(resource).__name__)
                return True
            return False
    
    def list_resources(self) -> Dict[str, str]:
        """List all registered resources."""
        with self.lock:
            return {name: type(resource).__name__ 
                   for name, resource in self.resources.items()}
    
    def _log_action(self, action: str, resource_name: str, resource_type: str):
        """Log resource management actions."""
        self.resource_history.append({
            "timestamp": datetime.now(),
            "action": action,
            "resource_name": resource_name,
            "resource_type": resource_type
        })
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get resource management history."""
        return self.resource_history.copy()


# ============================================
# Context Managers
# ============================================

@contextmanager
def managed_resource(resource_manager: ResourceManager, name: str, resource: Any):
    """Context manager for automatically managed resources."""
    try:
        # Register resource
        if not resource_manager.register_resource(name, resource):
            raise ValueError(f"Resource {name} already exists")
        
        print(f"🔄 Registered resource: {name} ({type(resource).__name__})")
        yield resource
        
    except Exception as e:
        print(f"❌ Error managing resource {name}: {e}")
        raise
    finally:
        # Always unregister
        if resource_manager.unregister_resource(name):
            print(f"✅ Unregistered resource: {name}")


@contextmanager
def temporary_directory(prefix: str = "temp_"):
    """Context manager for temporary directories."""
    temp_dir = tempfile.mkdtemp(prefix=prefix)
    try:
        print(f"📁 Created temporary directory: {temp_dir}")
        yield temp_dir
    finally:
        # Clean up directory
        import shutil
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"🗑️  Removed temporary directory: {temp_dir}")


@contextmanager
def file_lock(filename: str, timeout: float = 10.0):
    """Context manager for file-based locking."""
    lock_file = filename + ".lock"
    start_time = time.time()
    
    # Wait for lock
    while os.path.exists(lock_file):
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Could not acquire lock for {filename}")
        time.sleep(0.1)
    
    try:
        # Create lock file
        with open(lock_file, "w") as f:
            f.write(str(os.getpid()))
        print(f"🔒 Acquired lock for {filename}")
        
        yield filename
        
    finally:
        # Release lock
        if os.path.exists(lock_file):
            os.remove(lock_file)
            print(f"🔓 Released lock for {filename}")


@contextmanager
def performance_monitor(operation_name: str):
    """Context manager for performance monitoring."""
    start_time = time.time()
    start_memory = 0  # In real implementation, measure actual memory
    
    print(f"🚀 Starting operation: {operation_name}")
    try:
        yield
    finally:
        end_time = time.time()
        end_memory = 0  # In real implementation, measure actual memory
        duration = end_time - start_time
        
        print(f"✅ Operation '{operation_name}' completed")
        print(f"   Duration: {duration:.4f} seconds")
        print(f"   Memory change: {end_memory - start_memory} bytes")


@contextmanager
def retry_context(max_attempts: int = 3, delay: float = 1.0):
    """Context manager for retrying operations."""
    for attempt in range(max_attempts):
        try:
            print(f"🔄 Attempt {attempt + 1}/{max_attempts}")
            yield attempt + 1
            break  # Success, exit loop
        except Exception as e:
            if attempt == max_attempts - 1:  # Last attempt
                print(f"❌ All {max_attempts} attempts failed")
                raise
            else:
                print(f"⚠️  Attempt {attempt + 1} failed: {e}")
                print(f"   Waiting {delay} seconds before retry...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff


@contextmanager
def environment_variable(name: str, value: str):
    """Context manager for temporarily setting environment variables."""
    old_value = os.environ.get(name)
    os.environ[name] = value
    try:
        print(f"🔧 Set environment variable: {name}={value}")
        yield
    finally:
        if old_value is not None:
            os.environ[name] = old_value
            print(f"↩️  Restored environment variable: {name}={old_value}")
        else:
            os.environ.pop(name, None)
            print(f"↩️  Removed environment variable: {name}")


# ============================================
# Sample Resources
# ============================================

class DatabaseConnection:
    """Simulated database connection."""
    
    def __init__(self, host: str, port: int = 5432):
        self.host = host
        self.port = port
        self.connected = False
        self.connection_id = f"DB_{id(self)}"
    
    def connect(self):
        """Connect to database."""
        print(f"🔌 Connecting to database {self.host}:{self.port}")
        time.sleep(0.1)  # Simulate connection time
        self.connected = True
        return self
    
    def disconnect(self):
        """Disconnect from database."""
        if self.connected:
            print(f"🔌 Disconnecting from database {self.host}:{self.port}")
            self.connected = False
    
    def execute(self, query: str):
        """Execute a query."""
        if not self.connected:
            raise RuntimeError("Not connected to database")
        print(f"📊 Executing query: {query}")
        time.sleep(0.05)  # Simulate query time
        return f"Results for: {query}"
    
    def __enter__(self):
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


class FileHandler:
    """File handling resource."""
    
    def __init__(self, filename: str, mode: str = "r"):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def open(self):
        """Open file."""
        print(f"📂 Opening file: {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def close(self):
        """Close file."""
        if self.file:
            print(f"📂 Closing file: {self.filename}")
            self.file.close()
            self.file = None
    
    def __enter__(self):
        return self.open()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class NetworkConnection:
    """Simulated network connection."""
    
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connected = False
    
    def connect(self):
        """Connect to network resource."""
        print(f"🌐 Connecting to {self.host}:{self.port}")
        time.sleep(0.1)  # Simulate connection time
        self.connected = True
        return self
    
    def disconnect(self):
        """Disconnect from network resource."""
        if self.connected:
            print(f"🌐 Disconnecting from {self.host}:{self.port}")
            self.connected = False
    
    def send(self, data: str):
        """Send data."""
        if not self.connected:
            raise RuntimeError("Not connected")
        print(f"📤 Sending data: {data}")
        time.sleep(0.05)  # Simulate network delay
        return f"ACK: {data}"
    
    def __enter__(self):
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


# ============================================
# User Interface
# ============================================

def print_header(text: str):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70)


def print_menu():
    """Display main menu."""
    print("\n" + "-" * 70)
    print("\n📋 MAIN MENU:")
    print("1.  Register/Unregister Resources")
    print("2.  Managed Resource Context")
    print("3.  Temporary Directory")
    print("4.  File Locking")
    print("5.  Performance Monitoring")
    print("6.  Retry Context")
    print("7.  Environment Variables")
    print("8.  View Resource History")
    print("9.  Exit")


def register_resources_interactive(resource_manager: ResourceManager):
    """Register/unregister resources interactively."""
    print_header("🔄 RESOURCE REGISTRATION")
    
    while True:
        print("\nOptions:")
        print("1. Register resource")
        print("2. Unregister resource")
        print("3. List resources")
        print("4. Back to main menu")
        
        choice = input("Select option: ").strip()
        
        if choice == '1':
            name = input("Resource name: ").strip()
            resource_type = input("Resource type (db/network/file): ").strip()
            
            if resource_type == "db":
                host = input("Database host: ").strip() or "localhost"
                resource = DatabaseConnection(host)
            elif resource_type == "network":
                host = input("Network host: ").strip() or "localhost"
                port = int(input("Port (default 8080): ") or "8080")
                resource = NetworkConnection(host, port)
            elif resource_type == "file":
                filename = input("Filename: ").strip() or "test.txt"
                mode = input("Mode (default r): ").strip() or "r"
                resource = FileHandler(filename, mode)
            else:
                print("❌ Invalid resource type!")
                continue
            
            if resource_manager.register_resource(name, resource):
                print(f"✅ Registered {name}")
            else:
                print(f"❌ Resource {name} already exists!")
        
        elif choice == '2':
            name = input("Resource name to unregister: ").strip()
            if resource_manager.unregister_resource(name):
                print(f"✅ Unregistered {name}")
            else:
                print(f"❌ Resource {name} not found!")
        
        elif choice == '3':
            resources = resource_manager.list_resources()
            if resources:
                print("\n📋 Registered Resources:")
                for name, type_name in resources.items():
                    print(f"  • {name}: {type_name}")
            else:
                print("❌ No resources registered!")
        
        elif choice == '4':
            break
        
        else:
            print("❌ Invalid choice!")


def managed_resource_context_interactive(resource_manager: ResourceManager):
    """Demonstrate managed resource context."""
    print_header("🔄 MANAGED RESOURCE CONTEXT")
    
    print("Creating database connection with automatic management...")
    
    try:
        with managed_resource(resource_manager, "my_database", DatabaseConnection("localhost")) as db:
            db.connect()
            result = db.execute("SELECT * FROM users")
            print(f"Query result: {result}")
            
            # Simulate some work
            time.sleep(0.2)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n✅ Resource automatically unregistered!")


def temporary_directory_interactive():
    """Demonstrate temporary directory context."""
    print_header("📁 TEMPORARY DIRECTORY")
    
    try:
        with temporary_directory("demo_") as temp_dir:
            print(f"Working in: {temp_dir}")
            
            # Create some files
            test_file = os.path.join(temp_dir, "test.txt")
            with open(test_file, "w") as f:
                f.write("Hello, temporary directory!")
            
            # Read the file
            with open(test_file, "r") as f:
                content = f.read()
                print(f"File content: {content}")
            
            # List directory contents
            files = os.listdir(temp_dir)
            print(f"Directory contents: {files}")
            
            # Simulate some work
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("✅ Temporary directory automatically cleaned up!")


def file_locking_interactive():
    """Demonstrate file locking context."""
    print_header("🔒 FILE LOCKING")
    
    # Create test file
    test_file = "locked_file.txt"
    with open(test_file, "w") as f:
        f.write("This file will be locked!")
    
    print("Testing file locking...")
    
    try:
        with file_lock(test_file) as locked_file:
            print(f"✅ Acquired lock for {locked_file}")
            
            # Simulate file operations
            with open(locked_file, "a") as f:
                f.write("\nLocked and modified!")
            
            print("Performing operations...")
            time.sleep(2)
            
    except TimeoutError as e:
        print(f"❌ Timeout: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"🧹 Cleaned up {test_file}")


def performance_monitor_interactive():
    """Demonstrate performance monitoring context."""
    print_header("🚀 PERFORMANCE MONITORING")
    
    try:
        with performance_monitor("data_processing_operation"):
            # Simulate some work
            print("Processing data...")
            time.sleep(1)
            
            # More work
            print("Analyzing results...")
            time.sleep(0.5)
            
            print("Generating report...")
            time.sleep(0.3)
            
    except Exception as e:
        print(f"❌ Error: {e}")


def retry_context_interactive():
    """Demonstrate retry context."""
    print_header("🔄 RETRY CONTEXT")
    
    # Counter for simulating failures
    attempt_counter = 0
    
    def unreliable_operation():
        """Operation that fails a few times then succeeds."""
        global attempt_counter
        attempt_counter += 1
        
        if attempt_counter <= 2:
            raise ConnectionError(f"Connection failed on attempt {attempt_counter}")
        
        return f"Success on attempt {attempt_counter}"
    
    try:
        with retry_context(max_attempts=5, delay=0.5) as attempt:
            result = unreliable_operation()
            print(f"✅ Operation succeeded: {result}")
            
    except Exception as e:
        print(f"❌ All attempts failed: {e}")


def environment_variables_interactive():
    """Demonstrate environment variable context."""
    print_header("🔧 ENVIRONMENT VARIABLES")
    
    var_name = "TEST_VARIABLE"
    new_value = "test_value_123"
    
    print(f"Current value of {var_name}: {os.environ.get(var_name, 'Not set')}")
    
    try:
        with environment_variable(var_name, new_value):
            print(f"New value of {var_name}: {os.environ.get(var_name)}")
            
            # Simulate some work that uses the environment variable
            print("Performing operations with new environment...")
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"Restored value of {var_name}: {os.environ.get(var_name, 'Not set')}")


def view_resource_history_interactive(resource_manager: ResourceManager):
    """View resource management history."""
    print_header("📜 RESOURCE HISTORY")
    
    history = resource_manager.get_history()
    
    if not history:
        print("❌ No resource history available!")
        return
    
    print(f"Found {len(history)} historical events:\n")
    
    for event in history:
        timestamp = event["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        print(f"  {timestamp} - {event['action'].upper()}: {event['resource_name']} ({event['resource_type']})")


# ============================================
# Main Application
# ============================================

def main():
    """Main application loop."""
    resource_manager = ResourceManager()
    
    print("=" * 70)
    print("🔄  RESOURCE MANAGER  🔄".center(70))
    print("=" * 70)
    print("Comprehensive resource management system using context managers!")
    
    while True:
        print_menu()
        choice = input("\nYour choice: ").strip()
        
        if choice == '1':
            register_resources_interactive(resource_manager)
        elif choice == '2':
            managed_resource_context_interactive(resource_manager)
        elif choice == '3':
            temporary_directory_interactive()
        elif choice == '4':
            file_locking_interactive()
        elif choice == '5':
            performance_monitor_interactive()
        elif choice == '6':
            retry_context_interactive()
        elif choice == '7':
            environment_variables_interactive()
        elif choice == '8':
            view_resource_history_interactive(resource_manager)
        elif choice == '9':
            print("\n👋 Thank you for using the Resource Manager!")
            print("=" * 70 + "\n")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
