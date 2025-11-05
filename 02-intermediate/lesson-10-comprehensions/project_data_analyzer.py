"""
Mini Project: Data Analyzer

A powerful data analysis tool using comprehensions for efficient data processing.
"""

from typing import Dict, List, Any, Union
import json
import csv
from datetime import datetime


# ============================================
# Data Models
# ============================================

class DataRecord:
    """Represents a single data record."""
    
    def __init__(self, **kwargs):
        self.data = kwargs
        self.timestamp = datetime.now()
    
    def __getitem__(self, key):
        return self.data.get(key)
    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def keys(self):
        return self.data.keys()
    
    def values(self):
        return self.data.values()
    
    def items(self):
        return self.data.items()
    
    def to_dict(self):
        return self.data.copy()


class DataSet:
    """Represents a collection of data records."""
    
    def __init__(self, name: str = "Untitled"):
        self.name = name
        self.records: List[DataRecord] = []
        self.created_date = datetime.now()
    
    def add_record(self, record: DataRecord):
        """Add a record to the dataset."""
        self.records.append(record)
    
    def add_records(self, records: List[DataRecord]):
        """Add multiple records to the dataset."""
        self.records.extend(records)
    
    def __len__(self):
        return len(self.records)
    
    def __iter__(self):
        return iter(self.records)
    
    def __getitem__(self, index):
        return self.records[index]


# ============================================
# Data Analyzer
# ============================================

