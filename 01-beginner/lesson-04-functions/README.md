# Lesson 04: Functions & Scope

## 🎯 Learning Objectives
- Define and call functions
- Use parameters and return values
- Understand default and keyword arguments
- Master variable scope (local, global, nonlocal)
- Create lambda functions
- Use *args and **kwargs

## 📖 Theory

### Functions
Functions are reusable blocks of code that perform specific tasks:
```python
def function_name(parameters):
    """Docstring: describes the function"""
    # function body
    return value
```

### Parameters vs Arguments
- **Parameters**: Variables in function definition
- **Arguments**: Actual values passed to function

### Types of Arguments
1. **Positional**: Order matters
2. **Keyword**: Name specified
3. **Default**: Have default values
4. **Variable-length**: *args, **kwargs

### Scope
- **Local**: Inside function
- **Global**: Outside all functions
- **Nonlocal**: Enclosing function

## 💻 Examples

See `examples.py` for detailed demonstrations.

## 🚀 Mini Project: Password Generator & Validator

Create a tool that generates secure passwords and validates password strength!

**File**: `project_password_tool.py`

## 🎓 Key Takeaways
- Functions promote code reuse
- Always use docstrings to document functions
- Return values make functions testable
- Avoid global variables when possible
- Lambda functions are for simple one-liners

## 💪 Practice Challenges

1. Create a function that calculates factorial
2. Build a prime number checker function
3. Write a function that reverses a string
4. Make a function to find the maximum of three numbers
5. Create a decorator function (preview of advanced topic)

## 🔗 Next Lesson
[Lesson 05: Data Structures →](../lesson-05-data-structures/)
