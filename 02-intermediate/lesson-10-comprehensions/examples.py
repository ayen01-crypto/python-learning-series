"""
Lesson 10: List/Dict/Set Comprehensions
Comprehensive Examples
"""

from typing import List, Dict, Set
import time


# ============================================
# 1. List Comprehensions
# ============================================

print("=== LIST COMPREHENSIONS ===\n")

# Basic list comprehension
squares = [x**2 for x in range(10)]
print(f"Squares: {squares}")

# With condition
evens = [x for x in range(20) if x % 2 == 0]
print(f"Even numbers: {evens}")

# With condition and transformation
even_squares = [x**2 for x in range(20) if x % 2 == 0]
print(f"Even squares: {even_squares}")

# Compare with traditional loop
print("\nTraditional loop vs comprehension:")
# Traditional way
result1 = []
for x in range(10):
    if x % 2 == 0:
        result1.append(x**2)

# Comprehension way
result2 = [x**2 for x in range(10) if x % 2 == 0]

print(f"Traditional: {result1}")
print(f"Comprehension: {result2}")
print(f"Results equal: {result1 == result2}")


# ============================================
# 2. Conditional Expressions in Comprehensions
# ============================================

print("\n" + "="*60)
print("=== CONDITIONAL EXPRESSIONS ===\n")

# Ternary operator in comprehension
numbers = range(-5, 6)
processed = [x if x >= 0 else -x for x in numbers]
print(f"Absolute values: {processed}")

# Categorize numbers
categories = ["positive" if x > 0 else "negative" if x < 0 else "zero" for x in numbers]
print(f"Categories: {categories}")

# Process strings
words = ["hello", "world", "python", "comprehension"]
processed_words = [word.upper() if len(word) > 5 else word.lower() for word in words]
print(f"Processed words: {processed_words}")


# ============================================
# 3. Nested List Comprehensions
# ============================================

print("\n" + "="*60)
print("=== NESTED COMPREHENSIONS ===\n")

# Create a matrix
matrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]
print("Matrix:")
for row in matrix:
    print(f"  {row}")

# Flatten a matrix
flattened = [num for row in matrix for num in row]
print(f"Flattened: {flattened}")

# Transpose a matrix
transposed = [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]
print("Transposed matrix:")
for row in transposed:
    print(f"  {row}")

# Complex nested comprehension
coordinates = [(x, y) for x in range(3) for y in range(3) if x + y < 3]
print(f"Coordinates (x+y < 3): {coordinates}")


# ============================================
# 4. Dictionary Comprehensions
# ============================================

print("\n" + "="*60)
print("=== DICTIONARY COMPREHENSIONS ===\n")

# Basic dictionary comprehension
squares_dict = {x: x**2 for x in range(1, 6)}
print(f"Squares dict: {squares_dict}")

# From two lists
keys = ["name", "age", "city"]
values = ["Alice", 30, "New York"]
person = {k: v for k, v in zip(keys, values)}
print(f"Person dict: {person}")

# With conditions
even_squares_dict = {x: x**2 for x in range(1, 11) if x % 2 == 0}
print(f"Even squares dict: {even_squares_dict}")

# Transform keys and values
original = {"apple": 5, "banana": 3, "cherry": 8}
doubled = {f"{k}s": v*2 for k, v in original.items()}
print(f"Doubled: {doubled}")

# Conditional expressions in dict comprehension
grades = {"Alice": 85, "Bob": 92, "Charlie": 78, "Diana": 96}
letter_grades = {name: "A" if score >= 90 else "B" if score >= 80 else "C" 
                for name, score in grades.items()}
print(f"Letter grades: {letter_grades}")


# ============================================
# 5. Set Comprehensions
# ============================================

print("\n" + "="*60)
print("=== SET COMPREHENSIONS ===\n")

# Basic set comprehension
squares_set = {x**2 for x in range(1, 6)}
print(f"Squares set: {squares_set}")

# Unique characters in a string
text = "hello world"
unique_chars = {char for char in text if char != ' '}
print(f"Unique characters: {unique_chars}")

# Even numbers from a list with duplicates
numbers = [1, 2, 2, 3, 3, 4, 4, 5, 5]
unique_evens = {x for x in numbers if x % 2 == 0}
print(f"Unique even numbers: {unique_evens}")

# Set operations with comprehensions
set1 = {x for x in range(10) if x % 2 == 0}  # Even numbers
set2 = {x for x in range(10) if x % 3 == 0}  # Multiples of 3
print(f"Set 1 (even): {set1}")
print(f"Set 2 (multiples of 3): {set2}")
print(f"Union: {set1 | set2}")
print(f"Intersection: {set1 & set2}")
print(f"Difference: {set1 - set2}")


# ============================================
# 6. Generator Expressions
# ============================================

print("\n" + "="*60)
print("=== GENERATOR EXPRESSIONS ===\n")

# Generator expression (lazy evaluation)
squares_gen = (x**2 for x in range(10))
print(f"Generator object: {squares_gen}")
print(f"First few values: {[next(squares_gen) for _ in range(3)]}")

# Memory efficiency comparison
print("\nMemory efficiency:")
# List comprehension - creates entire list in memory
list_comp = [x**2 for x in range(1000)]
print(f"List comprehension size: {len(list_comp)} items")

