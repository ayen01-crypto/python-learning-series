"""
Simple Example of Data Analysis Pipeline
This script demonstrates how to use the pipeline with a simple dataset.
"""

import pandas as pd
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import Config
from orchestrator import PipelineOrchestrator


def create_sample_data():
    """Create sample data for demonstration."""
    # Create a simple dataset
    data = {
        'feature1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'feature2': [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
        'feature3': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
        'target': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
    }
    
    df = pd.DataFrame(data)
    
    # Save to CSV
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/sample_data.csv', index=False)
    
    print("Sample data created and saved to data/sample_data.csv")
    return df


def main():
    """Main function to run the example."""
    print("=== Simple Data Analysis Pipeline Example ===")
    
    # Create sample data
    df = create_sample_data()
    print(f"Created sample dataset with shape: {df.shape}")
    
    # Create configuration
    config = Config()
    
    # Update configuration for this example
    config.update_config("data_sources", [
        {
            "type": "csv",
            "path": "data/sample_data.csv",
            "name": "sample_data"
        }
    ])
    
    config.update_config("models", {
        "linear_regression": {},
        "random_forest": {"n_estimators": 10}
    })
    
    # Create and run pipeline
    orchestrator = PipelineOrchestrator(config)
    
    try:
        orchestrator.run_pipeline()
        
        # Print results
        status = orchestrator.get_pipeline_status()
        print("\n=== Pipeline Results ===")
        print(f"Steps completed: {status['steps_completed']}")
        print(f"Models trained: {status['models_trained']}")
        print(f"Best model: {status['best_model']}")
        print(f"Best score: {status['best_score']:.4f}")
        
        print("\n=== Example Completed Successfully ===")
        
    except Exception as e:
        print(f"Error running pipeline: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()