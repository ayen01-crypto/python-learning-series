"""
Mini Project: Data Pipeline

A streaming data processing pipeline using generators for efficient data handling.
"""

import json
import csv
import time
from typing import Generator, Iterator, Any, Dict, List
from datetime import datetime


# ============================================
# Data Pipeline Core
# ============================================

class DataPipeline:
    """Streaming data processing pipeline using generators."""
    
    def __init__(self):
        self.processors = []
    
    def add_processor(self, processor_func):
        """Add a processor function to the pipeline."""
        self.processors.append(processor_func)
        return self
    
    def process(self, data_source):
        """Process data through the pipeline."""
        # Start with the data source
        data_stream = data_source
        
        # Apply each processor in sequence
        for processor in self.processors:
            data_stream = processor(data_stream)
        
        return data_stream


# ============================================
# Data Sources
# ============================================

def file_reader(filename: str) -> Generator[Dict[str, Any], None, None]:
    """Read data from a JSON file line by line."""
    try:
        with open(filename, 'r') as f:
            for line in f:
                if line.strip():
                    yield json.loads(line)
    except FileNotFoundError:
        yield {"error": f"File {filename} not found"}
    except json.JSONDecodeError as e:
        yield {"error": f"JSON decode error: {e}"}

def csv_reader(filename: str) -> Generator[Dict[str, Any], None, None]:
    """Read data from a CSV file."""
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                for key, value in row.items():
                    if value.isdigit():
                        row[key] = int(value)
                    elif value.replace('.', '').isdigit():
                        row[key] = float(value)
                yield row
    except FileNotFoundError:
        yield {"error": f"File {filename} not found"}

def api_data_source(url: str) -> Generator[Dict[str, Any], None, None]:
    """Simulate API data source."""
    # In a real implementation, this would make HTTP requests
    sample_data = [
        {"id": 1, "name": "Alice", "age": 30, "city": "New York", "salary": 75000},
        {"id": 2, "name": "Bob", "age": 25, "city": "London", "salary": 65000},
        {"id": 3, "name": "Charlie", "age": 35, "city": "Paris", "salary": 80000},
        {"id": 4, "name": "Diana", "age": 28, "city": "Tokyo", "salary": 70000},
        {"id": 5, "name": "Ethan", "age": 32, "city": "Sydney", "salary": 85000}
    ]
    
    for record in sample_data:
        yield record
        time.sleep(0.1)  # Simulate network delay


# ============================================
# Data Processors
# ============================================

def filter_records(condition_func):
    """Filter records based on a condition."""
    def processor(data_stream):
        for record in data_stream:
            if "error" not in record and condition_func(record):
                yield record
    return processor

def transform_records(transform_func):
    """Transform records using a function."""
    def processor(data_stream):
        for record in data_stream:
            if "error" not in record:
                yield transform_func(record)
            else:
                yield record
    return processor

def add_timestamp(data_stream):
    """Add timestamp to records."""
    for record in data_stream:
        if "error" not in record:
            record["processed_at"] = datetime.now().isoformat()
        yield record

def limit_records(limit: int):
    """Limit the number of records."""
    def processor(data_stream):
        count = 0
        for record in data_stream:
            if count >= limit:
                break
            yield record
            count += 1
    return processor

def batch_records(batch_size: int):
    """Batch records into groups."""
    def processor(data_stream):
        batch = []
        for record in data_stream:
            batch.append(record)
            if len(batch) >= batch_size:
                yield batch
                batch = []
        if batch:  # Yield remaining records
            yield batch
    return processor


# ============================================
# Data Sinks
# ============================================

def console_sink(data_stream):
    """Output data to console."""
    for item in data_stream:
        print(json.dumps(item, indent=2))
        yield item

def file_sink(filename: str):
    """Write data to a file."""
    def sink(data_stream):
        with open(filename, 'w') as f:
            for item in data_stream:
                if isinstance(item, list):  # Batched data
                    for record in item:
                        f.write(json.dumps(record) + '\n')
                else:
                    f.write(json.dumps(item) + '\n')
                yield item
    return sink

