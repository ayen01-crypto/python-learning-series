"""
Reporting Module
This module handles report generation and visualization.
"""

import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, List
from datetime import datetime


class ReportGenerator:
    """Generates comprehensive reports."""

    def __init__(self, report_dir: str = "reports"):
        self.report_dir = report_dir
        os.makedirs(report_dir, exist_ok=True)
        self.figures_dir = os.path.join(report_dir, "figures")
        os.makedirs(self.figures_dir, exist_ok=True)

    def generate_data_summary_report(self, df: pd.DataFrame, eda_results: Dict[str, Any], 
                                   output_path: str = None) -> str:
        """Generate data summary report."""
        if output_path is None:
            output_path = os.path.join(self.report_dir, "data_summary.json")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "dataset_info": {
                "shape": df.shape,
                "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024,
                "columns": df.columns.tolist()
            },
            "data_quality": {
                "missing_values": eda_results.get("missing_values", {}),
                "missing_percentage": eda_results.get("missing_percentage", {}),
                "duplicate_rows": eda_results.get("duplicate_rows", 0)
            },
            "data_types": eda_results.get("data_types", {}),
            "numerical_summary": eda_results.get("numerical_summary", {}),
            "categorical_summary": eda_results.get("categorical_summary", {})
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        return output_path

    def generate_model_evaluation_report(self, evaluation_results: Dict[str, Dict[str, float]], 
                                       output_path: str = None) -> str:
        """Generate model evaluation report."""
        if output_path is None:
            output_path = os.path.join(self.report_dir, "model_evaluation.json")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "model_results": evaluation_results
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        return output_path

    def generate_pipeline_summary(self, orchestrator: Any, output_path: str = None) -> str:
        """Generate pipeline summary report."""
        if output_path is None:
            output_path = os.path.join(self.report_dir, "pipeline_summary.json")
        
        status = orchestrator.get_pipeline_status()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "pipeline_status": status,
            "execution_summary": {
                "total_execution_time": sum(status.get("execution_times", {}).values()),
                "steps_completed": len(status.get("steps_completed", []))
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        return output_path

    def create_visualizations(self, df: pd.DataFrame, evaluation_results: Dict[str, Dict[str, float]] = None) -> List[str]:
        """Create visualizations and save them."""
        saved_files = []
        
        # Data distribution plots
        try:
            numerical_cols = df.select_dtypes(include=['number']).columns
            if len(numerical_cols) > 0:
                fig, ax = plt.subplots(figsize=(12, 8))
                df[numerical_cols].hist(bins=20, ax=ax)
                ax.set_title("Data Distribution")
                fig_path = os.path.join(self.figures_dir, "data_distribution.png")
                plt.savefig(fig_path, dpi=300, bbox_inches='tight')
                saved_files.append(fig_path)
                plt.close()
        except Exception as e:
            print(f"Warning: Could not create distribution plot - {e}")
        
        # Correlation heatmap
        try:
            numerical_df = df.select_dtypes(include=['number'])
            if not numerical_df.empty and numerical_df.shape[1] > 1:
                plt.figure(figsize=(10, 8))
                sns.heatmap(numerical_df.corr(), annot=True, cmap='coolwarm', center=0)
                plt.title("Feature Correlation Matrix")
                corr_path = os.path.join(self.figures_dir, "correlation_matrix.png")
                plt.savefig(corr_path, dpi=300, bbox_inches='tight')
                saved_files.append(corr_path)
                plt.close()
        except Exception as e:
            print(f"Warning: Could not create correlation plot - {e}")
        
        # Model comparison chart
        if evaluation_results:
            try:
                model_names = list(evaluation_results.keys())
                metrics = []
                
                # Determine if regression or classification
                sample_result = list(evaluation_results.values())[0]
                is_regression = "rmse" in sample_result
                
                if is_regression:
                    metric_values = [results.get("rmse", 0) for results in evaluation_results.values()]
                    metric_name = "RMSE"
                else:
                    metric_values = [results.get("accuracy", 0) for results in evaluation_results.values()]
                    metric_name = "Accuracy"
                
                plt.figure(figsize=(10, 6))
                bars = plt.bar(model_names, metric_values)
                plt.title(f"Model Comparison - {metric_name}")
                plt.ylabel(metric_name)
                plt.xticks(rotation=45, ha='right')
                
                # Add value labels on bars
                for bar, value in zip(bars, metric_values):
                    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                            f'{value:.3f}', ha='center', va='bottom')
                
                plt.tight_layout()
                model_comp_path = os.path.join(self.figures_dir, "model_comparison.png")
                plt.savefig(model_comp_path, dpi=300, bbox_inches='tight')
                saved_files.append(model_comp_path)
                plt.close()
            except Exception as e:
                print(f"Warning: Could not create model comparison plot - {e}")
        
        return saved_files

    def generate_html_report(self, data_summary_path: str, model_eval_path: str, 
                           pipeline_summary_path: str, figure_paths: List[str], 
                           output_path: str = None) -> str:
        """Generate HTML report."""
        if output_path is None:
            output_path = os.path.join(self.report_dir, "pipeline_report.html")
        
        # Load JSON reports
        try:
            with open(data_summary_path, 'r') as f:
                data_summary = json.load(f)
        except:
            data_summary = {}
        
        try:
            with open(model_eval_path, 'r') as f:
                model_eval = json.load(f)
        except:
            model_eval = {}
        
        try:
            with open(pipeline_summary_path, 'r') as f:
                pipeline_summary = json.load(f)
        except:
            pipeline_summary = {}
        
        # Create HTML content
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Data Analysis and ML Pipeline Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1, h2, h3 {{ color: #333; }}
        .section {{ margin-bottom: 30px; }}
        .metrics {{ display: flex; flex-wrap: wrap; }}
        .metric {{ 
            background: #f5f5f5; 
            padding: 15px; 
            margin: 10px; 
            border-radius: 5px; 
            min-width: 200px;
        }}
        .figures {{ display: flex; flex-wrap: wrap; }}
        .figure {{ margin: 10px; text-align: center; }}
        .figure img {{ max-width: 400px; height: auto; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>Data Analysis and ML Pipeline Report</h1>
    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <div class="section">
        <h2>Pipeline Summary</h2>
        <div class="metrics">
            <div class="metric">
                <h3>Steps Completed</h3>
                <p>{len(pipeline_summary.get('pipeline_status', {}).get('steps_completed', []))}</p>
            </div>
            <div class="metric">
                <h3>Execution Time</h3>
                <p>{pipeline_summary.get('execution_summary', {}).get('total_execution_time', 0):.2f}s</p>
            </div>
            <div class="metric">
                <h3>Best Model</h3>
                <p>{pipeline_summary.get('pipeline_status', {}).get('best_model', 'N/A')}</p>
            </div>
            <div class="metric">
                <h3>Best Score</h3>
                <p>{pipeline_summary.get('pipeline_status', {}).get('best_score', 0):.4f}</p>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>Data Summary</h2>
        <table>
            <tr>
                <th>Dataset Shape</th>
                <td>{data_summary.get('dataset_info', {}).get('shape', 'N/A')}</td>
            </tr>
            <tr>
                <th>Memory Usage</th>
                <td>{data_summary.get('dataset_info', {}).get('memory_usage_mb', 0):.2f} MB</td>
            </tr>
            <tr>
                <th>Missing Values</th>
                <td>{sum(data_summary.get('data_quality', {}).get('missing_values', {}).values())}</td>
            </tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Model Evaluation</h2>
        <table>
            <tr>
                <th>Model</th>
                <th>Metric</th>
                <th>Value</th>
            </tr>
        """
        
        # Add model results
        for model_name, results in model_eval.get('model_results', {}).items():
            # Determine primary metric
            if 'accuracy' in results:
                metric_name, metric_value = 'Accuracy', results['accuracy']
            elif 'rmse' in results:
                metric_name, metric_value = 'RMSE', results['rmse']
            else:
                metric_name, metric_value = 'Score', list(results.values())[0] if results else 'N/A'
            
            html_content += f"""
            <tr>
                <td>{model_name}</td>
                <td>{metric_name}</td>
                <td>{metric_value if isinstance(metric_value, (int, float)) else metric_value:.4f if str(metric_value).replace('.', '').isdigit() else metric_value}</td>
            </tr>
            """
        
        html_content += """
        </table>
    </div>
    
    <div class="section">
        <h2>Visualizations</h2>
        <div class="figures">
        """
        
        # Add figures
        for fig_path in figure_paths:
            fig_name = os.path.basename(fig_path)
            html_content += f"""
            <div class="figure">
                <img src="{fig_name}" alt="{fig_name}">
            </div>
            """
        
        html_content += """
        </div>
    </div>
</body>
</html>
        """
        
        # Save HTML report
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        return output_path


# Convenience functions
def create_report_generator(report_dir: str = "reports") -> ReportGenerator:
    """Create a report generator."""
    return ReportGenerator(report_dir)


def generate_complete_report(orchestrator: Any, df: pd.DataFrame, eda_results: Dict[str, Any], 
                           evaluation_results: Dict[str, Dict[str, float]], report_dir: str = "reports") -> List[str]:
    """Generate a complete report package."""
    reporter = ReportGenerator(report_dir)
    
    # Generate JSON reports
    data_summary_path = reporter.generate_data_summary_report(df, eda_results)
    model_eval_path = reporter.generate_model_evaluation_report(evaluation_results)
    pipeline_summary_path = reporter.generate_pipeline_summary(orchestrator)
    
    # Create visualizations
    figure_paths = reporter.create_visualizations(df, evaluation_results)
    
    # Generate HTML report
    html_report_path = reporter.generate_html_report(
        data_summary_path, model_eval_path, pipeline_summary_path, figure_paths
    )
    
    return [data_summary_path, model_eval_path, pipeline_summary_path, html_report_path] + figure_paths