class DataAnalyzer:
    """Powerful data analysis tool using comprehensions."""
    
    def __init__(self):
        self.datasets: Dict[str, DataSet] = {}
    
    def create_dataset(self, name: str) -> DataSet:
        """Create a new dataset."""
        if name in self.datasets:
            raise ValueError(f"Dataset {name} already exists")
        
        dataset = DataSet(name)
        self.datasets[name] = dataset
        return dataset
    
    def get_dataset(self, name: str) -> DataSet:
        """Get dataset by name."""
        return self.datasets.get(name)
    
    def list_datasets(self) -> List[str]:
        """List all dataset names."""
        return list(self.datasets.keys())
    
    # ============================================
    # Statistical Analysis
    # ============================================
    
    def calculate_statistics(self, dataset_name: str, column: str) -> Dict[str, float]:
        """Calculate basic statistics for a numeric column."""
        dataset = self.get_dataset(dataset_name)
        if not dataset:
            raise ValueError(f"Dataset {dataset_name} not found")
        
        # Extract numeric values
        values = [float(record[column]) for record in dataset 
                 if record[column] is not None and str(record[column]).replace('.', '').isdigit()]
        
        if not values:
            return {"count": 0}
        
        return {
            "count": len(values),
            "sum": sum(values),
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "range": max(values) - min(values)
        }
    
    def find_extremes(self, dataset_name: str, column: str, 
                     count: int = 5) -> Dict[str, List[Dict]]:
        """Find highest and lowest values in a column."""
        dataset = self.get_dataset(dataset_name)
        if not dataset:
            raise ValueError(f"Dataset {dataset_name} not found")
        
        # Create list of (value, record) pairs for sortable values
        sortable_data = [(float(record[column]), record.to_dict()) 
                        for record in dataset 
                        if record[column] is not None and str(record[column]).replace('.', '').isdigit()]
        
        if not sortable_data:
            return {"highest": [], "lowest": []}
        
        # Sort and get extremes
        sorted_data = sorted(sortable_data, key=lambda x: x[0])
        
        return {
            "highest": [record for _, record in sorted_data[-count:]],
            "lowest": [record for _, record in sorted_data[:count]]
        }
    
    # ============================================
    # Data Filtering and Transformation
    # ============================================
    
    def filter_records(self, dataset_name: str, **conditions) -> List[Dict]:
        """Filter records based on conditions."""
        dataset = self.get_dataset(dataset_name)
        if not dataset:
            raise ValueError(f"Dataset {dataset_name} not found")
        
        def matches_conditions(record):
            for key, value in conditions.items():
                if key not in record.data:
                    return False
                if record[key] != value:
                    return False
            return True
        
        return [record.to_dict() for record in dataset if matches_conditions(record)]
    
    def transform_data(self, dataset_name: str, transformations: Dict[str, callable]) -> List[Dict]:
        """Apply transformations to data."""
        dataset = self.get_dataset(dataset_name)
        if not dataset:
            raise ValueError(f"Dataset {dataset_name} not found")
        
        transformed_records = []
        for record in dataset:
            new_record = record.to_dict()
            for column, transform_func in transformations.items():
                if column in new_record:
                    try:
                        new_record[column] = transform_func(new_record[column])
                    except Exception:
                        pass  # Keep original value if transformation fails
            transformed_records.append(new_record)
        
        return transformed_records
    
    # ============================================
    # Grouping and Aggregation
    # ============================================
    
    def group_by(self, dataset_name: str, group_column: str, 
                agg_column: str = None, agg_func: str = "count") -> Dict[Any, Any]:
        """Group records by a column and apply aggregation."""
        dataset = self.get_dataset(dataset_name)
        if not dataset:
            raise ValueError(f"Dataset {dataset_name} not found")
        
        # Group records by the specified column
        groups = {}
        for record in dataset:
            key = record[group_column]
            if key not in groups:
                groups[key] = []
            groups[key].append(record)
        
        # Apply aggregation if specified
        if agg_column and agg_func:
            result = {}
            for key, records in groups.items():
                if agg_func == "count":
                    result[key] = len(records)
                elif agg_func == "sum":
                    result[key] = sum(float(r[agg_column]) for r in records 
                                    if r[agg_column] is not None and str(r[agg_column]).replace('.', '').isdigit())
                elif agg_func == "avg":
                    values = [float(r[agg_column]) for r in records 
                             if r[agg_column] is not None and str(r[agg_column]).replace('.', '').isdigit()]
                    result[key] = sum(values) / len(values) if values else 0
                elif agg_func == "min":
                    values = [float(r[agg_column]) for r in records 
                             if r[agg_column] is not None and str(r[agg_column]).replace('.', '').isdigit()]
                    result[key] = min(values) if values else None
                elif agg_func == "max":
                    values = [float(r[agg_column]) for r in records 
                             if r[agg_column] is not None and str(r[agg_column]).replace('.', '').isdigit()]
                    result[key] = max(values) if values else None
            return result
        
        return {key: len(records) for key, records in groups.items()}
    
    # ============================================
    # Text Analysis
    # ============================================
    
    def analyze_text_column(self, dataset_name: str, column: str) -> Dict[str, Any]:
        """Perform text analysis on a column."""
        dataset = self.get_dataset(dataset_name)
        if not dataset:
            raise ValueError(f"Dataset {dataset_name} not found")
        
        # Extract text values
        texts = [str(record[column]) for record in dataset if record[column] is not None]
        
        if not texts:
            return {"total_records": 0}
        
        # Word analysis using comprehensions
        all_words = [word.lower().strip('.,!?";') 
                    for text in texts 
                    for word in text.split() 
                    if word.strip('.,!?";')]
        
        # Word frequency
        word_freq = {word: all_words.count(word) 
                    for word in set(all_words) 
                    if len(word) > 2}  # Only words longer than 2 characters
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Text statistics
        total_chars = sum(len(text) for text in texts)
        total_words = len(all_words)
        
        return {
            "total_records": len(texts),
            "total_characters": total_chars,
            "total_words": total_words,
            "average_words_per_record": total_words / len(texts) if texts else 0,
            "unique_words": len(set(all_words)),
            "most_common_words": sorted_words[:10],
            "longest_text": max(texts, key=len) if texts else "",
            "shortest_text": min(texts, key=len) if texts else ""
        }
    
    # ============================================
    # Export and Import
    # ============================================
    
    def export_to_json(self, dataset_name: str, filename: str) -> bool:
        """Export dataset to JSON file."""
        dataset = self.get_dataset(dataset_name)
        if not dataset:
            raise ValueError(f"Dataset {dataset_name} not found")
        
        try:
            data = [record.to_dict() for record in dataset]
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"❌ Error exporting to JSON: {e}")
            return False
    
    def import_from_json(self, dataset_name: str, filename: str) -> bool:
        """Import dataset from JSON file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            dataset = self.create_dataset(dataset_name)
            for record_data in data:
                record = DataRecord(**record_data)
                dataset.add_record(record)
            
            return True
        except Exception as e:
            print(f"❌ Error importing from JSON: {e}")
            return False
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all datasets."""
        return {
            "total_datasets": len(self.datasets),
            "datasets": {name: len(dataset) for name, dataset in self.datasets.items()}
        }


