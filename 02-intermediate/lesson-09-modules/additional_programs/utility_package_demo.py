#!/usr/bin/env python3
"""
Utility Package Demo
Demonstrates creating and using a custom utility package with math, string, and file functions.
"""

import os
import sys
import tempfile
from typing import List, Dict, Any


# First, let's create our utility modules as strings
MATH_UTILS_CONTENT = '''
"""Math utility functions."""

import math
from typing import List, Union

def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Add two numbers."""
    return a + b

def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Subtract second number from first."""
    return a - b

def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Multiply two numbers."""
    return a * b

def divide(a: Union[int, float], b: Union[int, float]) -> float:
    """Divide first number by second."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(base: Union[int, float], exponent: Union[int, float]) -> Union[int, float]:
    """Raise base to the power of exponent."""
    return base ** exponent

def factorial(n: int) -> int:
    """Calculate factorial of n."""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    return math.factorial(n)

def average(numbers: List[Union[int, float]]) -> float:
    """Calculate average of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Export public API
__all__ = [
    "add", "subtract", "multiply", "divide", "power",
    "factorial", "average", "is_prime"
]
'''

STRING_UTILS_CONTENT = '''
"""String utility functions."""

import re
from typing import List

def reverse_string(s: str) -> str:
    """Reverse a string."""
    return s[::-1]

def capitalize_words(s: str) -> str:
    """Capitalize the first letter of each word."""
    return ' '.join(word.capitalize() for word in s.split())

def count_vowels(s: str) -> int:
    """Count vowels in a string."""
    return len(re.findall(r'[aeiouAEIOU]', s))

def count_consonants(s: str) -> int:
    """Count consonants in a string."""
    return len(re.findall(r'[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]', s))

def is_palindrome(s: str) -> bool:
    """Check if a string is a palindrome (ignoring case and spaces)."""
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return cleaned == cleaned[::-1]

def snake_to_camel(s: str) -> str:
    """Convert snake_case to camelCase."""
    parts = s.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def camel_to_snake(s: str) -> str:
    """Convert camelCase to snake_case."""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

def word_count(s: str) -> int:
    """Count words in a string."""
    return len(s.split())

# Export public API
__all__ = [
    "reverse_string", "capitalize_words", "count_vowels",
    "count_consonants", "is_palindrome", "snake_to_camel",
    "camel_to_snake", "word_count"
]
'''

FILE_UTILS_CONTENT = '''
"""File utility functions."""

import os
import json
import csv
from typing import List, Dict, Any

def read_file(filepath: str) -> str:
    """Read entire file content."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(filepath: str, content: str) -> None:
    """Write content to file."""
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

def append_to_file(filepath: str, content: str) -> None:
    """Append content to file."""
    with open(filepath, 'a', encoding='utf-8') as file:
        file.write(content)

def file_exists(filepath: str) -> bool:
    """Check if file exists."""
    return os.path.exists(filepath)

def get_file_size(filepath: str) -> int:
    """Get file size in bytes."""
    if not file_exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    return os.path.getsize(filepath)

def read_json_file(filepath: str) -> Dict[str, Any]:
    """Read and parse JSON file."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json_file(filepath: str, data: Dict[str, Any]) -> None:
    """Write data to JSON file."""
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

def read_csv_file(filepath: str) -> List[Dict[str, str]]:
    """Read and parse CSV file."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return list(csv.DictReader(file))

def get_file_extension(filepath: str) -> str:
    """Get file extension."""
    return os.path.splitext(filepath)[1]

def create_directory(dirpath: str) -> None:
    """Create directory if it doesn't exist."""
    os.makedirs(dirpath, exist_ok=True)

# Export public API
__all__ = [
    "read_file", "write_file", "append_to_file", "file_exists",
    "get_file_size", "read_json_file", "write_json_file",
    "read_csv_file", "get_file_extension", "create_directory"
]
'''

PACKAGE_INIT_CONTENT = '''
"""Utility package for math, string, and file operations."""

# Import submodules
from . import math_utils
from . import string_utils
from . import file_utils

# Define package metadata
__version__ = "1.0.0"
__author__ = "Python Learning Series"

# Define what gets imported with "from utility_package import *"
__all__ = [
    "math_utils",
    "string_utils", 
    "file_utils"
]
'''

