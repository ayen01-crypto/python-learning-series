#!/usr/bin/env python3
"""
Log File Analyzer
A program that demonstrates reading and analyzing log files.
"""

import re
from collections import defaultdict
from datetime import datetime


def generate_sample_logs():
    """Generate sample log files for analysis."""
    sample_logs = [
        "2023-10-15 08:12:34 [INFO] User login successful for user123",
        "2023-10-15 08:15:22 [WARNING] High memory usage detected: 85%",
        "2023-10-15 08:20:45 [INFO] Database connection established",
        "2023-10-15 08:25:17 [ERROR] Failed to connect to external API",
        "2023-10-15 08:30:01 [INFO] User logout successful for user123",
        "2023-10-15 09:15:33 [ERROR] Database query timeout",
        "2023-10-15 09:22:45 [WARNING] Disk space low: 15% remaining",
        "2023-10-15 09:45:12 [INFO] Backup completed successfully",
        "2023-10-15 10:30:22 [ERROR] Authentication failed for user456",
        "2023-10-15 11:15:08 [INFO] System maintenance started",
        "2023-10-15 11:45:33 [WARNING] High CPU usage: 92%",
        "2023-10-15 12:00:15 [INFO] Maintenance completed successfully"
    ]
    
    with open("application.log", "w") as f:
        for log in sample_logs:
            f.write(log + "\n")
    
    print("Sample log file 'application.log' created.")


def parse_log_line(line):
    """
    Parse a log line and extract components.
    
    Args:
        line (str): A log line
        
    Returns:
        dict: Parsed components or None if invalid format
    """
    # Pattern to match: 2023-10-15 08:12:34 [INFO] User login successful
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.+)'
    match = re.match(pattern, line.strip())
    
    if match:
        return {
            'timestamp': match.group(1),
            'level': match.group(2),
            'message': match.group(3)
        }
    return None


def analyze_logs(filename):
    """
    Analyze log file and generate statistics.
    
    Args:
        filename (str): Path to log file
    """
    if not os.path.exists(filename):
        print(f"Error: Log file '{filename}' not found.")
        return
    
    # Statistics counters
    log_levels = defaultdict(int)
    error_messages = []
    warning_messages = []
    total_lines = 0
    
    try:
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                total_lines += 1
                parsed = parse_log_line(line)
                
                if parsed:
                    log_levels[parsed['level']] += 1
                    
                    if parsed['level'] == 'ERROR':
                        error_messages.append({
                            'line': line_num,
                            'timestamp': parsed['timestamp'],
                            'message': parsed['message']
                        })
                    elif parsed['level'] == 'WARNING':
                        warning_messages.append({
                            'line': line_num,
                            'timestamp': parsed['timestamp'],
                            'message': parsed['message']
                        })
                else:
                    print(f"Warning: Invalid log format on line {line_num}")
        
        # Display analysis results
        print(f"\n📊 LOG ANALYSIS RESULTS FOR '{filename}'")
        print("=" * 50)
        print(f"Total log entries: {total_lines}")
        print("\nLog Level Distribution:")
        for level, count in sorted(log_levels.items()):
            print(f"  {level}: {count}")
        
        if error_messages:
            print(f"\n❌ Errors ({len(error_messages)}):")
            for error in error_messages[:5]:  # Show first 5 errors
                print(f"  Line {error['line']}: [{error['timestamp']}] {error['message']}")
            if len(error_messages) > 5:
                print(f"  ... and {len(error_messages) - 5} more errors")
        
        if warning_messages:
            print(f"\n⚠️  Warnings ({len(warning_messages)}):")
            for warning in warning_messages[:5]:  # Show first 5 warnings
                print(f"  Line {warning['line']}: [{warning['timestamp']}] {warning['message']}")
            if len(warning_messages) > 5:
                print(f"  ... and {len(warning_messages) - 5} more warnings")
                
    except Exception as e:
        print(f"Error analyzing log file: {e}")


def search_logs(filename, search_term):
    """
    Search for specific terms in log file.
    
    Args:
        filename (str): Path to log file
        search_term (str): Term to search for
    """
    if not os.path.exists(filename):
        print(f"Error: Log file '{filename}' not found.")
        return
    
    matches = []
    try:
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                if search_term.lower() in line.lower():
                    matches.append({
                        'line': line_num,
                        'content': line.strip()
                    })
        
        if matches:
            print(f"\n🔍 Found {len(matches)} match(es) for '{search_term}':")
            print("-" * 40)
            for match in matches:
                print(f"Line {match['line']}: {match['content']}")
        else:
            print(f"No matches found for '{search_term}'")
            
    except Exception as e:
        print(f"Error searching log file: {e}")


def main():
    """Main program function."""
    import os
    
    print("🔍 Log File Analyzer")
    print("This program demonstrates file reading and text analysis.")
    
    # Generate sample logs if they don't exist
    if not os.path.exists("application.log"):
        generate_sample_logs()
    
    while True:
        print("\n" + "=" * 40)
        print("📋 LOG ANALYZER MENU")
        print("=" * 40)
        print("1. Analyze log file")
        print("2. Search in logs")
        print("3. Generate sample logs")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            filename = input("Enter log file name (default: application.log): ").strip()
            if not filename:
                filename = "application.log"
            analyze_logs(filename)
        
        elif choice == '2':
            filename = input("Enter log file name (default: application.log): ").strip()
            if not filename:
                filename = "application.log"
            search_term = input("Enter search term: ").strip()
            if search_term:
                search_logs(filename, search_term)
            else:
                print("Search term cannot be empty!")
        
        elif choice == '3':
            generate_sample_logs()
        
        elif choice == '4':
            print("Thank you for using Log File Analyzer!")
            break
        
        else:
            print("Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()