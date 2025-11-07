"""
Unit tests for recommendation engine
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.recommendation.engine import risk_band, generate_recommendations, _common_recos, _condition_specific


def test_risk_band_green():
    """Test green zone classification"""
    assert risk_band(15) == "green"
    assert risk_band(0) == "green"
    assert risk_band(30) == "green"


def test_risk_band_yellow():
    """Test yellow zone classification"""
    assert risk_band(45) == "yellow"
    assert risk_band(31) == "yellow"
    assert risk_band(70) == "yellow"


def test_risk_band_red():
    """Test red zone classification"""
    assert risk_band(85) == "red"
    assert risk_band(71) == "red"
    assert risk_band(100) == "red"


def test_generate_recommendations_diabetes():
    """Test diabetes recommendations"""
    result = generate_recommendations("diabetes", 45)
    
    assert result['condition'] == "diabetes"
    assert result['risk_score'] == 45
    assert result['risk_band'] == "yellow"
    assert isinstance(result['recommendations'], list)
    assert len(result['recommendations']) > 0


def test_generate_recommendations_heart():
    """Test heart disease recommendations"""
    result = generate_recommendations("heart", 25)
    
    assert result['condition'] == "heart"
    assert result['risk_band'] == "green"
    assert len(result['recommendations']) > 0


def test_generate_recommendations_kidney():
    """Test kidney disease recommendations"""
    result = generate_recommendations("kidney", 85)
    
    assert result['condition'] == "kidney"
    assert result['risk_band'] == "red"
    assert len(result['recommendations']) > 0


def test_common_recommendations_green():
    """Test common recommendations for green zone"""
    recos = _common_recos("green")
    
    assert isinstance(recos, list)
    assert len(recos) > 0
    assert any("exercise" in r.lower() for r in recos)


def test_common_recommendations_yellow():
    """Test common recommendations for yellow zone"""
    recos = _common_recos("yellow")
    
    assert isinstance(recos, list)
    assert any("physician" in r.lower() or "doctor" in r.lower() for r in recos)


def test_common_recommendations_red():
    """Test common recommendations for red zone"""
    recos = _common_recos("red")
    
    assert isinstance(recos, list)
    assert any("medical attention" in r.lower() or "er" in r.lower() for r in recos)


def test_condition_specific_diabetes_green():
    """Test diabetes-specific recommendations for green zone"""
    recos = _condition_specific("diabetes", "green")
    
    assert isinstance(recos, list)
    assert any("glucose" in r.lower() or "glycemic" in r.lower() for r in recos)


def test_condition_specific_heart_red():
    """Test heart-specific recommendations for red zone"""
    recos = _condition_specific("heart", "red")
    
    assert isinstance(recos, list)
    assert any("chest" in r.lower() or "er" in r.lower() for r in recos)


def test_recommendations_structure():
    """Test that recommendations have proper structure"""
    result = generate_recommendations("diabetes", 50)
    
    required_keys = ['condition', 'risk_score', 'risk_band', 'recommendations']
    for key in required_keys:
        assert key in result
    
    # Recommendations should be non-empty list of strings
    assert isinstance(result['recommendations'], list)
    assert all(isinstance(r, str) for r in result['recommendations'])
