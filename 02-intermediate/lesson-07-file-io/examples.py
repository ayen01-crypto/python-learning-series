"""
Lesson 07: File I/O & Working with Files
Comprehensive Examples
"""

import os
import json
import csv
from datetime import datetime


# ============================================
# 1. Basic File Operations
# ============================================

print("=== BASIC FILE OPERATIONS ===\n")

# Writing to a file
with open("sample.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("This is a sample file.\n")
    file.write("Python file handling is easy!")

# Reading from a file
with open("sample.txt", "r") as file:
    content = file.read()
    print("File content:")
    print(content)

# Reading line by line
print("\nReading line by line:")
with open("sample.txt", "r") as file:
    for line_num, line in enumerate(file, 1):
        print(f"Line {line_num}: {line.strip()}")

# Reading all lines into a list
with open("sample.txt", "r") as file:
    lines = file.readlines()
    print(f"\nTotal lines: {len(lines)}")


# ============================================
# 2. Different File Modes
# ============================================

print("\n" + "="*60)
print("=== FILE MODES ===\n")

# Append mode
with open("sample.txt", "a") as file:
    file.write("\nAppended line!")

# Read and write mode
with open("sample.txt", "r+") as file:
    content = file.read()
    file.write("\nAdded with r+ mode")

# Verify the changes
with open("sample.txt", "r") as file:
    print("Updated file content:")
    print(file.read())


# ============================================
# 3. Working with File Paths
# ============================================

print("\n" + "="*60)
print("=== FILE PATHS ===\n")

# Current working directory
print(f"Current directory: {os.getcwd()}")

# List files in current directory
print("Files in current directory:")
for item in os.listdir("."):
    if os.path.isfile(item):
        print(f"  📄 {item}")

# Create directory if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")
    print("Created 'data' directory")

# Join paths correctly
data_file = os.path.join("data", "info.txt")
print(f"Data file path: {data_file}")


# ============================================
# 4. Context Managers
# ============================================

print("\n" + "="*60)
print("=== CONTEXT MANAGERS ===\n")

# Proper file handling with context manager
try:
    with open("data/info.txt", "w") as file:
        file.write("This file is in the data directory.\n")
        file.write("Context managers ensure proper closing.")
    print("✅ File written successfully with context manager")
except Exception as e:
    print(f"❌ Error: {e}")

# Reading the file
try:
    with open("data/info.txt", "r") as file:
        content = file.read()
        print("File content:")
        print(content)
except FileNotFoundError:
    print("❌ File not found!")


# ============================================
# 5. JSON File Handling
# ============================================

print("\n" + "="*60)
print("=== JSON HANDLING ===\n")

# Sample data
data = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "hobbies": ["reading", "swimming", "coding"],
    "married": True
}

# Writing JSON to file
with open("data/person.json", "w") as file:
    json.dump(data, file, indent=2)
    print("✅ JSON data written to file")

# Reading JSON from file
with open("data/person.json", "r") as file:
    loaded_data = json.load(file)
    print("Loaded JSON data:")
    print(json.dumps(loaded_data, indent=2))

# JSON string operations
json_string = '{"product": "Laptop", "price": 999.99, "in_stock": true}'
product = json.loads(json_string)
print(f"\nParsed JSON string: {product}")
print(f"Product: {product['product']}, Price: ${product['price']}")


# ============================================
# 6. CSV File Handling
# ============================================

print("\n" + "="*60)
print("=== CSV HANDLING ===\n")

# Sample data for CSV
students = [
    ["Name", "Age", "Grade"],
    ["Alice", 20, "A"],
    ["Bob", 21, "B"],
    ["Charlie", 19, "A"],
    ["Diana", 22, "B+"]
]

