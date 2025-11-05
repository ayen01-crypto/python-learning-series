"""
Utility Functions
This module contains various utility functions for the data analysis and ML pipeline.
"""

import os
import json
import pickle
import logging
from typing import Dict, Any, List, Optional
import hashlib
import time
from functools import wraps


# Logging setup
def setup_logging(log_file: str = "pipeline.log", log_level: int = logging.INFO) -> logging.Logger:
    """Setup logging for the pipeline."""
    logger = logging.getLogger("ml_pipeline")
    logger.setLevel(log_level)
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Performance monitoring
def timing_decorator(func):
    """Decorator to time function execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper


# Data validation
def validate_dataframe(df, required_columns: List[str] = None) -> bool:
    """Validate dataframe structure."""
    if df is None:
        return False
    
    if required_columns:
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            print(f"Missing required columns: {missing_columns}")
            return False
    
    return True


def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """Validate JSON data against a schema."""
    for key, expected_type in schema.items():
        if key not in data:
            print(f"Missing required field: {key}")
            return False
        
        if not isinstance(data[key], expected_type):
            print(f"Field {key} has incorrect type. Expected {expected_type}, got {type(data[key])}")
            return False
    
    return True


# File operations
def safe_load_json(file_path: str) -> Optional[Dict[str, Any]]:
    """Safely load JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return None


def safe_save_json(data: Dict[str, Any], file_path: str) -> bool:
    """Safely save data to JSON file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        print(f"Error saving JSON file {file_path}: {e}")
        return False


def safe_load_pickle(file_path: str) -> Optional[Any]:
    """Safely load pickle file."""
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error loading pickle file {file_path}: {e}")
        return None


def safe_save_pickle(data: Any, file_path: str) -> bool:
    """Safely save data to pickle file."""
    try:
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
        return True
    except Exception as e:
        print(f"Error saving pickle file {file_path}: {e}")
        return False


# Data hashing
def hash_dataframe(df, method: str = "sha256") -> str:
    """Create hash of dataframe for versioning."""
    if method == "sha256":
        hash_obj = hashlib.sha256()
    else:
        raise ValueError(f"Unsupported hash method: {method}")
    
    # Convert dataframe to string and hash
    df_str = df.to_string().encode('utf-8')
    hash_obj.update(df_str)
    
    return hash_obj.hexdigest()


def hash_file(file_path: str, method: str = "sha256") -> str:
    """Create hash of file."""
    if method == "sha256":
        hash_obj = hashlib.sha256()
    else:
        raise ValueError(f"Unsupported hash method: {method}")
    
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        print(f"Error hashing file {file_path}: {e}")
        return ""


# Memory management
def get_memory_usage() -> Dict[str, int]:
    """Get current memory usage."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    return {
        "rss": memory_info.rss,  # Resident Set Size
        "vms": memory_info.vms,  # Virtual Memory Size
        "percent": process.memory_percent()
    }


def format_memory_size(bytes_size: int) -> str:
    """Format memory size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


# Configuration utilities
def merge_configs(default_config: Dict[str, Any], user_config: Dict[str, Any]) -> Dict[str, Any]:
    """Merge default and user configurations."""
    merged = default_config.copy()
    
    for key, value in user_config.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            # Recursively merge nested dictionaries
            merged[key] = merge_configs(merged[key], value)
        else:
            merged[key] = value
    
    return merged


def validate_config(config: Dict[str, Any], required_keys: List[str]) -> bool:
    """Validate configuration has required keys."""
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        print(f"Missing required configuration keys: {missing_keys}")
        return False
    return True


# Progress tracking
class ProgressTracker:
    """Track progress of long-running operations."""
    
    def __init__(self, total_steps: int):
        self.total_steps = total_steps
        self.current_step = 0
        self.start_time = time.time()
    
    def update(self, step_name: str = ""):
        """Update progress."""
        self.current_step += 1
        elapsed_time = time.time() - self.start_time
        progress_percent = (self.current_step / self.total_steps) * 100
        
        # Estimate remaining time
        if self.current_step > 0:
            time_per_step = elapsed_time / self.current_step
            remaining_steps = self.total_steps - self.current_step
            estimated_remaining = time_per_step * remaining_steps
        else:
            estimated_remaining = 0
        
        print(f"Progress: {progress_percent:.1f}% ({self.current_step}/{self.total_steps}) "
              f"- {step_name} - ETA: {estimated_remaining:.1f}s")


# Data sampling
def sample_dataframe(df, n: int = 1000, random_state: int = 42):
    """Sample dataframe for quick analysis."""
    if len(df) <= n:
        return df
    return df.sample(n=n, random_state=random_state)


# String utilities
def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    import re
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text


# Date utilities
def parse_date_string(date_str: str) -> Optional[str]:
    """Parse date string to standard format."""
    import dateutil.parser as parser
    
    try:
        parsed_date = parser.parse(date_str)
        return parsed_date.isoformat()
    except Exception:
        return None


# Convenience aliases
load_json = safe_load_json
save_json = safe_save_json
load_pickle = safe_load_pickle
save_pickle = safe_save_pickle