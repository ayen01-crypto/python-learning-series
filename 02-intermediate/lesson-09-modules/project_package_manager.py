"""
Mini Project: Package Manager

A comprehensive package management system demonstrating modules, packages, and imports.
"""

import os
import sys
import json
import importlib
from typing import Dict, List, Optional
from datetime import datetime


# ============================================
# Package Manager Classes
# ============================================

class Package:
    """Represents a Python package."""
    
    def __init__(self, name: str, version: str = "1.0.0", description: str = ""):
        self.name = name
        self.version = version
        self.description = description
        self.dependencies: List[str] = []
        self.files: List[str] = []
        self.created_date = datetime.now()
        self.installed = False
    
    def add_dependency(self, dependency: str):
        """Add a dependency."""
        if dependency not in self.dependencies:
            self.dependencies.append(dependency)
    
    def add_file(self, file_path: str):
        """Add a file to the package."""
        if file_path not in self.files:
            self.files.append(file_path)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'dependencies': self.dependencies,
            'files': self.files,
            'created_date': self.created_date.isoformat(),
            'installed': self.installed
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Package':
        """Create from dictionary."""
        package = cls(data['name'], data['version'], data['description'])
        package.dependencies = data.get('dependencies', [])
        package.files = data.get('files', [])
        package.created_date = datetime.fromisoformat(data.get('created_date', datetime.now().isoformat()))
        package.installed = data.get('installed', False)
        return package
    
    def __str__(self) -> str:
        return f"{self.name} v{self.version}"


