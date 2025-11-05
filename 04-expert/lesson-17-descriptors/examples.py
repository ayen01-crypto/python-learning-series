"""
Lesson 17: Descriptors & Properties
Comprehensive Examples
"""

import time
from typing import Any, Dict, Optional


# ============================================
# 1. Basic Descriptor Protocol
# ============================================

print("=== BASIC DESCRIPTOR PROTOCOL ===\n")

class SimpleDescriptor:
    """Simple descriptor demonstrating the protocol."""
    
    def __init__(self, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        print(f"Getting {self.name}")
        return obj.__dict__.get(self.name, "Not set")
    
    def __set__(self, obj, value):
        print(f"Setting {self.name} to {value}")
        obj.__dict__[self.name] = value
    
    def __delete__(self, obj):
        print(f"Deleting {self.name}")
        if self.name in obj.__dict__:
            del obj.__dict__[self.name]

class TestClass:
    """Test class with descriptor."""
    attr = SimpleDescriptor("attr")

# Test the descriptor
test = TestClass()
print(f"Initial value: {test.attr}")
test.attr = "Hello, World!"
print(f"After setting: {test.attr}")
del test.attr
print(f"After deleting: {test.attr}")


# ============================================
# 2. Validation Descriptor
# ============================================

print("\n" + "="*60)
print("=== VALIDATION DESCRIPTOR ===\n")

class PositiveNumber:
    """Descriptor that validates positive numbers."""
    
    def __init__(self, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, 0)
    
    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} must be a number")
        if value < 0:
            raise ValueError(f"{self.name} must be positive")
        obj.__dict__[self.name] = value

class Product:
    """Product class with validated attributes."""
    price = PositiveNumber("price")
    quantity = PositiveNumber("quantity")
    
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
    
    @property
    def total_value(self):
        """Computed property."""
        return self.price * self.quantity

# Test validation
try:
    product = Product("Laptop", 999.99, 5)
    print(f"Product: {product.name}")
    print(f"Price: ${product.price}")
    print(f"Quantity: {product.quantity}")
    print(f"Total value: ${product.total_value}")
    
    # This will raise an error
    product.price = -100
except ValueError as e:
    print(f"❌ {e}")


# ============================================
# 3. Property Decorator
# ============================================

print("\n" + "="*60)
print("=== PROPERTY DECORATOR ===\n")

class Circle:
    """Circle class demonstrating properties."""
    
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        """Get radius."""
        print("Getting radius")
        return self._radius
    
    @radius.setter
    def radius(self, value):
        """Set radius with validation."""
        print(f"Setting radius to {value}")
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @radius.deleter
    def radius(self):
        """Delete radius."""
        print("Deleting radius")
        del self._radius
    
    @property
    def area(self):
        """Calculate area (read-only property)."""
        return 3.14159 * self._radius ** 2
    
    @property
    def diameter(self):
        """Calculate diameter."""
        return 2 * self._radius
    
    @diameter.setter
    def diameter(self, value):
        """Set diameter by updating radius."""
        self.radius = value / 2

# Test properties
circle = Circle(5)
print(f"Radius: {circle.radius}")
print(f"Area: {circle.area:.2f}")
print(f"Diameter: {circle.diameter}")

circle.diameter = 20
print(f"New radius: {circle.radius}")


# ============================================
# 4. Typed Descriptor
# ============================================

print("\n" + "="*60)
print("=== TYPED DESCRIPTOR ===\n")

class TypedAttribute:
    """Descriptor that enforces type checking."""
    
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name} must be of type {self.expected_type.__name__}")
        obj.__dict__[self.name] = value

class Person:
    """Person class with typed attributes."""
    name = TypedAttribute("name", str)
    age = TypedAttribute("age", int)
    height = TypedAttribute("height", float)
    
    def __init__(self, name, age, height):
        self.name = name
        self.age = age
        self.height = height

# Test type checking
try:
    person = Person("Alice", 30, 5.6)
    print(f"Person: {person.name}, {person.age} years old, {person.height} feet tall")
    
    # This will raise a TypeError
    person.age = "thirty"
except TypeError as e:
    print(f"❌ {e}")


# ============================================
# 5. Lazy Loading Descriptor
# ============================================

print("\n" + "="*60)
print("=== LAZY LOADING DESCRIPTOR ===\n")

class LazyAttribute:
    """Descriptor that computes value only when accessed."""
    
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
        self.__doc__ = func.__doc__
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        
        # Check if value is already computed
        if self.name in obj.__dict__:
            return obj.__dict__[self.name]
        
        # Compute and store the value
        print(f"Computing {self.name}...")
        value = self.func(obj)
        obj.__dict__[self.name] = value
        return value

class DataProcessor:
    """Class with lazy-loaded attributes."""
    
    def __init__(self, data):
        self.data = data
        self.processed_count = 0
    
    @LazyAttribute
    def expensive_computation(self):
        """Expensive computation that's only done once."""
        time.sleep(0.1)  # Simulate expensive operation
        result = sum(x ** 2 for x in self.data)
        self.processed_count += 1
        return result
    
    @LazyAttribute
    def statistics(self):
        """Statistical analysis."""
        time.sleep(0.1)  # Simulate expensive operation
        return {
            "count": len(self.data),
            "sum": sum(self.data),
            "average": sum(self.data) / len(self.data) if self.data else 0,
            "min": min(self.data) if self.data else 0,
            "max": max(self.data) if self.data else 0
        }

