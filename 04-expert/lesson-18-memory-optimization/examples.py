"""
Lesson 18: Memory Management & Optimization
Comprehensive Examples
"""

import sys
import gc
import tracemalloc
import weakref
import time
from typing import List, Dict, Any
from collections import deque, namedtuple
import array


# ============================================
# 1. Reference Counting
# ============================================

print("=== REFERENCE COUNTING ===\n")

# Understanding reference counts
x = [1, 2, 3]
print(f"Initial reference count: {sys.getrefcount(x)}")

y = x  # Another reference
print(f"After assignment: {sys.getrefcount(x)}")

z = [x, x]  # Two more references in list
print(f"After list inclusion: {sys.getrefcount(x)}")

del y  # Remove one reference
print(f"After del y: {sys.getrefcount(x)}")

# When reference count reaches 0, object is deallocated
print("Object will be deallocated when reference count reaches 0")


# ============================================
# 2. Garbage Collection
# ============================================

print("\n" + "="*60)
print("=== GARBAGE COLLECTION ===\n")

# Circular references that reference counting can't handle
class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.children = []
    
    def add_child(self, child):
        child.parent = self
        self.children.append(child)

# Create circular reference
root = Node("root")
child1 = Node("child1")
child2 = Node("child2")

root.add_child(child1)
root.add_child(child2)
child1.add_child(child2)

# Remove references
del root, child1, child2

# Force garbage collection
collected = gc.collect()
print(f"Garbage collected {collected} objects")

# Check garbage collector stats
print(f"GC stats: {gc.get_stats()}")
print(f"GC thresholds: {gc.get_threshold()}")


# ============================================
# 3. Memory Profiling with tracemalloc
# ============================================

print("\n" + "="*60)
print("=== MEMORY PROFILING ===\n")

# Start tracing
tracemalloc.start()

def create_large_data():
    """Function that creates large data structures."""
    data = []
    for i in range(1000):
        data.append([j for j in range(100)])
    return data

# Take snapshot before
snapshot1 = tracemalloc.take_snapshot()

# Create data
large_data = create_large_data()

# Take snapshot after
snapshot2 = tracemalloc.take_snapshot()

# Calculate difference
top_stats = snapshot2.compare_to(snapshot1, 'lineno')
print("Top 3 memory allocations:")
for stat in top_stats[:3]:
    print(f"  {stat}")

# Stop tracing
tracemalloc.stop()


# ============================================
# 4. Memory-Efficient Classes with __slots__
# ============================================

print("\n" + "="*60)
print("=== MEMORY-EFFICIENT CLASSES ===\n")

