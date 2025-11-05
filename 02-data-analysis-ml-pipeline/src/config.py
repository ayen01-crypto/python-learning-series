"""
Configuration Module
This module handles configuration for the data analysis and ML pipeline.
"""

import os
import json
from typing import Dict, Any, Optional


class Config:
    """Configuration class for the pipeline."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config.json"
        self.config = self._load_config()
        
        # Data configuration
        self.data_sources = self.config.get("data_sources", [])
        self.data_dir = self.config.get("data_dir", "data")
        
        # Processing configuration
        self.test_size = self.config.get("test_size", 0.2)
        self.random_state = self.config.get("random_state", 42)
        self.scaling_method = self.config.get("scaling_method", "standard")
        
        # Model configuration
        self.models = self.config.get("models", {
            "linear_regression": {},
            "random_forest": {"n_estimators": 100},
            "gradient_boosting": {"n_estimators": 100}
        })
        self.cross_validation_folds = self.config.get("cross_validation_folds", 5)
        
        # Deployment configuration
        self.deploy_model = self.config.get("deploy_model", True)
        self.api_port = self.config.get("api_port", 5000)
        self.model_save_path = self.config.get("model_save_path", "models")
        
        # Reporting configuration
        self.generate_report = self.config.get("generate_report", True)
        self.report_save_path = self.config.get("report_save_path", "reports")
        
        # Performance configuration
        self.use_multiprocessing = self.config.get("use_multiprocessing", True)
        self.n_jobs = self.config.get("n_jobs", -1)
        
        # Create necessary directories
        self._create_directories()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            # Return default configuration
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "data_sources": [
                {
                    "type": "csv",
                    "path": "data/sample_data.csv",
                    "name": "sample_data"
                }
            ],
            "data_dir": "data",
            "test_size": 0.2,
            "random_state": 42,
            "scaling_method": "standard",
            "models": {
                "linear_regression": {},
                "random_forest": {"n_estimators": 100},
                "gradient_boosting": {"n_estimators": 100}
            },
            "cross_validation_folds": 5,
            "deploy_model": True,
            "api_port": 5000,
            "model_save_path": "models",
            "generate_report": True,
            "report_save_path": "reports",
            "use_multiprocessing": True,
            "n_jobs": -1
        }

    def _create_directories(self):
        """Create necessary directories."""
        directories = [
            self.data_dir,
            self.model_save_path,
            self.report_save_path
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def save_config(self, path: Optional[str] = None):
        """Save current configuration to file."""
        save_path = path or self.config_path
        with open(save_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def update_config(self, key: str, value: Any):
        """Update configuration value."""
        self.config[key] = value
        # Update corresponding attribute
        if hasattr(self, key):
            setattr(self, key, value)