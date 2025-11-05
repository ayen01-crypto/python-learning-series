"""
Lesson 04: Functions & Scope
Comprehensive Examples
"""

# ============================================
# 1. Basic Functions
# ============================================

print("=== BASIC FUNCTIONS ===\n")

def greet():
    """Simple function without parameters."""
    print("Hello, World!")

greet()  # Call the function


# ============================================
# 2. Functions with Parameters
# ============================================

print("\n" + "="*50)
print("=== FUNCTIONS WITH PARAMETERS ===\n")

def greet_person(name):
    """Function with one parameter."""
    print(f"Hello, {name}!")

greet_person("Alice")
greet_person("Bob")

def add_numbers(a, b):
    """Function with multiple parameters."""
    result = a + b
    print(f"{a} + {b} = {result}")

add_numbers(5, 3)
add_numbers(10, 20)


# ============================================
# 3. Return Values
# ============================================

print("\n" + "="*50)
print("=== RETURN VALUES ===\n")

def multiply(x, y):
    """Function that returns a value."""
    return x * y

result = multiply(4, 5)
print(f"4 × 5 = {result}")

# Multiple return values
def get_min_max(numbers):
    """Returns tuple of minimum and maximum."""
    return min(numbers), max(numbers)

nums = [3, 7, 2, 9, 1]
minimum, maximum = get_min_max(nums)
print(f"List: {nums}")
print(f"Min: {minimum}, Max: {maximum}")


# ============================================
# 4. Default Parameters
# ============================================

print("\n" + "="*50)
print("=== DEFAULT PARAMETERS ===\n")

def greet_with_title(name, title="Mr."):
    """Function with default parameter."""
    print(f"Hello, {title} {name}!")

greet_with_title("Smith")  # Uses default
greet_with_title("Johnson", "Dr.")  # Overrides default


def power(base, exponent=2):
    """Calculate power with default exponent."""
    return base ** exponent

print(f"5² = {power(5)}")
print(f"2³ = {power(2, 3)}")


# ============================================
# 5. Keyword Arguments
# ============================================

print("\n" + "="*50)
print("=== KEYWORD ARGUMENTS ===\n")

def describe_person(name, age, city):
    """Function demonstrating keyword arguments."""
    print(f"{name} is {age} years old and lives in {city}")

# Positional arguments
describe_person("Alice", 30, "New York")

# Keyword arguments (order doesn't matter)
describe_person(age=25, city="London", name="Bob")

# Mix of both
describe_person("Charlie", city="Paris", age=35)


# ============================================
# 6. Variable-Length Arguments (*args)
# ============================================

print("\n" + "="*50)
print("=== *ARGS (VARIABLE POSITIONAL) ===\n")

def sum_all(*numbers):
    """Sum any number of arguments."""
    total = sum(numbers)
    return total

print(f"sum_all(1, 2, 3) = {sum_all(1, 2, 3)}")
print(f"sum_all(10, 20, 30, 40) = {sum_all(10, 20, 30, 40)}")

def print_args(*args):
    """Print all arguments."""
    print(f"Received {len(args)} arguments:")
    for i, arg in enumerate(args, 1):
        print(f"  {i}. {arg}")

print_args("apple", "banana", "cherry", "date")


# ============================================
# 7. Keyword Variable-Length Arguments (**kwargs)
# ============================================

print("\n" + "="*50)
print("=== **KWARGS (VARIABLE KEYWORD) ===\n")

def print_info(**kwargs):
    """Print keyword arguments."""
    print("Information:")
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

print_info(name="Alice", age=30, city="NYC", job="Engineer")


def create_profile(name, **details):
    """Create profile with required name and optional details."""
    print(f"\nProfile for {name}:")
    for key, value in details.items():
        print(f"  {key.title()}: {value}")

create_profile("Bob", age=25, email="bob@email.com", country="USA")


# ============================================
# 8. Combining *args and **kwargs
# ============================================

print("\n" + "="*50)
print("=== COMBINING *ARGS AND **KWARGS ===\n")

