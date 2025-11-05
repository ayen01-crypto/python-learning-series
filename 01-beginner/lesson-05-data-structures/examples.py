"""
Lesson 05: Data Structures
Comprehensive Examples: Lists, Tuples, Sets, Dictionaries
"""

# ============================================
# 1. LISTS - Ordered, Mutable Collections
# ============================================

print("=== LISTS ===\n")

# Creating lists
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
empty = []

print(f"Fruits: {fruits}")
print(f"Numbers: {numbers}")
print(f"Mixed types: {mixed}")

# Accessing elements (0-indexed)
print(f"\nFirst fruit: {fruits[0]}")
print(f"Last fruit: {fruits[-1]}")

# Slicing
print(f"First two fruits: {fruits[0:2]}")
print(f"Last two fruits: {fruits[-2:]}")

# List methods
fruits.append("orange")  # Add to end
print(f"\nAfter append: {fruits}")

fruits.insert(1, "mango")  # Insert at index
print(f"After insert: {fruits}")

fruits.remove("banana")  # Remove by value
print(f"After remove: {fruits}")

popped = fruits.pop()  # Remove and return last
print(f"Popped: {popped}, Remaining: {fruits}")

# List operations
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = list1 + list2
print(f"\nCombined: {combined}")
print(f"Repeated: {list1 * 3}")

# List length and membership
print(f"\nLength: {len(fruits)}")
print(f"'apple' in fruits: {'apple' in fruits}")

# Sorting
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort()
print(f"\nSorted: {numbers}")

numbers.sort(reverse=True)
print(f"Reverse sorted: {numbers}")

# List comprehension (preview)
squares = [x**2 for x in range(1, 6)]
print(f"\nSquares: {squares}")


# ============================================
# 2. TUPLES - Ordered, Immutable Collections
# ============================================

print("\n" + "="*60)
print("=== TUPLES ===\n")

# Creating tuples
coordinates = (10, 20)
person = ("Alice", 30, "Engineer")
single = (42,)  # Note the comma!
empty_tuple = ()

print(f"Coordinates: {coordinates}")
print(f"Person: {person}")

# Accessing elements
print(f"\nFirst coordinate: {coordinates[0]}")
print(f"Name: {person[0]}, Age: {person[1]}")

# Tuple unpacking
x, y = coordinates
print(f"\nUnpacked: x={x}, y={y}")

name, age, job = person
print(f"Person details: {name}, {age}, {job}")

# Tuples are immutable
# coordinates[0] = 15  # This would raise an error!

# Tuple methods
numbers = (1, 2, 3, 2, 4, 2, 5)
print(f"\nCount of 2: {numbers.count(2)}")
print(f"Index of 3: {numbers.index(3)}")

# When to use tuples
# 1. Data that shouldn't change
RGB_RED = (255, 0, 0)
print(f"\nRGB Red: {RGB_RED}")

# 2. Multiple return values
def get_min_max(nums):
    return min(nums), max(nums)

minimum, maximum = get_min_max([3, 7, 1, 9, 2])
print(f"Min: {minimum}, Max: {maximum}")


# ============================================
# 3. SETS - Unordered, Unique Collections
# ============================================

print("\n" + "="*60)
print("=== SETS ===\n")

# Creating sets
fruits_set = {"apple", "banana", "cherry"}
numbers_set = {1, 2, 3, 4, 5}
from_list = set([1, 2, 2, 3, 3, 4])  # Duplicates removed
empty_set = set()  # Note: {} creates a dict!

print(f"Fruits set: {fruits_set}")
print(f"From list with duplicates: {from_list}")

# Adding and removing
fruits_set.add("orange")
print(f"\nAfter add: {fruits_set}")

fruits_set.remove("banana")  # Raises error if not found
print(f"After remove: {fruits_set}")

fruits_set.discard("grape")  # No error if not found
print(f"After discard (grape not in set): {fruits_set}")

# Set operations
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}

print(f"\nSet 1: {set1}")
print(f"Set 2: {set2}")
print(f"Union: {set1 | set2}")
print(f"Intersection: {set1 & set2}")
print(f"Difference (1-2): {set1 - set2}")
print(f"Symmetric difference: {set1 ^ set2}")

# Set membership (very fast!)
print(f"\n5 in set1: {5 in set1}")

# Removing duplicates from list
original = [1, 2, 2, 3, 3, 4, 4, 5]
unique = list(set(original))
print(f"\nOriginal: {original}")
print(f"Unique: {unique}")


# ============================================
# 4. DICTIONARIES - Key-Value Pairs
# ============================================

print("\n" + "="*60)
print("=== DICTIONARIES ===\n")

# Creating dictionaries
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "job": "Engineer"
}

print(f"Person: {person}")

# Accessing values
print(f"\nName: {person['name']}")
print(f"Age: {person.get('age')}")
print(f"Country: {person.get('country', 'Unknown')}")  # Default value

# Adding/updating
person["email"] = "alice@email.com"
person["age"] = 31
print(f"\nUpdated: {person}")

# Removing
del person["city"]
print(f"After deleting city: {person}")

removed = person.pop("job")
print(f"Removed job: {removed}")

# Dictionary methods
print(f"\nKeys: {person.keys()}")
print(f"Values: {person.values()}")
print(f"Items: {person.items()}")

