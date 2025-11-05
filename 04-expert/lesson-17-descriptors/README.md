# Lesson 17: Descriptors & Properties

## 🎯 Learning Objectives
- Understand the descriptor protocol (`__get__`, `__set__`, `__delete__`)
- Create custom descriptors for advanced attribute access
- Use `@property` decorator effectively
- Implement data validation with descriptors
- Apply descriptors for lazy evaluation and caching
- Master attribute access control

## 📖 Theory

### Descriptor Protocol
Descriptors control attribute access:
```python
class ValidatedAttribute:
    def __init__(self, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if value < 0:
            raise ValueError("Value must be positive")
        obj.__dict__[self.name] = value

class MyClass:
    score = ValidatedAttribute('score')
```

### Properties
Simplified descriptor implementation:
```python
class Person:
    def __init__(self, name):
        self._name = name
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value
```

## 💻 Examples

See `examples.py` for comprehensive descriptor demonstrations.

## 🚀 Mini Project: Configuration Manager

Build a configuration management system using descriptors!

**File**: `project_config_manager.py`

## 🎓 Key Takeaways
- Descriptors provide fine-grained control over attribute access
- Use for validation, type checking, and computed properties
- Properties are simplified descriptors for common cases
- Combine with metaclasses for powerful abstractions
- Understand the difference between data and non-data descriptors

## 💪 Practice Challenges

1. Create a type-checking descriptor
2. Build a lazy-loading descriptor
3. Implement a cached property descriptor
4. Make a configuration validation system
5. Create a permission-based attribute access system

## 🔗 Next Lesson
[Lesson 18: Memory Management & Optimization →](../lesson-18-memory-optimization/)