class RegularClass:
    """Regular class without __slots__."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlottedClass:
    """Class with __slots__ for memory efficiency."""
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Compare memory usage
regular = RegularClass(1, 2)
slotted = SlottedClass(1, 2)

print(f"Regular class dict: {regular.__dict__}")
print(f"Slotted class size: {sys.getsizeof(slotted)} bytes")

# Slotted classes can't have arbitrary attributes
try:
    slotted.z = 3
except AttributeError as e:
    print(f"❌ {e}")


# ============================================
# 5. Weak References
# ============================================

print("\n" + "="*60)
print("=== WEAK REFERENCES ===\n")

class DataObject:
    """Class to demonstrate weak references."""
    def __init__(self, name):
        self.name = name
    
    def __del__(self):
        print(f"🧹 {self.name} is being deleted")

# Create object
obj = DataObject("Test Object")

# Create weak reference
weak_ref = weakref.ref(obj)
print(f"Object name via weak reference: {weak_ref().name}")

# Delete strong reference
del obj

# Object is now deleted
print(f"Weak reference after deletion: {weak_ref()}")


# ============================================
# 6. Efficient Data Structures
# ============================================

print("\n" + "="*60)
print("=== EFFICIENT DATA STRUCTURES ===\n")

# Compare list vs deque for queue operations
def time_queue_operations():
    """Time queue operations."""
    # List as queue (inefficient)
    start = time.time()
    list_queue = []
    for i in range(10000):
        list_queue.append(i)
    for i in range(10000):
        list_queue.pop(0)  # O(n) operation
    list_time = time.time() - start
    
    # Deque as queue (efficient)
    start = time.time()
    deque_queue = deque()
    for i in range(10000):
        deque_queue.append(i)
    for i in range(10000):
        deque_queue.popleft()  # O(1) operation
    deque_time = time.time() - start
    
    print(f"List queue time: {list_time:.4f} seconds")
    print(f"Deque queue time: {deque_time:.4f} seconds")
    print(f"Deque is {list_time/deque_time:.1f}x faster")

time_queue_operations()

# Array vs list for numeric data
def compare_numeric_storage():
    """Compare memory usage for numeric data."""
    # List of integers
    int_list = [i for i in range(1000)]
    list_size = sys.getsizeof(int_list)
    
    # Array of integers
    int_array = array.array('i', range(1000))
    array_size = sys.getsizeof(int_array)
    
    print(f"List size: {list_size} bytes")
    print(f"Array size: {array_size} bytes")
    print(f"Array is {list_size/array_size:.1f}x more memory efficient")

compare_numeric_storage()


# ============================================
# 7. Memory Optimization Techniques
# ============================================

print("\n" + "="*60)
print("=== MEMORY OPTIMIZATION TECHNIQUES ===\n")

# String interning
def string_interning_demo():
    """Demonstrate string interning."""
    # These strings will be interned automatically
    a = "hello"
    b = "hello"
    print(f"Interned strings are identical: {a is b}")
    
    # Large strings won't be interned automatically
    c = "hello" * 1000
    d = "hello" * 1000
    print(f"Large strings identical: {c is d}")
    
    # Force interning
    e = sys.intern("hello" * 1000)
    f = sys.intern("hello" * 1000)
    print(f"Interned large strings identical: {e is f}")

string_interning_demo()

# Generator vs list for large datasets
def memory_efficient_iteration():
    """Compare memory usage of generators vs lists."""
    # List comprehension (loads everything into memory)
    list_comp = [x**2 for x in range(100000)]
    list_memory = sys.getsizeof(list_comp)
    
    # Generator expression (lazy evaluation)
    gen_exp = (x**2 for x in range(100000))
    gen_memory = sys.getsizeof(gen_exp)
    
    print(f"List comprehension memory: {list_memory} bytes")
    print(f"Generator expression memory: {gen_memory} bytes")
    print(f"Generator is {list_memory/gen_memory:.1f}x more memory efficient")

memory_efficient_iteration()


# ============================================
# 8. Named Tuples for Memory Efficiency
# ============================================

print("\n" + "="*60)
print("=== NAMED TUPLES ===\n")

# Regular class
class PointClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Named tuple
PointTuple = namedtuple('Point', ['x', 'y'])

# Compare memory usage
class_point = PointClass(1, 2)
tuple_point = PointTuple(1, 2)

class_memory = sys.getsizeof(class_point.__dict__)
tuple_memory = sys.getsizeof(tuple_point)

print(f"Class instance memory: {class_memory} bytes")
print(f"Named tuple memory: {tuple_memory} bytes")
print(f"Named tuple is {class_memory/tuple_memory:.1f}x more memory efficient")

print(f"Named tuple access: x={tuple_point.x}, y={tuple_point.y}")


# ============================================
# 9. Memory Leak Detection
# ============================================

print("\n" + "="*60)
print("=== MEMORY LEAK DETECTION ===\n")

class LeakyClass:
    """Class that might cause memory leaks."""
    leaky_data = []  # Class variable - shared by all instances
    
    def __init__(self, value):
        self.value = value
        # Accidentally appending to class variable instead of instance
        LeakyClass.leaky_data.append(value)

def detect_memory_leaks():
    """Demonstrate memory leak detection."""
    # Create instances
    instances = []
    for i in range(100):
        instances.append(LeakyClass(i))
    
    print(f"Leaky data size: {len(LeakyClass.leaky_data)}")
    
    # Delete instances
    del instances
    
    # Check if data persists (indicating potential leak)
    print(f"After deletion, leaky data still has {len(LeakyClass.leaky_data)} items")
    
    # Clean up
    LeakyClass.leaky_data.clear()

detect_memory_leaks()


# ============================================
# 10. Performance Monitoring
# ============================================

print("\n" + "="*60)
print("=== PERFORMANCE MONITORING ===\n")

def monitor_performance():
    """Monitor performance and memory usage."""
    # Start monitoring
    tracemalloc.start()
    
    # Record initial state
    start_time = time.time()
    start_memory = tracemalloc.get_traced_memory()
    
    # Perform some operations
    data = []
    for i in range(10000):
        data.append(i ** 2)
    
    # Record final state
    end_time = time.time()
    end_memory = tracemalloc.get_traced_memory()
    
    # Calculate metrics
    execution_time = end_time - start_time
    memory_used = end_memory[0] - start_memory[0]
    
    print(f"Execution time: {execution_time:.4f} seconds")
    print(f"Memory used: {memory_used} bytes")
    print(f"Performance: {len(data)/execution_time:.0f} operations/second")
    
    # Stop monitoring
    tracemalloc.stop()

monitor_performance()

print("\n" + "="*60)
print("🎯 PRACTICE EXERCISE")
print("="*60)
print("""
Try these exercises:

1. Create a memory profiler decorator
2. Build a cache with size limits and eviction
3. Implement a memory pool for object allocation
4. Make a performance benchmarking framework
5. Create a resource usage monitor for applications
""")
