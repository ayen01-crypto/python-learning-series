# Lesson 15: Async/Await & Asyncio

## 🎯 Learning Objectives
- Understand asynchronous programming concepts
- Master async/await syntax
- Use asyncio for concurrent I/O operations
- Handle asynchronous exceptions
- Implement async context managers and iterators
- Apply async patterns for web development

## 📖 Theory

### Async/Await Basics
Asynchronous functions use `async def` and `await`:
```python
import asyncio

async def fetch_data(url):
    print(f"Fetching {url}")
    await asyncio.sleep(1)  # Simulate I/O
    return f"Data from {url}"

async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

asyncio.run(main())
```

### Event Loop
The event loop manages asynchronous execution:
```python
# Python 3.7+
asyncio.run(main())

# Older versions
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## 💻 Examples

See `examples.py` for comprehensive async demonstrations.

## 🚀 Mini Project: Chat Server

Build a real-time chat server using asyncio!

**File**: `project_chat_server.py`

## 🎓 Key Takeaways
- Use `async def` for coroutine functions
- Use `await` to pause execution until awaited object completes
- asyncio is ideal for I/O-bound concurrent operations
- Handle exceptions in async code with try/except
- Use `async with` and `async for` for async context managers and iterators

## 💪 Practice Challenges

1. Create an async HTTP client
2. Build a real-time data streaming service
3. Implement an async database connection pool
4. Make an async file processor
5. Create a WebSocket-based game server

## 🔗 Next Lesson
[Lesson 16: Metaclasses & Class Factories →](../../04-expert/lesson-16-metaclasses/)
