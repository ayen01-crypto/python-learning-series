"""
Lesson 11: Decorators & Closures
Comprehensive Examples
"""

import time
import functools
from typing import Callable, Any


# ============================================
# 1. Closures
# ============================================

print("=== CLOSURES ===\n")

def outer_function(x):
    """Outer function that creates a closure."""
    def inner_function(y):
        """Inner function that captures x from outer scope."""
        return x + y
    return inner_function

# Create closures
add_five = outer_function(5)
add_ten = outer_function(10)

print(f"add_five(3) = {add_five(3)}")
print(f"add_ten(3) = {add_ten(3)}")

# Closure with multiple variables
def create_multiplier(factor):
    """Create a multiplier function."""
    def multiplier(number):
        return number * factor
    return multiplier

double = create_multiplier(2)
triple = create_multiplier(3)

print(f"double(5) = {double(5)}")
print(f"triple(5) = {triple(5)}")

# Closure that maintains state
def create_counter():
    """Create a counter that maintains its state."""
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

counter1 = create_counter()
counter2 = create_counter()

print(f"Counter1: {counter1()}, {counter1()}, {counter1()}")
print(f"Counter2: {counter2()}, {counter2()}")


# ============================================
# 2. Basic Decorators
# ============================================

print("\n" + "="*60)
print("=== BASIC DECORATORS ===\n")

def simple_decorator(func):
    """A simple decorator that adds behavior."""
    def wrapper(*args, **kwargs):
        print("Before function execution")
        result = func(*args, **kwargs)
        print("After function execution")
        return result
    return wrapper

@simple_decorator
def greet(name):
    """Greet someone."""
    print(f"Hello, {name}!")
    return f"Greeting sent to {name}"

result = greet("Alice")
print(f"Return value: {result}")


# ============================================
# 3. Preserving Function Metadata
# ============================================

print("\n" + "="*60)
print("=== PRESERVING METADATA ===\n")

def debug_decorator(func):
    """Decorator without preserving metadata."""
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def better_debug_decorator(func):
    """Decorator that preserves metadata."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@debug_decorator
def original_function():
    """This is the original function."""
    pass

@better_debug_decorator
def improved_function():
    """This is the improved function."""
    pass

print("Without functools.wraps:")
print(f"Name: {original_function.__name__}")
print(f"Doc: {original_function.__doc__}")

print("\nWith functools.wraps:")
print(f"Name: {improved_function.__name__}")
print(f"Doc: {improved_function.__doc__}")


# ============================================
# 4. Decorators with Parameters
# ============================================

print("\n" + "="*60)
print("=== DECORATORS WITH PARAMETERS ===\n")

def repeat(times: int):
    """Decorator that repeats function execution."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper
    return decorator

@repeat(3)
def say_hello(name):
    """Say hello to someone."""
    message = f"Hello, {name}!"
    print(message)
    return message

results = say_hello("Bob")
print(f"Results: {results}")


# ============================================
# 5. Timing Decorator
# ============================================

print("\n" + "="*60)
print("=== TIMING DECORATOR ===\n")

def timer(func):
    """Decorator that measures execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    """A function that takes some time."""
    time.sleep(0.1)
    return "Done!"

result = slow_function()


# ============================================
# 6. Memoization Decorator
# ============================================

print("\n" + "="*60)
print("=== MEMOIZATION DECORATOR ===\n")

def memoize(func):
    """Decorator that caches function results."""
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a key from arguments
        key = str(args) + str(sorted(kwargs.items()))
        
        if key in cache:
            print(f"Cache hit for {func.__name__}")
            return cache[key]
        
        print(f"Computing {func.__name__}")
        result = func(*args, **kwargs)
        cache[key] = result
        return result
    
    # Add cache info method
    wrapper.cache_info = lambda: f"Cache size: {len(cache)}"
    wrapper.cache_clear = lambda: cache.clear()
    
    return wrapper

@memoize
def fibonacci(n):
    """Calculate Fibonacci number recursively."""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print("Calculating fibonacci(10):")
result = fibonacci(10)
print(f"Result: {result}")
print(f"Cache info: {fibonacci.cache_info()}")

print("\nCalling fibonacci(10) again:")
result = fibonacci(10)
print(f"Result: {result}")


# ============================================
# 7. Validation Decorator
# ============================================

print("\n" + "="*60)
print("=== VALIDATION DECORATOR ===\n")

def validate_types(**expected_types):
    """Decorator that validates argument types."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validate types
            for param_name, expected_type in expected_types.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"Parameter '{param_name}' must be of type {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(name=str, age=int)
