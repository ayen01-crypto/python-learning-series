"""
Mini Project: Configuration Manager

A configuration management system using descriptors for validation and type checking.
"""

import json
import os
from typing import Dict, Any, Optional, Type, TypeVar
from datetime import datetime


# ============================================
# Configuration Descriptors
# ============================================

class ConfigDescriptor:
    """Base descriptor for configuration values."""
    
    def __init__(self, name: str, required: bool = False, default: Any = None):
        self.name = name
        self.required = required
        self.default = default
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj._config.get(self.name, self.default)
    
    def __set__(self, obj, value):
        if value is None and self.required:
            raise ValueError(f"Configuration '{self.name}' is required")
        validated_value = self.validate(value)
        obj._config[self.name] = validated_value
    
    def validate(self, value: Any) -> Any:
        """Validate the configuration value."""
        return value


class StringConfig(ConfigDescriptor):
    """String configuration descriptor."""
    
    def __init__(self, name: str, required: bool = False, default: str = "", 
                 min_length: int = 0, max_length: int = None):
        super().__init__(name, required, default)
        self.min_length = min_length
        self.max_length = max_length
    
    def validate(self, value: Any) -> str:
        if value is None:
            return self.default if not self.required else None
        
        if not isinstance(value, str):
            value = str(value)
        
        if len(value) < self.min_length:
            raise ValueError(f"Configuration '{self.name}' must be at least {self.min_length} characters")
        
        if self.max_length and len(value) > self.max_length:
            raise ValueError(f"Configuration '{self.name}' must be at most {self.max_length} characters")
        
        return value


class IntegerConfig(ConfigDescriptor):
    """Integer configuration descriptor."""
    
    def __init__(self, name: str, required: bool = False, default: int = 0,
                 min_value: int = None, max_value: int = None):
        super().__init__(name, required, default)
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, value: Any) -> int:
        if value is None:
            return self.default if not self.required else None
        
        try:
            int_value = int(value)
        except (ValueError, TypeError):
            raise ValueError(f"Configuration '{self.name}' must be an integer")
        
        if self.min_value is not None and int_value < self.min_value:
            raise ValueError(f"Configuration '{self.name}' must be at least {self.min_value}")
        
        if self.max_value is not None and int_value > self.max_value:
            raise ValueError(f"Configuration '{self.name}' must be at most {self.max_value}")
        
        return int_value


class BooleanConfig(ConfigDescriptor):
    """Boolean configuration descriptor."""
    
    def __init__(self, name: str, required: bool = False, default: bool = False):
        super().__init__(name, required, default)
    
    def validate(self, value: Any) -> bool:
        if value is None:
            return self.default if not self.required else None
        
        if isinstance(value, bool):
            return value
        
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        
        if isinstance(value, (int, float)):
            return bool(value)
        
        raise ValueError(f"Configuration '{self.name}' must be a boolean")


class ChoiceConfig(ConfigDescriptor):
    """Choice configuration descriptor."""
    
    def __init__(self, name: str, choices: list, required: bool = False, default: Any = None):
        super().__init__(name, required, default)
        self.choices = choices
    
    def validate(self, value: Any) -> Any:
        if value is None:
            return self.default if not self.required else None
        
        if value not in self.choices:
            raise ValueError(f"Configuration '{self.name}' must be one of {self.choices}")
        
        return value


# ============================================
# Configuration Manager
# ============================================

T = TypeVar('T', bound='ConfigManager')

