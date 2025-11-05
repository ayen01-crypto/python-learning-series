"""
Data Processing Module
This module handles data cleaning, transformation, and feature engineering.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from typing import Dict, Any, List, Tuple
import re


class DataCleaner:
    """Handles data cleaning operations."""

    def __init__(self):
        self.cleaning_operations = []

    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows."""
        initial_count = len(df)
        df = df.drop_duplicates()
        removed_count = initial_count - len(df)
        if removed_count > 0:
            print(f"Removed {removed_count} duplicate rows")
        return df

    def handle_missing_values(self, df: pd.DataFrame, strategy: str = "drop") -> pd.DataFrame:
        """Handle missing values."""
        missing_count = df.isnull().sum().sum()
        if missing_count == 0:
            return df
        
        print(f"Found {missing_count} missing values")
        
        if strategy == "drop":
            df = df.dropna()
        elif strategy == "mean":
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
        elif strategy == "median":
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
        elif strategy == "mode":
            for column in df.columns:
                df[column] = df[column].fillna(df[column].mode()[0] if not df[column].mode().empty else "Unknown")
        
        return df

    def remove_outliers(self, df: pd.DataFrame, columns: List[str] = None, method: str = "iqr") -> pd.DataFrame:
        """Remove outliers from specified columns."""
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        initial_count = len(df)
        
        for column in columns:
            if column not in df.columns:
                continue
                
            if method == "iqr":
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
            elif method == "zscore":
                z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
                df = df[z_scores < 3]
        
        removed_count = initial_count - len(df)
        if removed_count > 0:
            print(f"Removed {removed_count} outlier rows")
        
        return df


class DataTransformer:
    """Handles data transformation operations."""

    def __init__(self):
        self.scalers = {}
        self.encoders = {}

    def scale_features(self, df: pd.DataFrame, columns: List[str] = None, method: str = "standard") -> pd.DataFrame:
        """Scale numerical features."""
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if method == "standard":
            scaler = StandardScaler()
        elif method == "minmax":
            scaler = MinMaxScaler()
        else:
            raise ValueError(f"Unknown scaling method: {method}")
        
        df_scaled = df.copy()
        df_scaled[columns] = scaler.fit_transform(df[columns])
        
        # Store scaler for later use
        self.scalers[method] = scaler
        
        return df_scaled

    def encode_categorical(self, df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
        """Encode categorical variables."""
        if columns is None:
            columns = df.select_dtypes(include=['object']).columns.tolist()
        
        df_encoded = df.copy()
        
        for column in columns:
            if column not in df.columns:
                continue
            
            encoder = LabelEncoder()
            df_encoded[column] = encoder.fit_transform(df[column].astype(str))
            self.encoders[column] = encoder
        
        return df_encoded

    def create_dummy_variables(self, df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
        """Create dummy variables for categorical features."""
        if columns is None:
            columns = df.select_dtypes(include=['object']).columns.tolist()
        
        return pd.get_dummies(df, columns=columns, prefix=columns)


class FeatureEngineer:
    """Handles feature engineering operations."""

    def __init__(self):
        self.feature_operations = []

    def create_polynomial_features(self, df: pd.DataFrame, columns: List[str], degree: int = 2) -> pd.DataFrame:
        """Create polynomial features."""
        df_poly = df.copy()
        
        for column in columns:
            if column not in df.columns:
                continue
            
            for i in range(2, degree + 1):
                df_poly[f"{column}^{i}"] = df[column] ** i
        
        return df_poly

    def create_interaction_features(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Create interaction features."""
        df_interact = df.copy()
        
        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):
                col1, col2 = columns[i], columns[j]
                if col1 in df.columns and col2 in df.columns:
                    df_interact[f"{col1}*{col2}"] = df[col1] * df[col2]
        
        return df_interact

    def create_binned_features(self, df: pd.DataFrame, column: str, bins: int = 5) -> pd.DataFrame:
        """Create binned features."""
        if column not in df.columns:
            return df
        
        df_binned = df.copy()
        df_binned[f"{column}_binned"] = pd.cut(df[column], bins, labels=False)
        
        return df_binned

    def extract_datetime_features(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Extract features from datetime column."""
        if column not in df.columns:
            return df
        
        df_dt = df.copy()
        df_dt[column] = pd.to_datetime(df[column])
        
        df_dt[f"{column}_year"] = df_dt[column].dt.year
        df_dt[f"{column}_month"] = df_dt[column].dt.month
        df_dt[f"{column}_day"] = df_dt[column].dt.day
        df_dt[f"{column}_weekday"] = df_dt[column].dt.weekday
        df_dt[f"{column}_hour"] = df_dt[column].dt.hour
        
        return df_dt


class DataProcessor:
    """Main data processor that combines all operations."""

    def __init__(self):
        self.cleaner = DataCleaner()
        self.transformer = DataTransformer()
        self.engineer = FeatureEngineer()

    def process_data(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """Process data according to configuration."""
        df_processed = df.copy()
        
        # Data cleaning
        cleaning_config = config.get("cleaning", {})
        if cleaning_config.get("remove_duplicates", False):
            df_processed = self.cleaner.remove_duplicates(df_processed)
        
        missing_value_strategy = cleaning_config.get("missing_values", "drop")
        if missing_value_strategy != "none":
            df_processed = self.cleaner.handle_missing_values(df_processed, missing_value_strategy)
        
        # Data transformation
        transform_config = config.get("transformation", {})
        scaling_method = transform_config.get("scaling", "none")
        if scaling_method != "none":
            df_processed = self.transformer.scale_features(df_processed, method=scaling_method)
        
        encoding_method = transform_config.get("encoding", "none")
        if encoding_method == "label":
            df_processed = self.transformer.encode_categorical(df_processed)
        elif encoding_method == "dummy":
            df_processed = self.transformer.create_dummy_variables(df_processed)
        
        # Feature engineering
        feature_config = config.get("feature_engineering", {})
        if feature_config.get("polynomial", False):
            poly_columns = feature_config.get("polynomial_columns", [])
            poly_degree = feature_config.get("polynomial_degree", 2)
            df_processed = self.engineer.create_polynomial_features(df_processed, poly_columns, poly_degree)
        
        if feature_config.get("interactions", False):
            interaction_columns = feature_config.get("interaction_columns", [])
            df_processed = self.engineer.create_interaction_features(df_processed, interaction_columns)
        
        return df_processed

    def get_feature_names(self, df: pd.DataFrame) -> List[str]:
        """Get feature names from processed dataframe."""
        return df.columns.tolist()


# Convenience functions
def create_data_processor() -> DataProcessor:
    """Create a data processor."""
    return DataProcessor()


def split_features_target(df: pd.DataFrame, target_column: str) -> Tuple[pd.DataFrame, pd.Series]:
    """Split dataframe into features and target."""
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataframe")
    
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    return X, y