"""
Lesson 12: Generators & Iterators
Comprehensive Examples
"""

import time
from typing import Iterator, Generator


# ============================================
# 1. Basic Iterators
# ============================================

print("=== BASIC ITERATORS ===\n")

# Simple iterator class
class CountDown:
    """Iterator that counts down from a number."""
    
    def __init__(self, start: int):
        self.start = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.start <= 0:
            raise StopIteration
        self.start -= 1
        return self.start + 1

# Using the iterator
print("Countdown from 5:")
for num in CountDown(5):
    print(f"  {num}")

# Iterator with state
class FibonacciIterator:
    """Iterator that generates Fibonacci numbers."""
    
    def __init__(self, max_count: int = 10):
        self.max_count = max_count
        self.count = 0
        self.a, self.b = 0, 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.count >= self.max_count:
            raise StopIteration
        
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return result

print("\nFirst 8 Fibonacci numbers:")
fib_iter = FibonacciIterator(8)
for num in fib_iter:
    print(f"  {num}")


# ============================================
# 2. Generator Functions
# ============================================

print("\n" + "="*60)
print("=== GENERATOR FUNCTIONS ===\n")

def simple_generator():
    """Simple generator function."""
    yield 1
    yield 2
    yield 3

print("Simple generator:")
gen = simple_generator()
print(f"  First value: {next(gen)}")
print(f"  Second value: {next(gen)}")
print(f"  Third value: {next(gen)}")

# Generator with loop
def countdown_generator(start: int):
    """Generator that counts down."""
    while start > 0:
        yield start
        start -= 1

print("\nCountdown generator:")
for num in countdown_generator(3):
    print(f"  {num}")

# Generator with complex logic
def even_numbers(max_num: int):
    """Generate even numbers up to max_num."""
    current = 0
    while current <= max_num:
        if current % 2 == 0:
            yield current
        current += 1

print("\nEven numbers up to 10:")
evens = even_numbers(10)
print(f"  {list(evens)}")


# ============================================
# 3. Generator Expressions
# ============================================

print("\n" + "="*60)
print("=== GENERATOR EXPRESSIONS ===\n")

# Generator expression vs list comprehension
print("Memory comparison:")

# List comprehension - creates entire list in memory
list_comp = [x**2 for x in range(1000)]
print(f"  List comprehension size: {len(list_comp)} items")

# Generator expression - creates items on demand
gen_exp = (x**2 for x in range(1000))
print(f"  Generator expression: {type(gen_exp)}")
print(f"  First few values: {[next(gen_exp) for _ in range(5)]}")

# Generator expression with filtering
squares_of_evens = (x**2 for x in range(20) if x % 2 == 0)
print(f"\nSquares of even numbers: {list(squares_of_evens)}")


# ============================================
# 4. Advanced Generator Features
# ============================================

print("\n" + "="*60)
print("=== ADVANCED GENERATOR FEATURES ===\n")

# Generator with send()
def echo_generator():
    """Generator that can receive values."""
    received = yield "Ready"
    while received is not None:
        received = yield f"Echo: {received}"

echo_gen = echo_generator()
print(f"  {next(echo_gen)}")  # Prime the generator
print(f"  {echo_gen.send('Hello')}")
print(f"  {echo_gen.send('World')}")

# Generator with throw()
def error_handling_generator():
    """Generator that handles exceptions."""
    try:
        yield "Start"
        yield "Middle"
        yield "End"
    except ValueError as e:
        yield f"Caught exception: {e}"

error_gen = error_handling_generator()
print(f"  {next(error_gen)}")
print(f"  {next(error_gen)}")
# error_gen.throw(ValueError, "Test error")  # This would send an exception

# Generator with close()
def closable_generator():
    """Generator that can be closed."""
    try:
        yield "First"
        yield "Second"
        yield "Third"
    except GeneratorExit:
        print("  Generator closed")
        raise

close_gen = closable_generator()
print(f"  {next(close_gen)}")
close_gen.close()


# ============================================
# 5. Yield From (Delegation)
# ============================================

print("\n" + "="*60)
print("=== YIELD FROM ===\n")

def sub_generator():
    """Sub-generator."""
    yield 1
    yield 2
    yield 3

def main_generator():
    """Main generator that delegates to sub-generator."""
    yield 0
    yield from sub_generator()
    yield 4

print("Yield from example:")
for value in main_generator():
    print(f"  {value}")

# Chaining generators
def number_generator(start, end):
    """Generate numbers in a range."""
    for i in range(start, end + 1):
        yield i

