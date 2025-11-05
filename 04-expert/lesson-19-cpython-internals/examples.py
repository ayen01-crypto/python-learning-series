"""
Lesson 19: CPython Internals & C Extensions
Comprehensive Examples
"""

import sys
import dis
import inspect
from typing import Any


# ============================================
# 1. Bytecode Inspection
# ============================================

print("=== BYTECODE INSPECTION ===\n")

def simple_function(x, y):
    """Simple function for bytecode analysis."""
    z = x + y
    return z * 2

# Disassemble function
print("Bytecode for simple_function:")
dis.dis(simple_function)

# Get bytecode object
code_obj = simple_function.__code__
print(f"\nCode object attributes:")
print(f"  Filename: {code_obj.co_filename}")
print(f"  Line number: {code_obj.co_firstlineno}")
print(f"  Arguments: {code_obj.co_argcount}")
print(f"  Variables: {code_obj.co_varnames}")
print(f"  Constants: {code_obj.co_consts}")


# ============================================
# 2. Python Object Internals
# ============================================

print("\n" + "="*60)
print("=== PYTHON OBJECT INTERNALS ===\n")

# Inspect object structure
x = 42
print(f"Integer object {x}:")
print(f"  Type: {type(x)}")
print(f"  ID: {id(x)}")
print(f"  Size: {sys.getsizeof(x)} bytes")

# String interning
a = "hello"
b = "hello"
print(f"\nString interning:")
print(f"  a = '{a}', b = '{b}'")
print(f"  a is b: {a is b}")
print(f"  id(a): {id(a)}")
print(f"  id(b): {id(b)}")

# List internals
lst = [1, 2, 3]
print(f"\nList object {lst}:")
print(f"  Size: {sys.getsizeof(lst)} bytes")
print(f"  Capacity: {len(lst)} items")


# ============================================
# 3. Garbage Collection Internals
# ============================================

print("\n" + "="*60)
print("=== GARBAGE COLLECTION INTERNALS ===\n")

# Show garbage collector information
print("Garbage collector info:")
print(f"  Enabled: {gc.isenabled()}")
print(f"  Thresholds: {gc.get_threshold()}")
print(f"  Counts: {gc.get_count()}")

# Manual garbage collection
collected = gc.collect()
print(f"  Collected {collected} objects")


# ============================================
# 4. Function Call Internals
# ============================================

print("\n" + "="*60)
print("=== FUNCTION CALL INTERNALS ===\n")

def traced_function(a, b=10):
    """Function with tracing."""
    local_var = a + b
    return local_var * 2

# Show function attributes
print("Function attributes:")
print(f"  Name: {traced_function.__name__}")
print(f"  Qualname: {traced_function.__qualname__}")
print(f"  Module: {traced_function.__module__}")
print(f"  Defaults: {traced_function.__defaults__}")
print(f"  Code: {traced_function.__code__}")

# Show function signature
sig = inspect.signature(traced_function)
print(f"  Signature: {sig}")


# ============================================
# 5. Exception Handling Internals
# ============================================

print("\n" + "="*60)
print("=== EXCEPTION HANDLING INTERNALS ===\n")

import traceback

def exception_demo():
    """Demonstrate exception handling."""
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print("Exception caught:")
        print(f"  Exception type: {type(e)}")
        print(f"  Exception value: {e}")
        print("  Traceback:")
        traceback.print_exc()

exception_demo()


# ============================================
# 6. Memory Management Internals
# ============================================

print("\n" + "="*60)
print("=== MEMORY MANAGEMENT INTERNALS ===\n")

# Show memory usage
print("Memory usage information:")
print(f"  Current memory usage: {sys.getsizeof(locals())} bytes")

# Reference counting demonstration
class RefCountDemo:
    def __init__(self, value):
        self.value = value

obj = RefCountDemo(42)
print(f"Reference count for obj: {sys.getrefcount(obj)}")

# Show object references
import gc
refs = gc.get_referrers(obj)
print(f"Objects referencing obj: {len(refs)}")


# ============================================
# 7. Import System Internals
# ============================================

print("\n" + "="*60)
print("=== IMPORT SYSTEM INTERNALS ===\n")

# Show module search paths
print("Module search paths:")
for i, path in enumerate(sys.path[:5]):  # Show first 5
    print(f"  {i+1}. {path}")

# Show loaded modules
print(f"\nLoaded modules count: {len(sys.modules)}")
print("Some loaded modules:")
for i, (name, module) in enumerate(list(sys.modules.items())[:10]):
    if module:
        print(f"  {i+1}. {name}: {type(module)}")


# ============================================
# 8. Threading Internals
# ============================================

print("\n" + "="*60)
print("=== THREADING INTERNALS ===\n")

import threading

# Show threading information
print("Threading information:")
print(f"  Main thread: {threading.main_thread()}")
print(f"  Active threads: {threading.active_count()}")
print(f"  Current thread: {threading.current_thread()}")

# Global interpreter lock info
print(f"  GIL enabled: {hasattr(sys, '_current_frames')}")


# ============================================
# 9. Performance Profiling
# ============================================

print("\n" + "="*60)
print("=== PERFORMANCE PROFILING ===\n")

import cProfile
import pstats

def profiled_function():
    """Function to profile."""
    total = 0
    for i in range(1000):
        total += sum(range(i))
    return total

# Profile function
print("Profiling function execution:")
profiler = cProfile.Profile()
profiler.enable()
result = profiled_function()
profiler.disable()

# Show stats
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(5)  # Show top 5 functions


# ============================================
# 10. Advanced Debugging
# ============================================

print("\n" + "="*60)
print("=== ADVANCED DEBUGGING ===\n")

# Show Python internals
print("Python internals:")
print(f"  Version: {sys.version}")
print(f"  Implementation: {sys.implementation}")
print(f"  Platform: {sys.platform}")
print(f"  API version: {sys.api_version}")

# Show recursion limit
print(f"  Recursion limit: {sys.getrecursionlimit()}")

# Show maximum values
print(f"  Maximum size: {sys.maxsize}")
print(f"  Float info: {sys.float_info}")

print("\n" + "="*60)
print("🎯 PRACTICE EXERCISE")
print("="*60)
print("""
Try these exercises:

1. Create a custom iterator in C
2. Build a mathematical function library in C
3. Implement a string processing extension
4. Make a system utility extension
5. Create a multimedia processing extension
""")
