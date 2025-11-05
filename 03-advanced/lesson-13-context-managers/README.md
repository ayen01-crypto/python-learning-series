# Lesson 13: Context Managers

## 🎯 Learning Objectives
- Understand the context manager protocol (`__enter__`, `__exit__`)
- Use the `with` statement effectively
- Create custom context managers with classes
- Implement context managers with `contextlib`
- Handle exceptions in context managers
- Apply context managers for resource management

## 📖 Theory

### Context Manager Protocol
Context managers implement `__enter__()` and `__exit__()` methods:
```python
class DatabaseConnection:
    def __enter__(self):
        self.connection = connect_to_database()
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

with DatabaseConnection() as conn:
    # Use connection here
    pass
# Connection automatically closed
```

### Contextlib
Use `@contextmanager` decorator for simpler context managers:
```python
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.time()
    yield
    print(f"Elapsed: {time.time() - start}")

with timer():
    # Code to time
    pass
```

## 💻 Examples

See `examples.py` for comprehensive context manager demonstrations.

## 🚀 Mini Project: Resource Manager

Build a comprehensive resource management system using context managers!

**File**: `project_resource_manager.py`

## 🎓 Key Takeaways
- Context managers ensure proper resource cleanup
- Use `contextlib` for simpler implementations
- Handle exceptions properly in `__exit__`
- Combine multiple context managers
- Create reusable resource management patterns

## 💪 Practice Challenges

1. Create a file locker context manager
2. Build a database transaction manager
3. Implement a retry context manager
4. Make a temporary directory context manager
5. Create a performance monitoring context manager

## 🔗 Next Lesson
[Lesson 14: Multithreading & Multiprocessing →](../lesson-14-concurrency/)
