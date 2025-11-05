# Lesson 09: Modules, Packages & Imports

## 🎯 Learning Objectives
- Understand Python's module system
- Create and use custom modules
- Work with packages and `__init__.py`
- Master different import styles
- Use `if __name__ == "__main__"` effectively
- Manage module paths and PYTHONPATH

## 📖 Theory

### Modules
A module is a file containing Python code:
```python
# math_utils.py
def add(a, b):
    return a + b

# main.py
import math_utils
result = math_utils.add(5, 3)
```

### Import Styles
```python
import module
from module import function
from module import *
import module as alias
```

### Packages
Packages are directories containing modules with `__init__.py`:
```
mypackage/
    __init__.py
    module1.py
    module2.py
```

### PYTHONPATH
Control where Python looks for modules:
```bash
export PYTHONPATH=/path/to/modules
```

## 💻 Examples

See `examples.py` for comprehensive module demonstrations.

## 🚀 Mini Project: Package Manager

Build a complete package management system!

**File**: `project_package_manager.py`

## 🎓 Key Takeaways
- Use absolute imports when possible
- Avoid circular imports
- Structure packages logically
- Use `__all__` to control exports
- Leverage `if __name__ == "__main__"` for testing

## 💪 Practice Challenges

1. Create a utility package with math, string, and file functions
2. Build a configuration management system
3. Implement a plugin architecture
4. Make a logging utility package
5. Create a database abstraction package

## 🔗 Next Lesson
[Lesson 10: List/Dict/Set Comprehensions →](../lesson-10-comprehensions/)