def flexible_function(*args, **kwargs):
    """Function accepting both variable arguments."""
    print(f"Positional args: {args}")
    print(f"Keyword args: {kwargs}")

flexible_function(1, 2, 3, name="Alice", age=30)


# ============================================
# 9. Local vs Global Scope
# ============================================

print("\n" + "="*50)
print("=== VARIABLE SCOPE ===\n")

global_var = "I'm global"

def scope_demo():
    """Demonstrate local scope."""
    local_var = "I'm local"
    print(f"Inside function - Global: {global_var}")
    print(f"Inside function - Local: {local_var}")

scope_demo()
print(f"Outside function - Global: {global_var}")
# print(local_var)  # This would cause an error!


# ============================================
# 10. Global Keyword
# ============================================

print("\n" + "="*50)
print("=== GLOBAL KEYWORD ===\n")

counter = 0

def increment():
    """Modify global variable."""
    global counter
    counter += 1
    print(f"Counter: {counter}")

increment()
increment()
increment()


# ============================================
# 11. Nonlocal Keyword
# ============================================

print("\n" + "="*50)
print("=== NONLOCAL KEYWORD ===\n")

def outer():
    """Outer function with nested function."""
    x = 10
    
    def inner():
        """Inner function modifying outer's variable."""
        nonlocal x
        x += 5
        print(f"Inner x: {x}")
    
    print(f"Before inner: x = {x}")
    inner()
    print(f"After inner: x = {x}")

outer()


# ============================================
# 12. Lambda Functions
# ============================================

print("\n" + "="*50)
print("=== LAMBDA FUNCTIONS ===\n")

# Simple lambda
square = lambda x: x ** 2
print(f"square(5) = {square(5)}")

# Lambda with multiple arguments
add = lambda a, b: a + b
print(f"add(3, 7) = {add(3, 7)}")

# Lambda in sorted
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
sorted_students = sorted(students, key=lambda x: x[1], reverse=True)
print(f"\nStudents sorted by score: {sorted_students}")


# ============================================
# 13. Higher-Order Functions
# ============================================

print("\n" + "="*50)
print("=== HIGHER-ORDER FUNCTIONS ===\n")

def apply_operation(func, value):
    """Function that takes another function as argument."""
    return func(value)

result = apply_operation(lambda x: x * 2, 10)
print(f"Double 10: {result}")

# map() example
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(f"\nOriginal: {numbers}")
print(f"Squared: {squared}")

# filter() example
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Even numbers: {even_numbers}")


# ============================================
# 14. Recursion
# ============================================

print("\n" + "="*50)
print("=== RECURSION ===\n")

def factorial(n):
    """Calculate factorial recursively."""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

print(f"5! = {factorial(5)}")
print(f"7! = {factorial(7)}")


def fibonacci(n):
    """Get nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(f"\nFirst 10 Fibonacci numbers:")
for i in range(10):
    print(fibonacci(i), end=" ")
print()


# ============================================
# 15. Docstrings and Type Hints
# ============================================

print("\n" + "="*50)
print("=== DOCSTRINGS AND TYPE HINTS ===\n")

def calculate_area(length: float, width: float) -> float:
    """
    Calculate the area of a rectangle.
    
    Args:
        length (float): Length of the rectangle
        width (float): Width of the rectangle
    
    Returns:
        float: Area of the rectangle
    """
    return length * width

area = calculate_area(5.0, 3.0)
print(f"Area: {area}")

# Access docstring
print(f"\nDocstring:\n{calculate_area.__doc__}")


# ============================================
# Practice Exercise
# ============================================

print("\n" + "="*50)
print("🎯 PRACTICE EXERCISE")
print("="*50)
print("""
Create these functions:

1. is_prime(n) - Check if number is prime
2. reverse_string(s) - Reverse a string
3. count_vowels(s) - Count vowels in a string
4. celsius_to_fahrenheit(c) - Temperature conversion
5. find_max(*numbers) - Find maximum using *args
""")