class ConfigManager:
    """Base configuration manager using descriptors."""
    
    def __init__(self, config_file: str = None):
        self._config: Dict[str, Any] = {}
        self._config_file = config_file
        self._loaded_at = None
        self._modified = False
        
        # Load from file if specified
        if config_file and os.path.exists(config_file):
            self.load()
    
    def load(self, config_file: str = None):
        """Load configuration from file."""
        file_path = config_file or self._config_file
        if not file_path or not os.path.exists(file_path):
            return
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Set values through descriptors for validation
            for key, value in data.items():
                if hasattr(self.__class__, key):
                    setattr(self, key, value)
            
            self._loaded_at = datetime.now()
            self._modified = False
            print(f"✅ Configuration loaded from {file_path}")
            
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
    
    def save(self, config_file: str = None):
        """Save configuration to file."""
        file_path = config_file or self._config_file
        if not file_path:
            raise ValueError("No configuration file specified")
        
        try:
            # Get all configuration values
            config_data = {}
            for key in self._config:
                config_data[key] = self._config[key]
            
            # Add metadata
            config_data['_metadata'] = {
                'saved_at': datetime.now().isoformat(),
                'loaded_at': self._loaded_at.isoformat() if self._loaded_at else None
            }
            
            with open(file_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            self._modified = False
            print(f"✅ Configuration saved to {file_path}")
            
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")
    
    def reload(self):
        """Reload configuration from file."""
        self.load()
    
    def reset(self):
        """Reset configuration to defaults."""
        self._config.clear()
        self._modified = True
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        self._config[key] = value
        self._modified = True
    
    def validate(self) -> Dict[str, str]:
        """Validate all configuration values."""
        errors = {}
        
        # Check required fields
        for attr_name in dir(self.__class__):
            attr = getattr(self.__class__, attr_name)
            if isinstance(attr, ConfigDescriptor) and attr.required:
                if attr_name not in self._config or self._config[attr_name] is None:
                    errors[attr_name] = f"Required configuration '{attr_name}' is missing"
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self._config.copy()


# ============================================
# Sample Configuration Classes
# ============================================

class DatabaseConfig(ConfigManager):
    """Database configuration."""
    host = StringConfig("host", default="localhost")
    port = IntegerConfig("port", default=5432, min_value=1, max_value=65535)
    username = StringConfig("username", required=True, min_length=1)
    password = StringConfig("password", required=True, min_length=1)
    database = StringConfig("database", required=True, min_length=1)
    ssl_enabled = BooleanConfig("ssl_enabled", default=False)


class WebServerConfig(ConfigManager):
    """Web server configuration."""
    host = StringConfig("host", default="0.0.0.0")
    port = IntegerConfig("port", default=8000, min_value=1, max_value=65535)
    debug = BooleanConfig("debug", default=False)
    log_level = ChoiceConfig("log_level", ["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO")
    max_connections = IntegerConfig("max_connections", default=100, min_value=1)
    timeout = IntegerConfig("timeout", default=30, min_value=1)


class CacheConfig(ConfigManager):
    """Cache configuration."""
    backend = ChoiceConfig("backend", ["memory", "redis", "memcached"], default="memory")
    default_timeout = IntegerConfig("default_timeout", default=300, min_value=1)
    max_entries = IntegerConfig("max_entries", default=1000, min_value=1)
    enable_compression = BooleanConfig("enable_compression", default=True)


# ============================================
# Configuration Registry
# ============================================

class ConfigRegistry:
    """Registry for managing multiple configuration objects."""
    
    def __init__(self):
        self._configs: Dict[str, ConfigManager] = {}
    
    def register(self, name: str, config: ConfigManager):
        """Register a configuration object."""
        self._configs[name] = config
    
    def get(self, name: str) -> Optional[ConfigManager]:
        """Get a configuration object by name."""
        return self._configs.get(name)
    
    def all(self) -> Dict[str, ConfigManager]:
        """Get all registered configurations."""
        return self._configs.copy()
    
    def load_all(self):
        """Load all configurations."""
        for name, config in self._configs.items():
            try:
                config.load()
            except Exception as e:
                print(f"❌ Error loading {name} configuration: {e}")
    
    def save_all(self):
        """Save all configurations."""
        for name, config in self._configs.items():
            try:
                config.save()
            except Exception as e:
                print(f"❌ Error saving {name} configuration: {e}")
    
    def validate_all(self) -> Dict[str, Dict[str, str]]:
        """Validate all configurations."""
        results = {}
        for name, config in self._configs.items():
            errors = config.validate()
            if errors:
                results[name] = errors
        return results


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
    print("1.  Create Database Config")
    print("2.  Create Web Server Config")
    print("3.  Create Cache Config")
    print("4.  Load Configuration")
    print("5.  Save Configuration")
    print("6.  View Configuration")
    print("7.  Validate Configuration")
    print("8.  Configuration Manager Features")
    print("9.  Exit")


def create_database_config_interactive():
    """Create database configuration."""
    print_header("🔧 CREATE DATABASE CONFIG")
    
    try:
        config = DatabaseConfig()
        
        print("Database Configuration:")
        host = input("Host (default: localhost): ").strip() or "localhost"
        port = int(input("Port (default: 5432): ") or "5432")
        username = input("Username (required): ").strip()
        password = input("Password (required): ").strip()
        database = input("Database (required): ").strip()
        ssl = input("SSL enabled? (y/N): ").strip().lower() == 'y'
        
        if not username or not password or not database:
            print("❌ Username, password, and database are required!")
            return
        
        config.host = host
        config.port = port
        config.username = username
        config.password = password
        config.database = database
        config.ssl_enabled = ssl
        
        filename = input("Save to file (default: db_config.json): ").strip() or "db_config.json"
        config._config_file = filename
        config.save()
        
        print("✅ Database configuration created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating database configuration: {e}")


def create_web_server_config_interactive():
    """Create web server configuration."""
    print_header("🔧 CREATE WEB SERVER CONFIG")
    
    try:
        config = WebServerConfig()
        
        print("Web Server Configuration:")
        host = input("Host (default: 0.0.0.0): ").strip() or "0.0.0.0"
        port = int(input("Port (default: 8000): ") or "8000")
        debug = input("Debug mode? (y/N): ").strip().lower() == 'y'
        log_level = input("Log level (DEBUG/INFO/WARNING/ERROR, default: INFO): ").strip() or "INFO"
        max_conn = int(input("Max connections (default: 100): ") or "100")
        timeout = int(input("Timeout (default: 30): ") or "30")
        
        config.host = host
        config.port = port
        config.debug = debug
        config.log_level = log_level
        config.max_connections = max_conn
        config.timeout = timeout
        
        filename = input("Save to file (default: web_config.json): ").strip() or "web_config.json"
        config._config_file = filename
        config.save()
        
        print("✅ Web server configuration created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating web server configuration: {e}")


def create_cache_config_interactive():
    """Create cache configuration."""
    print_header("🔧 CREATE CACHE CONFIG")
    
    try:
        config = CacheConfig()
        
        print("Cache Configuration:")
        backend = input("Backend (memory/redis/memcached, default: memory): ").strip() or "memory"
        timeout = int(input("Default timeout (default: 300): ") or "300")
        max_entries = int(input("Max entries (default: 1000): ") or "1000")
        compression = input("Enable compression? (Y/n): ").strip().lower() != 'n'
        
        config.backend = backend
        config.default_timeout = timeout
        config.max_entries = max_entries
        config.enable_compression = compression
        
        filename = input("Save to file (default: cache_config.json): ").strip() or "cache_config.json"
        config._config_file = filename
        config.save()
        
        print("✅ Cache configuration created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating cache configuration: {e}")


def load_configuration_interactive():
    """Load configuration from file."""
    print_header("📥 LOAD CONFIGURATION")
    
    filename = input("Configuration file: ").strip()
    if not filename:
        print("❌ Filename is required!")
        return
    
    if not os.path.exists(filename):
        print("❌ File not found!")
        return
    
    try:
        # Try to determine config type from filename
        if "db" in filename.lower():
            config = DatabaseConfig(filename)
        elif "web" in filename.lower() or "server" in filename.lower():
            config = WebServerConfig(filename)
        elif "cache" in filename.lower():
            config = CacheConfig(filename)
        else:
            # Generic config
            config = ConfigManager(filename)
            config.load()
        
        print("✅ Configuration loaded successfully!")
        print(f"Configuration data: {config.to_dict()}")
        
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")


def save_configuration_interactive():
    """Save configuration to file."""
    print_header("📤 SAVE CONFIGURATION")
    
    print("This would save the current configuration to a file.")
    print("In a real implementation, you would modify config values and save them.")
    
    # Example of what saving looks like
    config = WebServerConfig()
    config.host = "127.0.0.1"
    config.port = 8080
    config.debug = True
    
    filename = "example_config.json"
    config._config_file = filename
    
    try:
        config.save()
        print(f"✅ Configuration saved to {filename}")
        
        # Show saved content
        with open(filename, 'r') as f:
            content = f.read()
        print(f"Saved content:\n{content}")
        
        # Clean up
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        print(f"❌ Error saving configuration: {e}")


def view_configuration_interactive():
    """View current configuration."""
    print_header("👁️  VIEW CONFIGURATION")
    
    print("Sample Database Configuration:")
    db_config = DatabaseConfig()
    db_config.host = "localhost"
    db_config.port = 5432
    db_config.username = "admin"
    db_config.password = "secret"
    db_config.database = "myapp"
    db_config.ssl_enabled = True
    
    config_dict = db_config.to_dict()
    print(json.dumps(config_dict, indent=2))
    
    print("\nSample Web Server Configuration:")
    web_config = WebServerConfig()
    web_config.host = "0.0.0.0"
    web_config.port = 8000
    web_config.debug = False
    web_config.log_level = "INFO"
    
    config_dict = web_config.to_dict()
    print(json.dumps(config_dict, indent=2))


def validate_configuration_interactive():
    """Validate configuration."""
    print_header("✅ VALIDATE CONFIGURATION")
    
    print("Configuration Validation Features:")
    print()
    print("🔍 Type Checking:")
    print("  • String length validation")
    print("  • Numeric range validation")
    print("  • Boolean conversion")
    print("  • Choice validation")
    print()
    print("🛡️  Required Fields:")
    print("  • Mandatory field checking")
    print("  • Default value handling")
    print("  • Error reporting")
    print()
    print("📋 Validation Process:")
    print("  1. Define configuration schema with descriptors")
    print("  2. Set configuration values")
    print("  3. Run validation to check for errors")
    print("  4. Get detailed error reports")


def configuration_manager_features_interactive():
    """Show configuration manager features."""
    print_header("⚙️  CONFIGURATION MANAGER FEATURES")
    
    print("Configuration Manager Features:")
    print()
    print("🔧 Descriptor-Based Validation:")
    print("  • Automatic type checking")
    print("  • Custom validation rules")
    print("  • Required field enforcement")
    print()
    print("💾 File Operations:")
    print("  • JSON serialization")
    print("  • File loading/saving")
    print("  • Configuration reloading")
    print()
    print("🏛️  Configuration Registry:")
    print("  • Multiple config management")
    print("  • Centralized access")
    print("  • Batch operations")
    print()
    print("🛡️  Safety Features:")
    print("  • Input validation")
    print("  • Error handling")
    print("  • Default values")
    print()
    print("⚡ Advanced Features:")
    print("  • Metadata tracking")
    print("  • Modification detection")
    print("  • Configuration inheritance")


# ============================================
# Main Application
# ============================================

def main():
    """Main application loop."""
    
    print("=" * 70)
    print("🔧  CONFIGURATION MANAGER  🔧".center(70))
    print("=" * 70)
    print("Configuration management system using descriptors!")
    
    while True:
        print_menu()
        choice = input("\nYour choice: ").strip()
        
        if choice == '1':
            create_database_config_interactive()
        elif choice == '2':
            create_web_server_config_interactive()
        elif choice == '3':
            create_cache_config_interactive()
        elif choice == '4':
            load_configuration_interactive()
        elif choice == '5':
            save_configuration_interactive()
        elif choice == '6':
            view_configuration_interactive()
        elif choice == '7':
            validate_configuration_interactive()
        elif choice == '8':
            configuration_manager_features_interactive()
        elif choice == '9':
            print("\n👋 Thank you for using the Configuration Manager!")
            print("=" * 70 + "\n")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
