# Lesson 14: Multithreading & Multiprocessing

## 🎯 Learning Objectives
- Understand the difference between threading and multiprocessing
- Create and manage threads with the `threading` module
- Use locks, semaphores, and other synchronization primitives
- Implement multiprocessing for CPU-bound tasks
- Handle inter-process communication
- Apply concurrency patterns effectively

## 📖 Theory

### Threading
Threads share memory space and are good for I/O-bound tasks:
```python
import threading

def worker(name):
    print(f"Worker {name} started")
    time.sleep(2)
    print(f"Worker {name} finished")

thread = threading.Thread(target=worker, args=("A",))
thread.start()
thread.join()  # Wait for completion
```

### Multiprocessing
Processes have separate memory spaces and are good for CPU-bound tasks:
```python
from multiprocessing import Process

def worker(name):
    print(f"Process {name} started")
    # CPU-intensive work
    print(f"Process {name} finished")

process = Process(target=worker, args=("A",))
process.start()
process.join()  # Wait for completion
```

## 💻 Examples

See `examples.py` for comprehensive concurrency demonstrations.

## 🚀 Mini Project: Web Crawler

Build a concurrent web crawler using threading and multiprocessing!

**File**: `project_web_crawler.py`

## 🎓 Key Takeaways
- Use threading for I/O-bound tasks
- Use multiprocessing for CPU-bound tasks
- Always synchronize access to shared resources
- Handle exceptions in concurrent code
- Monitor and limit resource usage

## 💪 Practice Challenges

1. Create a concurrent file downloader
2. Build a multi-threaded web server
3. Implement a parallel data processor
4. Make a distributed task queue
5. Create a real-time data aggregator

## 🔗 Next Lesson
[Lesson 15: Async/Await & Asyncio →](../lesson-15-async/)
