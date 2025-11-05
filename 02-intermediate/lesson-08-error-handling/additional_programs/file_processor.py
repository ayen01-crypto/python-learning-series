#!/usr/bin/env python3
"""
File Processor with Error Handling
A program that processes files with comprehensive error handling.
"""

import os
import json
import csv
from typing import List, Dict, Any


class FileProcessorError(Exception):
    """Custom exception for file processing errors."""
    pass


class FileProcessor:
    """A robust file processor with comprehensive error handling."""
    
    def __init__(self):
        """Initialize file processor."""
        self.processed_files = []
        self.errors = []
    
    def read_text_file(self, filepath: str) -> str:
        """
        Read a text file with error handling.
        
        Args:
            filepath (str): Path to the file
            
        Returns:
            str: File contents
            
        Raises:
            FileProcessorError: If file cannot be read
        """
        try:
            if not os.path.exists(filepath):
                raise FileProcessorError(f"File not found: {filepath}")
            
            if not os.path.isfile(filepath):
                raise FileProcessorError(f"Not a file: {filepath}")
            
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            self.processed_files.append(filepath)
            print(f"✅ Successfully read text file: {filepath}")
            return content
            
        except PermissionError:
            error_msg = f"Permission denied reading file: {filepath}"
            self.errors.append(error_msg)
            raise FileProcessorError(error_msg)
        except UnicodeDecodeError:
            error_msg = f"Cannot decode file (not UTF-8): {filepath}"
            self.errors.append(error_msg)
            raise FileProcessorError(error_msg)
        except Exception as e:
            error_msg = f"Error reading file '{filepath}': {str(e)}"
            self.errors.append(error_msg)
            raise FileProcessorError(error_msg)
    
    def write_text_file(self, filepath: str, content: str) -> None:
        """
        Write content to a text file with error handling.
        
        Args:
            filepath (str): Path to the file
            content (str): Content to write
            
        Raises:
            FileProcessorError: If file cannot be written
        """
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            
            self.processed_files.append(filepath)
            print(f"✅ Successfully wrote text file: {filepath}")
            
        except PermissionError:
            error_msg = f"Permission denied writing file: {filepath}"
            self.errors.append(error_msg)
            raise FileProcessorError(error_msg)
        except OSError as e:
            error_msg = f"OS error writing file '{filepath}': {str(e)}"
            self.errors.append(error_msg)
            raise FileProcessorError(error_msg)
        except Exception as e:
            error_msg = f"Error writing file '{filepath}': {str(e)}"
            self.errors.append(error_msg)
            raise FileProcessorError(error_msg)
    
    def read_json_file(self, filepath: str) -> Dict[Any, Any]:
        """
        Read and parse a JSON file with error handling.
        
        Args:
            filepath (str): Path to the JSON file
            
        Returns:
            dict: Parsed JSON data
            
        Raises:
            FileProcessorError: If JSON file cannot be read or parsed
        """
        try:
            content = self.read_text_file(filepath)
            data = json.loads(content)
            print(f"✅ Successfully parsed JSON file: {filepath}")
            return data
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in file '{filepath}': {str(e)}"
            self.errors.append(error_msg)
            raise FileProcessorError(error_msg)
        except Exception as e:
            error_msg = f"Error processing JSON file '{filepath}': {str(e)}"
            self.errors.append(error_msg)
            raise FileProcessorError(error_msg)
    
    def read_csv_file(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Read and parse a CSV file with error handling.
        
        Args:
            filepath (str): Path to the CSV file
            
        Returns:
            list: List of dictionaries representing CSV rows
            
        Raises:
            FileProcessorError: If CSV file cannot be read or parsed
        """
        try:
            if not os.path.exists(filepath):
                raise FileProcessorError(f"File not found: {filepath}")
            
            data = []
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row_num, row in enumerate(reader, 1):
                    # Handle potential issues with CSV data
                    cleaned_row = {k.strip(): v.strip() if v else '' for k, v in row.items()}
                    data.append(cleaned_row)
            
            self.processed_files.append(filepath)
            print(f"✅ Successfully read CSV file: {filepath} ({len(data)} rows)")
            return data
            
        except FileNotFoundError:
            error_msg = f"CSV file not found: {filepath}"
            self.errors.append(error_msg)
            raise FileProcessorError(error_msg)
        except PermissionError:
            error_msg = f"Permission denied reading CSV file: {filepath}"
            self.errors.append(error_msg)
            raise FileProcessorError(error_msg)
        except csv.Error as e:
            error_msg = f"CSV parsing error in '{filepath}' at line {reader.line_num if 'reader' in locals() else 'unknown'}: {str(e)}"
            self.errors.append(error_msg)
            raise FileProcessorError(error_msg)
        except Exception as e:
            error_msg = f"Error reading CSV file '{filepath}': {str(e)}"
            self.errors.append(error_msg)
            raise FileProcessorError(error_msg)
    
    def process_large_file(self, filepath: str, chunk_size: int = 1024) -> int:
        """
        Process a large file in chunks with error handling.
        
        Args:
            filepath (str): Path to the file
            chunk_size (int): Size of chunks to read
            
        Returns:
            int: Number of characters processed
            
        Raises:
            FileProcessorError: If file cannot be processed
        """
        try:
            if not os.path.exists(filepath):
                raise FileProcessorError(f"File not found: {filepath}")
            
            char_count = 0
            with open(filepath, 'r', encoding='utf-8') as file:
                while True:
                    chunk = file.read(chunk_size)
                    if not chunk:
                        break
                    char_count += len(chunk)
                    # Simulate processing
                    # In a real application, you might process the chunk here
            
            self.processed_files.append(filepath)
            print(f"✅ Successfully processed large file: {filepath} ({char_count} characters)")
            return char_count
            
        except FileNotFoundError:
            error_msg = f"Large file not found: {filepath}"
            self.errors.append(error_msg)
            raise FileProcessorError(error_msg)
        except PermissionError:
            error_msg = f"Permission denied processing file: {filepath}"
            self.errors.append(error_msg)
            raise FileProcessorError(error_msg)
        except UnicodeDecodeError:
            error_msg = f"Cannot decode large file (not UTF-8): {filepath}"
            self.errors.append(error_msg)
            raise FileProcessorError(error_msg)
        except MemoryError:
            error_msg = f"Insufficient memory to process large file: {filepath}"
            self.errors.append(error_msg)
            raise FileProcessorError(error_msg)
        except Exception as e:
            error_msg = f"Error processing large file '{filepath}': {str(e)}"
            self.errors.append(error_msg)
            raise FileProcessorError(error_msg)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            "files_processed": len(self.processed_files),
            "errors_occurred": len(self.errors),
            "processed_files": self.processed_files.copy(),
            "error_log": self.errors.copy()
        }
    
    def clear_statistics(self):
        """Clear processing statistics."""
        self.processed_files.clear()
        self.errors.clear()
        print("Statistics cleared.")


def create_sample_files():
    """Create sample files for testing."""
    # Create sample text file
    with open("sample.txt", "w") as f:
        f.write("This is a sample text file.\n")
        f.write("It contains multiple lines.\n")
        f.write("Used for testing file processing.\n")
    
    # Create sample JSON file
    sample_data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York",
        "hobbies": ["reading", "swimming", "coding"]
    }
    with open("sample.json", "w") as f:
        json.dump(sample_data, f, indent=2)
    
    # Create sample CSV file
    csv_data = [
        ["name", "age", "city"],
        ["Alice", "25", "Boston"],
        ["Bob", "35", "Chicago"],
        ["Charlie", "45", "Denver"]
    ]
    with open("sample.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
    
    # Create a large file
    with open("large_sample.txt", "w") as f:
        for i in range(1000):
            f.write(f"This is line number {i+1} in our large sample file.\n")
    
    print("Sample files created for testing.")


def main():
    """Main file processor program."""
    processor = FileProcessor()
    
    print("📁 File Processor with Error Handling")
    print("This program demonstrates comprehensive file error handling in Python.")
    
    # Create sample files if they don't exist
    required_files = ["sample.txt", "sample.json", "sample.csv", "large_sample.txt"]
    if not all(os.path.exists(f) for f in required_files):
        create_sample_files()
    
    while True:
        print("\n" + "=" * 40)
        print("📁 FILE PROCESSOR MENU")
        print("=" * 40)
        print("1. Read Text File")
        print("2. Write Text File")
        print("3. Read JSON File")
        print("4. Read CSV File")
        print("5. Process Large File")
        print("6. Show Statistics")
        print("7. Clear Statistics")
        print("8. Create Sample Files")
        print("9. Exit")
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        try:
            if choice == '1':
                filepath = input("Enter text file path: ").strip()
                if filepath:
                    content = processor.read_text_file(filepath)
                    print(f"\n📄 File Contents:\n{content[:200]}{'...' if len(content) > 200 else ''}")
                else:
                    print("❌ File path cannot be empty.")
            
            elif choice == '2':
                filepath = input("Enter output file path: ").strip()
                content = input("Enter content to write: ")
                if filepath:
                    processor.write_text_file(filepath, content)
                    print("✅ File written successfully.")
                else:
                    print("❌ File path cannot be empty.")
            
            elif choice == '3':
                filepath = input("Enter JSON file path: ").strip()
                if filepath:
                    data = processor.read_json_file(filepath)
                    print(f"\n📄 JSON Data:\n{json.dumps(data, indent=2)[:200]}{'...' if len(json.dumps(data, indent=2)) > 200 else ''}")
                else:
                    print("❌ File path cannot be empty.")
            
            elif choice == '4':
                filepath = input("Enter CSV file path: ").strip()
                if filepath:
                    data = processor.read_csv_file(filepath)
                    print(f"\n📄 CSV Data (first 3 rows):")
                    for i, row in enumerate(data[:3]):
                        print(f"  Row {i+1}: {row}")
                else:
                    print("❌ File path cannot be empty.")
            
            elif choice == '5':
                filepath = input("Enter large file path: ").strip()
                chunk_size = input("Enter chunk size (default 1024): ").strip()
                chunk_size = int(chunk_size) if chunk_size.isdigit() else 1024
                
                if filepath:
                    char_count = processor.process_large_file(filepath, chunk_size)
                    print(f"✅ Processed {char_count} characters.")
                else:
                    print("❌ File path cannot be empty.")
            
            elif choice == '6':
                stats = processor.get_statistics()
                print(f"\n📊 Processing Statistics:")
                print(f"  Files Processed: {stats['files_processed']}")
                print(f"  Errors Occurred: {stats['errors_occurred']}")
                if stats['processed_files']:
                    print("  Processed Files:")
                    for file in stats['processed_files']:
                        print(f"    - {file}")
                if stats['error_log']:
                    print("  Recent Errors:")
                    for error in stats['error_log'][-3:]:  # Show last 3 errors
                        print(f"    - {error}")
            
            elif choice == '7':
                processor.clear_statistics()
            
            elif choice == '8':
                create_sample_files()
            
            elif choice == '9':
                print("Thank you for using File Processor!")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1-9.")
        
        except FileProcessorError as e:
            print(f"❌ File Processing Error: {e}")
        except ValueError as e:
            print(f"❌ Value Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")


if __name__ == "__main__":
    main()