"""
Lesson 15: Async/Await & Asyncio
Comprehensive Examples
"""

import asyncio
import time
from typing import List, AsyncIterator


# ============================================
# 1. Basic Async/Await
# ============================================

print("=== BASIC ASYNC/AWAIT ===\n")

async def simple_coroutine(name: str, delay: float):
    """Simple async coroutine."""
    print(f"Coroutine {name} started")
    await asyncio.sleep(delay)
    print(f"Coroutine {name} finished")
    return f"Result from {name}"

async def main_basic():
    """Main function demonstrating basic async/await."""
    # Run coroutines sequentially
    print("Running coroutines sequentially:")
    start_time = time.time()
    
    result1 = await simple_coroutine("A", 1)
    result2 = await simple_coroutine("B", 1)
    result3 = await simple_coroutine("C", 1)
    
    end_time = time.time()
    print(f"Sequential results: {result1}, {result2}, {result3}")
    print(f"Sequential time: {end_time - start_time:.2f} seconds\n")
    
    # Run coroutines concurrently
    print("Running coroutines concurrently:")
    start_time = time.time()
    
    results = await asyncio.gather(
        simple_coroutine("X", 1),
        simple_coroutine("Y", 1),
        simple_coroutine("Z", 1)
    )
    
    end_time = time.time()
    print(f"Concurrent results: {results}")
    print(f"Concurrent time: {end_time - start_time:.2f} seconds")

# Run the basic example
print("Running basic async example:")
asyncio.run(main_basic())


# ============================================
# 2. Async Tasks
# ============================================

print("\n" + "="*60)
print("=== ASYNC TASKS ===\n")

async def task_worker(name: str, work_time: float):
    """Worker that performs some work."""
    print(f"Worker {name} starting work")
    await asyncio.sleep(work_time)
    print(f"Worker {name} completed work")
    return f"Work result from {name}"

async def main_tasks():
    """Main function demonstrating task management."""
    # Create tasks
    task1 = asyncio.create_task(task_worker("Task-1", 2))
    task2 = asyncio.create_task(task_worker("Task-2", 1))
    task3 = asyncio.create_task(task_worker("Task-3", 3))
    
    print("Tasks created, doing other work...")
    await asyncio.sleep(0.5)  # Do some other work
    
    # Wait for tasks to complete
    print("Waiting for tasks to complete...")
    results = await asyncio.gather(task1, task2, task3)
    print(f"Task results: {results}")

# Run the tasks example
print("Running tasks example:")
asyncio.run(main_tasks())


# ============================================
# 3. Async Context Managers
# ============================================

print("\n" + "="*60)
print("=== ASYNC CONTEXT MANAGERS ===\n")

class AsyncDatabaseConnection:
    """Async context manager for database connections."""
    
    def __init__(self, host: str):
        self.host = host
        self.connected = False
    
    async def __aenter__(self):
        print(f"Connecting to database at {self.host}")
        await asyncio.sleep(0.5)  # Simulate connection time
        self.connected = True
        print("Database connected")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Closing database connection")
        await asyncio.sleep(0.2)  # Simulate disconnection time
        self.connected = False
        print("Database disconnected")
        return False
    
    async def execute_query(self, query: str):
        """Execute a database query."""
        if not self.connected:
            raise RuntimeError("Not connected to database")
        print(f"Executing query: {query}")
        await asyncio.sleep(0.3)  # Simulate query time
        return f"Results for: {query}"

async def main_context_manager():
    """Main function demonstrating async context managers."""
    async with AsyncDatabaseConnection("localhost") as db:
        result1 = await db.execute_query("SELECT * FROM users")
        result2 = await db.execute_query("UPDATE users SET name='John'")
        print(f"Query results: {result1}, {result2}")

# Run the context manager example
print("Running async context manager example:")
asyncio.run(main_context_manager())


# ============================================
# 4. Async Iterators
# ============================================

print("\n" + "="*60)
print("=== ASYNC ITERATORS ===\n")

class AsyncNumberGenerator:
    """Async iterator that generates numbers."""
    
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.current = start
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.end:
            raise StopAsyncIteration
        await asyncio.sleep(0.1)  # Simulate async work
        result = self.current
        self.current += 1
        return result

async def main_async_iterator():
    """Main function demonstrating async iterators."""
    print("Using async iterator:")
    async for number in AsyncNumberGenerator(1, 6):
        print(f"  Number: {number}")

# Run the async iterator example
print("Running async iterator example:")
asyncio.run(main_async_iterator())


# ============================================
# 5. Async Generators
# ============================================

print("\n" + "="*60)
print("=== ASYNC GENERATORS ===\n")

async def async_data_stream():
    """Async generator that yields data."""
    for i in range(5):
        await asyncio.sleep(0.2)  # Simulate data fetching
        yield f"Data item {i}"

async def main_async_generator():
    """Main function demonstrating async generators."""
    print("Using async generator:")
    async for item in async_data_stream():
        print(f"  Received: {item}")

# Run the async generator example
print("Running async generator example:")
asyncio.run(main_async_generator())


# ============================================
# 6. Exception Handling
# ============================================

print("\n" + "="*60)
print("=== EXCEPTION HANDLING ===\n")

async def risky_operation(should_fail: bool):
    """Operation that may fail."""
    await asyncio.sleep(0.5)
    if should_fail:
        raise ValueError("Operation failed!")
    return "Operation succeeded"

