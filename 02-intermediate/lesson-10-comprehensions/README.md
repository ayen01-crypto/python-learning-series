# Lesson 10: List/Dict/Set Comprehensions

## 🎯 Learning Objectives
- Master list comprehensions for concise data processing
- Use dictionary and set comprehensions effectively
- Apply conditional logic in comprehensions
- Understand nested comprehensions
- Compare comprehensions with traditional loops
- Optimize performance with comprehensions

## 📖 Theory

### List Comprehensions
Concise way to create lists:
```python
# Traditional way
squares = []
for x in range(10):
    squares.append(x**2)

# List comprehension
squares = [x**2 for x in range(10)]
```

### Conditional Comprehensions
Filter elements with conditions:
```python
# Filter even numbers
evens = [x for x in range(20) if x % 2 == 0]

# Conditional expressions
processed = [x if x % 2 == 0 else -x for x in range(10)]
```

### Nested Comprehensions
Work with nested data structures:
```python
# Flatten a matrix
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
```

## 💻 Examples

See `examples.py` for comprehensive comprehension demonstrations.

## 🚀 Mini Project: Data Analyzer

Build a powerful data analysis tool using comprehensions!

**File**: `project_data_analyzer.py`

## 🎓 Key Takeaways
- Comprehensions are more readable and often faster than loops
- Use parentheses for generator expressions
- Apply conditions to filter data efficiently
- Combine comprehensions with built-in functions
- Avoid overly complex comprehensions

## 💪 Practice Challenges

1. Create a word frequency analyzer
2. Build a data transformation pipeline
3. Implement a matrix processing tool
4. Make a social media analytics dashboard
5. Create a financial data processor

## 🔗 Next Lesson
[Lesson 11: Decorators & Closures →](../../03-advanced/lesson-11-decorators/)
