"""
Main Entry Point for Data Analysis and ML Pipeline
This script orchestrates the entire pipeline from data ingestion to model deployment.
"""

import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.orchestrator import PipelineOrchestrator
from src.config import Config


def main():
    """Main function to run the pipeline."""
    print("=== Data Analysis and ML Pipeline ===")
    print(f"Start time: {datetime.now()}")
    
    # Load configuration
    config = Config()
    print(f"Configuration loaded from: {config.config_path}")
    
    # Initialize orchestrator
    orchestrator = PipelineOrchestrator(config)
    
    try:
        # Run the complete pipeline
        orchestrator.run_pipeline()
        
        print("\n=== Pipeline Completed Successfully ===")
        print(f"End time: {datetime.now()}")
        
        # Print summary
        print("\nPipeline Summary:")
        print(f"- Data sources processed: {len(orchestrator.data_sources)}")
        print(f"- Models trained: {len(orchestrator.trained_models)}")
        print(f"- Best model: {orchestrator.best_model_name}")
        print(f"- Model accuracy: {orchestrator.best_model_score:.4f}")
        
        # Start API server (optional)
        if config.deploy_model:
            print("\nStarting model API server...")
            from src.deployment import start_api_server
            start_api_server(orchestrator.best_model, config.api_port)
        
    except Exception as e:
        print(f"\n=== Pipeline Failed ===")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()