# Iterating through dictionary
print("\nIterating:")
for key, value in person.items():
    print(f"  {key}: {value}")

# Nested dictionaries
students = {
    "S001": {"name": "Alice", "grade": 85},
    "S002": {"name": "Bob", "grade": 92},
    "S003": {"name": "Charlie", "grade": 78}
}

print(f"\nStudent S002: {students['S002']}")
print(f"Bob's grade: {students['S002']['grade']}")

# Dictionary comprehension
squares_dict = {x: x**2 for x in range(1, 6)}
print(f"\nSquares dictionary: {squares_dict}")


# ============================================
# 5. NESTED DATA STRUCTURES
# ============================================

print("\n" + "="*60)
print("=== NESTED DATA STRUCTURES ===\n")

# List of dictionaries
inventory = [
    {"item": "apple", "quantity": 50, "price": 0.5},
    {"item": "banana", "quantity": 30, "price": 0.3},
    {"item": "cherry", "quantity": 20, "price": 1.0}
]

print("Inventory:")
for product in inventory:
    print(f"  {product['item']}: {product['quantity']} @ ${product['price']}")

# Dictionary of lists
grades = {
    "Alice": [85, 90, 92],
    "Bob": [78, 85, 88],
    "Charlie": [92, 95, 89]
}

print(f"\nAlice's grades: {grades['Alice']}")
print(f"Alice's average: {sum(grades['Alice']) / len(grades['Alice']):.1f}")


# ============================================
# 6. COMMON OPERATIONS
# ============================================

print("\n" + "="*60)
print("=== COMMON OPERATIONS ===\n")

# Finding maximum/minimum
numbers = [45, 23, 67, 12, 89, 34]
print(f"List: {numbers}")
print(f"Max: {max(numbers)}, Min: {min(numbers)}")

# Sorting
print(f"Sorted: {sorted(numbers)}")
print(f"Original unchanged: {numbers}")

# Reversing
print(f"Reversed: {numbers[::-1]}")

# Counting
letters = ['a', 'b', 'a', 'c', 'a', 'b']
print(f"\nLetters: {letters}")
print(f"Count of 'a': {letters.count('a')}")

# Finding index
print(f"Index of 'c': {letters.index('c')}")

# List to set to list (remove duplicates, maintain uniqueness)
unique_letters = list(set(letters))
print(f"Unique letters: {unique_letters}")


# ============================================
# 7. COPYING DATA STRUCTURES
# ============================================

print("\n" + "="*60)
print("=== COPYING ===\n")

# Shallow copy
original_list = [1, 2, 3]
shallow_copy = original_list.copy()
shallow_copy2 = original_list[:]

print(f"Original: {original_list}")
print(f"Shallow copy: {shallow_copy}")

shallow_copy.append(4)
print(f"After modifying copy: Original={original_list}, Copy={shallow_copy}")

# Deep copy (for nested structures)
import copy

nested = [[1, 2], [3, 4]]
deep = copy.deepcopy(nested)
deep[0].append(999)

print(f"\nNested original: {nested}")
print(f"Deep copy modified: {deep}")


# ============================================
# 8. ADVANCED LIST OPERATIONS
# ============================================

print("\n" + "="*60)
print("=== ADVANCED LIST OPERATIONS ===\n")

# List comprehension with condition
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = [x for x in numbers if x % 2 == 0]
print(f"Even numbers: {evens}")

# Nested list comprehension
matrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]
print(f"\nMultiplication table:")
for row in matrix:
    print(row)

# zip() - combine lists
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]
combined = list(zip(names, scores))
print(f"\nZipped: {combined}")

# Create dictionary from two lists
grade_dict = dict(zip(names, scores))
print(f"Grade dictionary: {grade_dict}")

# enumerate() - index and value
print("\nEnumerated:")
for i, name in enumerate(names, 1):
    print(f"  {i}. {name}")


# ============================================
# 9. CHOOSING THE RIGHT DATA STRUCTURE
# ============================================

print("\n" + "="*60)
print("=== CHOOSING THE RIGHT STRUCTURE ===\n")

print("""
When to use each:

📋 LIST - Use when:
  • Order matters
  • Need to modify elements
  • Allow duplicates
  • Need indexing
  Example: Shopping cart, task list

📦 TUPLE - Use when:
  • Data shouldn't change
  • Multiple return values
  • Dictionary keys (lists can't be keys)
  Example: Coordinates, RGB colors

🎯 SET - Use when:
  • Need unique elements
  • Fast membership testing
  • Set operations (union, intersection)
  Example: Unique users, tags

📚 DICTIONARY - Use when:
  • Key-value mapping
  • Fast lookups by key
  • Associating data
  Example: User profiles, configurations
""")


# ============================================
# Practice Exercise
# ============================================

print("\n" + "="*60)
print("🎯 PRACTICE EXERCISE")
print("="*60)
print("""
Try these challenges:

1. Create a list of 5 numbers and find their average
2. Use a tuple to store RGB color values
3. Remove duplicates from a list using a set
4. Create a dictionary for a student with name, age, and grades (list)
5. Build a nested structure: list of student dictionaries
6. Use list comprehension to get all numbers divisible by 3 from 1-30
7. Create a dictionary mapping names to phone numbers
8. Find common elements between two lists using sets
""")