def create_person(name, age, city="Unknown"):
    """Create a person record."""
    return f"Person: {name}, Age: {age}, City: {city}"

try:
    person = create_person("Alice", 30)
    print(person)
    
    # This will raise an error
    person = create_person("Bob", "thirty")
except TypeError as e:
    print(f"❌ {e}")


# ============================================
# 8. Class Decorators
# ============================================

print("\n" + "="*60)
print("=== CLASS DECORATORS ===\n")

def add_method(method_name, method):
    """Class decorator that adds a method."""
    def decorator(cls):
        setattr(cls, method_name, method)
        return cls
    return decorator

def log_methods(cls):
    """Class decorator that logs method calls."""
    # Get all methods
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if callable(attr) and not attr_name.startswith('_'):
            # Wrap the method
            @functools.wraps(attr)
            def wrapped_method(*args, **kwargs):
                print(f"Calling {attr_name}")
                return attr(*args, **kwargs)
            setattr(cls, attr_name, wrapped_method)
    
    return cls

@log_methods
class Calculator:
    """Simple calculator class."""
    
    def add(self, a, b):
        """Add two numbers."""
        return a + b
    
    def multiply(self, a, b):
        """Multiply two numbers."""
        return a * b

calc = Calculator()
print(f"5 + 3 = {calc.add(5, 3)}")
print(f"4 × 7 = {calc.multiply(4, 7)}")


# ============================================
# 9. Property Decorator
# ============================================

print("\n" + "="*60)
print("=== PROPERTY DECORATOR ===\n")

class Circle:
    """Circle class demonstrating property decorator."""
    
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        """Get radius."""
        return self._radius
    
    @radius.setter
    def radius(self, value):
        """Set radius with validation."""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @property
    def area(self):
        """Calculate area (read-only property)."""
        return 3.14159 * self._radius ** 2
    
    @property
    def diameter(self):
        """Calculate diameter."""
        return 2 * self._radius

circle = Circle(5)
print(f"Radius: {circle.radius}")
print(f"Area: {circle.area:.2f}")
print(f"Diameter: {circle.diameter}")

circle.radius = 10
print(f"New radius: {circle.radius}")
print(f"New area: {circle.area:.2f}")


# ============================================
# 10. Advanced Decorator Patterns
# ============================================

print("\n" + "="*60)
print("=== ADVANCED PATTERNS ===\n")

# Decorator that can be used with or without parentheses
def optional_parentheses_decorator(*args, **kwargs):
    """Decorator that works with or without parentheses."""
    # Check if called with arguments (decorator factory)
    if args and callable(args[0]):
        # Called without parentheses
        func = args[0]
        @functools.wraps(func)
        def wrapper(*func_args, **func_kwargs):
            print("Decorator without parentheses")
            return func(*func_args, **func_kwargs)
        return wrapper
    else:
        # Called with parentheses
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*func_args, **func_kwargs):
                print("Decorator with parentheses")
                if args:
                    print(f"Arguments: {args}")
                if kwargs:
                    print(f"Keyword arguments: {kwargs}")
                return func(*func_args, **func_kwargs)
            return wrapper
        return decorator

@optional_parentheses_decorator
def function1():
    """Function decorated without parentheses."""
    print("Function 1 executed")

@optional_parentheses_decorator("arg1", key="value")
def function2():
    """Function decorated with parentheses."""
    print("Function 2 executed")

print("Calling function1:")
function1()

print("\nCalling function2:")
function2()


# ============================================
# Practice Exercise
# ============================================

print("\n" + "="*60)
print("🎯 PRACTICE EXERCISE")
print("="*60)
print("""
Try these exercises:

1. Create a retry decorator with exponential backoff
2. Build a rate-limiting decorator
3. Implement a decorator that converts function output to JSON
4. Make a decorator that logs function arguments and return values
5. Create a decorator that measures memory usage
""")
