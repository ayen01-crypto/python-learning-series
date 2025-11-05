"""
Lesson 16: Metaclasses & Class Factories
Comprehensive Examples
"""

import time
import functools
from typing import Dict, Any


# ============================================
# 1. Basic Metaclass Understanding
# ============================================

print("=== BASIC METACLASS UNDERSTANDING ===\n")

# Default metaclass is 'type'
class RegularClass:
    pass

print(f"RegularClass metaclass: {type(RegularClass)}")
print(f"type metaclass: {type(type)}")

# Creating classes dynamically with type()
def init_method(self, value):
    self.value = value

def str_method(self):
    return f"MyClass instance with value: {self.value}"

# Create class dynamically
MyClass = type('MyClass', (), {
    '__init__': init_method,
    '__str__': str_method,
    'class_attribute': 'Created with type()'
})

instance = MyClass(42)
print(f"Dynamic class instance: {instance}")
print(f"Class attribute: {getattr(MyClass, 'class_attribute', 'Not found')}")


# ============================================
# 2. Custom Metaclass with __new__
# ============================================

print("\n" + "="*60)
print("=== CUSTOM METACLASS WITH __new__ ===\n")

class AttributeTrackerMeta(type):
    """Metaclass that tracks class attributes."""
    
    def __new__(cls, name, bases, attrs):
        # Add creation timestamp
        attrs['_created_at'] = time.time()
        
        # Count methods
        method_count = sum(1 for key, value in attrs.items() 
                          if callable(value) and not key.startswith('_'))
        attrs['_method_count'] = method_count
        
        # Track attribute names
        attrs['_attribute_names'] = [key for key in attrs.keys() 
                                   if not key.startswith('_')]
        
        print(f"Creating class '{name}' with {method_count} methods")
        return super().__new__(cls, name, bases, attrs)

class TrackedClass(metaclass=AttributeTrackerMeta):
    """Class that uses the tracking metaclass."""
    
    def method_one(self):
        return "Method one"
    
    def method_two(self):
        return "Method two"
    
    class_attribute = "I'm a class attribute"

# Access the attributes through the class
tracked_class_attrs = TrackedClass.__dict__
print(f"Class created at: {tracked_class_attrs.get('_created_at', 'Not found')}")
print(f"Method count: {tracked_class_attrs.get('_method_count', 'Not found')}")
print(f"Attribute names: {tracked_class_attrs.get('_attribute_names', 'Not found')}")


# ============================================
# 3. Metaclass with __init__
# ============================================

print("\n" + "="*60)
print("=== METACLASS WITH __init__ ===\n")

class RegistryMeta(type):
    """Metaclass that registers classes."""
    
    # Class registry
    registry = {}
    
    def __new__(cls, name, bases, attrs):
        # Create the class
        new_class = super().__new__(cls, name, bases, attrs)
        return new_class
    
    def __init__(cls, name, bases, attrs):
        # Register the class after creation
        super().__init__(name, bases, attrs)
        if name != 'BaseClass':  # Don't register base class
            RegistryMeta.registry[name] = cls
        print(f"Registered class: {name}")

class BaseClass(metaclass=RegistryMeta):
    """Base class for registered classes."""
    pass

class ServiceA(BaseClass):
    def process(self):
        return "Service A processing"

class ServiceB(BaseClass):
    def process(self):
        return "Service B processing"

class ServiceC(BaseClass):
    def process(self):
        return "Service C processing"

print(f"Registered classes: {list(RegistryMeta.registry.keys())}")

# Use registered classes
for name, cls in RegistryMeta.registry.items():
    instance = cls()
    print(f"{name}: {instance.process()}")


# ============================================
# 4. Singleton Metaclass
# ============================================

print("\n" + "="*60)
print("=== SINGLETON METACLASS ===\n")

