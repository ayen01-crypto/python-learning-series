"""
Data Ingestion Module
This module handles loading data from various sources.
"""

import os
import pandas as pd
import json
import sqlite3
from typing import Dict, Any, List
import requests
from abc import ABC, abstractmethod


class DataSource(ABC):
    """Abstract base class for data sources."""

    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config

    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """Load data from the source."""
        pass


class CSVDataSource(DataSource):
    """CSV data source."""

    def load_data(self) -> pd.DataFrame:
        """Load data from CSV file."""
        file_path = self.config.get("path")
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        
        return pd.read_csv(file_path)


class JSONDataSource(DataSource):
    """JSON data source."""

    def load_data(self) -> pd.DataFrame:
        """Load data from JSON file."""
        file_path = self.config.get("path")
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        return pd.DataFrame(data)


class SQLDataSource(DataSource):
    """SQL database data source."""

    def load_data(self) -> pd.DataFrame:
        """Load data from SQL database."""
        db_path = self.config.get("path")
        query = self.config.get("query")
        
        if not db_path or not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")
        
        if not query:
            raise ValueError("SQL query not provided")
        
        conn = sqlite3.connect(db_path)
        try:
            df = pd.read_sql_query(query, conn)
        finally:
            conn.close()
        
        return df


class APIDataSource(DataSource):
    """API data source."""

    def load_data(self) -> pd.DataFrame:
        """Load data from API."""
        url = self.config.get("url")
        if not url:
            raise ValueError("API URL not provided")
        
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        return pd.DataFrame(data)


class DataIngestionManager:
    """Manages data ingestion from multiple sources."""

    def __init__(self):
        self.data_sources: Dict[str, DataSource] = {}
        self._register_default_sources()

    def _register_default_sources(self):
        """Register default data source types."""
        self.source_types = {
            "csv": CSVDataSource,
            "json": JSONDataSource,
            "sql": SQLDataSource,
            "api": APIDataSource
        }

    def register_source(self, source_type: str, source_class: type):
        """Register a new data source type."""
        self.source_types[source_type] = source_class

    def add_source(self, name: str, source_type: str, config: Dict[str, Any]):
        """Add a data source."""
        if source_type not in self.source_types:
            raise ValueError(f"Unknown source type: {source_type}")
        
        source_class = self.source_types[source_type]
        self.data_sources[name] = source_class(name, config)

    def load_data(self, source_name: str) -> pd.DataFrame:
        """Load data from a specific source."""
        if source_name not in self.data_sources:
            raise ValueError(f"Unknown data source: {source_name}")
        
        return self.data_sources[source_name].load_data()

    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """Load data from all sources."""
        data = {}
        for name, source in self.data_sources.items():
            try:
                data[name] = source.load_data()
            except Exception as e:
                print(f"Warning: Failed to load data from {name}: {e}")
        return data

    def combine_data(self, sources: List[str] = None) -> pd.DataFrame:
        """Combine data from multiple sources."""
        if sources is None:
            sources = list(self.data_sources.keys())
        
        dfs = []
        for source_name in sources:
            if source_name in self.data_sources:
                df = self.load_data(source_name)
                df['source'] = source_name  # Add source identifier
                dfs.append(df)
        
        if not dfs:
            return pd.DataFrame()
        
        return pd.concat(dfs, ignore_index=True)


# Convenience functions
def create_data_ingestion_manager(config: Dict[str, Any]) -> DataIngestionManager:
    """Create a data ingestion manager from configuration."""
    manager = DataIngestionManager()
    
    # Add sources from configuration
    data_sources = config.get("data_sources", [])
    for source_config in data_sources:
        name = source_config.get("name")
        source_type = source_config.get("type")
        if name and source_type:
            manager.add_source(name, source_type, source_config)
    
    return manager