# ============================================
# Sample Data Generators
# ============================================

def generate_sales_data(analyzer: DataAnalyzer, count: int = 100):
    """Generate sample sales data."""
    import random
    
    dataset = analyzer.create_dataset("sales_data")
    
    products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones"]
    regions = ["North", "South", "East", "West"]
    
    for i in range(count):
        record = DataRecord(
            id=i+1,
            product=random.choice(products),
            region=random.choice(regions),
            quantity=random.randint(1, 20),
            price=round(random.uniform(10, 1000), 2),
            customer=f"Customer {random.randint(1, 50)}",
            description=f"Sale of {random.choice(products).lower()}"
        )
        dataset.add_record(record)
    
    print(f"✅ Generated {count} sales records")


def generate_survey_data(analyzer: DataAnalyzer, count: int = 50):
    """Generate sample survey data."""
    import random
    
    dataset = analyzer.create_dataset("survey_data")
    
    responses = ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
    questions = [
        "Product quality meets expectations",
        "Customer service is responsive",
        "Delivery was on time",
        "Overall satisfaction"
    ]
    
    for i in range(count):
        record = DataRecord(
            respondent_id=i+1,
            age=random.randint(18, 70),
            gender=random.choice(["Male", "Female", "Other"]),
            location=random.choice(["Urban", "Suburban", "Rural"]),
            satisfaction_score=random.randint(1, 10),
            feedback=f"This is feedback from respondent {i+1}. " +
                    f"They chose {random.choice(responses).lower()} for all questions."
        )
        
        # Add question responses
        for question in questions:
            record[question.replace(" ", "_").lower()] = random.choice(responses)
        
        dataset.add_record(record)
    
    print(f"✅ Generated {count} survey records")


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
    print("1.  Create Dataset")
    print("2.  List Datasets")
    print("3.  Generate Sample Data")
    print("4.  Calculate Statistics")
    print("5.  Find Extremes")
    print("6.  Filter Records")
    print("7.  Group Data")
    print("8.  Analyze Text")
    print("9.  View Dataset Summary")
    print("10. Export Dataset")
    print("11. Import Dataset")
    print("12. Exit")


def create_dataset_interactive(analyzer: DataAnalyzer):
    """Interactive dataset creation."""
    print_header("➕ CREATE DATASET")
    
    name = input("Dataset name: ").strip()
    if not name:
        print("❌ Dataset name is required!")
        return
    
    try:
        dataset = analyzer.create_dataset(name)
        print(f"✅ Dataset '{name}' created successfully!")
    except ValueError as e:
        print(f"❌ {e}")


def list_datasets_interactive(analyzer: DataAnalyzer):
    """List all datasets."""
    print_header("📂 DATASETS")
    
    datasets = analyzer.list_datasets()
    
    if not datasets:
        print("❌ No datasets found!")
        return
    
    print(f"Found {len(datasets)} dataset(s):\n")
    for name in sorted(datasets):
        dataset = analyzer.get_dataset(name)
        print(f"  📊 {name} ({len(dataset)} records)")


def generate_sample_data_interactive(analyzer: DataAnalyzer):
    """Generate sample data."""
    print_header("📊 GENERATE SAMPLE DATA")
    
    print("Available sample data types:")
    print("1. Sales Data")
    print("2. Survey Data")
    
    choice = input("Select type (1-2): ").strip()
    count = input("Number of records (default 50): ").strip()
    
    try:
        record_count = int(count) if count else 50
    except ValueError:
        record_count = 50
    
    if choice == '1':
        generate_sales_data(analyzer, record_count)
    elif choice == '2':
        generate_survey_data(analyzer, record_count)
    else:
        print("❌ Invalid choice!")