class SingletonMeta(type):
    """Metaclass for singleton pattern."""
    
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseConnection(metaclass=SingletonMeta):
    """Database connection that uses singleton pattern."""
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.connection_id = id(self)
            print(f"Creating database connection {self.connection_id}")
    
    def query(self, sql):
        return f"Executing: {sql}"

# Test singleton behavior
db1 = DatabaseConnection()
db2 = DatabaseConnection()
db3 = DatabaseConnection()

print(f"db1 id: {id(db1)}")
print(f"db2 id: {id(db2)}")
print(f"db3 id: {id(db3)}")
print(f"Are they the same? {db1 is db2 is db3}")

result1 = db1.query("SELECT * FROM users")
result2 = db2.query("SELECT * FROM products")
print(f"db1 result: {result1}")
print(f"db2 result: {result2}")


# ============================================
# 5. Class Factory Pattern
# ============================================

print("\n" + "="*60)
print("=== CLASS FACTORY PATTERN ===\n")

def class_factory(class_name: str, base_classes: tuple, attributes: dict, 
                 add_debug: bool = False, add_timestamp: bool = False):
    """Factory function to create classes with additional features."""
    
    # Add debug functionality
    if add_debug:
        def debug_info(self):
            return f"Debug: {self.__class__.__name__} instance"
        attributes['debug_info'] = debug_info
    
    # Add timestamp
    if add_timestamp:
        attributes['_created_at'] = time.time()
    
    # Create and return the class
    return type(class_name, base_classes, attributes)

# Create classes with factory
PersonClass = class_factory(
    'Person',
    (),
    {
        '__init__': lambda self, name: setattr(self, 'name', name),
        '__str__': lambda self: f"Person: {getattr(self, 'name', 'Unknown')}"
    },
    add_debug=True,
    add_timestamp=True
)

ProductClass = class_factory(
    'Product',
    (),
    {
        '__init__': lambda self, name, price: (setattr(self, 'name', name), setattr(self, 'price', price)),
        '__str__': lambda self: f"Product: {getattr(self, 'name', 'Unknown')} (${getattr(self, 'price', 0)})"
    },
    add_debug=True
)

# Use factory-created classes
person = PersonClass("Alice")
product = ProductClass("Laptop", 999.99)

print(f"Person: {person}")
print(f"Product: {product}")
print(f"Person debug: {person.debug_info()}")
print(f"Product debug: {product.debug_info()}")
if hasattr(person, '_created_at'):
    print(f"Person created at: {person._created_at}")


# ============================================
# 6. ORM-Style Metaclass
# ============================================

print("\n" + "="*60)
print("=== ORM-STYLE METACLASS ===\n")

class ModelMeta(type):
    """Metaclass for ORM-style models."""
    
    def __new__(cls, name, bases, attrs):
        # Don't modify the base Model class
        if name == 'Model':
            return super().__new__(cls, name, bases, attrs)
        
        # Extract field definitions
        fields = {}
        for key, value in list(attrs.items()):
            if isinstance(value, type) and hasattr(value, '__name__'):
                # This is a field type specification
                fields[key] = value
                attrs.pop(key)
        
        # Add fields to class
        attrs['_fields'] = fields
        attrs['_table_name'] = name.lower()
        
        # Add methods
        def save(self):
            field_values = {field: getattr(self, field, None) for field in fields}
            return f"INSERT INTO {self._table_name} {tuple(field_values.keys())} VALUES {tuple(field_values.values())}"
        
        def __repr__(self):
            field_values = {field: getattr(self, field, None) for field in fields}
            return f"{name}({', '.join(f'{k}={v}' for k, v in field_values.items())})"
        
        attrs['save'] = save
        attrs['__repr__'] = __repr__
        
        print(f"Creating model class '{name}' with fields: {list(fields.keys())}")
        return super().__new__(cls, name, bases, attrs)

class Model(metaclass=ModelMeta):
    """Base model class."""
    pass

# Define model classes
class User(Model):
    name = str
    age = int
    email = str

class Product(Model):
    title = str
    price = float
    category = str