# Writing CSV file
with open("data/students.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(students)
    print("✅ CSV file written")

# Reading CSV file
with open("data/students.csv", "r") as file:
    reader = csv.reader(file)
    print("CSV content:")
    for row in reader:
        print(f"  {row}")

# Reading CSV as dictionary
with open("data/students.csv", "r") as file:
    reader = csv.DictReader(file)
    print("\nCSV as dictionaries:")
    for row in reader:
        print(f"  {row}")


# ============================================
# 7. File Information and Metadata
# ============================================

print("\n" + "="*60)
print("=== FILE INFORMATION ===\n")

# File statistics
if os.path.exists("sample.txt"):
    stat = os.stat("sample.txt")
    print(f"File size: {stat.st_size} bytes")
    print(f"Created: {datetime.fromtimestamp(stat.st_ctime)}")
    print(f"Modified: {datetime.fromtimestamp(stat.st_mtime)}")

# Check file existence and type
files_to_check = ["sample.txt", "data", "nonexistent.txt"]
for item in files_to_check:
    if os.path.exists(item):
        if os.path.isfile(item):
            print(f"📄 {item} is a file")
        elif os.path.isdir(item):
            print(f"📁 {item} is a directory")
    else:
        print(f"❌ {item} does not exist")


# ============================================
# 8. Exception Handling with Files
# ============================================

print("\n" + "="*60)
print("=== FILE EXCEPTIONS ===\n")

# Handle file not found
try:
    with open("nonexistent.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("❌ File not found - handled gracefully")

# Handle permission errors
try:
    with open("/root/protected.txt", "w") as file:
        file.write("Trying to write to protected area")
except PermissionError:
    print("❌ Permission denied - handled gracefully")
except Exception as e:
    print(f"❌ Other error: {e}")

# Handle encoding issues
try:
    with open("sample.txt", "r", encoding="utf-8") as file:
        content = file.read()
        print("✅ File read with UTF-8 encoding")
except UnicodeDecodeError:
    print("❌ Encoding error - file may be in different encoding")


# ============================================
# 9. Working with Binary Files
# ============================================

print("\n" + "="*60)
print("=== BINARY FILES ===\n")

# Writing binary data
binary_data = b"Binary data: \x00\x01\x02\x03"
with open("data/binary.dat", "wb") as file:
    file.write(binary_data)
    print("✅ Binary data written")

# Reading binary data
with open("data/binary.dat", "rb") as file:
    read_data = file.read()
    print(f"Read binary data: {read_data}")


# ============================================
# 10. File Processing Patterns
# ============================================

print("\n" + "="*60)
print("=== FILE PROCESSING PATTERNS ===\n")

# Process large files line by line
def process_large_file(filename):
    """Process a large file without loading everything into memory."""
    try:
        with open(filename, "r") as file:
            line_count = 0
            for line in file:
                line_count += 1
                # Process each line here
                if line_count <= 3:  # Show first 3 lines as example
                    print(f"Processing: {line.strip()}")
            print(f"Processed {line_count} lines")
    except FileNotFoundError:
        print("File not found")

# Create a larger sample file
with open("data/large_sample.txt", "w") as file:
    for i in range(100):
        file.write(f"Line {i+1}: Sample data for processing\n")

# Process the file
process_large_file("data/large_sample.txt")


# ============================================
# 11. Temporary Files
# ============================================

print("\n" + "="*60)
print("=== TEMPORARY FILES ===\n")

import tempfile

# Create a temporary file
with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as temp_file:
    temp_file.write("This is temporary data")
    temp_filename = temp_file.name
    print(f"Created temporary file: {temp_filename}")

# Read from temporary file
with open(temp_filename, "r") as file:
    content = file.read()
    print(f"Temporary file content: {content}")

# Clean up
os.unlink(temp_filename)
print("Temporary file deleted")


# ============================================
# Practice Exercise
# ============================================

print("\n" + "="*60)
print("🎯 PRACTICE EXERCISE")
print("="*60)
print("""
Try these exercises:

1. Create a log file that records timestamps and messages
2. Build a configuration file reader that loads settings from JSON
3. Make a file backup utility that copies files with timestamps
4. Implement a simple database using CSV files
5. Create a file encryption/decryption tool
""")

# Clean up sample files
files_to_clean = ["sample.txt", "data/info.txt", "data/person.json", 
                  "data/students.csv", "data/binary.dat", "data/large_sample.txt"]

for file_path in files_to_clean:
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Cleaned up: {file_path}")

if os.path.exists("data") and not os.listdir("data"):
    os.rmdir("data")
    print("Cleaned up: data directory")