def range_generator():
    """Generate multiple ranges."""
    yield from number_generator(1, 3)
    yield from number_generator(10, 12)
    yield from number_generator(20, 22)

print("\nChained generators:")
print(f"  {list(range_generator())}")


# ============================================
# 6. Infinite Generators
# ============================================

print("\n" + "="*60)
print("=== INFINITE GENERATORS ===\n")

def infinite_counter(start: int = 0):
    """Infinite counter generator."""
    current = start
    while True:
        yield current
        current += 1

# Use with islice to limit
from itertools import islice

counter = infinite_counter(10)
first_5 = list(islice(counter, 5))
print(f"First 5 numbers from infinite counter: {first_5}")

# Fibonacci generator (infinite)
def fibonacci_generator():
    """Infinite Fibonacci generator."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci_generator()
first_10_fib = list(islice(fib, 10))
print(f"First 10 Fibonacci numbers: {first_10_fib}")


# ============================================
# 7. Practical Generator Examples
# ============================================

print("\n" + "="*60)
print("=== PRACTICAL EXAMPLES ===\n")

# File processing generator
def read_lines(filename: str):
    """Generator that reads file lines."""
    try:
        with open(filename, 'r') as f:
            for line in f:
                yield line.strip()
    except FileNotFoundError:
        yield f"File {filename} not found"

# Create a sample file
with open("sample.txt", "w") as f:
    f.write("Line 1\nLine 2\nLine 3\n")

print("File reading generator:")
for line in read_lines("sample.txt"):
    print(f"  {line}")

# Data processing pipeline
def filter_numbers(numbers):
    """Filter even numbers."""
    for num in numbers:
        if num % 2 == 0:
            yield num

def square_numbers(numbers):
    """Square numbers."""
    for num in numbers:
        yield num ** 2

def limit_numbers(numbers, limit):
    """Limit number of items."""
    count = 0
    for num in numbers:
        if count >= limit:
            break
        yield num
        count += 1

# Pipeline example
numbers = range(1, 21)
pipeline = limit_numbers(square_numbers(filter_numbers(numbers)), 5)
print(f"\nData pipeline result: {list(pipeline)}")


# ============================================
# 8. Performance Comparison
# ============================================

print("\n" + "="*60)
print("=== PERFORMANCE COMPARISON ===\n")

def time_function(func, *args, **kwargs):
    """Time a function execution."""
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return result, end - start

# Memory usage comparison
import sys

def list_approach(n):
    """Create list of squares."""
    return [x**2 for x in range(n)]

def generator_approach(n):
    """Create generator of squares."""
    return (x**2 for x in range(n))

n = 10000

# List approach
list_result, list_time = time_function(list_approach, n)
list_memory = sys.getsizeof(list_result)

# Generator approach
gen_result, gen_time = time_function(generator_approach, n)
gen_memory = sys.getsizeof(gen_result)

print(f"List approach:")
print(f"  Time: {list_time:.6f} seconds")
print(f"  Memory: {list_memory} bytes")

print(f"\nGenerator approach:")
print(f"  Time: {gen_time:.6f} seconds")
print(f"  Memory: {gen_memory} bytes")

print(f"\nGenerator is {list_memory/gen_memory:.1f}x more memory efficient")


# ============================================
# 9. Custom Iterable Classes
# ============================================

print("\n" + "="*60)
print("=== CUSTOM ITERABLE CLASSES ===\n")

class NumberRange:
    """Iterable class that generates a range of numbers."""
    
    def __init__(self, start: int, end: int, step: int = 1):
        self.start = start
        self.end = end
        self.step = step
    
    def __iter__(self):
        return NumberRangeIterator(self.start, self.end, self.step)

class NumberRangeIterator:
    """Iterator for NumberRange."""
    
    def __init__(self, start: int, end: int, step: int):
        self.current = start
        self.end = end
        self.step = step
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        result = self.current
        self.current += self.step
        return result

print("Custom iterable class:")
for num in NumberRange(0, 10, 2):
    print(f"  {num}")


# ============================================
# Practice Exercise
# ============================================

print("\n" + "="*60)
print("🎯 PRACTICE EXERCISE")
print("="*60)
print("""
Try these exercises:

1. Create a prime number generator
2. Build a CSV file processor with generators
3. Implement a web scraping pipeline
4. Make a real-time data stream processor
5. Create a memory-efficient log analyzer
""")

# Clean up sample file
import os
if os.path.exists("sample.txt"):
    os.remove("sample.txt")
    print("\n🧹 Cleaned up sample.txt")
