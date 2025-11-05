"""
Orchestrator Module
This module orchestrates the entire data analysis and ML pipeline.
"""

import pandas as pd
import time
from typing import Dict, Any, List
from src.data_ingestion import create_data_ingestion_manager
from src.data_processing import create_data_processor, split_features_target
from src.analysis import perform_eda, generate_report
from src.ml_pipeline import create_ml_pipeline, train_and_evaluate
from src.deployment import deploy_model
from src.reporting import ReportGenerator


class PipelineOrchestrator:
    """Orchestrates the complete pipeline."""

    def __init__(self, config: Any):
        self.config = config
        self.data_sources = {}
        self.processed_data = None
        self.trained_models = {}
        self.evaluation_results = {}
        self.best_model_name = None
        self.best_model = None
        self.best_model_score = 0.0
        self.pipeline_steps = []
        self.execution_times = {}

    def run_pipeline(self):
        """Run the complete pipeline."""
        print("Starting pipeline execution...")
        
        # Step 1: Data Ingestion
        start_time = time.time()
        self._ingest_data()
        self.execution_times["data_ingestion"] = time.time() - start_time
        
        # Step 2: Data Processing
        start_time = time.time()
        self._process_data()
        self.execution_times["data_processing"] = time.time() - start_time
        
        # Step 3: Exploratory Data Analysis
        start_time = time.time()
        self._perform_eda()
        self.execution_times["eda"] = time.time() - start_time
        
        # Step 4: Machine Learning
        start_time = time.time()
        self._train_models()
        self.execution_times["ml_training"] = time.time() - start_time
        
        # Step 5: Model Deployment
        start_time = time.time()
        self._deploy_model()
        self.execution_times["deployment"] = time.time() - start_time
        
        # Step 6: Reporting
        start_time = time.time()
        self._generate_report()
        self.execution_times["reporting"] = time.time() - start_time
        
        print("Pipeline execution completed successfully!")

    def _ingest_data(self):
        """Step 1: Ingest data from sources."""
        print("Step 1: Ingesting data...")
        
        # Create data ingestion manager
        ingestion_manager = create_data_ingestion_manager(self.config.config)
        
        # Load all data
        self.data_sources = ingestion_manager.load_all_data()
        
        # Combine data if multiple sources
        if len(self.data_sources) > 1:
            # For simplicity, we'll use the first data source
            first_source = list(self.data_sources.keys())[0]
            self.processed_data = self.data_sources[first_source]
        elif len(self.data_sources) == 1:
            self.processed_data = list(self.data_sources.values())[0]
        else:
            raise ValueError("No data sources found")
        
        print(f"Loaded data with shape: {self.processed_data.shape}")
        self.pipeline_steps.append("data_ingestion")

    def _process_data(self):
        """Step 2: Process and clean data."""
        print("Step 2: Processing data...")
        
        if self.processed_data is None:
            raise ValueError("No data to process")
        
        # Create data processor
        processor = create_data_processor()
        
        # Process data
        self.processed_data = processor.process_data(self.processed_data, self.config.config)
        
        print(f"Processed data with shape: {self.processed_data.shape}")
        self.pipeline_steps.append("data_processing")

    def _perform_eda(self):
        """Step 3: Perform exploratory data analysis."""
        print("Step 3: Performing exploratory data analysis...")
        
        if self.processed_data is None:
            raise ValueError("No data for analysis")
        
        # Perform EDA
        eda_results, stat_results = perform_eda(self.processed_data)
        
        # Store results
        self.eda_results = eda_results
        self.stat_results = stat_results
        
        print("EDA completed")
        self.pipeline_steps.append("eda")

    def _train_models(self):
        """Step 4: Train machine learning models."""
        print("Step 4: Training machine learning models...")
        
        if self.processed_data is None:
            raise ValueError("No data for training")
        
        # For this example, we'll assume the target column is 'target'
        # In a real scenario, this would be configurable
        target_column = "target"
        
        try:
            # Split features and target
            X, y = split_features_target(self.processed_data, target_column)
            
            # Train and evaluate models
            self.trained_models, self.evaluation_results, self.best_model_name, self.best_model, self.best_model_score = train_and_evaluate(
                X, y, self.config.config
            )
            
            print(f"Trained {len(self.trained_models)} models")
            print(f"Best model: {self.best_model_name} with score: {self.best_model_score:.4f}")
            self.pipeline_steps.append("ml_training")
            
        except Exception as e:
            print(f"Warning: Could not train models - {e}")
            # Create a simple model as fallback
            from sklearn.dummy import DummyRegressor
            self.best_model = DummyRegressor()
            self.best_model_name = "dummy_regressor"
            self.best_model_score = 0.0

    def _deploy_model(self):
        """Step 5: Deploy the best model."""
        print("Step 5: Deploying model...")
        
        if self.best_model is None:
            print("No model to deploy")
            return
        
        try:
            # Deploy model
            model_path = deploy_model(
                self.best_model, 
                self.best_model_name, 
                self.config.config
            )
            
            print(f"Model deployed to: {model_path}")
            self.pipeline_steps.append("deployment")
            
        except Exception as e:
            print(f"Warning: Could not deploy model - {e}")

    def _generate_report(self):
        """Step 6: Generate pipeline report."""
        print("Step 6: Generating report...")
        
        try:
            # Create report generator
            reporter = ReportGenerator(self.config.report_save_path)
            
            # Generate summary report
            if hasattr(self, 'eda_results') and hasattr(self, 'stat_results'):
                report_path = generate_report(
                    self.processed_data, 
                    self.eda_results, 
                    self.stat_results, 
                    self.config.report_save_path
                )
                print(f"Report generated at: {report_path}")
            
            # Generate execution summary
            summary = {
                "pipeline_steps": self.pipeline_steps,
                "execution_times": self.execution_times,
                "data_shape": self.processed_data.shape if self.processed_data is not None else None,
                "models_trained": list(self.trained_models.keys()) if self.trained_models else [],
                "best_model": self.best_model_name,
                "best_score": self.best_model_score
            }
            
            summary_path = f"{self.config.report_save_path}/pipeline_summary.json"
            import json
            with open(summary_path, 'w') as f:
                json.dump(summary, f, indent=2, default=str)
            
            print(f"Pipeline summary saved to: {summary_path}")
            self.pipeline_steps.append("reporting")
            
        except Exception as e:
            print(f"Warning: Could not generate report - {e}")

    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status."""
        return {
            "steps_completed": self.pipeline_steps,
            "execution_times": self.execution_times,
            "data_loaded": self.processed_data is not None,
            "models_trained": len(self.trained_models),
            "best_model": self.best_model_name,
            "best_score": self.best_model_score
        }


# Convenience functions
def run_complete_pipeline(config: Any) -> PipelineOrchestrator:
    """Run the complete pipeline and return the orchestrator."""
    orchestrator = PipelineOrchestrator(config)
    orchestrator.run_pipeline()
    return orchestrator