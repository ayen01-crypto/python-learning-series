"""
Mini Project: Extension Builder

A framework for building and managing C extensions for Python.
"""

import os
import sys
import subprocess
import tempfile
import shutil
from typing import Dict, List, Optional
from pathlib import Path


# ============================================
# Extension Builder Core
# ============================================

class ExtensionBuilder:
    """Framework for building C extensions for Python."""
    
    def __init__(self, name: str, source_dir: str = "."):
        self.name = name
        self.source_dir = Path(source_dir)
        self.build_dir = self.source_dir / "build"
        self.extensions_dir = self.source_dir / "extensions"
        self.setup_file = self.source_dir / "setup.py"
        
        # Create directories
        self.build_dir.mkdir(exist_ok=True)
        self.extensions_dir.mkdir(exist_ok=True)
    
    def create_extension_template(self, extension_name: str) -> str:
        """Create a template for a new C extension."""
        template = f'''#include <Python.h>

/* Function implementations */
static PyObject* {extension_name}_hello(PyObject* self, PyObject* args) {{
    return PyUnicode_FromString("Hello from {extension_name} extension!");
}}

static PyObject* {extension_name}_add(PyObject* self, PyObject* args) {{
    long a, b;
    if (!PyArg_ParseTuple(args, "ll", &a, &b)) {{
        return NULL;
    }}
    return PyLong_FromLong(a + b);
}}

/* Method definitions */
static PyMethodDef {extension_name}_methods[] = {{
    {{"hello", {extension_name}_hello, METH_NOARGS, "Say hello"}},
    {{"add", {extension_name}_add, METH_VARARGS, "Add two integers"}},
    {{NULL, NULL, 0, NULL}}  /* Sentinel */
}};

/* Module definition */
static struct PyModuleDef {extension_name}_module = {{
    PyModuleDef_HEAD_INIT,
    "{extension_name}",
    "Example C extension module",
    -1,
    {extension_name}_methods
}};

/* Module initialization */
PyMODINIT_FUNC PyInit_{extension_name}(void) {{
    return PyModule_Create(&{extension_name}_module);
}}
'''
        return template
    
    def create_setup_file(self, extensions: List[str]) -> str:
        """Create setup.py file for building extensions."""
        ext_modules = []
        for ext in extensions:
            ext_modules.append(f"Extension('{ext}', ['{ext}.c'])")
        
        setup_content = f'''from setuptools import setup, Extension

# Extension modules
extensions = [
    {',\\n    '.join(ext_modules)}
]

# Setup configuration
setup(
    name='{self.name}',
    version='1.0.0',
    description='C extensions built with ExtensionBuilder',
    ext_modules=extensions,
    zip_safe=False,
)
'''
        return setup_content
    
    def create_extension(self, extension_name: str, force: bool = False) -> bool:
        """Create a new C extension."""
        ext_file = self.extensions_dir / f"{extension_name}.c"
        
        if ext_file.exists() and not force:
            print(f"❌ Extension '{extension_name}' already exists!")
            return False
        
        # Create extension source
        template = self.create_extension_template(extension_name)
        with open(ext_file, 'w') as f:
            f.write(template)
        
        print(f"✅ Created extension '{extension_name}' at {ext_file}")
        return True
    
    def build_extension(self, extension_name: str) -> bool:
        """Build a C extension."""
        ext_file = self.extensions_dir / f"{extension_name}.c"
        
        if not ext_file.exists():
            print(f"❌ Extension '{extension_name}' not found!")
            return False
        
        try:
            # Create temporary setup.py
            setup_content = self.create_setup_file([extension_name])
            setup_path = self.build_dir / "setup.py"
            
            with open(setup_path, 'w') as f:
                f.write(setup_content)
            
            # Build extension
            print(f"🔨 Building extension '{extension_name}'...")
            result = subprocess.run([
                sys.executable, str(setup_path), "build_ext", "--inplace"
            ], cwd=self.build_dir, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Extension '{extension_name}' built successfully!")
                return True
            else:
                print(f"❌ Build failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error building extension: {e}")
            return False
    
    def build_all_extensions(self) -> Dict[str, bool]:
        """Build all extensions."""
        results = {}
        c_files = list(self.extensions_dir.glob("*.c"))
        
        if not c_files:
            print("❌ No extensions found!")
            return results
        
        for c_file in c_files:
            ext_name = c_file.stem
            results[ext_name] = self.build_extension(ext_name)
        
        return results
    
    def install_extension(self, extension_name: str) -> bool:
        """Install a built extension."""
        try:
            # Create setup.py for installation
            setup_content = self.create_setup_file([extension_name])
            setup_path = self.build_dir / "setup.py"
            
            with open(setup_path, 'w') as f:
                f.write(setup_content)
            
            # Install extension
            print(f"📦 Installing extension '{extension_name}'...")
            result = subprocess.run([
                sys.executable, str(setup_path), "install"
            ], cwd=self.build_dir, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Extension '{extension_name}' installed successfully!")
                return True
            else:
                print(f"❌ Installation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error installing extension: {e}")
            return False
    
    def list_extensions(self) -> List[str]:
        """List all available extensions."""
        c_files = list(self.extensions_dir.glob("*.c"))
        return [f.stem for f in c_files]
    
    def clean_build(self):
        """Clean build directory."""
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
            self.build_dir.mkdir()
            print("✅ Build directory cleaned")


# ============================================
# Cython Integration
# ============================================

class CythonBuilder:
    """Framework for building Cython extensions."""
    
    def __init__(self, source_dir: str = "."):
        self.source_dir = Path(source_dir)
        self.cython_dir = self.source_dir / "cython_extensions"
        self.cython_dir.mkdir(exist_ok=True)
    
    def create_cython_template(self, module_name: str) -> str:
        """Create a template for a Cython extension."""
        template = f'''# cython: language_level=3

def fibonacci(int n):
    """Calculate Fibonacci number using Cython."""
    cdef int a = 0
    cdef int b = 1
    cdef int i
    
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    for i in range(2, n + 1):
        a, b = b, a + b
    
    return b

def fast_sum(list numbers):
    """Fast sum using Cython."""
    cdef double total = 0.0
    cdef int i
    cdef int n = len(numbers)
    
    for i in range(n):
        total += numbers[i]
    
    return total
'''
        return template
    
    def create_setup_file(self, modules: List[str]) -> str:
        """Create setup.py for Cython extensions."""
        setup_content = f'''from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize([
        {',\\n        '.join(f"'{mod}.pyx'" for mod in modules)}
    ]),
    zip_safe=False,
)
'''
        return setup_content
    
    def create_cython_extension(self, module_name: str) -> bool:
        """Create a new Cython extension."""
        pyx_file = self.cython_dir / f"{module_name}.pyx"
        
        if pyx_file.exists():
            print(f"❌ Cython module '{module_name}' already exists!")
            return False
        
        # Create Cython source
        template = self.create_cython_template(module_name)
        with open(pyx_file, 'w') as f:
            f.write(template)
        
        print(f"✅ Created Cython module '{module_name}' at {pyx_file}")
        return True
    
    def build_cython_extension(self, module_name: str) -> bool:
        """Build a Cython extension."""
        pyx_file = self.cython_dir / f"{module_name}.pyx"
        
        if not pyx_file.exists():
            print(f"❌ Cython module '{module_name}' not found!")
            return False
        
        try:
            # Create setup.py
            setup_content = self.create_setup_file([module_name])
            setup_path = self.cython_dir / "setup.py"
            
            with open(setup_path, 'w') as f:
                f.write(setup_content)
            
            # Build extension
            print(f"🔨 Building Cython extension '{module_name}'...")
            result = subprocess.run([
                sys.executable, str(setup_path), "build_ext", "--inplace"
            ], cwd=self.cython_dir, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Cython extension '{module_name}' built successfully!")
                return True
            else:
                print(f"❌ Build failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error building Cython extension: {e}")
            return False


# ============================================
# Performance Testing
# ============================================

class PerformanceTester:
    """Performance testing for extensions."""
    
    def __init__(self):
        self.results = {}
    
    def time_function(self, func, *args, iterations: int = 10000, **kwargs) -> float:
        """Time a function execution."""
        import time
        
        # Warm up
        for _ in range(100):
            func(*args, **kwargs)
        
        # Time execution
        start = time.perf_counter()
        for _ in range(iterations):
            func(*args, **kwargs)
        end = time.perf_counter()
        
        return (end - start) / iterations
    
    def compare_implementations(self, implementations: Dict[str, callable], 
                              *args, iterations: int = 10000, **kwargs):
        """Compare multiple implementations."""
        results = {}
        
        for name, func in implementations.items():
            avg_time = self.time_function(func, *args, iterations=iterations, **kwargs)
            results[name] = avg_time
        
        # Sort by performance
        sorted_results = sorted(results.items(), key=lambda x: x[1])
        
        print("📊 Performance Comparison:")
        print("-" * 50)
        print(f"{'Implementation':<20} {'Avg Time (s)':<15} {'Speedup'}")
        print("-" * 50)
        
        baseline = sorted_results[0][1]
        for name, time in sorted_results:
            speedup = baseline / time if time > 0 else 0
            print(f"{name:<20} {time:<15.8f} {speedup:.2f}x")
        
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
    print("1.  Create C Extension")
    print("2.  Build C Extension")
    print("3.  Build All Extensions")
    print("4.  Install Extension")
    print("5.  Create Cython Extension")
    print("6.  Build Cython Extension")
    print("7.  List Extensions")
    print("8.  Performance Testing")
    print("9.  Extension Builder Features")
    print("10. Exit")


def create_c_extension_interactive(builder: ExtensionBuilder):
    """Create a new C extension."""
    print_header("🔧 CREATE C EXTENSION")
    
    name = input("Extension name: ").strip()
    if not name:
        print("❌ Extension name is required!")
        return
    
    if builder.create_extension(name):
        print(f"✅ Extension '{name}' created successfully!")
        print("   You can now edit the C source file and build it.")


def build_c_extension_interactive(builder: ExtensionBuilder):
    """Build a C extension."""
    print_header("🔨 BUILD C EXTENSION")
    
    extensions = builder.list_extensions()
    if not extensions:
        print("❌ No extensions found!")
        return
    
    print("Available extensions:")
    for i, ext in enumerate(extensions, 1):
        print(f"  {i}. {ext}")
    
    try:
        choice = int(input("Select extension: ")) - 1
        if 0 <= choice < len(extensions):
            ext_name = extensions[choice]
            if builder.build_extension(ext_name):
                print("✅ Extension built successfully!")
                print("   You can now import and use the extension.")
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Invalid input!")


def build_all_extensions_interactive(builder: ExtensionBuilder):
    """Build all extensions."""
    print_header("🏭 BUILD ALL EXTENSIONS")
    
    results = builder.build_all_extensions()
    if results:
        print("Build Results:")
        for ext_name, success in results.items():
            status = "✅ Success" if success else "❌ Failed"
            print(f"  {ext_name}: {status}")
    else:
        print("❌ No extensions to build!")


def install_extension_interactive(builder: ExtensionBuilder):
    """Install an extension."""
    print_header("📦 INSTALL EXTENSION")
    
    extensions = builder.list_extensions()
    if not extensions:
        print("❌ No extensions found!")
        return
    
    print("Available extensions:")
    for i, ext in enumerate(extensions, 1):
        print(f"  {i}. {ext}")
    
    try:
        choice = int(input("Select extension to install: ")) - 1
        if 0 <= choice < len(extensions):
            ext_name = extensions[choice]
            if builder.install_extension(ext_name):
                print("✅ Extension installed successfully!")
                print("   You can now use it in any Python script.")
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Invalid input!")


def create_cython_extension_interactive(cython_builder: CythonBuilder):
    """Create a Cython extension."""
    print_header("🐍 CREATE CYTHON EXTENSION")
    
    name = input("Module name: ").strip()
    if not name:
        print("❌ Module name is required!")
        return
    
    if cython_builder.create_cython_extension(name):
        print(f"✅ Cython module '{name}' created successfully!")
        print("   You can now edit the .pyx file and build it.")


def build_cython_extension_interactive(cython_builder: CythonBuilder):
    """Build a Cython extension."""
    print_header("🐍 BUILD CYTHON EXTENSION")
    
    # Check if Cython is installed
    try:
        import Cython
        print(f"✅ Cython version {Cython.__version__} detected")
    except ImportError:
        print("❌ Cython not installed! Please install with: pip install cython")
        return
    
    # For demo purposes, we'll show the process
    print("In a real implementation, this would:")
    print("1. Compile .pyx to .c")
    print("2. Compile .c to shared library")
    print("3. Create importable Python module")
    print("\nExample usage after building:")
    print("  import my_cython_module")
    print("  result = my_cython_module.fibonacci(10)")


def list_extensions_interactive(builder: ExtensionBuilder):
    """List all extensions."""
    print_header("📋 LIST EXTENSIONS")
    
    extensions = builder.list_extensions()
    if extensions:
        print(f"Found {len(extensions)} extension(s):")
        for ext in extensions:
            print(f"  📄 {ext}")
    else:
        print("❌ No extensions found!")


def performance_testing_interactive():
    """Demonstrate performance testing."""
    print_header("⚡ PERFORMANCE TESTING")
    
    print("Performance Testing Features:")
    print()
    print("⏱️  Function Timing:")
    print("  • Microsecond precision timing")
    print("  • Warm-up runs for accuracy")
    print("  • Statistical analysis")
    print()
    print("🔬 Implementation Comparison:")
    print("  • Python vs C extension")
    print("  • Pure Python vs Cython")
    print("  • Different algorithms")
    print()
    print("📊 Reporting:")
    print("  • Side-by-side comparison")
    print("  • Speedup calculations")
    print("  • Performance trends")


def extension_builder_features_interactive():
    """Show extension builder features."""
    print_header("⚙️  EXTENSION BUILDER FEATURES")
    
    print("Extension Builder Features:")
    print()
    print("🔧 C Extension Development:")
    print("  • Template generation")
    print("  • Build automation")
    print("  • Installation management")
    print()
    print("🐍 Cython Integration:")
    print("  • Cython template creation")
    print("  • Automatic compilation")
    print("  • Type annotations")
    print()
    print("🏗️  Build System:")
    print("  • Cross-platform support")
    print("  • Dependency management")
    print("  • Error handling")
    print()
    print("🛡️  Safety Features:")
    print("  • Input validation")
    print("  • Error recovery")
    print("  • Cleanup utilities")
    print()
    print("⚡ Performance:")
    print("  • Optimized builds")
    print("  • Memory management")
    print("  • Profiling tools")


# ============================================
# Main Application
# ============================================

def main():
    """Main application loop."""
    
    # Create builders
    builder = ExtensionBuilder("MyExtensions")
    cython_builder = CythonBuilder()
    tester = PerformanceTester()
    
    print("=" * 70)
    print("🔧  EXTENSION BUILDER  🔧".center(70))
    print("=" * 70)
    print("Framework for building C and Cython extensions!")
    
    while True:
        print_menu()
        choice = input("\nYour choice: ").strip()
        
        if choice == '1':
            create_c_extension_interactive(builder)
        elif choice == '2':
            build_c_extension_interactive(builder)
        elif choice == '3':
            build_all_extensions_interactive(builder)
        elif choice == '4':
            install_extension_interactive(builder)
        elif choice == '5':
            create_cython_extension_interactive(cython_builder)
        elif choice == '6':
            build_cython_extension_interactive(cython_builder)
        elif choice == '7':
            list_extensions_interactive(builder)
        elif choice == '8':
            performance_testing_interactive()
        elif choice == '9':
            extension_builder_features_interactive()
        elif choice == '10':
            print("\n👋 Thank you for using the Extension Builder!")
            print("=" * 70 + "\n")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