# Test lazy loading
data = list(range(1000))
processor = DataProcessor(data)

print("Accessing expensive_computation first time:")
result1 = processor.expensive_computation
print(f"Result: {result1}")

print("\nAccessing expensive_computation second time:")
result2 = processor.expensive_computation
print(f"Result: {result2} (cached)")

print(f"\nProcessed count: {processor.processed_count}")

print("\nAccessing statistics:")
stats = processor.statistics
print(f"Statistics: {stats}")


# ============================================
# 6. Cached Property Descriptor
# ============================================

print("\n" + "="*60)
print("=== CACHED PROPERTY DESCRIPTOR ===\n")

class CachedProperty:
    """Descriptor that caches property values."""
    
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
        self.__doc__ = func.__doc__
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        
        # Check cache
        cache_attr = f"_cache_{self.name}"
        if hasattr(obj, cache_attr):
            print(f"Returning cached {self.name}")
            return getattr(obj, cache_attr)
        
        # Compute and cache
        print(f"Computing {self.name}")
        value = self.func(obj)
        setattr(obj, cache_attr, value)
        return value
    
    def __set__(self, obj, value):
        cache_attr = f"_cache_{self.name}"
        setattr(obj, cache_attr, value)
    
    def __delete__(self, obj):
        cache_attr = f"_cache_{self.name}"
        if hasattr(obj, cache_attr):
            delattr(obj, cache_attr)

class FibonacciCalculator:
    """Class that calculates Fibonacci numbers with caching."""
    
    def __init__(self):
        self.calculation_count = 0
    
    @CachedProperty
    def fibonacci_10(self):
        """Calculate 10th Fibonacci number."""
        self.calculation_count += 1
        a, b = 0, 1
        for _ in range(10):
            a, b = b, a + b
        return a
    
    @CachedProperty
    def fibonacci_20(self):
        """Calculate 20th Fibonacci number."""
        self.calculation_count += 1
        a, b = 0, 1
        for _ in range(20):
            a, b = b, a + b
        return a

# Test caching
calc = FibonacciCalculator()

print("First access to fibonacci_10:")
result1 = calc.fibonacci_10
print(f"Result: {result1}")

print("\nSecond access to fibonacci_10:")
result2 = calc.fibonacci_10
print(f"Result: {result2} (cached)")

print(f"\nCalculation count: {calc.calculation_count}")

# Manually set a cached value
calc.fibonacci_10 = 999
print(f"\nAfter manual setting: {calc.fibonacci_10}")

# Clear cache
del calc.fibonacci_10
print("After clearing cache:")
result3 = calc.fibonacci_10
print(f"Result: {result3}")


# ============================================
# 7. Advanced Descriptor Patterns
# ============================================

print("\n" + "="*60)
print("=== ADVANCED DESCRIPTOR PATTERNS ===\n")

class LoggedAttribute:
    """Descriptor that logs all access."""
    
    def __init__(self, name, log_level="INFO"):
        self.name = name
        self.log_level = log_level
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.name, "Not set")
        print(f"[{self.log_level}] GET {self.name}: {value}")
        return value
    
    def __set__(self, obj, value):
        old_value = obj.__dict__.get(self.name, "Not set")
        obj.__dict__[self.name] = value
        print(f"[{self.log_level}] SET {self.name}: {old_value} -> {value}")
    
    def __delete__(self, obj):
        old_value = obj.__dict__.get(self.name, "Not set")
        if self.name in obj.__dict__:
            del obj.__dict__[self.name]
        print(f"[{self.log_level}] DELETE {self.name}: {old_value}")

class MonitoredClass:
    """Class with logged attributes."""
    name = LoggedAttribute("name", "INFO")
    score = LoggedAttribute("score", "DEBUG")
    
    def __init__(self, name, score):
        self.name = name
        self.score = score

# Test logging descriptor
print("Testing logged attributes:")
monitored = MonitoredClass("Alice", 95)
print(f"Name: {monitored.name}")
monitored.score = 98
del monitored.name


# ============================================
# 8. Descriptor vs Property Comparison
# ============================================

print("\n" + "="*60)
print("=== DESCRIPTOR VS PROPERTY COMPARISON ===\n")

class PropertyExample:
    """Example using properties."""
    
    def __init__(self, value):
        self._value = value
    
    @property
    def value(self):
        print("Property getter called")
        return self._value
    
    @value.setter
    def value(self, new_value):
        print(f"Property setter called with {new_value}")
        self._value = new_value

class DescriptorExample:
    """Example using descriptors."""
    
    def __init__(self, value):
        self._value = value
    
    class ValueDescriptor:
        def __get__(self, obj, objtype=None):
            if obj is None:
                return self
            print("Descriptor getter called")
            return obj._value
        
        def __set__(self, obj, value):
            print(f"Descriptor setter called with {value}")
            obj._value = value
    
    value = ValueDescriptor()

# Compare usage
print("Property example:")
prop_obj = PropertyExample(42)
print(f"Value: {prop_obj.value}")
prop_obj.value = 100

print("\nDescriptor example:")
desc_obj = DescriptorExample(42)
print(f"Value: {desc_obj.value}")
desc_obj.value = 100

print("\n" + "="*60)
print("🎯 PRACTICE EXERCISE")
print("="*60)
print("""
Try these exercises:

1. Create a password validation descriptor
2. Build a unit conversion descriptor
3. Implement a history-tracking descriptor
4. Make a rate-limiting property descriptor
5. Create a configuration descriptor with defaults
""")