def statistics_sink(data_stream):
    """Collect statistics from data stream."""
    stats = {
        "total_records": 0,
        "processing_start": datetime.now(),
        "errors": 0,
        "fields": set()
    }
    
    for item in data_stream:
        stats["total_records"] += 1
        if isinstance(item, dict) and "error" in item:
            stats["errors"] += 1
        elif isinstance(item, dict):
            stats["fields"].update(item.keys())
        yield item
    
    stats["processing_end"] = datetime.now()
    stats["processing_time"] = (stats["processing_end"] - stats["processing_start"]).total_seconds()
    stats["fields"] = list(stats["fields"])
    
    print("\n📊 Processing Statistics:")
    print(f"  Total Records: {stats['total_records']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Processing Time: {stats['processing_time']:.2f} seconds")
    print(f"  Fields Found: {', '.join(stats['fields'])}")


# ============================================
# Sample Data Generators
# ============================================

def generate_sample_json_data(filename: str, count: int = 100):
    """Generate sample JSON data."""
    import random
    
    cities = ["New York", "London", "Paris", "Tokyo", "Sydney", "Berlin", "Rome", "Madrid"]
    departments = ["Engineering", "Marketing", "Sales", "HR", "Finance", "Operations"]
    
    with open(filename, 'w') as f:
        for i in range(count):
            record = {
                "id": i + 1,
                "name": f"Employee {i + 1}",
                "age": random.randint(22, 65),
                "city": random.choice(cities),
                "department": random.choice(departments),
                "salary": random.randint(40000, 120000),
                "experience": random.randint(0, 40)
            }
            f.write(json.dumps(record) + '\n')
    
    print(f"✅ Generated {count} sample records in {filename}")

def generate_sample_csv_data(filename: str, count: int = 100):
    """Generate sample CSV data."""
    import random
    
    cities = ["New York", "London", "Paris", "Tokyo", "Sydney", "Berlin", "Rome", "Madrid"]
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        # Header
        writer.writerow(["id", "name", "age", "city", "score"])
        
        # Data
        for i in range(count):
            writer.writerow([
                i + 1,
                f"User {i + 1}",
                random.randint(18, 80),
                random.choice(cities),
                random.randint(0, 100)
            ])
    
    print(f"✅ Generated {count} sample records in {filename}")


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
    print("1.  Generate Sample Data")
    print("2.  Process JSON Data")
    print("3.  Process CSV Data")
    print("4.  Real-time API Simulation")
    print("5.  Complex Pipeline Example")
    print("6.  Batch Processing")
    print("7.  Filter and Transform")
    print("8.  View Pipeline Statistics")
    print("9.  Exit")


def generate_sample_data_interactive():
    """Generate sample data files."""
    print_header("📊 GENERATE SAMPLE DATA")
    
    print("Choose data type:")
    print("1. JSON Lines (.jsonl)")
    print("2. CSV (.csv)")
    
    choice = input("Select type (1-2): ").strip()
    filename = input("Filename (default: sample.jsonl): ").strip()
    
    if not filename:
        filename = "sample.jsonl" if choice == "1" else "sample.csv"
    
    count = input("Number of records (default 50): ").strip()
    try:
        record_count = int(count) if count else 50
    except ValueError:
        record_count = 50
    
    if choice == "1":
        generate_sample_json_data(filename, record_count)
    elif choice == "2":
        generate_sample_csv_data(filename, record_count)
    else:
        print("❌ Invalid choice!")


def process_json_data_interactive():
    """Process JSON data."""
    print_header("📄 PROCESS JSON DATA")
    
    filename = input("JSON filename (default: sample.jsonl): ").strip()
    if not filename:
        filename = "sample.jsonl"
    
    # Create pipeline
    pipeline = DataPipeline()
    
    # Add processors
    pipeline.add_processor(filter_records(lambda r: r.get("age", 0) >= 25))
    pipeline.add_processor(transform_records(lambda r: {**r, "age_group": "senior" if r.get("age", 0) >= 35 else "junior"}))
    pipeline.add_processor(add_timestamp)
    pipeline.add_processor(limit_records(10))
    pipeline.add_processor(console_sink)
    pipeline.add_processor(statistics_sink)
    
    # Process data
    print("Processing JSON data...")
    list(pipeline.process(file_reader(filename)))


