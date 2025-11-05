# Lesson 11: Decorators & Closures

## 🎯 Learning Objectives
- Understand closures and their use cases
- Master function decorators for code enhancement
- Create decorators with parameters
- Implement class decorators
- Use built-in decorators (@property, @staticmethod, @classmethod)
- Apply decorators for logging, timing, and caching

## 📖 Theory

### Closures
A closure is a function that captures variables from its enclosing scope:
```python
def outer_function(x):
    def inner_function(y):
        return x + y  # x is captured from outer scope
    return inner_function

add_five = outer_function(5)
result = add_five(3)  # Returns 8
```

### Decorators
Decorators are functions that modify the behavior of other functions:
```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function")
        result = func(*args, **kwargs)
        print("After function")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()  # Prints: Before function, Hello!, After function
```

## 💻 Examples

See `examples.py` for comprehensive decorator demonstrations.

## 🚀 Mini Project: API Framework

Build a lightweight API framework using decorators!

**File**: `project_api_framework.py`

## 🎓 Key Takeaways
- Decorators are syntactic sugar for `function = decorator(function)`
- Use `functools.wraps` to preserve function metadata
- Closures capture variables from enclosing scopes
- Decorators can modify function behavior without changing code
- Combine multiple decorators for complex functionality

## 💪 Practice Challenges

1. Create a retry decorator with exponential backoff
2. Build a validation decorator for function parameters
3. Implement a rate-limiting decorator
4. Make a memoization decorator for caching
5. Create a decorator for automatic type conversion

## 🔗 Next Lesson
[Lesson 12: Generators & Iterators →](../lesson-12-generators/)