def calculate_statistics_interactive(analyzer: DataAnalyzer):
    """Calculate statistics for a dataset."""
    print_header("📈 CALCULATE STATISTICS")
    
    datasets = analyzer.list_datasets()
    if not datasets:
        print("❌ No datasets available!")
        return
    
    print("Available datasets:")
    for i, name in enumerate(datasets, 1):
        print(f"  {i}. {name}")
    
    try:
        choice = int(input("Select dataset: ")) - 1
        if 0 <= choice < len(datasets):
            dataset_name = datasets[choice]
            dataset = analyzer.get_dataset(dataset_name)
            
            if len(dataset) == 0:
                print("❌ Dataset is empty!")
                return
            
            # Show available numeric columns
            numeric_columns = set()
            for record in dataset:
                for key, value in record.items():
                    if isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '').isdigit()):
                        numeric_columns.add(key)
            
            if not numeric_columns:
                print("❌ No numeric columns found!")
                return
            
            print(f"\nNumeric columns in {dataset_name}:")
            for i, column in enumerate(sorted(numeric_columns), 1):
                print(f"  {i}. {column}")
            
            column_choice = int(input("Select column: ")) - 1
            columns_list = sorted(list(numeric_columns))
            if 0 <= column_choice < len(columns_list):
                column_name = columns_list[column_choice]
                stats = analyzer.calculate_statistics(dataset_name, column_name)
                
                print(f"\n📊 Statistics for {column_name}:")
                for key, value in stats.items():
                    if isinstance(value, float):
                        print(f"  {key.capitalize()}: {value:.2f}")
                    else:
                        print(f"  {key.capitalize()}: {value}")
            else:
                print("❌ Invalid column selection!")
        else:
            print("❌ Invalid dataset selection!")
    except ValueError:
        print("❌ Invalid input!")


def find_extremes_interactive(analyzer: DataAnalyzer):
    """Find extreme values in a dataset."""
    print_header("🔍 FIND EXTREMES")
    
    datasets = analyzer.list_datasets()
    if not datasets:
        print("❌ No datasets available!")
        return
    
    print("Available datasets:")
    for i, name in enumerate(datasets, 1):
        print(f"  {i}. {name}")
    
    try:
        choice = int(input("Select dataset: ")) - 1
        if 0 <= choice < len(datasets):
            dataset_name = datasets[choice]
            dataset = analyzer.get_dataset(dataset_name)
            
            if len(dataset) == 0:
                print("❌ Dataset is empty!")
                return
            
            # Show available numeric columns
            numeric_columns = set()
            for record in dataset:
                for key, value in record.items():
                    if isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '').isdigit()):
                        numeric_columns.add(key)
            
            if not numeric_columns:
                print("❌ No numeric columns found!")
                return
            
            print(f"\nNumeric columns in {dataset_name}:")
            for i, column in enumerate(sorted(numeric_columns), 1):
                print(f"  {i}. {column}")
            
            column_choice = int(input("Select column: ")) - 1
            columns_list = sorted(list(numeric_columns))
            if 0 <= column_choice < len(columns_list):
                column_name = columns_list[column_choice]
                extremes = analyzer.find_extremes(dataset_name, column_name)
                
                print(f"\n🏆 Highest values for {column_name}:")
                for record in extremes["highest"]:
                    print(f"  {record}")
                
                print(f"\n🔻 Lowest values for {column_name}:")
                for record in extremes["lowest"]:
                    print(f"  {record}")
            else:
                print("❌ Invalid column selection!")
        else:
            print("❌ Invalid dataset selection!")
    except ValueError:
        print("❌ Invalid input!")