class PackageManager:
    """Manages Python packages."""
    
    def __init__(self, packages_dir: str = "packages"):
        self.packages_dir = packages_dir
        self.registry_file = os.path.join(packages_dir, "registry.json")
        self.packages: Dict[str, Package] = {}
        self._ensure_directories()
        self._load_registry()
    
    def _ensure_directories(self):
        """Ensure required directories exist."""
        os.makedirs(self.packages_dir, exist_ok=True)
        for subdir in ["installed", "downloads", "cache"]:
            os.makedirs(os.path.join(self.packages_dir, subdir), exist_ok=True)
    
    def _load_registry(self):
        """Load package registry."""
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, 'r') as f:
                    data = json.load(f)
                    self.packages = {name: Package.from_dict(pkg_data) 
                                   for name, pkg_data in data.items()}
            except Exception as e:
                print(f"❌ Error loading registry: {e}")
        else:
            # Create default registry
            self._save_registry()
    
    def _save_registry(self):
        """Save package registry."""
        try:
            data = {name: package.to_dict() for name, package in self.packages.items()}
            with open(self.registry_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving registry: {e}")
    
    def create_package(self, name: str, version: str = "1.0.0", 
                      description: str = "") -> Package:
        """Create a new package."""
        if name in self.packages:
            raise ValueError(f"Package {name} already exists")
        
        package = Package(name, version, description)
        self.packages[name] = package
        self._save_registry()
        
        # Create package directory
        package_dir = os.path.join(self.packages_dir, "downloads", name)
        os.makedirs(package_dir, exist_ok=True)
        
        return package
    
    def get_package(self, name: str) -> Optional[Package]:
        """Get package by name."""
        return self.packages.get(name)
    
    def list_packages(self) -> List[Package]:
        """List all packages."""
        return list(self.packages.values())
    
    def search_packages(self, query: str) -> List[Package]:
        """Search packages by name or description."""
        query_lower = query.lower()
        results = []
        for package in self.packages.values():
            if (query_lower in package.name.lower() or 
                query_lower in package.description.lower()):
                results.append(package)
        return results
    
    def install_package(self, name: str) -> bool:
        """Install a package."""
        package = self.get_package(name)
        if not package:
            print(f"❌ Package {name} not found")
            return False
        
        if package.installed:
            print(f"✅ Package {name} is already installed")
            return True
        
        try:
            # Install dependencies first
            for dep_name in package.dependencies:
                if not self.install_package(dep_name):
                    print(f"❌ Failed to install dependency {dep_name}")
                    return False
            
            # Create installation directory
            install_dir = os.path.join(self.packages_dir, "installed", package.name)
            os.makedirs(install_dir, exist_ok=True)
            
            # Create basic package structure
            self._create_package_structure(install_dir, package)
            
            # Mark as installed
            package.installed = True
            self._save_registry()
            
            print(f"✅ Installed {package}")
            return True
            
        except Exception as e:
            print(f"❌ Error installing {name}: {e}")
            return False
    
    def uninstall_package(self, name: str) -> bool:
        """Uninstall a package."""
        package = self.get_package(name)
        if not package:
            print(f"❌ Package {name} not found")
            return False
        
        if not package.installed:
            print(f"❌ Package {name} is not installed")
            return False
        
        try:
            # Remove installation directory
            install_dir = os.path.join(self.packages_dir, "installed", package.name)
            if os.path.exists(install_dir):
                import shutil
                shutil.rmtree(install_dir)
            
            # Mark as uninstalled
            package.installed = False
            self._save_registry()
            
            print(f"✅ Uninstalled {package}")
            return True
            
        except Exception as e:
            print(f"❌ Error uninstalling {name}: {e}")
            return False
    
    def _create_package_structure(self, install_dir: str, package: Package):
        """Create basic package structure."""
        # Create __init__.py
        init_content = f'''
"""{package.name} - {package.description}"""

__version__ = "{package.version}"
__author__ = "Package Manager"

print("{package.name} v{package.version} loaded")
'''
        
        with open(os.path.join(install_dir, "__init__.py"), "w") as f:
            f.write(init_content)
        
        # Create main module
        main_content = f'''
"""Main module for {package.name}."""

def hello():
    """Say hello from {package.name}."""
    return "Hello from {package.name} v{package.version}!"

def get_info():
    """Get package information."""
    return {{
        "name": "{package.name}",
        "version": "{package.version}",
        "description": "{package.description}",
        "installed": True
    }}
'''
        
        with open(os.path.join(install_dir, "main.py"), "w") as f:
            f.write(main_content)
        
        # Create utils module
        utils_content = '''
"""Utility functions."""

def utility_function():
    """A sample utility function."""
    return "Utility function executed"

def helper_function(data):
    """A helper function."""
    return f"Processed: {data}"
'''
        
        with open(os.path.join(install_dir, "utils.py"), "w") as f:
            f.write(utils_content)
        
        # Add files to package record
        package.add_file("__init__.py")
        package.add_file("main.py")
        package.add_file("utils.py")
    
    def add_dependency(self, package_name: str, dependency_name: str) -> bool:
        """Add a dependency to a package."""
        package = self.get_package(package_name)
        if not package:
            print(f"❌ Package {package_name} not found")
            return False
        
        dep_package = self.get_package(dependency_name)
        if not dep_package:
            print(f"❌ Dependency {dependency_name} not found")
            return False
        
        package.add_dependency(dependency_name)
        self._save_registry()
        print(f"✅ Added {dependency_name} as dependency to {package_name}")
        return True
    
    def get_installed_packages(self) -> List[Package]:
        """Get all installed packages."""
        return [pkg for pkg in self.packages.values() if pkg.installed]
    
    def get_package_info(self, name: str) -> Dict:
        """Get detailed package information."""
        package = self.get_package(name)
        if not package:
            return {"error": f"Package {name} not found"}
        
        install_dir = os.path.join(self.packages_dir, "installed", name)
        files = []
        if os.path.exists(install_dir):
            files = [f for f in os.listdir(install_dir) if f.endswith('.py')]
        
        return {
            "name": package.name,
            "version": package.version,
            "description": package.description,
            "dependencies": package.dependencies,
            "installed": package.installed,
            "files": files,
            "created_date": package.created_date.isoformat()
        }


# ============================================
# Package Testing System
# ============================================

class PackageTester:
    """Test installed packages."""
    
    def __init__(self, package_manager: PackageManager):
        self.pm = package_manager
    
    def test_package(self, package_name: str) -> Dict:
        """Test a package by importing and running basic functions."""
        package = self.pm.get_package(package_name)
        if not package:
            return {"success": False, "error": f"Package {package_name} not found"}
        
        if not package.installed:
            return {"success": False, "error": f"Package {package_name} not installed"}
        
        try:
            # Add to path if not already there
            install_dir = os.path.join(self.pm.packages_dir, "installed")
            if install_dir not in sys.path:
                sys.path.insert(0, install_dir)
            
            # Import the package
            pkg_module = importlib.import_module(package_name)
            
            # Test main functions
            results = {
                "success": True,
                "package": package_name,
                "tests": []
            }
            
            # Test hello function
            try:
                if hasattr(pkg_module, 'main'):
                    main_module = getattr(pkg_module, 'main')
                    if hasattr(main_module, 'hello'):
                        result = main_module.hello()
                        results["tests"].append({
                            "test": "hello_function",
                            "passed": True,
                            "result": result
                        })
                    
                    if hasattr(main_module, 'get_info'):
                        info = main_module.get_info()
                        results["tests"].append({
                            "test": "get_info",
                            "passed": True,
                            "result": info
                        })
            except Exception as e:
                results["tests"].append({
                    "test": "main_module",
                    "passed": False,
                    "error": str(e)
                })
            
            # Test utils functions
            try:
                if hasattr(pkg_module, 'utils'):
                    utils_module = getattr(pkg_module, 'utils')
                    if hasattr(utils_module, 'utility_function'):
                        result = utils_module.utility_function()
                        results["tests"].append({
                            "test": "utility_function",
                            "passed": True,
                            "result": result
                        })
            except Exception as e:
                results["tests"].append({
                    "test": "utils_module",
                    "passed": False,
                    "error": str(e)
                })
            
            return results
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to import {package_name}: {e}"
            }


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
    print("1.  Create Package")
    print("2.  List All Packages")
    print("3.  Search Packages")
    print("4.  Install Package")
    print("5.  Uninstall Package")
    print("6.  Add Dependency")
    print("7.  View Package Info")
    print("8.  Test Package")
    print("9.  View Installed Packages")
    print("10. Load Sample Data")
    print("11. Exit")