MAIN_DEMO_CONTENT = '''
#!/usr/bin/env python3
"""
Main demo script showing how to use the utility package.
"""

# Add current directory to Python path so we can import our package
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Import our utility package
import utility_package
from utility_package import math_utils, string_utils, file_utils

def demo_math_functions():
    """Demonstrate math utility functions."""
    print("🧮 Math Utilities Demo")
    print("=" * 30)
    
    # Basic arithmetic
    print(f"Addition: 5 + 3 = {math_utils.add(5, 3)}")
    print(f"Subtraction: 10 - 4 = {math_utils.subtract(10, 4)}")
    print(f"Multiplication: 6 * 7 = {math_utils.multiply(6, 7)}")
    print(f"Division: 15 / 3 = {math_utils.divide(15, 3)}")
    print(f"Power: 2^8 = {math_utils.power(2, 8)}")
    
    # Advanced math
    print(f"Factorial of 5: {math_utils.factorial(5)}")
    print(f"Average of [1, 2, 3, 4, 5]: {math_utils.average([1, 2, 3, 4, 5])}")
    print(f"Is 17 prime? {math_utils.is_prime(17)}")
    print(f"Is 15 prime? {math_utils.is_prime(15)}")
    print()

def demo_string_functions():
    """Demonstrate string utility functions."""
    print("🔤 String Utilities Demo")
    print("=" * 30)
    
    sample_text = "hello world python programming"
    print(f"Original text: '{sample_text}'")
    print(f"Reversed: '{string_utils.reverse_string(sample_text)}'")
    print(f"Capitalized: '{string_utils.capitalize_words(sample_text)}'")
    print(f"Vowel count: {string_utils.count_vowels(sample_text)}")
    print(f"Consonant count: {string_utils.count_consonants(sample_text)}")
    print(f"Word count: {string_utils.word_count(sample_text)}")
    
    # Palindrome check
    palindrome = "A man a plan a canal Panama"
    print(f"Is '{palindrome}' a palindrome? {string_utils.is_palindrome(palindrome)}")
    
    # Case conversion
    snake_case = "convert_this_string"
    camel_case = string_utils.snake_to_camel(snake_case)
    print(f"Snake to Camel: {snake_case} -> {camel_case}")
    print(f"Camel to Snake: {camel_case} -> {string_utils.camel_to_snake(camel_case)}")
    print()

def demo_file_functions():
    """Demonstrate file utility functions."""
    print("📁 File Utilities Demo")
    print("=" * 30)
    
    # Create a sample file
    sample_content = "This is a sample file.\\nIt has multiple lines.\\nUsed for testing file utilities."
    sample_file = "sample_demo.txt"
    
    # Write file
    file_utils.write_file(sample_file, sample_content)
    print(f"Created file: {sample_file}")
    
    # Read file
    content = file_utils.read_file(sample_file)
    print(f"File content:\\n{content}")
    
    # File info
    print(f"File exists: {file_utils.file_exists(sample_file)}")
    print(f"File size: {file_utils.get_file_size(sample_file)} bytes")
    print(f"File extension: {file_utils.get_file_extension(sample_file)}")
    
    # JSON demo
    sample_data = {
        "name": "John Doe",
        "age": 30,
        "skills": ["Python", "JavaScript", "SQL"]
    }
    json_file = "sample_demo.json"
    file_utils.write_json_file(json_file, sample_data)
    loaded_data = file_utils.read_json_file(json_file)
    print(f"JSON data: {loaded_data}")
    
    # Cleanup
    os.remove(sample_file)
    os.remove(json_file)
    print("Cleaned up temporary files.")
    print()

def main():
    """Main demo function."""
    print("📦 Utility Package Demo")
    print("This program demonstrates creating and using a custom utility package.")
    print(f"Package version: {utility_package.__version__}")
    print(f"Package author: {utility_package.__author__}")
    print()
    
    demo_math_functions()
    demo_string_functions()
    demo_file_functions()
    
    print("🎉 Demo completed successfully!")

if __name__ == "__main__":
    main()
'''


