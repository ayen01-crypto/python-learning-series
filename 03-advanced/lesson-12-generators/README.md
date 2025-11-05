# Lesson 12: Generators & Iterators

## 🎯 Learning Objectives
- Understand the iterator protocol and how it works
- Create custom iterators and iterable objects
- Master generator functions with `yield`
- Use generator expressions for memory-efficient processing
- Implement coroutines with generators
- Apply generators for streaming data processing

## 📖 Theory

### Iterators
Objects that implement `__iter__()` and `__next__()` methods:
```python
class CountDown:
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.start <= 0:
            raise StopIteration
        self.start -= 1
        return self.start + 1

for num in CountDown(3):
    print(num)  # Prints: 3, 2, 1
```

### Generators
Functions that use `yield` to produce a sequence of values:
```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Use generator
fib = fibonacci()
for _ in range(5):
    print(next(fib))  # Prints: 0, 1, 1, 2, 3
```

## 💻 Examples

See `examples.py` for comprehensive generator demonstrations.

## 🚀 Mini Project: Data Pipeline

Build a streaming data processing pipeline using generators!

**File**: `project_data_pipeline.py`

## 🎓 Key Takeaways
- Generators are memory-efficient for large datasets
- Use `yield from` to delegate to other generators
- Generators can receive values with `send()`
- Implement the iterator protocol for custom iteration
- Combine generators for powerful data processing pipelines

## 💪 Practice Challenges

1. Create a log file processor with generators
2. Build a streaming JSON parser
3. Implement a real-time data analyzer
4. Make a web scraper with generator-based pagination
5. Create a memory-efficient file merger

## 🔗 Next Lesson
[Lesson 13: Context Managers →](../lesson-13-context-managers/)
