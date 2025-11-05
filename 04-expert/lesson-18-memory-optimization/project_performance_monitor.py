"""
Mini Project: Performance Monitor

A comprehensive memory and performance monitoring tool for Python applications.
"""

import tracemalloc
import gc
import psutil
import time
import threading
from typing import Dict, List, Optional, Callable
from datetime import datetime
from collections import defaultdict, deque
import sys


# ============================================
# Performance Monitor Core
# ============================================

class PerformanceMonitor:
    """Comprehensive performance and memory monitoring tool."""
    
    def __init__(self, enable_tracing: bool = True):
        self.enable_tracing = enable_tracing
        self.is_monitoring = False
        self.metrics_history = defaultdict(deque)
        self.max_history = 1000  # Keep last 1000 measurements
        self.monitoring_thread = None
        self.stop_monitoring = threading.Event()
        
        if enable_tracing:
            tracemalloc.start()
    
    def start_monitoring(self, interval: float = 1.0):
        """Start continuous monitoring."""
        if self.is_monitoring:
            print("⚠️  Monitoring already started")
            return
        
        self.is_monitoring = True
        self.stop_monitoring.clear()
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop, 
            args=(interval,),
            daemon=True
        )
        self.monitoring_thread.start()
        print(f"✅ Performance monitoring started (interval: {interval}s)")
    
    def stop_monitoring(self):
        """Stop continuous monitoring."""
        if not self.is_monitoring:
            print("⚠️  Monitoring not started")
            return
        
        self.stop_monitoring.set()
        if self.monitoring_thread:
            self.monitoring_thread.join()
        
        self.is_monitoring = False
        print("✅ Performance monitoring stopped")
    
    def _monitoring_loop(self, interval: float):
        """Background monitoring loop."""
        while not self.stop_monitoring.is_set():
            try:
                metrics = self._collect_metrics()
                self._store_metrics(metrics)
                time.sleep(interval)
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
    
    def _collect_metrics(self) -> Dict[str, Any]:
        """Collect current performance metrics."""
        metrics = {
            'timestamp': datetime.now(),
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'memory_available': psutil.virtual_memory().available,
        }
        
        # Add process-specific metrics
        process = psutil.Process()
        metrics['process_memory'] = process.memory_info().rss
        metrics['process_cpu'] = process.cpu_percent()
        
        # Add garbage collector info
        gc_stats = gc.get_stats()
        metrics['gc_collections'] = sum(stat['collections'] for stat in gc_stats)
        metrics['gc_collected'] = sum(stat['collected'] for stat in gc_stats)
        
        # Add tracemalloc info if enabled
        if self.enable_tracing:
            current, peak = tracemalloc.get_traced_memory()
            metrics['traced_memory_current'] = current
            metrics['traced_memory_peak'] = peak
        
        return metrics
    
    def _store_metrics(self, metrics: Dict[str, Any]):
        """Store metrics in history."""
        timestamp = metrics['timestamp']
        for key, value in metrics.items():
            if key != 'timestamp':
                self.metrics_history[key].append((timestamp, value))
                # Keep history within limits
                while len(self.metrics_history[key]) > self.max_history:
                    self.metrics_history[key].popleft()
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        return self._collect_metrics()
    
    def get_metrics_history(self, metric_name: str, limit: int = None) -> List[tuple]:
        """Get historical metrics for a specific metric."""
        history = list(self.metrics_history[metric_name])
        if limit:
            history = history[-limit:]
        return history
    
    def get_peak_memory(self) -> Optional[int]:
        """Get peak memory usage."""
        if not self.enable_tracing:
            return None
        
        current, peak = tracemalloc.get_traced_memory()
        return peak
    
    def get_memory_snapshot(self, limit: int = 10) -> List[str]:
        """Get memory usage snapshot."""
        if not self.enable_tracing:
            return ["Tracemalloc not enabled"]
        
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        
        lines = []
        for stat in top_stats[:limit]:
            lines.append(f"{stat.size_diff} bytes in {stat.count_diff} blocks: {stat.traceback.format()}")
        
        return lines
    
    def reset_peak_memory(self):
        """Reset peak memory tracking."""
        if self.enable_tracing:
            tracemalloc.stop()
            tracemalloc.start()
    
    def force_gc(self) -> Dict[str, int]:
        """Force garbage collection and return stats."""
        before = len(gc.get_objects())
        collected = gc.collect()
        after = len(gc.get_objects())
        
        return {
            'before_objects': before,
            'after_objects': after,
            'collected_objects': collected
        }
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information."""
        vm = psutil.virtual_memory()
        return {
            'cpu_count': psutil.cpu_count(),
            'total_memory': vm.total,
            'available_memory': vm.available,
            'memory_percent': vm.percent,
            'python_version': sys.version,
            'platform': sys.platform
        }


# ============================================
# Memory Profiler Decorator
# ============================================

def profile_memory(func: Callable):
    """Decorator to profile memory usage of a function."""
    def wrapper(*args, **kwargs):
        # Start tracing
        tracemalloc.start()
        
        # Take snapshot before
        snapshot1 = tracemalloc.take_snapshot()
        
        # Execute function
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # Take snapshot after
        snapshot2 = tracemalloc.take_snapshot()
        
        # Calculate difference
        top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        
        # Print results
        print(f"\n📊 Memory Profile for {func.__name__}:")
        print(f"   Execution time: {end_time - start_time:.4f} seconds")
        print("   Top 5 memory allocations:")
        for stat in top_stats[:5]:
            print(f"     {stat}")
        
        # Stop tracing
        tracemalloc.stop()
        
        return result
    
    return wrapper


# ============================================
# Cache with Memory Management
# ============================================

class MemoryAwareCache:
    """Cache with memory usage tracking and limits."""
    
    def __init__(self, max_size: int = 1000, max_memory_mb: int = 100):
        self.cache = {}
        self.access_times = {}
        self.memory_usage = {}
        self.max_size = max_size
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.total_memory = 0
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key in self.cache:
            self.hits += 1
            self.access_times[key] = time.time()
            return self.cache[key]
        else:
            self.misses += 1
            return None
    
    def put(self, key: str, value: Any):
        """Put value in cache."""
        # Estimate memory usage
        memory_estimate = sys.getsizeof(value)
        
        # Check if we need to evict
        while (len(self.cache) >= self.max_size or 
               self.total_memory + memory_estimate > self.max_memory_bytes) and self.cache:
            # Evict least recently used
            lru_key = min(self.access_times.items(), key=lambda x: x[1])[0]
            self._remove_key(lru_key)
        
        # Add new item
        self.cache[key] = value
        self.access_times[key] = time.time()
        self.memory_usage[key] = memory_estimate
        self.total_memory += memory_estimate
    
    def _remove_key(self, key: str):
        """Remove key from cache."""
        if key in self.cache:
            self.total_memory -= self.memory_usage.get(key, 0)
            del self.cache[key]
            del self.access_times[key]
            del self.memory_usage[key]
    
    def clear(self):
        """Clear cache."""
        self.cache.clear()
        self.access_times.clear()
        self.memory_usage.clear()
        self.total_memory = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self.hits + self.misses
        hit_rate = self.hits / total_requests if total_requests > 0 else 0
        
        return {
            'size': len(self.cache),
            'total_memory': self.total_memory,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'max_size': self.max_size
        }


# ============================================
# Performance Benchmarking
# ============================================

class Benchmark:
    """Performance benchmarking utility."""
    
    def __init__(self):
        self.results = {}
    
    def time_function(self, func: Callable, *args, iterations: int = 1000, **kwargs) -> Dict[str, float]:
        """Time a function execution."""
        times = []
        
        # Warm up
        for _ in range(10):
            func(*args, **kwargs)
        
        # Actual timing
        for _ in range(iterations):
            start = time.perf_counter()
            func(*args, **kwargs)
            end = time.perf_counter()
            times.append(end - start)
        
        return {
            'min': min(times),
            'max': max(times),
            'avg': sum(times) / len(times),
            'total': sum(times),
            'iterations': iterations
        }
    
    def compare_functions(self, functions: Dict[str, Callable], *args, iterations: int = 1000, **kwargs):
        """Compare multiple functions."""
        results = {}
        for name, func in functions.items():
            results[name] = self.time_function(func, *args, iterations=iterations, **kwargs)
        
        # Sort by average time
        sorted_results = sorted(results.items(), key=lambda x: x[1]['avg'])
        
        print("📊 Function Performance Comparison:")
        print("-" * 60)
        print(f"{'Function':<20} {'Avg Time':<15} {'Min Time':<15} {'Max Time'}")
        print("-" * 60)
        
        for name, stats in sorted_results:
            print(f"{name:<20} {stats['avg']*1000:<15.4f} {stats['min']*1000:<15.4f} {stats['max']*1000:.4f} ms")
        
        return results


# ============================================
# User Interface
# ============================================

def print_header(text: str):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70)


def print_menu():
    """Display main menu."""
    print("\n" + "-" * 70)
    print("\n📋 MAIN MENU:")
    print("1.  Start Continuous Monitoring")
    print("2.  Get Current Metrics")
    print("3.  View Metrics History")
    print("4.  Memory Profiling")
    print("5.  Cache Performance")
    print("6.  Function Benchmarking")
    print("7.  System Information")
    print("8.  Performance Monitor Features")
    print("9.  Exit")


def start_continuous_monitoring_interactive(monitor: PerformanceMonitor):
    """Start continuous monitoring."""
    print_header("🔄 START CONTINUOUS MONITORING")
    
    try:
        interval = float(input("Monitoring interval in seconds (default 1.0): ") or "1.0")
        monitor.start_monitoring(interval)
        print("ℹ️  Monitoring started. Press Enter to stop...")
        input()
        monitor.stop_monitoring()
    except Exception as e:
        print(f"❌ Error: {e}")


def get_current_metrics_interactive(monitor: PerformanceMonitor):
    """Get current metrics."""
    print_header("📊 CURRENT METRICS")
    
    try:
        metrics = monitor.get_current_metrics()
        
        print("Current System Metrics:")
        print(f"  CPU Usage: {metrics['cpu_percent']:.1f}%")
        print(f"  Memory Usage: {metrics['memory_percent']:.1f}%")
        print(f"  Available Memory: {metrics['memory_available'] / (1024**3):.2f} GB")
        print(f"  Process Memory: {metrics['process_memory'] / (1024**2):.2f} MB")
        print(f"  Process CPU: {metrics['process_cpu']:.1f}%")
        
        if monitor.enable_tracing:
            print(f"  Traced Memory: {metrics['traced_memory_current'] / (1024**2):.2f} MB")
            print(f"  Peak Memory: {metrics['traced_memory_peak'] / (1024**2):.2f} MB")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def view_metrics_history_interactive(monitor: PerformanceMonitor):
    """View metrics history."""
    print_header("📈 METRICS HISTORY")
    
    try:
        print("Available metrics:")
        print("1. CPU Usage")
        print("2. Memory Usage")
        print("3. Process Memory")
        
        choice = input("Select metric (1-3): ").strip()
        metric_map = {"1": "cpu_percent", "2": "memory_percent", "3": "process_memory"}
        
        if choice in metric_map:
            metric_name = metric_map[choice]
            history = monitor.get_metrics_history(metric_name, limit=10)
            
            if history:
                print(f"\nLast 10 {metric_name} measurements:")
                for timestamp, value in history:
                    if metric_name == "process_memory":
                        value = f"{value / (1024**2):.2f} MB"
                    else:
                        value = f"{value:.1f}%"
                    print(f"  {timestamp.strftime('%H:%M:%S')}: {value}")
            else:
                print("❌ No history available")
        else:
            print("❌ Invalid choice")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def memory_profiling_interactive():
    """Demonstrate memory profiling."""
    print_header("🔍 MEMORY PROFILING")
    
    @profile_memory
    def memory_intensive_function():
        """Function that uses memory."""
        # Create some data structures
        data = []
        for i in range(1000):
            data.append([j for j in range(100)])
        
        # Create a dictionary
        mapping = {f"key_{i}": f"value_{i}" for i in range(1000)}
        
        return len(data), len(mapping)
    
    print("Running memory-intensive function with profiling...")
    result = memory_intensive_function()
    print(f"Function result: {result}")


def cache_performance_interactive():
    """Demonstrate cache performance."""
    print_header("キャッシング CACHE PERFORMANCE")
    
    cache = MemoryAwareCache(max_size=100, max_memory_mb=50)
    
    # Populate cache
    for i in range(150):
        cache.put(f"key_{i}", f"value_{i}" * 100)
    
    # Test cache hits/misses
    for i in range(100):
        cache.get(f"key_{i}")
    
    for i in range(100, 120):
        cache.get(f"key_{i}")
    
    stats = cache.get_stats()
    print("Cache Statistics:")
    print(f"  Size: {stats['size']}")
    print(f"  Total Memory: {stats['total_memory'] / 1024:.2f} KB")
    print(f"  Hits: {stats['hits']}")
    print(f"  Misses: {stats['misses']}")
    print(f"  Hit Rate: {stats['hit_rate']:.2%}")


def function_benchmarking_interactive():
    """Demonstrate function benchmarking."""
    print_header("⏱️  FUNCTION BENCHMARKING")
    
    def method1(data):
        """List comprehension method."""
        return [x * 2 for x in data]
    
    def method2(data):
        """Map method."""
        return list(map(lambda x: x * 2, data))
    
    def method3(data):
        """Loop method."""
        result = []
        for x in data:
            result.append(x * 2)
        return result
    
    # Create test data
    test_data = list(range(10000))
    
    # Benchmark
    benchmark = Benchmark()
    functions = {
        "List Comprehension": method1,
        "Map Function": method2,
        "For Loop": method3
    }
    
    benchmark.compare_functions(functions, test_data, iterations=100)


def system_information_interactive(monitor: PerformanceMonitor):
    """Show system information."""
    print_header("🖥️  SYSTEM INFORMATION")
    
    try:
        info = monitor.get_system_info()
        
        print("System Information:")
        print(f"  CPU Cores: {info['cpu_count']}")
        print(f"  Total Memory: {info['total_memory'] / (1024**3):.2f} GB")
        print(f"  Available Memory: {info['available_memory'] / (1024**3):.2f} GB")
        print(f"  Memory Usage: {info['memory_percent']:.1f}%")
        print(f"  Python Version: {info['python_version']}")
        print(f"  Platform: {info['platform']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def performance_monitor_features_interactive():
    """Show performance monitor features."""
    print_header("⚙️  PERFORMANCE MONITOR FEATURES")
    
    print("Performance Monitor Features:")
    print()
    print("🔄 Continuous Monitoring:")
    print("  • Real-time metrics collection")
    print("  • Configurable intervals")
    print("  • Background monitoring thread")
    print()
    print("📊 Memory Tracking:")
    print("  • Tracemalloc integration")
    print("  • Peak memory detection")
    print("  • Memory leak identification")
    print()
    print("⚡ Performance Metrics:")
    print("  • CPU usage monitoring")
    print("  • Memory usage tracking")
    print("  • Process-specific metrics")
    print()
    print("🛡️  Safety Features:")
    print("  • Automatic history management")
    print("  • Resource cleanup")
    print("  • Error handling")
    print()
    print("🔧 Advanced Tools:")
    print("  • Memory profiling decorator")
    print("  • Cache with LRU eviction")
    print("  • Function benchmarking")
    print("  • Garbage collection monitoring")


# ============================================
# Main Application
# ============================================

def main():
    """Main application loop."""
    
    # Create performance monitor
    monitor = PerformanceMonitor()
    
    print("=" * 70)
    print("📊  PERFORMANCE MONITOR  📊".center(70))
    print("=" * 70)
    print("Comprehensive memory and performance monitoring tool!")
    
    while True:
        print_menu()
        choice = input("\nYour choice: ").strip()
        
        if choice == '1':
            start_continuous_monitoring_interactive(monitor)
        elif choice == '2':
            get_current_metrics_interactive(monitor)
        elif choice == '3':
            view_metrics_history_interactive(monitor)
        elif choice == '4':
            memory_profiling_interactive()
        elif choice == '5':
            cache_performance_interactive()
        elif choice == '6':
            function_benchmarking_interactive()
        elif choice == '7':
            system_information_interactive(monitor)
        elif choice == '8':
            performance_monitor_features_interactive()
        elif choice == '9':
            monitor.stop_monitoring()
            print("\n👋 Thank you for using the Performance Monitor!")
            print("=" * 70 + "\n")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
