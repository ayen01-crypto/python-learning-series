"""
Tests for Data Processing Module
"""

import unittest
import pandas as pd
import numpy as np
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_processing import DataCleaner, DataTransformer, FeatureEngineer, DataProcessor


class TestDataCleaner(unittest.TestCase):
    """Test data cleaner components."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'value': [10, 20, np.nan, 40, 50],
            'category': ['A', 'B', 'A', 'B', 'A']
        })

    def test_remove_duplicates(self):
        """Test removing duplicates."""
        cleaner = DataCleaner()
        
        # Add duplicate row
        df_with_duplicates = self.sample_data.append(self.sample_data.iloc[0], ignore_index=True)
        
        # Remove duplicates
        df_cleaned = cleaner.remove_duplicates(df_with_duplicates)
        
        self.assertEqual(len(df_cleaned), 5)  # Should have 5 rows after removing duplicate

    def test_handle_missing_values(self):
        """Test handling missing values."""
        cleaner = DataCleaner()
        
        # Handle missing values with mean strategy
        df_cleaned = cleaner.handle_missing_values(self.sample_data, strategy="mean")
        
        self.assertFalse(df_cleaned.isnull().any().any())  # No missing values
        self.assertEqual(len(df_cleaned), 5)  # All rows preserved


class TestDataTransformer(unittest.TestCase):
    """Test data transformer components."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'value1': [10, 20, 30, 40, 50],
            'value2': [100, 200, 300, 400, 500],
            'category': ['A', 'B', 'A', 'B', 'A']
        })

    def test_scale_features(self):
        """Test scaling features."""
        transformer = DataTransformer()
        
        # Scale features
        df_scaled = transformer.scale_features(self.sample_data, ['value1', 'value2'], method="standard")
        
        # Check that scaled values have mean ~0 and std ~1
        self.assertAlmostEqual(df_scaled['value1'].mean(), 0, places=10)
        self.assertAlmostEqual(df_scaled['value1'].std(), 1, places=10)

    def test_encode_categorical(self):
        """Test encoding categorical variables."""
        transformer = DataTransformer()
        
        # Encode categorical variables
        df_encoded = transformer.encode_categorical(self.sample_data, ['category'])
        
        # Check that category column is now numeric
        self.assertTrue(np.issubdtype(df_encoded['category'].dtype, np.number))


class TestFeatureEngineer(unittest.TestCase):
    """Test feature engineering components."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'value1': [2, 3, 4, 5, 6],
            'value2': [1, 2, 3, 4, 5]
        })

    def test_create_polynomial_features(self):
        """Test creating polynomial features."""
        engineer = FeatureEngineer()
        
        # Create polynomial features
        df_poly = engineer.create_polynomial_features(self.sample_data, ['value1'], degree=2)
        
        # Check that squared column was created
        self.assertIn('value1^2', df_poly.columns)
        self.assertEqual(df_poly['value1^2'].iloc[0], 4)  # 2^2 = 4

    def test_create_interaction_features(self):
        """Test creating interaction features."""
        engineer = FeatureEngineer()
        
        # Create interaction features
        df_interact = engineer.create_interaction_features(self.sample_data, ['value1', 'value2'])
        
        # Check that interaction column was created
        self.assertIn('value1*value2', df_interact.columns)
        self.assertEqual(df_interact['value1*value2'].iloc[0], 2)  # 2 * 1 = 2


class TestDataProcessor(unittest.TestCase):
    """Test data processor components."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'value1': [10, 20, np.nan, 40, 50],
            'value2': [100, 200, 300, 400, 500],
            'category': ['A', 'B', 'A', 'B', 'A'],
            'target': [1, 2, 3, 4, 5]
        })
        
        self.config = {
            "cleaning": {
                "remove_duplicates": False,
                "missing_values": "mean"
            },
            "transformation": {
                "scaling": "standard",
                "encoding": "label"
            },
            "feature_engineering": {
                "polynomial": True,
                "polynomial_columns": ["value1"],
                "polynomial_degree": 2
            }
        }

    def test_process_data(self):
        """Test processing data with configuration."""
        processor = DataProcessor()
        
        # Process data
        df_processed = processor.process_data(self.sample_data, self.config)
        
        # Check that processing completed
        self.assertIsInstance(df_processed, pd.DataFrame)
        self.assertGreater(len(df_processed.columns), len(self.sample_data.columns))  # More columns after processing


if __name__ == '__main__':
    unittest.main()