def create_package_interactive(pm: PackageManager):
    """Interactive package creation."""
    print_header("➕ CREATE NEW PACKAGE")
    
    name = input("Package name: ").strip()
    if not name:
        print("❌ Package name is required!")
        return
    
    if pm.get_package(name):
        print("❌ Package already exists!")
        return
    
    version = input("Version (1.0.0): ").strip() or "1.0.0"
    description = input("Description: ").strip()
    
    try:
        package = pm.create_package(name, version, description)
        print(f"✅ Package '{name}' created successfully!")
    except Exception as e:
        print(f"❌ Error creating package: {e}")


def list_packages_interactive(pm: PackageManager):
    """List all packages."""
    print_header("📦 ALL PACKAGES")
    
    packages = pm.list_packages()
    
    if not packages:
        print("❌ No packages found!")
        return
    
    print(f"{'NAME':<20} {'VERSION':<12} {'STATUS':<12} {'DESCRIPTION'}")
    print("-" * 70)
    
    for package in sorted(packages, key=lambda p: p.name):
        status = "✅ Installed" if package.installed else "❌ Not Installed"
        print(f"{package.name:<20} {package.version:<12} {status:<12} {package.description}")


def search_packages_interactive(pm: PackageManager):
    """Search packages."""
    print_header("🔍 SEARCH PACKAGES")
    
    query = input("Search query: ").strip()
    if not query:
        print("❌ Search query is required!")
        return
    
    results = pm.search_packages(query)
    
    if not results:
        print("❌ No packages found!")
        return
    
    print(f"\n✅ Found {len(results)} package(s):\n")
    for package in results:
        status = "✅" if package.installed else "❌"
        print(f"  {status} {package.name} v{package.version} - {package.description}")


def install_package_interactive(pm: PackageManager):
    """Install a package."""
    print_header("📥 INSTALL PACKAGE")
    
    name = input("Package name: ").strip()
    if not name:
        print("❌ Package name is required!")
        return
    
    if pm.install_package(name):
        print(f"✅ Package installation completed!")
    else:
        print("❌ Package installation failed!")


def uninstall_package_interactive(pm: PackageManager):
    """Uninstall a package."""
    print_header("🗑️  UNINSTALL PACKAGE")
    
    name = input("Package name: ").strip()
    if not name:
        print("❌ Package name is required!")
        return
    
    # Confirm uninstallation
    package = pm.get_package(name)
    if package and package.installed:
        confirm = input(f"Uninstall {package}? (y/N): ").strip().lower()
        if confirm != 'y':
            print("ℹ️  Uninstallation cancelled.")
            return
    
    if pm.uninstall_package(name):
        print(f"✅ Package uninstallation completed!")
    else:
        print("❌ Package uninstallation failed!")


def add_dependency_interactive(pm: PackageManager):
    """Add dependency to package."""
    print_header("🔗 ADD DEPENDENCY")
    
    package_name = input("Package name: ").strip()
    dependency_name = input("Dependency name: ").strip()
    
    if not package_name or not dependency_name:
        print("❌ Both package and dependency names are required!")
        return
    
    pm.add_dependency(package_name, dependency_name)