def process_csv_data_interactive():
    """Process CSV data."""
    print_header("📊 PROCESS CSV DATA")
    
    filename = input("CSV filename (default: sample.csv): ").strip()
    if not filename:
        filename = "sample.csv"
    
    # Create pipeline
    pipeline = DataPipeline()
    
    # Add processors
    pipeline.add_processor(filter_records(lambda r: int(r.get("age", 0)) >= 30))
    pipeline.add_processor(transform_records(lambda r: {**r, "category": "high" if int(r.get("score", 0)) >= 70 else "low"}))
    pipeline.add_processor(add_timestamp)
    pipeline.add_processor(console_sink)
    pipeline.add_processor(statistics_sink)
    
    # Process data
    print("Processing CSV data...")
    list(pipeline.process(csv_reader(filename)))


def real_time_api_simulation_interactive():
    """Simulate real-time API data processing."""
    print_header("🌐 REAL-TIME API SIMULATION")
    
    print("Simulating real-time data stream...")
    print("(Press Ctrl+C to stop)")
    
    try:
        # Create pipeline
        pipeline = DataPipeline()
        pipeline.add_processor(filter_records(lambda r: r.get("age", 0) >= 30))
        pipeline.add_processor(transform_records(lambda r: {**r, "experience_level": "senior" if r.get("age", 0) >= 40 else "mid"}))
        pipeline.add_processor(console_sink)
        
        # Process data with delay simulation
        count = 0
        for item in pipeline.process(api_data_source("https://api.example.com/data")):
            count += 1
            if count >= 5:  # Limit for demo
                break
            time.sleep(1)  # Simulate real-time processing
            
    except KeyboardInterrupt:
        print("\n⏹️  Stopped by user")


def complex_pipeline_example_interactive():
    """Run a complex pipeline example."""
    print_header("🔧 COMPLEX PIPELINE EXAMPLE")
    
    # Generate sample data
    generate_sample_json_data("complex_sample.jsonl", 200)
    
    # Create complex pipeline
    pipeline = DataPipeline()
    
    # Filter: Only employees with salary > 60000
    pipeline.add_processor(filter_records(lambda r: r.get("salary", 0) > 60000))
    
    # Transform: Add calculated fields
    def add_calculations(record):
        record["salary_category"] = "high" if record.get("salary", 0) > 80000 else "medium"
        record["experience_ratio"] = record.get("experience", 0) / max(record.get("age", 1), 1)
        return record
    
    pipeline.add_processor(transform_records(add_calculations))
    
    # Filter: Only senior employees
    pipeline.add_processor(filter_records(lambda r: r.get("age", 0) >= 35))
    
    # Transform: Format for output
    def format_output(record):
        return {
            "employee_id": record["id"],
            "name": record["name"],
            "compensation": f"${record['salary']:,}",
            "category": record["salary_category"],
            "experience_ratio": round(record["experience_ratio"], 2)
        }
    
    pipeline.add_processor(transform_records(format_output))
    
    # Limit results
    pipeline.add_processor(limit_records(15))
    
    # Output to file
    pipeline.add_processor(file_sink("processed_employees.jsonl"))
    
    # Show statistics
    pipeline.add_processor(statistics_sink)
    
    # Process data
    print("Running complex data pipeline...")
    list(pipeline.process(file_reader("complex_sample.jsonl")))
    print("✅ Results saved to processed_employees.jsonl")


