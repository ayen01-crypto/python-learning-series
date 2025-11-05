# Lesson 16: Metaclasses & Class Factories

## 🎯 Learning Objectives
- Understand metaclasses and the class creation process
- Create custom metaclasses for advanced class behavior
- Use `__new__` and `__init__` in metaclasses
- Implement class factories with metaclasses
- Apply metaclasses for ORM and framework development
- Master advanced object creation patterns

## 📖 Theory

### Metaclasses
Metaclasses control class creation:
```python
class Meta(type):
    def __new__(cls, name, bases, attrs):
        # Modify class attributes before creation
        attrs['created_at'] = time.time()
        return super().__new__(cls, name, bases, attrs)

class MyClass(metaclass=Meta):
    pass

print(MyClass.created_at)  # Timestamp when class was created
```

### Class Factory Pattern
Dynamic class creation based on parameters:
```python
def class_factory(name, bases, attrs):
    # Add common functionality
    attrs['debug'] = True
    return type(name, bases, attrs)

MyClass = class_factory('MyClass', (), {'value': 42})
```

## 💻 Examples

See `examples.py` for comprehensive metaclass demonstrations.

## 🚀 Mini Project: ORM Framework

Build a simple ORM framework using metaclasses!

**File**: `project_orm_framework.py`

## 🎓 Key Takeaways
- Metaclasses are powerful but should be used sparingly
- They control the class creation process
- Use for framework development and advanced patterns
- Combine with descriptors for powerful abstractions
- Understand the difference between `__new__` and `__init__`

## 💪 Practice Challenges

1. Create a validation framework with metaclasses
2. Build a serialization library
3. Implement a plugin system
4. Make a dependency injection framework
5. Create a mock object framework

## 🔗 Next Lesson
[Lesson 17: Descriptors & Properties →](../lesson-17-descriptors/)
