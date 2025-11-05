# Lesson 07: File I/O & Working with Files

## 🎯 Learning Objectives
- Read from and write to text files
- Work with different file modes (r, w, a, r+, etc.)
- Handle file paths and directories
- Process CSV and JSON files
- Use context managers (with statement)
- Handle file exceptions properly

## 📖 Theory

### File Operations
Python provides built-in functions for file handling:
```python
# Basic file operations
file = open('filename.txt', 'r')
content = file.read()
file.close()

# Better approach with context manager
with open('filename.txt', 'r') as file:
    content = file.read()
```

### File Modes
- `'r'`: Read (default)
- `'w'`: Write (overwrites existing)
- `'a'`: Append
- `'r+'`: Read and write
- `'b'`: Binary mode (e.g., `'rb'`, `'wb'`)

### Context Managers
Always use `with` statement for automatic file closing:
```python
with open('file.txt', 'r') as f:
    data = f.read()
# File automatically closed here
```

## 💻 Examples

See `examples.py` for comprehensive file handling demonstrations.

## 🚀 Mini Project: Contact Manager

Build a complete contact management system with file persistence!

**File**: `project_contact_manager.py`

## 🎓 Key Takeaways
- Always use context managers (`with` statement) for file operations
- Handle file exceptions with try/except blocks
- Use appropriate file modes for your needs
- Process files line by line for large files
- JSON is great for structured data storage

## 💪 Practice Challenges

1. Create a simple note-taking application
2. Build a log file analyzer
3. Make a configuration file reader
4. Implement a data backup system
5. Create a file search utility

## 🔗 Next Lesson
[Lesson 08: Error Handling & Exceptions →](../lesson-08-error-handling/)
