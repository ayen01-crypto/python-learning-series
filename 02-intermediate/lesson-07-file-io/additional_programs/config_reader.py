#!/usr/bin/env python3
"""
Configuration File Reader
A program that demonstrates reading and writing configuration files in different formats.
"""

import json
import csv
import os
from typing import Dict, Any


def create_sample_config():
    """Create sample configuration files."""
    # Sample JSON config
    json_config = {
        "app_name": "MyApplication",
        "version": "1.0.0",
        "debug": True,
        "database": {
            "host": "localhost",
            "port": 5432,
            "username": "admin",
            "password": "secret123"
        },
        "features": {
            "enable_logging": True,
            "max_connections": 100,
            "timeout": 30
        }
    }
    
    with open("config.json", "w") as f:
        json.dump(json_config, f, indent=2)
    
    # Sample CSV config
    csv_data = [
        ["setting", "value", "type"],
        ["app_name", "MyApplication", "string"],
        ["version", "1.0.0", "string"],
        ["debug", "true", "boolean"],
        ["max_users", "1000", "integer"],
        ["refresh_rate", "5.5", "float"]
    ]
    
    with open("settings.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
    
    print("Sample configuration files created:")
    print("  - config.json")
    print("  - settings.csv")


def read_json_config(filename: str) -> Dict[str, Any]:
    """
    Read and parse JSON configuration file.
    
    Args:
        filename (str): Path to JSON config file
        
    Returns:
        dict: Configuration data
    """
    if not os.path.exists(filename):
        print(f"Error: Configuration file '{filename}' not found.")
        return {}
    
    try:
        with open(filename, 'r') as file:
            config = json.load(file)
        print(f"✅ Successfully loaded JSON config from '{filename}'")
        return config
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return {}
    except Exception as e:
        print(f"❌ Error reading config file: {e}")
        return {}


def read_csv_config(filename: str) -> Dict[str, Any]:
    """
    Read and parse CSV configuration file.
    
    Args:
        filename (str): Path to CSV config file
        
    Returns:
        dict: Configuration data
    """
    if not os.path.exists(filename):
        print(f"Error: Configuration file '{filename}' not found.")
        return {}
    
    config = {}
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                setting = row['setting']
                value = row['value']
                type_hint = row.get('type', 'string')
                
                # Convert value based on type hint
                if type_hint == 'integer':
                    config[setting] = int(value)
                elif type_hint == 'float':
                    config[setting] = float(value)
                elif type_hint == 'boolean':
                    config[setting] = value.lower() in ('true', '1', 'yes', 'on')
                else:
                    config[setting] = value
        
        print(f"✅ Successfully loaded CSV config from '{filename}'")
        return config
    except Exception as e:
        print(f"❌ Error reading CSV config: {e}")
        return {}


def display_config(config: Dict[str, Any], format_type: str):
    """
    Display configuration data in a formatted way.
    
    Args:
        config (dict): Configuration data
        format_type (str): Type of config (JSON/CSV)
    """
    if not config:
        print("No configuration data to display.")
        return
    
    print(f"\n🔧 {format_type.upper()} CONFIGURATION")
    print("=" * 40)
    
    def print_dict(d, indent=0):
        """Recursively print dictionary with indentation."""
        for key, value in d.items():
            if isinstance(value, dict):
                print("  " * indent + f"{key}:")
                print_dict(value, indent + 1)
            else:
                print("  " * indent + f"{key}: {value}")
    
    print_dict(config)


def update_json_config(filename: str, updates: Dict[str, Any]):
    """
    Update JSON configuration file with new values.
    
    Args:
        filename (str): Path to JSON config file
        updates (dict): Values to update
    """
    # Read existing config
    config = read_json_config(filename)
    if not config:
        config = {}
    
    # Apply updates
    config.update(updates)
    
    # Write updated config
    try:
        with open(filename, 'w') as file:
            json.dump(config, file, indent=2)
        print(f"✅ Configuration updated in '{filename}'")
    except Exception as e:
        print(f"❌ Error updating config: {e}")


def main():
    """Main program function."""
    print("⚙️  Configuration File Reader")
    print("This program demonstrates reading different configuration file formats.")
    
    # Create sample configs if they don't exist
    if not (os.path.exists("config.json") and os.path.exists("settings.csv")):
        create_sample_config()
    
    while True:
        print("\n" + "=" * 40)
        print("📋 CONFIG READER MENU")
        print("=" * 40)
        print("1. Read JSON config")
        print("2. Read CSV config")
        print("3. Update JSON config")
        print("4. Create sample configs")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            filename = input("Enter JSON config file name (default: config.json): ").strip()
            if not filename:
                filename = "config.json"
            config = read_json_config(filename)
            display_config(config, "JSON")
        
        elif choice == '2':
            filename = input("Enter CSV config file name (default: settings.csv): ").strip()
            if not filename:
                filename = "settings.csv"
            config = read_csv_config(filename)
            display_config(config, "CSV")
        
        elif choice == '3':
            filename = input("Enter JSON config file name (default: config.json): ").strip()
            if not filename:
                filename = "config.json"
            
            if os.path.exists(filename):
                setting = input("Enter setting name to update: ").strip()
                value = input("Enter new value: ").strip()
                
                # Try to convert to appropriate type
                if value.lower() in ('true', 'false'):
                    value = value.lower() == 'true'
                elif value.isdigit():
                    value = int(value)
                else:
                    try:
                        value = float(value)
                    except ValueError:
                        # Keep as string
                        pass
                
                update_json_config(filename, {setting: value})
            else:
                print(f"Config file '{filename}' not found.")
        
        elif choice == '4':
            create_sample_config()
        
        elif choice == '5':
            print("Thank you for using Configuration File Reader!")
            break
        
        else:
            print("Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()