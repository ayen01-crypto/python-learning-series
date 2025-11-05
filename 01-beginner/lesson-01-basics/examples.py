"""
Lesson 01: Python Basics & Setup
Examples and Demonstrations
"""

# ============================================
# 1. Your First Python Program
# ============================================

print("Hello, World!")
print("Welcome to Python Programming!")


# ============================================
# 2. Comments in Python
# ============================================

# This is a single-line comment

"""
This is a multi-line comment
or docstring. It can span
multiple lines.
"""


# ============================================
# 3. Basic Print Statements
# ============================================

# Printing different types of data
print(42)                    # Integer
print(3.14)                  # Float
print("Python")              # String
print(True)                  # Boolean

# Multiple items in one print
print("I", "love", "Python")

# Print with separator
print("apple", "banana", "cherry", sep=", ")

# Print without newline
print("Hello", end=" ")
print("World!")


# ============================================
# 4. Getting User Input
# ============================================

# Basic input
name = input("What is your name? ")
print("Hello, " + name + "!")

# Input always returns a string
age_str = input("How old are you? ")
print("You entered:", age_str)
print("Type:", type(age_str))


# ============================================
# 5. Python as a Calculator
# ============================================

print("\n=== Python Calculator ===")
print(5 + 3)        # Addition: 8
print(10 - 4)       # Subtraction: 6
print(6 * 7)        # Multiplication: 42
print(15 / 3)       # Division: 5.0
print(17 // 5)      # Floor division: 3
print(17 % 5)       # Modulus: 2
print(2 ** 8)       # Exponentiation: 256


# ============================================
# 6. The Python Interactive Shell (REPL)
# ============================================

"""
Open your terminal/command prompt and type: python
Then try these commands:
>>> 2 + 2
>>> print("Hello from REPL")
>>> quit()
"""


# ============================================
# 7. Basic String Operations
# ============================================

print("\n=== String Operations ===")
greeting = "Hello"
name = "Python"

# Concatenation
full_greeting = greeting + " " + name + "!"
print(full_greeting)

# String repetition
print("=" * 30)
print("Python! " * 3)


# ============================================
# 8. Escape Characters
# ============================================

print("\n=== Escape Characters ===")
print("Line 1\nLine 2")              # Newline
print("Tab\there")                   # Tab
print("He said, \"Python is awesome!\"")  # Quotes
print("Path: C:\\Users\\Python")     # Backslash


# ============================================
# 9. F-Strings (Preview - more in next lesson)
# ============================================

print("\n=== F-Strings Preview ===")
language = "Python"
year = 1991
print(f"{language} was created in {year}")


# ============================================
# 10. Checking Python Version
# ============================================

import sys
print(f"\nPython version: {sys.version}")


# ============================================
# Practice Exercise
# ============================================

print("\n" + "="*50)
print("PRACTICE: Try modifying the values above!")
print("Experiment with different print statements!")
print("="*50)
