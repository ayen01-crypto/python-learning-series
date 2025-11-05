"""
Analysis Module
This module handles exploratory data analysis and statistical analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Dict, Any, List, Tuple
import json
import os


class ExploratoryDataAnalyzer:
    """Performs exploratory data analysis."""

    def __init__(self):
        # Set style for plots
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")

    def get_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get comprehensive summary of the data."""
        summary = {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "data_types": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "missing_percentage": (df.isnull().sum() / len(df) * 100).to_dict(),
            "duplicate_rows": df.duplicated().sum(),
            "memory_usage": df.memory_usage(deep=True).sum()
        }
        
        # Numerical columns summary
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0:
            summary["numerical_summary"] = df[numerical_cols].describe().to_dict()
        
        # Categorical columns summary
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            summary["categorical_summary"] = {}
            for col in categorical_cols:
                summary["categorical_summary"][col] = {
                    "unique_values": df[col].nunique(),
                    "top_values": df[col].value_counts().head().to_dict()
                }
        
        return summary

    def plot_distributions(self, df: pd.DataFrame, columns: List[str] = None, save_path: str = None):
        """Plot distributions of numerical columns."""
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        n_cols = len(columns)
        if n_cols == 0:
            return
        
        n_rows = (n_cols + 2) // 3
        fig, axes = plt.subplots(n_rows, min(3, n_cols), figsize=(15, 5 * n_rows))
        axes = axes.flatten() if n_cols > 1 else [axes]
        
        for i, col in enumerate(columns):
            if col not in df.columns:
                continue
            
            # Histogram
            axes[i].hist(df[col].dropna(), bins=30, alpha=0.7, color='skyblue', edgecolor='black')
            axes[i].set_title(f'Distribution of {col}')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Frequency')
            
            # Add statistics
            mean_val = df[col].mean()
            axes[i].axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
            axes[i].legend()
        
        # Hide empty subplots
        for i in range(n_cols, len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()

    def plot_correlation_matrix(self, df: pd.DataFrame, save_path: str = None):
        """Plot correlation matrix."""
        numerical_df = df.select_dtypes(include=[np.number])
        if numerical_df.empty:
            return
        
        corr_matrix = numerical_df.corr()
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                    square=True, linewidths=0.5, cbar_kws={"shrink": .8})
        plt.title('Correlation Matrix')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()

    def plot_categorical_distributions(self, df: pd.DataFrame, columns: List[str] = None, save_path: str = None):
        """Plot distributions of categorical columns."""
        if columns is None:
            columns = df.select_dtypes(include=['object']).columns.tolist()
        
        n_cols = len(columns)
        if n_cols == 0:
            return
        
        n_rows = (n_cols + 1) // 2
        fig, axes = plt.subplots(n_rows, min(2, n_cols), figsize=(15, 6 * n_rows))
        axes = axes.flatten() if n_cols > 1 else [axes]
        
        for i, col in enumerate(columns):
            if col not in df.columns:
                continue
            
            value_counts = df[col].value_counts().head(10)  # Top 10 values
            axes[i].bar(range(len(value_counts)), value_counts.values, color='lightcoral')
            axes[i].set_title(f'Distribution of {col}')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Count')
            axes[i].set_xticks(range(len(value_counts)))
            axes[i].set_xticklabels(value_counts.index, rotation=45, ha='right')
        
        # Hide empty subplots
        for i in range(n_cols, len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()


class StatisticalAnalyzer:
    """Performs statistical analysis."""

    def __init__(self):
        pass

    def normality_test(self, df: pd.DataFrame, columns: List[str] = None) -> Dict[str, Dict[str, float]]:
        """Perform normality tests on numerical columns."""
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        results = {}
        for col in columns:
            if col not in df.columns:
                continue
            
            data = df[col].dropna()
            if len(data) < 8:  # Minimum sample size for reliable tests
                continue
            
            # Shapiro-Wilk test
            try:
                shapiro_stat, shapiro_p = stats.shapiro(data.sample(min(5000, len(data))))
            except:
                shapiro_stat, shapiro_p = np.nan, np.nan
            
            # Kolmogorov-Smirnov test
            try:
                ks_stat, ks_p = stats.kstest(data, 'norm')
            except:
                ks_stat, ks_p = np.nan, np.nan
            
            results[col] = {
                "shapiro_statistic": shapiro_stat,
                "shapiro_p_value": shapiro_p,
                "ks_statistic": ks_stat,
                "ks_p_value": ks_p,
                "is_normal_shapiro": shapiro_p > 0.05,
                "is_normal_ks": ks_p > 0.05
            }
        
        return results

    def correlation_analysis(self, df: pd.DataFrame, method: str = 'pearson') -> pd.DataFrame:
        """Perform correlation analysis."""
        numerical_df = df.select_dtypes(include=[np.number])
        if numerical_df.empty:
            return pd.DataFrame()
        
        return numerical_df.corr(method=method)

    def hypothesis_testing(self, df: pd.DataFrame, column1: str, column2: str, test_type: str = 'ttest') -> Dict[str, float]:
        """Perform hypothesis testing between two columns."""
        if column1 not in df.columns or column2 not in df.columns:
            raise ValueError("One or both columns not found in dataframe")
        
        data1 = df[column1].dropna()
        data2 = df[column2].dropna()
        
        if test_type == 'ttest':
            stat, p_value = stats.ttest_ind(data1, data2)
        elif test_type == 'mannwhitney':
            stat, p_value = stats.mannwhitneyu(data1, data2)
        elif test_type == 'anova':
            stat, p_value = stats.f_oneway(data1, data2)
        else:
            raise ValueError(f"Unknown test type: {test_type}")
        
        return {
            "statistic": stat,
            "p_value": p_value,
            "significant": p_value < 0.05
        }


class ReportGenerator:
    """Generates analysis reports."""

    def __init__(self, report_dir: str = "reports"):
        self.report_dir = report_dir
        os.makedirs(report_dir, exist_ok=True)

    def generate_summary_report(self, df: pd.DataFrame, eda_results: Dict[str, Any], 
                              stat_results: Dict[str, Any], save_path: str = None) -> str:
        """Generate a summary report."""
        if save_path is None:
            save_path = os.path.join(self.report_dir, "analysis_summary.json")
        
        report = {
            "dataset_info": {
                "rows": eda_results["shape"][0],
                "columns": eda_results["shape"][1],
                "memory_usage_mb": eda_results["memory_usage"] / 1024 / 1024
            },
            "data_quality": {
                "missing_values": sum(eda_results["missing_values"].values()),
                "duplicate_rows": eda_results["duplicate_rows"],
                "completeness": 100 - (sum(eda_results["missing_percentage"].values()) / len(eda_results["missing_percentage"]) if eda_results["missing_percentage"] else 0)
            },
            "columns": eda_results["columns"],
            "data_types": eda_results["data_types"],
            "normality_tests": stat_results.get("normality", {})
        }
        
        with open(save_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        return save_path

    def generate_visualizations(self, df: pd.DataFrame, save_dir: str = None) -> List[str]:
        """Generate visualizations and save them."""
        if save_dir is None:
            save_dir = os.path.join(self.report_dir, "figures")
        os.makedirs(save_dir, exist_ok=True)
        
        eda = ExploratoryDataAnalyzer()
        saved_files = []
        
        # Distribution plots
        dist_path = os.path.join(save_dir, "distributions.png")
        eda.plot_distributions(df, save_path=dist_path)
        saved_files.append(dist_path)
        
        # Correlation matrix
        corr_path = os.path.join(save_dir, "correlation_matrix.png")
        eda.plot_correlation_matrix(df, save_path=corr_path)
        saved_files.append(corr_path)
        
        # Categorical distributions
        cat_path = os.path.join(save_dir, "categorical_distributions.png")
        eda.plot_categorical_distributions(df, save_path=cat_path)
        saved_files.append(cat_path)
        
        return saved_files


# Convenience functions
def perform_eda(df: pd.DataFrame) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Perform comprehensive exploratory data analysis."""
    eda_analyzer = ExploratoryDataAnalyzer()
    stat_analyzer = StatisticalAnalyzer()
    
    # Get data summary
    eda_results = eda_analyzer.get_data_summary(df)
    
    # Perform statistical tests
    stat_results = {
        "normality": stat_analyzer.normality_test(df),
        "correlations": stat_analyzer.correlation_analysis(df).to_dict()
    }
    
    return eda_results, stat_results


def generate_report(df: pd.DataFrame, eda_results: Dict[str, Any], 
                   stat_results: Dict[str, Any], report_dir: str = "reports") -> str:
    """Generate analysis report."""
    reporter = ReportGenerator(report_dir)
    return reporter.generate_summary_report(df, eda_results, stat_results)