async def main_exception_handling():
    """Main function demonstrating exception handling."""
    # Handle individual exceptions
    print("Handling individual exceptions:")
    try:
        result = await risky_operation(True)
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Caught exception: {e}")
    
    # Handle exceptions in gather
    print("\nHandling exceptions in gather:")
    try:
        results = await asyncio.gather(
            risky_operation(False),
            risky_operation(True),  # This will fail
            risky_operation(False),
            return_exceptions=True  # Don't cancel other tasks
        )
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Task {i} failed: {result}")
            else:
                print(f"Task {i} succeeded: {result}")
    except Exception as e:
        print(f"Overall exception: {e}")

# Run the exception handling example
print("Running exception handling example:")
asyncio.run(main_exception_handling())


# ============================================
# 7. Async Queue
# ============================================

print("\n" + "="*60)
print("=== ASYNC QUEUE ===\n")

async def producer(queue: asyncio.Queue, name: str):
    """Producer that puts items in queue."""
    for i in range(3):
        item = f"{name}-item-{i}"
        await queue.put(item)
        print(f"Producer {name} produced: {item}")
        await asyncio.sleep(0.5)

async def consumer(queue: asyncio.Queue, name: str):
    """Consumer that gets items from queue."""
    while True:
        try:
            item = await asyncio.wait_for(queue.get(), timeout=2.0)
            print(f"Consumer {name} consumed: {item}")
            queue.task_done()
            await asyncio.sleep(0.3)
        except asyncio.TimeoutError:
            print(f"Consumer {name} timed out")
            break

async def main_async_queue():
    """Main function demonstrating async queue."""
    queue = asyncio.Queue(maxsize=5)
    
    # Create producer and consumer tasks
    producer_task = asyncio.create_task(producer(queue, "Producer-1"))
    consumer_tasks = [
        asyncio.create_task(consumer(queue, f"Consumer-{i}"))
        for i in range(2)
    ]
    
    # Wait for producer to finish
    await producer_task
    
    # Wait for queue to be empty
    await queue.join()
    
    # Cancel consumers
    for task in consumer_tasks:
        task.cancel()
    
    # Wait for consumers to be cancelled
    await asyncio.gather(*consumer_tasks, return_exceptions=True)

# Run the async queue example
print("Running async queue example:")
asyncio.run(main_async_queue())


# ============================================
# 8. Performance Comparison
# ============================================

print("\n" + "="*60)
print("=== PERFORMANCE COMPARISON ===\n")

async def async_io_operation(name: str):
    """Async I/O operation."""
    print(f"Starting async operation {name}")
    await asyncio.sleep(1)  # Simulate I/O
    print(f"Completed async operation {name}")
    return f"Result {name}"

def sync_io_operation(name: str):
    """Synchronous I/O operation."""
    print(f"Starting sync operation {name}")
    time.sleep(1)  # Simulate I/O
    print(f"Completed sync operation {name}")
    return f"Result {name}"

async def main_performance_comparison():
    """Compare async vs sync performance."""
    print("Sequential synchronous operations:")
    start_time = time.time()
    results = [sync_io_operation(f"Sync-{i}") for i in range(3)]
    sync_time = time.time() - start_time
    print(f"Synchronous time: {sync_time:.2f} seconds\n")
    
    print("Concurrent asynchronous operations:")
    start_time = time.time()
    results = await asyncio.gather(
        async_io_operation("Async-1"),
        async_io_operation("Async-2"),
        async_io_operation("Async-3")
    )
    async_time = time.time() - start_time
    print(f"Asynchronous time: {async_time:.2f} seconds")
    print(f"Speedup: {sync_time/async_time:.2f}x")

# Run the performance comparison
print("Running performance comparison:")
asyncio.run(main_performance_comparison())


# ============================================
# 9. Advanced Patterns
# ============================================

print("\n" + "="*60)
print("=== ADVANCED PATTERNS ===\n")

async def timeout_example():
    """Example with timeout handling."""
    try:
        # This will timeout
        await asyncio.wait_for(asyncio.sleep(2), timeout=1.0)
    except asyncio.TimeoutError:
        print("Operation timed out")

async def semaphore_example():
    """Example with semaphore for rate limiting."""
    semaphore = asyncio.Semaphore(2)  # Allow max 2 concurrent operations
    
    async def limited_operation(name: str):
        async with semaphore:
            print(f"Operation {name} started")
            await asyncio.sleep(1)
            print(f"Operation {name} completed")
    
    # Start 5 operations, but only 2 run concurrently
    await asyncio.gather(
        limited_operation("A"),
        limited_operation("B"),
        limited_operation("C"),
        limited_operation("D"),
        limited_operation("E")
    )

async def main_advanced_patterns():
    """Main function for advanced patterns."""
    print("Timeout example:")
    await timeout_example()
    
    print("\nSemaphore example:")
    await semaphore_example()

# Run advanced patterns
print("Running advanced patterns:")
asyncio.run(main_advanced_patterns())


# ============================================
# Practice Exercise
# ============================================

print("\n" + "="*60)
print("🎯 PRACTICE EXERCISE")
print("="*60)
print("""
Try these exercises:

1. Create an async web scraper
2. Build a real-time chat application
3. Implement an async file processor
4. Make an async API client with retry logic
5. Create a WebSocket-based game server
""")
