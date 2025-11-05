"""
Deployment Module
This module handles model deployment and API serving.
"""

import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
import json
import os
from typing import Dict, Any, List, Optional
import threading
import time


class ModelServer:
    """Serves trained models via REST API."""

    def __init__(self, model_path: str = None, model: Any = None):
        self.app = Flask(__name__)
        self.model = None
        self.model_metadata = {}
        
        # Load model if path provided
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        elif model:
            self.model = model
        
        # Setup routes
        self._setup_routes()

    def load_model(self, model_path: str):
        """Load a trained model."""
        self.model = joblib.load(model_path)
        
        # Load metadata if available
        metadata_path = model_path.replace('.joblib', '_metadata.json')
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                self.model_metadata = json.load(f)

    def save_model(self, model_path: str):
        """Save the current model."""
        joblib.dump(self.model, model_path)
        
        # Save metadata
        metadata_path = model_path.replace('.joblib', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(self.model_metadata, f, indent=2)

    def _setup_routes(self):
        """Setup API routes."""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint."""
            return jsonify({
                "status": "healthy",
                "model_loaded": self.model is not None,
                "timestamp": time.time()
            })

        @self.app.route('/predict', methods=['POST'])
        def predict():
            """Prediction endpoint."""
            if not self.model:
                return jsonify({"error": "No model loaded"}), 500
            
            try:
                # Get input data
                data = request.get_json()
                
                if not data:
                    return jsonify({"error": "No input data provided"}), 400
                
                # Handle different input formats
                if "features" in data:
                    features = data["features"]
                else:
                    features = data
                
                # Convert to DataFrame
                if isinstance(features, dict):
                    # Single prediction
                    df = pd.DataFrame([features])
                elif isinstance(features, list):
                    if isinstance(features[0], dict):
                        # Multiple predictions
                        df = pd.DataFrame(features)
                    else:
                        # Single prediction as list
                        df = pd.DataFrame([features], columns=self.model_metadata.get("feature_names", []))
                else:
                    return jsonify({"error": "Invalid input format"}), 400
                
                # Make prediction
                predictions = self.model.predict(df)
                
                # Format response
                response = {
                    "predictions": predictions.tolist(),
                    "model": self.model_metadata.get("model_name", "unknown"),
                    "timestamp": time.time()
                }
                
                return jsonify(response)
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route('/model/info', methods=['GET'])
        def model_info():
            """Get model information."""
            if not self.model:
                return jsonify({"error": "No model loaded"}), 500
            
            info = {
                "model_type": type(self.model).__name__,
                "metadata": self.model_metadata,
                "features": self.model_metadata.get("feature_names", [])
            }
            
            return jsonify(info)

    def run(self, host: str = 'localhost', port: int = 5000, debug: bool = False):
        """Run the API server."""
        self.app.run(host=host, port=port, debug=debug)


class ModelDeployer:
    """Handles model deployment operations."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.deployed_models = {}

    def deploy_model(self, model: Any, model_name: str, feature_names: List[str] = None) -> str:
        """Deploy a model and return the deployment path."""
        model_save_path = self.config.get("model_save_path", "models")
        os.makedirs(model_save_path, exist_ok=True)
        
        # Save model
        model_path = os.path.join(model_save_path, f"{model_name}.joblib")
        joblib.dump(model, model_path)
        
        # Save metadata
        metadata = {
            "model_name": model_name,
            "feature_names": feature_names or [],
            "timestamp": time.time(),
            "model_type": type(model).__name__
        }
        
        metadata_path = model_path.replace('.joblib', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Store deployed model info
        self.deployed_models[model_name] = {
            "path": model_path,
            "metadata": metadata
        }
        
        return model_path

    def create_api_server(self, model_path: str = None, model: Any = None) -> ModelServer:
        """Create an API server for a model."""
        return ModelServer(model_path, model)


class PredictionCache:
    """Caches predictions for performance."""

    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
        self.access_times = {}

    def get(self, key: str) -> Optional[Any]:
        """Get cached prediction."""
        if key in self.cache:
            self.access_times[key] = time.time()
            return self.cache[key]
        return None

    def put(self, key: str, value: Any):
        """Cache a prediction."""
        # Remove oldest entries if cache is full
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
            del self.cache[oldest_key]
            del self.access_times[oldest_key]
        
        self.cache[key] = value
        self.access_times[key] = time.time()

    def clear(self):
        """Clear the cache."""
        self.cache.clear()
        self.access_times.clear()


# Global model server instance
_model_server = None
_prediction_cache = PredictionCache()


def start_api_server(model: Any = None, port: int = 5000, host: str = 'localhost'):
    """Start the API server."""
    global _model_server
    
    if _model_server is None:
        _model_server = ModelServer(model=model)
    
    # Run server in a separate thread
    server_thread = threading.Thread(
        target=_model_server.run, 
        kwargs={'host': host, 'port': port, 'debug': False}
    )
    server_thread.daemon = True
    server_thread.start()
    
    print(f"Model API server started on http://{host}:{port}")
    print("Endpoints available:")
    print("  - GET  /health        - Health check")
    print("  - POST /predict       - Make predictions")
    print("  - GET  /model/info    - Model information")
    
    return _model_server


def make_prediction(model_path: str, features: Dict[str, Any]) -> List[float]:
    """Make a prediction using a saved model."""
    # Create cache key
    cache_key = f"{model_path}_{hash(str(features))}"
    
    # Check cache first
    cached_result = _prediction_cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    
    # Load model and make prediction
    model = joblib.load(model_path)
    df = pd.DataFrame([features])
    predictions = model.predict(df).tolist()
    
    # Cache result
    _prediction_cache.put(cache_key, predictions)
    
    return predictions


# Convenience functions
def deploy_model(model: Any, model_name: str, config: Dict[str, Any], 
                feature_names: List[str] = None) -> str:
    """Deploy a model."""
    deployer = ModelDeployer(config)
    return deployer.deploy_model(model, model_name, feature_names)