def filter_records_interactive(analyzer: DataAnalyzer):
    """Filter records in a dataset."""
    print_header("🔍 FILTER RECORDS")
    
    datasets = analyzer.list_datasets()
    if not datasets:
        print("❌ No datasets available!")
        return
    
    print("Available datasets:")
    for i, name in enumerate(datasets, 1):
        print(f"  {i}. {name}")
    
    try:
        choice = int(input("Select dataset: ")) - 1
        if 0 <= choice < len(datasets):
            dataset_name = datasets[choice]
            dataset = analyzer.get_dataset(dataset_name)
            
            if len(dataset) == 0:
                print("❌ Dataset is empty!")
                return
            
            # Show available columns
            all_columns = set()
            for record in dataset:
                all_columns.update(record.keys())
            
            print(f"\nAvailable columns in {dataset_name}:")
            columns_list = sorted(list(all_columns))
            for i, column in enumerate(columns_list, 1):
                print(f"  {i}. {column}")
            
            column_choice = int(input("Select column to filter by: ")) - 1
            if 0 <= column_choice < len(columns_list):
                column_name = columns_list[column_choice]
                filter_value = input(f"Enter value for {column_name}: ").strip()
                
                # Try to convert to appropriate type
                filtered = analyzer.filter_records(dataset_name, **{column_name: filter_value})
                
                print(f"\n✅ Found {len(filtered)} matching records:")
                for i, record in enumerate(filtered[:10]):  # Show first 10
                    print(f"  {i+1}. {record}")
                if len(filtered) > 10:
                    print(f"  ... and {len(filtered) - 10} more records")
            else:
                print("❌ Invalid column selection!")
        else:
            print("❌ Invalid dataset selection!")
    except ValueError:
        print("❌ Invalid input!")


def group_data_interactive(analyzer: DataAnalyzer):
    """Group data in a dataset."""
    print_header("📊 GROUP DATA")
    
    datasets = analyzer.list_datasets()
    if not datasets:
        print("❌ No datasets available!")
        return
    
    print("Available datasets:")
    for i, name in enumerate(datasets, 1):
        print(f"  {i}. {name}")
    
    try:
        choice = int(input("Select dataset: ")) - 1
        if 0 <= choice < len(datasets):
            dataset_name = datasets[choice]
            dataset = analyzer.get_dataset(dataset_name)
            
            if len(dataset) == 0:
                print("❌ Dataset is empty!")
                return
            
            # Show available columns
            all_columns = set()
            for record in dataset:
                all_columns.update(record.keys())
            
            print(f"\nAvailable columns in {dataset_name}:")
            columns_list = sorted(list(all_columns))
            for i, column in enumerate(columns_list, 1):
                print(f"  {i}. {column}")
            
            group_choice = int(input("Select column to group by: ")) - 1
            if 0 <= group_choice < len(columns_list):
                group_column = columns_list[group_choice]
                
                # Ask for aggregation
                print("\nAggregation options:")
                print("1. Count")
                print("2. Sum")
                print("3. Average")
                print("4. Min")
                print("5. Max")
                
                agg_choice = input("Select aggregation (1-5, or Enter for count): ").strip()
                agg_options = {"1": "count", "2": "sum", "3": "avg", "4": "min", "5": "max"}
                agg_func = agg_options.get(agg_choice, "count")
                
                agg_column = None
                if agg_func != "count":
                    agg_choice = int(input("Select column to aggregate: ")) - 1
                    if 0 <= agg_choice < len(columns_list):
                        agg_column = columns_list[agg_choice]
                
                grouped = analyzer.group_by(dataset_name, group_column, agg_column, agg_func)
                
                print(f"\n📊 Grouped data by {group_column}:")
                for key, value in sorted(grouped.items()):
                    print(f"  {key}: {value}")
            else:
                print("❌ Invalid column selection!")
        else:
            print("❌ Invalid dataset selection!")
    except ValueError:
        print("❌ Invalid input!")


def analyze_text_interactive(analyzer: DataAnalyzer):
    """Analyze text in a dataset."""
    print_header("📝 ANALYZE TEXT")
    
    datasets = analyzer.list_datasets()
    if not datasets:
        print("❌ No datasets available!")
        return
    
    print("Available datasets:")
    for i, name in enumerate(datasets, 1):
        print(f"  {i}. {name}")
    
    try:
        choice = int(input("Select dataset: ")) - 1
        if 0 <= choice < len(datasets):
            dataset_name = datasets[choice]
            dataset = analyzer.get_dataset(dataset_name)
            
            if len(dataset) == 0:
                print("❌ Dataset is empty!")
                return
            
            # Show available text columns
            text_columns = set()
            for record in dataset:
                for key, value in record.items():
                    if isinstance(value, str) and len(value) > 10:
                        text_columns.add(key)
            
            if not text_columns:
                print("❌ No suitable text columns found!")
                return
            
            print(f"\nText columns in {dataset_name}:")
            columns_list = sorted(list(text_columns))
            for i, column in enumerate(columns_list, 1):
                print(f"  {i}. {column}")
            
            column_choice = int(input("Select column to analyze: ")) - 1
            if 0 <= column_choice < len(columns_list):
                column_name = columns_list[column_choice]
                analysis = analyzer.analyze_text_column(dataset_name, column_name)
                
                print(f"\n📝 Text Analysis for {column_name}:")
                print(f"  Total Records: {analysis['total_records']}")
                print(f"  Total Characters: {analysis['total_characters']}")
                print(f"  Total Words: {analysis['total_words']}")
                print(f"  Average Words/Record: {analysis['average_words_per_record']:.2f}")
                print(f"  Unique Words: {analysis['unique_words']}")
                print(f"  Longest Text: {analysis['longest_text'][:50]}...")
                print(f"  Shortest Text: {analysis['shortest_text'][:50]}...")
                
                print(f"\n🏆 Most Common Words:")
                for word, count in analysis['most_common_words'][:10]:
                    print(f"  {word}: {count}")
            else:
                print("❌ Invalid column selection!")
        else:
            print("❌ Invalid dataset selection!")
    except ValueError:
        print("❌ Invalid input!")


