"""
Lesson 09: Modules, Packages & Imports
Comprehensive Examples
"""

import sys
import os
from typing import List, Dict


# ============================================
# 1. Basic Module Import
# ============================================

print("=== BASIC MODULE IMPORT ===\n")

# Import built-in modules
import math
import random
import datetime

print(f"Math constants: π = {math.pi:.4f}")
print(f"Random number: {random.randint(1, 10)}")
print(f"Current time: {datetime.datetime.now()}")

# Import specific functions
from statistics import mean, median, mode
from collections import Counter, defaultdict

data = [1, 2, 2, 3, 4, 4, 4, 5]
print(f"Mean: {mean(data)}")
print(f"Median: {median(data)}")
try:
    print(f"Mode: {mode(data)}")
except Exception as e:
    print(f"Mode error: {e}")

# Import with alias
import json as json_parser
import csv as csv_handler

print("✅ Basic imports demonstrated")


# ============================================
# 2. Creating and Using Custom Modules
# ============================================

print("\n" + "="*60)
print("=== CUSTOM MODULES ===\n")

# Create a simple module file
module_content = '''
"""Simple math utilities module."""

def add(a, b):
    """Add two numbers."""
    return a + b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

def power(base, exponent):
    """Raise base to the power of exponent."""
    return base ** exponent

# Module-level variable
PI = 3.14159

# This runs when module is imported
print("Math utilities module loaded")

if __name__ == "__main__":
    # This runs only when module is executed directly
    print("Running math utilities as script")
    print(f"5 + 3 = {add(5, 3)}")
'''

# Write the module file
with open("math_utils.py", "w") as f:
    f.write(module_content)

# Import and use the custom module
import math_utils

print(f"Using custom module:")
print(f"  5 + 3 = {math_utils.add(5, 3)}")
print(f"  4 × 7 = {math_utils.multiply(4, 7)}")
print(f"  π = {math_utils.PI}")

# Import specific functions
from math_utils import power, PI

print(f"  2^8 = {power(2, 8)}")
print(f"  PI = {PI}")


# ============================================
# 3. Package Structure
# ============================================

print("\n" + "="*60)
print("=== PACKAGE STRUCTURE ===\n")

# Create package directory structure
os.makedirs("mypackage", exist_ok=True)
os.makedirs("mypackage/subpackage", exist_ok=True)

# Create __init__.py files
init_content = '''
"""MyPackage - Main package initialization."""

__version__ = "1.0.0"
__author__ = "Python Learner"

print("MyPackage initialized")

# Control what gets imported with "from mypackage import *"
__all__ = ["math_operations", "text_utils"]
'''

with open("mypackage/__init__.py", "w") as f:
    f.write(init_content)

# Create module files
math_module = '''
"""Math operations module."""

def calculate_area(length, width):
    """Calculate rectangle area."""
    return length * width

def calculate_volume(length, width, height):
    """Calculate rectangular volume."""
    return length * width * height

class Calculator:
    """Simple calculator class."""
    
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def get_history(self):
        return self.history
'''

text_module = '''
"""Text utilities module."""

def reverse_string(text):
    """Reverse a string."""
    return text[::-1]

def count_words(text):
    """Count words in text."""
    return len(text.split())

def is_palindrome(text):
    """Check if text is a palindrome."""
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]
'''

with open("mypackage/math_operations.py", "w") as f:
    f.write(math_module)

with open("mypackage/text_utils.py", "w") as f:
    f.write(text_module)

# Create subpackage
subpackage_init = '''
"""Subpackage initialization."""
print("Subpackage initialized")
'''

subpackage_module = '''
"""Advanced utilities module."""

def fibonacci(n):
    """Generate Fibonacci sequence."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

def is_prime(n):
    """Check if number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
'''

with open("mypackage/subpackage/__init__.py", "w") as f:
    f.write(subpackage_init)

with open("mypackage/subpackage/advanced_utils.py", "w") as f:
    f.write(subpackage_module)

# Use the package
sys.path.append(".")  # Add current directory to path

import mypackage
from mypackage import math_operations, text_utils
from mypackage.subpackage import advanced_utils

print("Package usage:")
print(f"  Area: {math_operations.calculate_area(5, 3)}")
print(f"  Reversed: {text_utils.reverse_string('hello')}")
print(f"  Fibonacci: {advanced_utils.fibonacci(8)}")


# ============================================
# 4. Different Import Styles
# ============================================

