"""
Tests for Data Ingestion Module
"""

import unittest
import pandas as pd
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_ingestion import DataIngestionManager, CSVDataSource


class TestDataIngestion(unittest.TestCase):
    """Test data ingestion components."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_data = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35]
        })
        
        # Create sample CSV file for testing
        self.test_csv_path = 'test_data.csv'
        self.sample_data.to_csv(self.test_csv_path, index=False)

    def tearDown(self):
        """Tear down test fixtures."""
        if os.path.exists(self.test_csv_path):
            os.remove(self.test_csv_path)

    def test_csv_data_source(self):
        """Test CSV data source."""
        config = {"path": self.test_csv_path}
        source = CSVDataSource("test_csv", config)
        
        df = source.load_data()
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)
        self.assertEqual(list(df.columns), ['id', 'name', 'age'])

    def test_data_ingestion_manager(self):
        """Test data ingestion manager."""
        manager = DataIngestionManager()
        
        # Add source
        config = {"path": self.test_csv_path}
        manager.add_source("test_data", "csv", config)
        
        # Load data
        df = manager.load_data("test_data")
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)

    def test_combine_data(self):
        """Test combining data from multiple sources."""
        manager = DataIngestionManager()
        
        # Add source
        config = {"path": self.test_csv_path}
        manager.add_source("test_data", "csv", config)
        
        # Combine data
        combined_df = manager.combine_data(["test_data"])
        
        self.assertIsInstance(combined_df, pd.DataFrame)
        self.assertEqual(len(combined_df), 3)
        self.assertIn('source', combined_df.columns)


if __name__ == '__main__':
    unittest.main()