# Use model classes
user = User()
setattr(user, 'name', "Alice")
setattr(user, 'age', 30)
setattr(user, 'email', "alice@example.com")

product = Product()
setattr(product, 'title', "Laptop")
setattr(product, 'price', 999.99)
setattr(product, 'category', "Electronics")

print(f"User: {user}")
print(f"User save: {getattr(user, 'save')() if hasattr(user, 'save') else 'Method not found'}")
print(f"Product: {product}")
print(f"Product save: {getattr(product, 'save')() if hasattr(product, 'save') else 'Method not found'}")


# ============================================
# 7. Validation Metaclass
# ============================================

print("\n" + "="*60)
print("=== VALIDATION METACLASS ===\n")

class ValidationMeta(type):
    """Metaclass that adds validation to classes."""
    
    def __new__(cls, name, bases, attrs):
        # Add validation methods
        validators = {}
        for key, value in list(attrs.items()):
            if key.startswith('validate_') and callable(value):
                field_name = key[9:]  # Remove 'validate_' prefix
                validators[field_name] = value
                attrs.pop(key)
        
        attrs['_validators'] = validators
        
        # Add validation method
        def validate(self):
            errors = []
            for field, validator in validators.items():
                if hasattr(self, field):
                    try:
                        validator(self, getattr(self, field, None))
                    except ValueError as e:
                        errors.append(f"{field}: {e}")
            return errors
        
        attrs['validate'] = validate
        
        return super().__new__(cls, name, bases, attrs)

class UserValidator(metaclass=ValidationMeta):
    """Class with validation."""
    
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email
    
    def validate_name(self, value):
        if not value or len(value) < 2:
            raise ValueError("Name must be at least 2 characters")
    
    def validate_age(self, value):
        if not isinstance(value, int) or value < 0 or value > 150:
            raise ValueError("Age must be between 0 and 150")
    
    def validate_email(self, value):
        if '@' not in value:
            raise ValueError("Email must contain @ symbol")

# Test validation
valid_user = UserValidator("Alice", 30, "alice@example.com")
invalid_user = UserValidator("A", -5, "invalid-email")

print("Valid user validation:")
validate_func = getattr(valid_user, 'validate', lambda: [])
errors = validate_func()
print(f"Errors: {errors}")

print("\nInvalid user validation:")
validate_func = getattr(invalid_user, 'validate', lambda: [])
errors = validate_func()
print(f"Errors: {errors}")


# ============================================
# 8. Advanced Metaclass Patterns
# ============================================

print("\n" + "="*60)
print("=== ADVANCED PATTERNS ===\n")

class DecoratorMeta(type):
    """Metaclass that applies decorators to methods."""
    
    def __new__(cls, name, bases, attrs):
        # Apply timing decorator to all methods
        def timer(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start = time.time()
                result = func(*args, **kwargs)
                end = time.time()
                print(f"{func.__name__} executed in {end - start:.4f} seconds")
                return result
            return wrapper
        
        # Apply timer to all callable attributes
        for key, value in attrs.items():
            if callable(value) and not key.startswith('_'):
                attrs[key] = timer(value)
        
        return super().__new__(cls, name, bases, attrs)

class TimedClass(metaclass=DecoratorMeta):
    """Class with timed methods."""
    
    def slow_method(self):
        time.sleep(0.1)
        return "Slow method completed"
    
    def fast_method(self):
        return "Fast method completed"

# Test timed methods
timed_instance = TimedClass()
result1 = timed_instance.slow_method()
result2 = timed_instance.fast_method()


# ============================================
# Practice Exercise
# ============================================

print("\n" + "="*60)
print("🎯 PRACTICE EXERCISE")
print("="*60)
print("""
Try these exercises:

1. Create a logging metaclass that logs all method calls
2. Build a configuration metaclass that validates class attributes
3. Implement a serialization metaclass for JSON conversion
4. Make a caching metaclass for expensive computations
5. Create a permission system metaclass for access control
""")