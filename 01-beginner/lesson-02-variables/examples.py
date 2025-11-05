"""
Lesson 02: Variables, Data Types & Operators
Comprehensive Examples
"""

# ============================================
# 1. Variables and Assignment
# ============================================

print("=== VARIABLES ===\n")

# Basic variable assignment
x = 10
name = "Alice"
is_active = True

print(f"x = {x}")
print(f"name = {name}")
print(f"is_active = {is_active}")

# Multiple assignment
a, b, c = 1, 2, 3
print(f"\nMultiple assignment: a={a}, b={b}, c={c}")

# Same value to multiple variables
x = y = z = 100
print(f"Same value: x={x}, y={y}, z={z}")

# Swapping variables
x, y = 5, 10
print(f"\nBefore swap: x={x}, y={y}")
x, y = y, x
print(f"After swap: x={x}, y={y}")


# ============================================
# 2. Data Types
# ============================================

print("\n" + "="*50)
print("=== DATA TYPES ===\n")

# Integer
age = 25
print(f"Integer: {age}, Type: {type(age)}")

# Float
price = 19.99
print(f"Float: {price}, Type: {type(price)}")

# String
message = "Hello, Python!"
print(f"String: {message}, Type: {type(message)}")

# Boolean
is_python_fun = True
print(f"Boolean: {is_python_fun}, Type: {type(is_python_fun)}")

# None
nothing = None
print(f"None: {nothing}, Type: {type(nothing)}")

# Complex (advanced numeric type)
complex_num = 3 + 4j
print(f"Complex: {complex_num}, Type: {type(complex_num)}")


# ============================================
# 3. Type Conversion (Casting)
# ============================================

print("\n" + "="*50)
print("=== TYPE CONVERSION ===\n")

# String to Integer
str_num = "42"
int_num = int(str_num)
print(f"String '{str_num}' → Integer {int_num}")

# Integer to Float
int_val = 10
float_val = float(int_val)
print(f"Integer {int_val} → Float {float_val}")

# Float to Integer (truncates decimal)
float_val = 3.99
int_val = int(float_val)
print(f"Float {float_val} → Integer {int_val}")

# Number to String
num = 100
str_num = str(num)
print(f"Number {num} → String '{str_num}'")

# String to Boolean (non-empty = True)
print(f"bool('Hello') = {bool('Hello')}")
print(f"bool('') = {bool('')}")
print(f"bool(0) = {bool(0)}")
print(f"bool(42) = {bool(42)}")


# ============================================
# 4. Arithmetic Operators
# ============================================

print("\n" + "="*50)
print("=== ARITHMETIC OPERATORS ===\n")

a, b = 17, 5

print(f"a = {a}, b = {b}")
print(f"Addition: {a} + {b} = {a + b}")
print(f"Subtraction: {a} - {b} = {a - b}")
print(f"Multiplication: {a} * {b} = {a * b}")
print(f"Division: {a} / {b} = {a / b}")
print(f"Floor Division: {a} // {b} = {a // b}")
print(f"Modulus: {a} % {b} = {a % b}")
print(f"Exponentiation: {a} ** 2 = {a ** 2}")


# ============================================
# 5. Comparison Operators
# ============================================

print("\n" + "="*50)
print("=== COMPARISON OPERATORS ===\n")

x, y = 10, 20

print(f"x = {x}, y = {y}")
print(f"x == y: {x == y}")  # Equal
print(f"x != y: {x != y}")  # Not equal
print(f"x > y: {x > y}")    # Greater than
print(f"x < y: {x < y}")    # Less than
print(f"x >= y: {x >= y}")  # Greater than or equal
print(f"x <= y: {x <= y}")  # Less than or equal


# ============================================
# 6. Logical Operators
# ============================================

print("\n" + "="*50)
print("=== LOGICAL OPERATORS ===\n")

is_sunny = True
is_warm = True
is_raining = False

print(f"is_sunny = {is_sunny}")
print(f"is_warm = {is_warm}")
print(f"is_raining = {is_raining}")
print()
print(f"is_sunny AND is_warm: {is_sunny and is_warm}")
print(f"is_sunny OR is_raining: {is_sunny or is_raining}")
print(f"NOT is_raining: {not is_raining}")


# ============================================
# 7. Assignment Operators
# ============================================

print("\n" + "="*50)
print("=== ASSIGNMENT OPERATORS ===\n")

counter = 10
print(f"Initial: counter = {counter}")

counter += 5  # counter = counter + 5
print(f"After += 5: counter = {counter}")

counter -= 3  # counter = counter - 3
print(f"After -= 3: counter = {counter}")

counter *= 2  # counter = counter * 2
print(f"After *= 2: counter = {counter}")

counter //= 4  # counter = counter // 4
print(f"After //= 4: counter = {counter}")


# ============================================
# 8. String Operations
# ============================================

print("\n" + "="*50)
print("=== STRING OPERATIONS ===\n")

first_name = "John"
last_name = "Doe"

# Concatenation
full_name = first_name + " " + last_name
print(f"Full name: {full_name}")

# Repetition
print(f"Repeat: {'Ha' * 5}")

# String length
print(f"Length of '{full_name}': {len(full_name)}")

# String methods
text = "python programming"
print(f"\nOriginal: {text}")
print(f"Upper: {text.upper()}")
print(f"Title: {text.title()}")
print(f"Capitalize: {text.capitalize()}")
print(f"Replace: {text.replace('python', 'Python')}")


# ============================================
# 9. String Indexing and Slicing
# ============================================

print("\n" + "="*50)
print("=== STRING INDEXING & SLICING ===\n")

word = "Python"
print(f"Word: {word}")
print(f"First character: {word[0]}")
print(f"Last character: {word[-1]}")
print(f"First 3 characters: {word[0:3]}")
print(f"Last 3 characters: {word[-3:]}")
print(f"Reverse: {word[::-1]}")


# ============================================
# 10. F-Strings (Formatted Strings)
# ============================================

print("\n" + "="*50)
print("=== F-STRINGS ===\n")

name = "Alice"
age = 30
height = 5.6

# Basic f-string
print(f"My name is {name} and I am {age} years old.")

# Expressions in f-strings
print(f"Next year, I'll be {age + 1} years old.")

# Formatting numbers
pi = 3.14159265359
print(f"Pi to 2 decimal places: {pi:.2f}")

price = 1234.5
print(f"Price: ${price:,.2f}")

# Alignment
print(f"{'Left':<10}|{'Center':^10}|{'Right':>10}")


# ============================================
# 11. Input with Type Conversion
# ============================================

print("\n" + "="*50)
print("=== USER INPUT WITH CONVERSION ===\n")

print("Example of getting numeric input:")
print('age = int(input("Enter your age: "))')
print('height = float(input("Enter your height in meters: "))')
print()
print("Note: Run this interactively to test!")


# ============================================
# 12. Constants (Convention)
# ============================================

print("\n" + "="*50)
print("=== CONSTANTS ===\n")

# By convention, use UPPERCASE for constants
PI = 3.14159
MAX_SPEED = 120
COMPANY_NAME = "TechCorp"

print(f"PI = {PI}")
print(f"MAX_SPEED = {MAX_SPEED}")
print(f"COMPANY_NAME = {COMPANY_NAME}")


# ============================================
# Practice Exercise
# ============================================

print("\n" + "="*50)
print("🎯 PRACTICE EXERCISE")
print("="*50)
print("""
Try these on your own:
1. Create variables for your personal info (name, age, city)
2. Calculate your age in months and days
3. Create a sentence using f-strings
4. Swap two variables without using a third variable
5. Convert temperature from Celsius to Fahrenheit
""")
