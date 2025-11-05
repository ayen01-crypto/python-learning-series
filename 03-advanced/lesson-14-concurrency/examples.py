"""
Lesson 14: Multithreading & Multiprocessing
Comprehensive Examples
"""

import threading
import multiprocessing
import time
import queue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List


# ============================================
# 1. Basic Threading
# ============================================

print("=== BASIC THREADING ===\n")

def worker_function(name: str, duration: int):
    """Simple worker function."""
    print(f"Thread {name} started")
    time.sleep(duration)
    print(f"Thread {name} finished")

# Create and start threads
threads = []
for i in range(3):
    thread = threading.Thread(target=worker_function, args=(f"Worker-{i}", 2))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("All threads completed\n")


# ============================================
# 2. Thread Synchronization
# ============================================

print("="*60)
print("=== THREAD SYNCHRONIZATION ===\n")

# Shared resource
counter = 0
counter_lock = threading.Lock()

def increment_counter(name: str, iterations: int):
    """Increment counter with locking."""
    global counter
    for i in range(iterations):
        with counter_lock:  # Acquire lock
            temp = counter
            time.sleep(0.001)  # Simulate some work
            counter = temp + 1
        print(f"{name}: {counter}")

# Create threads without proper synchronization
print("Without synchronization:")
counter = 0
threads = []
for i in range(3):
    thread = threading.Thread(target=increment_counter, args=(f"Thread-{i}", 5))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(f"Final counter value: {counter}\n")

# Reset and try with proper synchronization
print("With synchronization:")
counter = 0
threads = []
for i in range(3):
    thread = threading.Thread(target=increment_counter, args=(f"Thread-{i}", 5))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(f"Final counter value: {counter}\n")


# ============================================
# 3. Producer-Consumer Pattern
# ============================================

print("="*60)
print("=== PRODUCER-CONSUMER ===\n")

# Thread-safe queue
work_queue = queue.Queue()
result_queue = queue.Queue()

def producer(name: str, items: List[int]):
    """Produce items and put them in queue."""
    for item in items:
        work_queue.put(item)
        print(f"Producer {name} produced: {item}")
        time.sleep(0.1)

def consumer(name: str):
    """Consume items from queue."""
    while True:
        try:
            item = work_queue.get(timeout=1)
            # Process item
            result = item * 2
            result_queue.put(result)
            print(f"Consumer {name} processed: {item} -> {result}")
            work_queue.task_done()
            time.sleep(0.2)
        except queue.Empty:
            print(f"Consumer {name} timed out")
            break

# Start producer and consumers
producer_thread = threading.Thread(target=producer, args=("P1", [1, 2, 3, 4, 5]))
consumer_threads = []
for i in range(2):
    consumer_thread = threading.Thread(target=consumer, args=(f"C{i}",))
    consumer_threads.append(consumer_thread)

producer_thread.start()
for thread in consumer_threads:
    thread.start()

producer_thread.join()
for thread in consumer_threads:
    thread.join()

print("Producer-Consumer pattern completed\n")


# ============================================
# 4. Thread Pools
# ============================================

print("="*60)
print("=== THREAD POOLS ===\n")

def cpu_bound_task(n: int) -> int:
    """CPU-bound task."""
    result = 0
    for i in range(n * 1000000):
        result += i
    return result

def io_bound_task(name: str, delay: int) -> str:
    """I/O-bound task."""
    print(f"Task {name} started")
    time.sleep(delay)
    print(f"Task {name} completed")
    return f"Result from {name}"

# Using ThreadPoolExecutor for I/O-bound tasks
print("ThreadPoolExecutor for I/O-bound tasks:")
with ThreadPoolExecutor(max_workers=3) as executor:
    # Submit tasks
    futures = []
    for i in range(5):
        future = executor.submit(io_bound_task, f"Task-{i}", 1)
        futures.append(future)
    
    # Get results
    for future in futures:
        result = future.result()
        print(f"Got result: {result}")

print()


# ============================================
# 5. Basic Multiprocessing
# ============================================

print("="*60)
print("=== BASIC MULTIPROCESSING ===\n")

def process_worker(name: str, duration: int):
    """Worker function for processes."""
    print(f"Process {name} started (PID: {multiprocessing.current_process().pid})")
    time.sleep(duration)
    print(f"Process {name} finished")
    return f"Result from {name}"

# Create and start processes
if __name__ == "__main__":
    processes = []
    for i in range(3):
        process = multiprocessing.Process(target=process_worker, args=(f"Process-{i}", 2))
        processes.append(process)
        process.start()
    
    # Wait for all processes to complete
    for process in processes:
        process.join()
    
    print("All processes completed\n")


# ============================================
# 6. Process Pools
# ============================================

print("="*60)
print("=== PROCESS POOLS ===\n")

def calculate_square(n: int) -> int:
    """Calculate square of a number."""
    time.sleep(0.1)  # Simulate work
    return n * n