# Generator expression - creates items on demand
gen_exp = (x**2 for x in range(1000))
print(f"Generator expression: {type(gen_exp)}")
print("Generator creates items on demand - memory efficient!")


# ============================================
# 7. Performance Comparison
# ============================================

print("\n" + "="*60)
print("=== PERFORMANCE COMPARISON ===\n")

def time_function(func, *args, **kwargs):
    """Time a function execution."""
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return result, end - start

# Traditional loop
def traditional_squares(n):
    result = []
    for x in range(n):
        if x % 2 == 0:
            result.append(x**2)
    return result

# List comprehension
def comprehension_squares(n):
    return [x**2 for x in range(n) if x % 2 == 0]

# Test with smaller dataset
n = 10000
traditional_result, traditional_time = time_function(traditional_squares, n)
comprehension_result, comprehension_time = time_function(comprehension_squares, n)

print(f"Traditional loop: {traditional_time:.6f} seconds")
print(f"List comprehension: {comprehension_time:.6f} seconds")
print(f"Comprehension is {traditional_time/comprehension_time:.2f}x faster")
print(f"Results equal: {traditional_result == comprehension_result}")


# ============================================
# 8. Complex Comprehension Examples
# ============================================

print("\n" + "="*60)
print("=== COMPLEX EXAMPLES ===\n")

# Data processing example
students = [
    {"name": "Alice", "grades": [85, 90, 92], "age": 20},
    {"name": "Bob", "grades": [78, 85, 88], "age": 21},
    {"name": "Charlie", "grades": [92, 95, 89], "age": 19},
    {"name": "Diana", "grades": [76, 82, 80], "age": 20}
]

# Calculate average grades
avg_grades = {student["name"]: sum(student["grades"])/len(student["grades"]) 
              for student in students}
print(f"Average grades: {avg_grades}")

# Find top students
top_students = [student["name"] for student in students 
                if sum(student["grades"])/len(student["grades"]) >= 85]
print(f"Top students: {top_students}")

# Group by age
students_by_age = {age: [student["name"] for student in students if student["age"] == age]
                   for age in {student["age"] for student in students}}
print(f"Students by age: {students_by_age}")

# Create report cards
report_cards = {
    student["name"]: {
        "average": sum(student["grades"])/len(student["grades"]),
        "highest": max(student["grades"]),
        "lowest": min(student["grades"])
    }
    for student in students
}
print(f"Report cards: {report_cards}")


# ============================================
# 9. Practical Applications
# ============================================

print("\n" + "="*60)
print("=== PRACTICAL APPLICATIONS ===\n")

# Text processing
text = "The quick brown fox jumps over the lazy dog"
words = text.split()

# Word lengths
word_lengths = {word: len(word) for word in words}
print(f"Word lengths: {word_lengths}")

# Words longer than 4 characters
long_words = [word for word in words if len(word) > 4]
print(f"Long words: {long_words}")

# Unique word frequencies (case-insensitive)
cleaned_words = [word.lower().strip('.,!?') for word in words]
word_freq = {word: cleaned_words.count(word) for word in set(cleaned_words)}
print(f"Word frequencies: {word_freq}")

# File processing simulation
file_lines = [
    "apple,red,fruit",
    "banana,yellow,fruit", 
    "carrot,orange,vegetable",
    "grape,purple,fruit"
]

# Parse CSV-like data
parsed_data = [line.split(',') for line in file_lines]
print(f"Parsed data: {parsed_data}")

# Extract specific columns
names = [row[0] for row in parsed_data]
categories = [row[2] for row in parsed_data]
print(f"Names: {names}")
print(f"Categories: {categories}")

# Filter by category
fruits = [row[0] for row in parsed_data if row[2] == "fruit"]
print(f"Fruits: {fruits}")


# ============================================
# 10. Best Practices and Pitfalls
# ============================================

print("\n" + "="*60)
print("=== BEST PRACTICES ===\n")

print("""
Best Practices for Comprehensions:

1. Keep them readable - don't make them too complex
2. Use comprehensions for simple transformations and filtering
3. Prefer comprehensions over map() and filter() for readability
4. Use generator expressions for large datasets
5. Consider using loops for complex logic
6. Use parentheses for generator expressions
7. Combine with built-in functions like sum(), max(), min()
""")

# Good example - readable
evens_squared = [x**2 for x in range(20) if x % 2 == 0]
print(f"Evens squared: {evens_squared}")

# Bad example - too complex (avoid this)
# complex_result = [x**2 if x % 2 == 0 else -x**2 for x in range(20) if x % 3 == 0]

# Better as a loop
print("\nWhen to use loops instead:")
complex_data = []
for x in range(20):
    if x % 3 == 0:
        if x % 2 == 0:
            complex_data.append(x**2)
        else:
            complex_data.append(-x**2)
print(f"Complex logic with loop: {complex_data}")


# ============================================
# Practice Exercise
# ============================================

print("\n" + "="*60)
print("🎯 PRACTICE EXERCISE")
print("="*60)
print("""
Try these exercises:

1. Create a matrix transposition tool using nested comprehensions
2. Build a word frequency analyzer for text files
3. Implement a data filtering pipeline for CSV data
4. Make a social media hashtag extractor
5. Create a financial portfolio analyzer with comprehensions
""")