def view_summary_interactive(analyzer: DataAnalyzer):
    """View dataset summary."""
    print_header("📋 DATASET SUMMARY")
    
    summary = analyzer.get_summary()
    
    print(f"Total Datasets: {summary['total_datasets']}")
    print("\nDataset Details:")
    for name, count in summary['datasets'].items():
        print(f"  📊 {name}: {count} records")


def export_dataset_interactive(analyzer: DataAnalyzer):
    """Export dataset to file."""
    print_header("📤 EXPORT DATASET")
    
    datasets = analyzer.list_datasets()
    if not datasets:
        print("❌ No datasets available!")
        return
    
    print("Available datasets:")
    for i, name in enumerate(datasets, 1):
        print(f"  {i}. {name}")
    
    try:
        choice = int(input("Select dataset: ")) - 1
        if 0 <= choice < len(datasets):
            dataset_name = datasets[choice]
            filename = input("Output filename (default: dataset.json): ").strip()
            if not filename:
                filename = "dataset.json"
            
            if analyzer.export_to_json(dataset_name, filename):
                print(f"✅ Dataset exported to {filename}")
            else:
                print("❌ Export failed!")
        else:
            print("❌ Invalid dataset selection!")
    except ValueError:
        print("❌ Invalid input!")


def import_dataset_interactive(analyzer: DataAnalyzer):
    """Import dataset from file."""
    print_header("📥 IMPORT DATASET")
    
    name = input("Dataset name: ").strip()
    if not name:
        print("❌ Dataset name is required!")
        return
    
    filename = input("Input filename: ").strip()
    if not filename:
        print("❌ Filename is required!")
        return
    
    if analyzer.import_from_json(name, filename):
        dataset = analyzer.get_dataset(name)
        print(f"✅ Dataset imported successfully! ({len(dataset)} records)")
    else:
        print("❌ Import failed!")


# ============================================
# Main Application
# ============================================

def main():
    """Main application loop."""
    analyzer = DataAnalyzer()
    
    print("=" * 70)
    print("📊  DATA ANALYZER  📊".center(70))
    print("=" * 70)
    print("Powerful data analysis tool using comprehensions!")
    
    while True:
        print_menu()
        choice = input("\nYour choice: ").strip()
        
        if choice == '1':
            create_dataset_interactive(analyzer)
        elif choice == '2':
            list_datasets_interactive(analyzer)
        elif choice == '3':
            generate_sample_data_interactive(analyzer)
        elif choice == '4':
            calculate_statistics_interactive(analyzer)
        elif choice == '5':
            find_extremes_interactive(analyzer)
        elif choice == '6':
            filter_records_interactive(analyzer)
        elif choice == '7':
            group_data_interactive(analyzer)
        elif choice == '8':
            analyze_text_interactive(analyzer)
        elif choice == '9':
            view_summary_interactive(analyzer)
        elif choice == '10':
            export_dataset_interactive(analyzer)
        elif choice == '11':
            import_dataset_interactive(analyzer)
        elif choice == '12':
            print("\n👋 Thank you for using the Data Analyzer!")
            print("=" * 70 + "\n")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