if __name__ == "__main__":
    # Using ProcessPoolExecutor for CPU-bound tasks
    print("ProcessPoolExecutor for CPU-bound tasks:")
    with ProcessPoolExecutor(max_workers=3) as executor:
        # Submit tasks
        numbers = [1, 2, 3, 4, 5, 6, 7, 8]
        futures = [executor.submit(calculate_square, n) for n in numbers]
        
        # Get results
        results = [future.result() for future in futures]
        print(f"Squares: {results}")
    
    print()


# ============================================
# 7. Inter-Process Communication
# ============================================

print("="*60)
print("=== INTER-PROCESS COMMUNICATION ===\n")

def sender(queue, data):
    """Send data through queue."""
    for item in data:
        queue.put(item)
        print(f"Sent: {item}")
        time.sleep(0.1)
    queue.put(None)  # Sentinel value

def receiver(queue):
    """Receive data from queue."""
    while True:
        item = queue.get()
        if item is None:  # Sentinel value
            break
        print(f"Received: {item}")
        queue.task_done()

if __name__ == "__main__":
    # Create queue for communication
    ipc_queue = multiprocessing.Queue()
    
    # Start sender and receiver processes
    data_to_send = ["Hello", "World", "From", "Process"]
    sender_process = multiprocessing.Process(target=sender, args=(ipc_queue, data_to_send))
    receiver_process = multiprocessing.Process(target=receiver, args=(ipc_queue,))
    
    sender_process.start()
    receiver_process.start()
    
    sender_process.join()
    receiver_process.join()
    
    print("IPC completed\n")


# ============================================
# 8. Shared Memory
# ============================================

print("="*60)
print("=== SHARED MEMORY ===\n")

def increment_shared_value(shared_value, lock, iterations):
    """Increment shared value."""
    for _ in range(iterations):
        with lock:
            shared_value.value += 1

if __name__ == "__main__":
    # Shared value and lock
    shared_counter = multiprocessing.Value('i', 0)
    shared_lock = multiprocessing.Lock()
    
    # Create processes
    processes = []
    for i in range(3):
        process = multiprocessing.Process(
            target=increment_shared_value, 
            args=(shared_counter, shared_lock, 100)
        )
        processes.append(process)
        process.start()
    
    # Wait for completion
    for process in processes:
        process.join()
    
    print(f"Final shared counter value: {shared_counter.value}\n")


# ============================================
# 9. Performance Comparison
# ============================================

print("="*60)
print("=== PERFORMANCE COMPARISON ===\n")

def time_function(func, *args, **kwargs):
    """Time a function execution."""
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return result, end - start

def sequential_execution():
    """Execute tasks sequentially."""
    results = []
    for i in range(5):
        result = io_bound_task(f"Sequential-{i}", 0.5)
        results.append(result)
    return results

def threaded_execution():
    """Execute tasks with threading."""
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(io_bound_task, f"Threaded-{i}", 0.5) for i in range(5)]
        return [future.result() for future in futures]

if __name__ == "__main__":
    # Compare sequential vs threaded execution
    print("Performance comparison:")
    
    _, sequential_time = time_function(sequential_execution)
    _, threaded_time = time_function(threaded_execution)
    
    print(f"Sequential execution: {sequential_time:.2f} seconds")
    print(f"Threaded execution: {threaded_time:.2f} seconds")
    print(f"Speedup: {sequential_time/threaded_time:.2f}x\n")


# ============================================
# 10. Advanced Concurrency Patterns
# ============================================

print("="*60)
print("=== ADVANCED PATTERNS ===\n")

# Semaphore example
semaphore = threading.Semaphore(2)  # Allow max 2 threads

def limited_worker(name: str):
    """Worker that respects semaphore limit."""
    with semaphore:
        print(f"{name} acquired semaphore")
        time.sleep(2)
        print(f"{name} releasing semaphore")

print("Semaphore example:")
threads = []
for i in range(4):
    thread = threading.Thread(target=limited_worker, args=(f"Worker-{i}",))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print()

# Event example
event = threading.Event()

def waiter(name: str):
    """Thread that waits for event."""
    print(f"{name} waiting for event")
    event.wait()
    print(f"{name} received event")

def setter():
    """Thread that sets event."""
    time.sleep(2)
    print("Setting event")
    event.set()

print("Event example:")
waiter_threads = [threading.Thread(target=waiter, args=(f"Waiter-{i}",)) for i in range(3)]
setter_thread = threading.Thread(target=setter)

for thread in waiter_threads:
    thread.start()
setter_thread.start()

for thread in waiter_threads:
    thread.join()
setter_thread.join()

print("\n" + "="*60)
print("🎯 PRACTICE EXERCISE")
print("="*60)
print("""
Try these exercises:

1. Create a concurrent web scraper
2. Build a multi-threaded file processor
3. Implement a producer-consumer queue system
4. Make a parallel image processor
5. Create a distributed task scheduler
""")
