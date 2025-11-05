"""
Machine Learning Pipeline Module
This module handles model training, evaluation, and selection.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib
import os
from typing import Dict, Any, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class ModelTrainer:
    """Handles model training and hyperparameter tuning."""

    def __init__(self):
        self.models = {}
        self._initialize_models()

    def _initialize_models(self):
        """Initialize default models."""
        # Regression models
        self.models["linear_regression"] = LinearRegression()
        self.models["random_forest_regressor"] = RandomForestRegressor(random_state=42)
        self.models["gradient_boosting_regressor"] = GradientBoostingRegressor(random_state=42)
        
        # Classification models
        self.models["logistic_regression"] = LogisticRegression(random_state=42, max_iter=1000)
        self.models["random_forest_classifier"] = RandomForestClassifier(random_state=42)
        self.models["gradient_boosting_classifier"] = GradientBoostingClassifier(random_state=42)

    def train_model(self, X: pd.DataFrame, y: pd.Series, model_name: str, 
                   hyperparameters: Dict[str, Any] = None) -> Any:
        """Train a specific model."""
        if model_name not in self.models:
            raise ValueError(f"Unknown model: {model_name}")
        
        model = self.models[model_name]
        
        # Set hyperparameters if provided
        if hyperparameters:
            model.set_params(**hyperparameters)
        
        # Train the model
        model.fit(X, y)
        
        return model

    def tune_hyperparameters(self, X: pd.DataFrame, y: pd.Series, model_name: str, 
                           param_grid: Dict[str, List[Any]], cv: int = 5) -> Tuple[Any, Dict[str, Any]]:
        """Tune hyperparameters using grid search."""
        if model_name not in self.models:
            raise ValueError(f"Unknown model: {model_name}")
        
        model = self.models[model_name]
        
        # Perform grid search
        grid_search = GridSearchCV(model, param_grid, cv=cv, n_jobs=-1, scoring='accuracy' if hasattr(model, 'predict_proba') else 'neg_mean_squared_error')
        grid_search.fit(X, y)
        
        return grid_search.best_estimator_, grid_search.best_params_

    def cross_validate_model(self, X: pd.DataFrame, y: pd.Series, model_name: str, 
                           cv: int = 5) -> Dict[str, float]:
        """Perform cross-validation on a model."""
        if model_name not in self.models:
            raise ValueError(f"Unknown model: {model_name}")
        
        model = self.models[model_name]
        
        # Determine scoring metric
        scoring = 'accuracy' if hasattr(model, 'predict_proba') else 'neg_mean_squared_error'
        
        # Perform cross-validation
        scores = cross_val_score(model, X, y, cv=cv, scoring=scoring, n_jobs=-1)
        
        return {
            "mean_score": scores.mean(),
            "std_score": scores.std(),
            "scores": scores.tolist()
        }


class ModelEvaluator:
    """Handles model evaluation."""

    def __init__(self):
        pass

    def evaluate_regression_model(self, model: Any, X_test: pd.DataFrame, 
                                y_test: pd.Series) -> Dict[str, float]:
        """Evaluate a regression model."""
        y_pred = model.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(y_test - y_pred))
        
        # R-squared
        ss_res = np.sum((y_test - y_pred) ** 2)
        ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
        r2 = 1 - (ss_res / ss_tot)
        
        return {
            "mse": mse,
            "rmse": rmse,
            "mae": mae,
            "r2": r2
        }

    def evaluate_classification_model(self, model: Any, X_test: pd.DataFrame, 
                                    y_test: pd.Series) -> Dict[str, Any]:
        """Evaluate a classification model."""
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        
        # Classification report
        report = classification_report(y_test, y_pred, output_dict=True)
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        return {
            "accuracy": accuracy,
            "classification_report": report,
            "confusion_matrix": cm.tolist()
        }

    def compare_models(self, results: Dict[str, Dict[str, float]]) -> str:
        """Compare models and return the best one."""
        if not results:
            return None
        
        # For regression, lower is better (RMSE, MAE)
        # For classification, higher is better (Accuracy)
        regression_metrics = ["rmse", "mae"]
        classification_metrics = ["accuracy"]
        
        # Determine if this is regression or classification based on available metrics
        sample_result = list(results.values())[0]
        is_regression = any(metric in sample_result for metric in regression_metrics)
        
        if is_regression:
            # Find model with lowest RMSE
            best_model = min(results.items(), key=lambda x: x[1].get("rmse", float('inf')))
        else:
            # Find model with highest accuracy
            best_model = max(results.items(), key=lambda x: x[1].get("accuracy", 0))
        
        return best_model[0]


class ModelPipeline:
    """Main ML pipeline that combines training and evaluation."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.trainer = ModelTrainer()
        self.evaluator = ModelEvaluator()
        self.trained_models = {}
        self.evaluation_results = {}

    def prepare_data(self, X: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Prepare data for training."""
        test_size = self.config.get("test_size", 0.2)
        random_state = self.config.get("random_state", 42)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Scale features if required
        scaling_method = self.config.get("scaling_method", "none")
        if scaling_method != "none":
            scaler = StandardScaler()
            X_train_scaled = pd.DataFrame(
                scaler.fit_transform(X_train), 
                columns=X_train.columns, 
                index=X_train.index
            )
            X_test_scaled = pd.DataFrame(
                scaler.transform(X_test), 
                columns=X_test.columns, 
                index=X_test.index
            )
            return X_train_scaled, X_test_scaled, y_train, y_test
        
        return X_train, X_test, y_train, y_test

    def train_models(self, X_train: pd.DataFrame, y_train: pd.Series) -> Dict[str, Any]:
        """Train all configured models."""
        models_config = self.config.get("models", {})
        
        for model_name, model_params in models_config.items():
            try:
                print(f"Training {model_name}...")
                model = self.trainer.train_model(X_train, y_train, model_name, model_params)
                self.trained_models[model_name] = model
                print(f"Successfully trained {model_name}")
            except Exception as e:
                print(f"Failed to train {model_name}: {e}")
        
        return self.trained_models

    def evaluate_models(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, Dict[str, float]]:
        """Evaluate all trained models."""
        for model_name, model in self.trained_models.items():
            try:
                print(f"Evaluating {model_name}...")
                
                # Determine if this is a regression or classification problem
                if hasattr(model, 'predict_proba') or y_test.dtype == 'object':
                    # Classification
                    results = self.evaluator.evaluate_classification_model(model, X_test, y_test)
                else:
                    # Regression
                    results = self.evaluator.evaluate_regression_model(model, X_test, y_test)
                
                self.evaluation_results[model_name] = results
                print(f"Successfully evaluated {model_name}")
            except Exception as e:
                print(f"Failed to evaluate {model_name}: {e}")
        
        return self.evaluation_results

    def select_best_model(self) -> Tuple[str, Any, float]:
        """Select the best model based on evaluation results."""
        if not self.evaluation_results:
            return None, None, 0.0
        
        best_model_name = self.evaluator.compare_models(self.evaluation_results)
        best_model = self.trained_models[best_model_name]
        
        # Get the primary metric
        best_result = self.evaluation_results[best_model_name]
        if "accuracy" in best_result:
            score = best_result["accuracy"]
        elif "rmse" in best_result:
            score = best_result["rmse"]
        else:
            score = 0.0
        
        return best_model_name, best_model, score

    def save_model(self, model: Any, model_name: str, save_path: str = None) -> str:
        """Save a trained model."""
        if save_path is None:
            model_save_dir = self.config.get("model_save_path", "models")
            os.makedirs(model_save_dir, exist_ok=True)
            save_path = os.path.join(model_save_dir, f"{model_name}.joblib")
        
        joblib.dump(model, save_path)
        return save_path

    def load_model(self, model_path: str) -> Any:
        """Load a saved model."""
        return joblib.load(model_path)


# Convenience functions
def create_ml_pipeline(config: Dict[str, Any]) -> ModelPipeline:
    """Create an ML pipeline."""
    return ModelPipeline(config)


def train_and_evaluate(X: pd.DataFrame, y: pd.Series, config: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Dict[str, float]], str, Any, float]:
    """Train and evaluate models."""
    pipeline = ModelPipeline(config)
    
    # Prepare data
    X_train, X_test, y_train, y_test = pipeline.prepare_data(X, y)
    
    # Train models
    trained_models = pipeline.train_models(X_train, y_train)
    
    # Evaluate models
    evaluation_results = pipeline.evaluate_models(X_test, y_test)
    
    # Select best model
    best_model_name, best_model, best_score = pipeline.select_best_model()
    
    return trained_models, evaluation_results, best_model_name, best_model, best_score