"""
Data loading module for Smart Health Assistant
Loads and validates diabetes, heart disease, and kidney disease datasets
"""
import os
import pandas as pd
import numpy as np
import yaml
import os
from pathlib import Path

class DataLoader:
    """Load and validate healthcare datasets"""
    
    def __init__(self, config_path='config/config.yaml'):
        """
        Initialize data loader with configuration
        
        Args:
            config_path (str): Path to configuration YAML file
        """
        # Handle relative paths from different directories
        if not os.path.exists(config_path):
            # Try from project root
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            config_path = os.path.join(project_root, 'config', 'config.yaml')
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.raw_dir = self.config['data']['raw_dir']
        self.processed_dir = self.config['data']['processed_dir']
        
        # Create directories if they don't exist
        Path(self.raw_dir).mkdir(parents=True, exist_ok=True)
        Path(self.processed_dir).mkdir(parents=True, exist_ok=True)
    
    def load_diabetes_data(self):
        """
        Load PIMA Diabetes dataset
        
        Returns:
            pandas.DataFrame: Diabetes dataset or None if error
        """
        file_path = os.path.join(self.raw_dir, self.config['data']['diabetes_file'])
        
        try:
            df = pd.read_csv(file_path)
            print(f"✓ Diabetes data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
            
        except FileNotFoundError:
            print(f"✗ Error: File not found at {file_path}")
            print(f"   Please download dataset and place it in {self.raw_dir}")
            return None
        except Exception as e:
            print(f"✗ Error loading diabetes data: {str(e)}")
            return None
    
    def load_heart_data(self):
        """
        Load Heart Disease dataset
        
        Returns:
            pandas.DataFrame: Heart disease dataset or None if error
        """
        file_path = os.path.join(self.raw_dir, self.config['data']['heart_file'])
        
        try:
            df = pd.read_csv(file_path)
            print(f"✓ Heart disease data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
            
        except FileNotFoundError:
            print(f"✗ Error: File not found at {file_path}")
            print(f"   Please download dataset and place it in {self.raw_dir}")
            return None
        except Exception as e:
            print(f"✗ Error loading heart data: {str(e)}")
            return None
    
    def load_kidney_data(self):
        """
        Load Chronic Kidney Disease dataset
        
        Returns:
            pandas.DataFrame: Kidney disease dataset or None if error
        """
        file_path = os.path.join(self.raw_dir, self.config['data']['kidney_file'])
        
        try:
            df = pd.read_csv(file_path)
            print(f"✓ Kidney disease data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
            
        except FileNotFoundError:
            print(f"✗ Error: File not found at {file_path}")
            print(f"   Please download dataset and place it in {self.raw_dir}")
            return None
        except Exception as e:
            print(f"✗ Error loading kidney data: {str(e)}")
            return None
    
    def load_all_datasets(self):
        """
        Load all datasets at once
        
        Returns:
            dict: Dictionary with dataset names as keys and DataFrames as values
        """
        print("Loading all datasets...")
        print("-" * 50)
        
        datasets = {
            'diabetes': self.load_diabetes_data(),
            'heart': self.load_heart_data(),
            'kidney': self.load_kidney_data()
        }
        
        print("-" * 50)
        loaded = sum(1 for df in datasets.values() if df is not None)
        print(f"✓ Successfully loaded {loaded}/3 datasets")
        
        return datasets
    
    def get_data_info(self, df, dataset_name):
        """
        Get detailed information about a dataset
        
        Args:
            df (pandas.DataFrame): Dataset to analyze
            dataset_name (str): Name of the dataset
        """
        if df is None:
            print(f"Cannot display info for {dataset_name} - data not loaded")
            return
        
        print(f"\n{'='*60}")
        print(f"Dataset: {dataset_name.upper()}")
        print(f"{'='*60}")
        print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"\nColumns: {list(df.columns)}")
        print(f"\nData Types:\n{df.dtypes}")
        print(f"\nMissing Values:\n{df.isnull().sum()}")
        print(f"\nBasic Statistics:\n{df.describe()}")
        
        # Check for target variable
        possible_targets = ['Outcome', 'target', 'classification', 'class']
        for target in possible_targets:
            if target in df.columns:
                print(f"\nTarget Variable: {target}")
                print(f"Distribution:\n{df[target].value_counts()}")
                print(f"Percentage:\n{df[target].value_counts(normalize=True) * 100}")
                break

# Test the data loader
if __name__ == "__main__":
    print("Testing Data Loader...")
    print("="*60)
    
    # Create loader instance
    loader = DataLoader()
    
    # Load all datasets
    datasets = loader.load_all_datasets()
    
    # Display information about each dataset
    for name, df in datasets.items():
        if df is not None:
            loader.get_data_info(df, name)