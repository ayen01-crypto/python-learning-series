# Lesson 05: Data Structures (Lists, Tuples, Sets, Dictionaries)

## 🎯 Learning Objectives
- Master Python's built-in data structures
- Work with lists (mutable sequences)
- Use tuples (immutable sequences)
- Understand sets (unique unordered collections)
- Manipulate dictionaries (key-value pairs)
- Choose the right data structure for your needs

## 📖 Theory

### Lists
Ordered, mutable collections that can contain duplicate elements.
```python
fruits = ["apple", "banana", "cherry"]
```

### Tuples
Ordered, immutable collections.
```python
coordinates = (10, 20)
```

### Sets
Unordered collections of unique elements.
```python
unique_numbers = {1, 2, 3, 4, 5}
```

### Dictionaries
Unordered collections of key-value pairs.
```python
person = {"name": "Alice", "age": 30}
```

## 📊 Comparison Table

| Structure | Ordered | Mutable | Duplicates | Syntax |
|-----------|---------|---------|------------|--------|
| List      | ✅      | ✅      | ✅         | `[]`   |
| Tuple     | ✅      | ❌      | ✅         | `()`   |
| Set       | ❌      | ✅      | ❌         | `{}`   |
| Dict      | ✅*     | ✅      | Keys: ❌   | `{:}`  |

*Python 3.7+ maintains insertion order

## 💻 Examples

See `examples.py` for comprehensive demonstrations.

## 🚀 Mini Project: Student Grade Manager

Build a complete system to manage student records and calculate statistics!

**File**: `project_student_manager.py`

## 🎓 Key Takeaways
- Lists are the most versatile data structure
- Use tuples for data that shouldn't change
- Sets are perfect for uniqueness and fast membership testing
- Dictionaries map keys to values efficiently
- List comprehensions create lists concisely

## 💪 Practice Challenges

1. Create a shopping cart system using dictionaries
2. Find duplicate elements in a list using sets
3. Implement a simple phone book with search
4. Sort a list of dictionaries by a specific key
5. Create nested data structures (list of dicts, etc.)

## 🔗 Next Lesson
[Lesson 06: Object-Oriented Programming →](../../02-intermediate/lesson-06-oop/)

---

**Congratulations!** You've completed the Beginner Level! 🎉
You're ready to move to Intermediate concepts.
