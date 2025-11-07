"""
Unit tests for ML training utilities
"""
import pytest
import sys
import os
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.trainer import _detect_target_column, _split_features


def test_detect_target_column_outcome():
    """Test target detection with 'Outcome' column"""
    df = pd.DataFrame({
        'feature1': [1, 2, 3],
        'feature2': [4, 5, 6],
        'Outcome': [0, 1, 0]
    })
    
    target = _detect_target_column(df)
    assert target == 'Outcome'


def test_detect_target_column_target():
    """Test target detection with 'target' column"""
    df = pd.DataFrame({
        'age': [25, 30, 35],
        'bp': [120, 130, 140],
        'target': [1, 0, 1]
    })
    
    target = _detect_target_column(df)
    assert target == 'target'


def test_detect_target_column_classification():
    """Test target detection with 'classification' column"""
    df = pd.DataFrame({
        'feature1': [1, 2, 3],
        'classification': [0, 1, 0]
    })
    
    target = _detect_target_column(df)
    assert target == 'classification'


def test_detect_target_column_last():
    """Test target detection falls back to last binary column"""
    df = pd.DataFrame({
        'feature1': [1, 2, 3],
        'feature2': [4, 5, 6],
        'label': [0, 1, 0]
    })
    
    target = _detect_target_column(df)
    assert target == 'label'


def test_split_features():
    """Test feature splitting"""
    df = pd.DataFrame({
        'feature1': [1, 2, 3],
        'feature2': [4, 5, 6],
        'Outcome': [0, 1, 0]
    })
    
    X, y = _split_features(df, 'Outcome')
    
    assert 'Outcome' not in X.columns
    assert len(X.columns) == 2
    assert len(y) == 3
    assert list(y) == [0, 1, 0]


def test_split_features_no_target():
    """Test feature splitting when target doesn't exist"""
    df = pd.DataFrame({
        'feature1': [1, 2, 3],
        'feature2': [4, 5, 6]
    })
    
    X, y = _split_features(df, 'nonexistent')
    
    assert len(X.columns) == 2
    assert y is None
