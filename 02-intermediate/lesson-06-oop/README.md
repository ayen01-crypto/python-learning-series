# Lesson 06: Object-Oriented Programming (OOP)

## 🎯 Learning Objectives
- Understand classes and objects
- Master attributes and methods
- Use constructors (__init__)
- Implement inheritance and polymorphism
- Apply encapsulation principles
- Use special methods (magic/dunder methods)

## 📖 Theory

### Classes and Objects
A **class** is a blueprint for creating objects. An **object** is an instance of a class.

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def bark(self):
        return f"{self.name} says Woof!"

my_dog = Dog("Buddy", 3)
```

### Four Pillars of OOP

1. **Encapsulation**: Bundling data and methods
2. **Inheritance**: Reusing code from parent classes
3. **Polymorphism**: Same interface, different implementations
4. **Abstraction**: Hiding complex implementation details

### Key Concepts

- **`self`**: Refers to the instance itself
- **`__init__`**: Constructor method
- **Instance variables**: Unique to each object
- **Class variables**: Shared by all instances
- **Methods**: Functions defined inside a class

## 💻 Examples

See `examples.py` for detailed OOP demonstrations.

## 🚀 Mini Project: Library Management System

Build a complete OOP system to manage books, members, and transactions!

**File**: `project_library_system.py`

## 🎓 Key Takeaways
- Classes organize code into logical units
- Inheritance promotes code reuse
- Encapsulation protects data
- Use `@property` for controlled attribute access
- Special methods customize object behavior

## 💪 Practice Challenges

1. Create a `BankAccount` class with deposit/withdraw methods
2. Build a `Vehicle` hierarchy (Car, Truck, Motorcycle)
3. Implement a `Shape` class with area calculation
4. Create a `Student` class with GPA calculation
5. Design a simple game with character classes

## 🔗 Next Lesson
[Lesson 07: File I/O →](../lesson-07-file-io/)