print("\n" + "="*60)
print("=== IMPORT STYLES ===\n")

# Standard import
import random
print(f"Random with standard import: {random.randint(1, 5)}")

# Import with alias
import random as rnd
print(f"Random with alias: {rnd.randint(1, 5)}")

# Import specific functions
from random import randint, choice
print(f"Specific import randint: {randint(1, 5)}")

# Import all (not recommended)
from random import *
print(f"Import all: {randrange(1, 10, 2)}")

# Relative imports (in packages)
print("Relative imports work within packages")


# ============================================
# 5. Module Search Path
# ============================================

print("\n" + "="*60)
print("=== MODULE SEARCH PATH ===\n")

print("Python search path:")
for i, path in enumerate(sys.path[:5]):  # Show first 5 paths
    print(f"  {i+1}. {path}")

# Add custom path
custom_path = os.path.abspath("mypackage")
if custom_path not in sys.path:
    sys.path.insert(0, custom_path)
    print(f"Added custom path: {custom_path}")


# ============================================
# 6. Reloading Modules
# ============================================

print("\n" + "="*60)
print("=== MODULE RELOADING ===\n")

import importlib

# Reload a module (useful during development)
importlib.reload(math_utils)
print("Module reloaded")


# ============================================
# 7. Conditional Execution
# ============================================

print("\n" + "="*60)
print("=== CONDITIONAL EXECUTION ===\n")

# This demonstrates __name__ == "__main__"
print(f"Current module name: {__name__}")

# When we run math_utils directly, its __name__ will be "__main__"
# When we import it, its __name__ will be "math_utils"


# ============================================
# 8. Module Documentation
# ============================================

print("\n" + "="*60)
print("=== MODULE DOCUMENTATION ===\n")

print(f"math module doc: {math.__doc__[:50]}...")
print(f"math_utils module doc: {math_utils.__doc__}")
print(f"Module file: {math_utils.__file__}")
print(f"Module name: {math_utils.__name__}")
print(f"Module package: {math_utils.__package__}")


# ============================================
# 9. Circular Imports (How to Avoid)
# ============================================

print("\n" + "="*60)
print("=== CIRCULAR IMPORTS ===\n")

print("""
Avoid circular imports by:
1. Restructuring code logically
2. Using import inside functions
3. Moving shared code to a third module
4. Using importlib for dynamic imports
""")

# Example of import inside function (to avoid circular imports)
def delayed_import():
    """Import inside function to avoid circular imports."""
    import json  # This is fine for avoiding circular imports
    return json.dumps({"example": "data"})

print(f"Delayed import result: {delayed_import()}")


# ============================================
# 10. Best Practices
# ============================================

print("\n" + "="*60)
print("=== BEST PRACTICES ===\n")

print("""
Module and Package Best Practices:

1. Use absolute imports when possible
2. Group imports at the top of the file
3. Separate standard library, third-party, and local imports
4. Use __all__ to control exports
5. Write docstrings for modules and functions
6. Use meaningful module names
7. Keep modules focused on a single responsibility
8. Avoid from module import * in production code
""")

# Example of good import organization
import os           # Standard library
import sys          # Standard library

import requests     # Third-party (if installed)
import numpy as np  # Third-party (if installed)

import mypackage    # Local package
from mypackage import math_operations  # Local module


# ============================================
# Practice Exercise
# ============================================

print("\n" + "="*60)
print("🎯 PRACTICE EXERCISE")
print("="*60)
print("""
Try these exercises:

1. Create a utilities package with submodules for different functions
2. Build a configuration management system using modules
3. Implement a plugin architecture with dynamic module loading
4. Create a logging utility package with different handlers
5. Design a database abstraction package with multiple backends
""")

# Clean up created files
files_to_clean = [
    "math_utils.py",
    "mypackage/__init__.py",
    "mypackage/math_operations.py",
    "mypackage/text_utils.py",
    "mypackage/subpackage/__init__.py",
    "mypackage/subpackage/advanced_utils.py"
]

for file_path in files_to_clean:
    if os.path.exists(file_path):
        os.remove(file_path)

# Clean up directories
dirs_to_clean = ["mypackage/subpackage", "mypackage"]
for dir_path in dirs_to_clean:
    if os.path.exists(dir_path) and not os.listdir(dir_path):
        os.rmdir(dir_path)

print("\n🧹 Cleaned up temporary files and directories")