def create_utility_package():
    """Create the utility package structure."""
    # Create package directory
    package_dir = "utility_package"
    os.makedirs(package_dir, exist_ok=True)
    
    # Create module files
    with open(os.path.join(package_dir, "math_utils.py"), "w") as f:
        f.write(MATH_UTILS_CONTENT.strip())
    
    with open(os.path.join(package_dir, "string_utils.py"), "w") as f:
        f.write(STRING_UTILS_CONTENT.strip())
    
    with open(os.path.join(package_dir, "file_utils.py"), "w") as f:
        f.write(FILE_UTILS_CONTENT.strip())
    
    with open(os.path.join(package_dir, "__init__.py"), "w") as f:
        f.write(PACKAGE_INIT_CONTENT.strip())
    
    # Create main demo file
    with open("main_demo.py", "w") as f:
        f.write(MAIN_DEMO_CONTENT.strip())
    
    print(f"✅ Created utility package in '{package_dir}' directory")
    print("✅ Created main demo script 'main_demo.py'")
    print("\n📁 Package structure:")
    print(f"  {package_dir}/")
    print(f"    ├── __init__.py")
    print(f"    ├── math_utils.py")
    print(f"    ├── string_utils.py")
    print(f"    └── file_utils.py")
    print(f"  main_demo.py")


def run_demo():
    """Run the utility package demo."""
    try:
        # Execute the main demo script
        import subprocess
        result = subprocess.run([sys.executable, "main_demo.py"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Demo executed successfully!")
            print("\n📄 Output:")
            print(result.stdout)
        else:
            print("❌ Demo failed with errors:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Error running demo: {e}")


def main():
    """Main program function."""
    print("📦 Utility Package Creator")
    print("This program demonstrates creating a custom utility package with math, string, and file functions.")
    
    while True:
        print("\n" + "=" * 40)
        print("📦 UTILITY PACKAGE MENU")
        print("=" * 40)
        print("1. Create utility package")
        print("2. Run demo")
        print("3. Show package structure")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            try:
                create_utility_package()
            except Exception as e:
                print(f"❌ Error creating package: {e}")
        
        elif choice == '2':
            if os.path.exists("main_demo.py"):
                run_demo()
            else:
                print("❌ Demo script not found. Please create the package first.")
        
        elif choice == '3':
            print("\n📁 Utility Package Structure:")
            print("utility_package/")
            print("  ├── __init__.py          # Package initializer")
            print("  ├── math_utils.py        # Mathematical functions")
            print("  │   ├── add(a, b)        # Addition")
            print("  │   ├── subtract(a, b)   # Subtraction")
            print("  │   ├── multiply(a, b)   # Multiplication")
            print("  │   ├── divide(a, b)     # Division")
            print("  │   ├── power(base, exp) # Exponentiation")
            print("  │   ├── factorial(n)     # Factorial")
            print("  │   ├── average(numbers) # Average calculation")
            print("  │   └── is_prime(n)      # Prime number check")
            print("  ├── string_utils.py      # String manipulation functions")
            print("  │   ├── reverse_string(s)     # Reverse string")
            print("  │   ├── capitalize_words(s)   # Capitalize words")
            print("  │   ├── count_vowels(s)       # Count vowels")
            print("  │   ├── count_consonants(s)   # Count consonants")
            print("  │   ├── is_palindrome(s)      # Check palindrome")
            print("  │   ├── snake_to_camel(s)     # Convert snake_case to camelCase")
            print("  │   ├── camel_to_snake(s)     # Convert camelCase to snake_case")
            print("  │   └── word_count(s)         # Count words")
            print("  └── file_utils.py        # File operations")
            print("      ├── read_file(path)       # Read file content")
            print("      ├── write_file(path, content) # Write to file")
            print("      ├── append_to_file(path, content) # Append to file")
            print("      ├── file_exists(path)     # Check if file exists")
            print("      ├── get_file_size(path)   # Get file size")
            print("      ├── read_json_file(path)  # Read JSON file")
            print("      ├── write_json_file(path, data) # Write JSON file")
            print("      ├── read_csv_file(path)   # Read CSV file")
            print("      ├── get_file_extension(path) # Get file extension")
            print("      └── create_directory(path) # Create directory")
            print()
            print("main_demo.py               # Main demo script")
        
        elif choice == '4':
            print("Thank you for using Utility Package Creator!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()