def view_package_info_interactive(pm: PackageManager):
    """View detailed package information."""
    print_header("ℹ️  PACKAGE INFORMATION")
    
    name = input("Package name: ").strip()
    if not name:
        print("❌ Package name is required!")
        return
    
    info = pm.get_package_info(name)
    
    if "error" in info:
        print(f"❌ {info['error']}")
        return
    
    print(f"\n📦 {info['name']} v{info['version']}")
    print(f"📝 Description: {info['description']}")
    print(f"📊 Status: {'Installed' if info['installed'] else 'Not Installed'}")
    print(f"📅 Created: {info['created_date']}")
    
    if info['dependencies']:
        print(f"\n🔗 Dependencies:")
        for dep in info['dependencies']:
            print(f"  • {dep}")
    
    if info['files']:
        print(f"\n📁 Files:")
        for file in info['files']:
            print(f"  • {file}")


def test_package_interactive(pm: PackageManager):
    """Test a package."""
    print_header("🧪 TEST PACKAGE")
    
    name = input("Package name: ").strip()
    if not name:
        print("❌ Package name is required!")
        return
    
    tester = PackageTester(pm)
    results = tester.test_package(name)
    
    if not results["success"]:
        print(f"❌ {results['error']}")
        return
    
    print(f"✅ Testing {results['package']}:")
    passed = 0
    total = len(results["tests"])
    
    for test in results["tests"]:
        status = "✅ PASS" if test.get("passed", False) else "❌ FAIL"
        print(f"  {status} {test['test']}")
        if test.get("passed", False):
            passed += 1
        if "result" in test:
            print(f"    Result: {test['result']}")
        if "error" in test:
            print(f"    Error: {test['error']}")
    
    print(f"\n📊 Test Results: {passed}/{total} passed")


def view_installed_packages(pm: PackageManager):
    """View installed packages."""
    print_header("✅ INSTALLED PACKAGES")
    
    packages = pm.get_installed_packages()
    
    if not packages:
        print("❌ No installed packages!")
        return
    
    print(f"{'NAME':<25} {'VERSION':<15} {'FILES'}")
    print("-" * 70)
    
    for package in sorted(packages, key=lambda p: p.name):
        install_dir = os.path.join(pm.packages_dir, "installed", package.name)
        file_count = 0
        if os.path.exists(install_dir):
            file_count = len([f for f in os.listdir(install_dir) if f.endswith('.py')])
        
        print(f"{package.name:<25} {package.version:<15} {file_count} files")


def load_sample_data(pm: PackageManager):
    """Load sample packages for testing."""
    try:
        # Create sample packages
        math_pkg = pm.create_package("math_utils", "2.1.0", "Mathematical utilities")
        text_pkg = pm.create_package("text_utils", "1.5.2", "Text processing utilities")
        web_pkg = pm.create_package("web_utils", "3.0.1", "Web development utilities")
        
        # Add dependencies
        pm.add_dependency("web_utils", "text_utils")
        
        # Install some packages
        pm.install_package("math_utils")
        pm.install_package("text_utils")
        
        print("✅ Sample data loaded successfully!")
        print("   • Created 3 packages")
        print("   • Added 1 dependency")
        print("   • Installed 2 packages")
        
    except Exception as e:
        print(f"❌ Error loading sample data: {e}")


# ============================================
# Main Application
# ============================================

def main():
    """Main application loop."""
    pm = PackageManager()
    
    print("=" * 70)
    print("📦  PACKAGE MANAGER  📦".center(70))
    print("=" * 70)
    print("Complete package management system with modules and imports!")
    
    while True:
        print_menu()
        choice = input("\nYour choice: ").strip()
        
        if choice == '1':
            create_package_interactive(pm)
        elif choice == '2':
            list_packages_interactive(pm)
        elif choice == '3':
            search_packages_interactive(pm)
        elif choice == '4':
            install_package_interactive(pm)
        elif choice == '5':
            uninstall_package_interactive(pm)
        elif choice == '6':
            add_dependency_interactive(pm)
        elif choice == '7':
            view_package_info_interactive(pm)
        elif choice == '8':
            test_package_interactive(pm)
        elif choice == '9':
            view_installed_packages(pm)
        elif choice == '10':
            load_sample_data(pm)
        elif choice == '11':
            print("\n👋 Thank you for using the Package Manager!")
            print("=" * 70 + "\n")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