def batch_processing_interactive():
    """Demonstrate batch processing."""
    print_header("📦 BATCH PROCESSING")
    
    # Generate sample data
    generate_sample_json_data("batch_sample.jsonl", 150)
    
    # Create batch processing pipeline
    pipeline = DataPipeline()
    pipeline.add_processor(batch_records(25))  # Process in batches of 25
    pipeline.add_processor(console_sink)
    pipeline.add_processor(statistics_sink)
    
    print("Processing data in batches...")
    batch_count = 0
    for batch in pipeline.process(file_reader("batch_sample.jsonl")):
        batch_count += 1
        print(f"\n📦 Batch {batch_count} ({len(batch)} records):")
        for i, record in enumerate(batch[:3]):  # Show first 3 of each batch
            print(f"  {i+1}. {record['name']} - {record['city']}")
        if len(batch) > 3:
            print(f"  ... and {len(batch) - 3} more")
    
    print(f"\n✅ Processed {batch_count} batches")


def filter_transform_interactive():
    """Demonstrate filtering and transformation."""
    print_header("🔍 FILTER & TRANSFORM")
    
    # Generate sample data
    generate_sample_csv_data("filter_sample.csv", 75)
    
    # Create filtering pipeline
    pipeline = DataPipeline()
    
    print("Available filters:")
    print("1. Age >= 30")
    print("2. Score >= 75")
    print("3. Both filters")
    
    choice = input("Select filter (1-3): ").strip()
    
    if choice == "1":
        pipeline.add_processor(filter_records(lambda r: int(r.get("age", 0)) >= 30))
    elif choice == "2":
        pipeline.add_processor(filter_records(lambda r: int(r.get("score", 0)) >= 75))
    elif choice == "3":
        pipeline.add_processor(filter_records(lambda r: int(r.get("age", 0)) >= 30 and int(r.get("score", 0)) >= 75))
    
    # Add transformation
    def categorize_score(record):
        score = int(record.get("score", 0))
        if score >= 90:
            record["grade"] = "A"
        elif score >= 80:
            record["grade"] = "B"
        elif score >= 70:
            record["grade"] = "C"
        else:
            record["grade"] = "D"
        return record
    
    pipeline.add_processor(transform_records(categorize_score))
    pipeline.add_processor(add_timestamp)
    pipeline.add_processor(console_sink)
    pipeline.add_processor(statistics_sink)
    
    print("Processing filtered data...")
    list(pipeline.process(csv_reader("filter_sample.csv")))


def view_pipeline_statistics_interactive():
    """View pipeline statistics."""
    print_header("📈 PIPELINE STATISTICS")
    
    print("""
Data Pipeline Features:

📊 Memory Efficiency:
  • Generators process data on-demand
  • No need to load entire datasets into memory
  • Perfect for large files and real-time streams

🔧 Flexibility:
  • Chain multiple processors together
  • Easy to add/remove processing steps
  • Reusable processor functions

⚡ Performance:
  • Lazy evaluation - only process what's needed
  • Early termination with limit processors
  • Streaming architecture for real-time data

🔄 Supported Data Sources:
  • JSON Lines files
  • CSV files
  • API endpoints (simulated)
  • Database queries (can be added)

📤 Supported Data Sinks:
  • Console output
  • File output
  • Database writes (can be added)
  • Analytics collectors (can be added)
    """)


# ============================================
# Main Application
# ============================================

def main():
    """Main application loop."""
    
    print("=" * 70)
    print("📊  DATA PIPELINE  📊".center(70))
    print("=" * 70)
    print("Streaming data processing pipeline using generators!")
    
    while True:
        print_menu()
        choice = input("\nYour choice: ").strip()
        
        if choice == '1':
            generate_sample_data_interactive()
        elif choice == '2':
            process_json_data_interactive()
        elif choice == '3':
            process_csv_data_interactive()
        elif choice == '4':
            real_time_api_simulation_interactive()
        elif choice == '5':
            complex_pipeline_example_interactive()
        elif choice == '6':
            batch_processing_interactive()
        elif choice == '7':
            filter_transform_interactive()
        elif choice == '8':
            view_pipeline_statistics_interactive()
        elif choice == '9':
            print("\n👋 Thank you for using the Data Pipeline!")
            print("=" * 70 + "\n")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
