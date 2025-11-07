"""
Unit tests for the Flask API
"""
import pytest
import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.app import app, EXPECTED_FEATURES


@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    """Test the home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'version' in data


def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'models_loaded' in data


def test_predict_diabetes_valid(client):
    """Test diabetes prediction with valid data"""
    valid_data = {
        "Pregnancies": 6,
        "Glucose": 148,
        "BloodPressure": 72,
        "SkinThickness": 35,
        "Insulin": 0,
        "BMI": 33.6,
        "DiabetesPedigreeFunction": 0.627,
        "Age": 50
    }
    
    response = client.post('/predict/diabetes',
                          data=json.dumps(valid_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'risk_score' in data
    assert 'zone' in data
    assert data['disease'] == 'diabetes'
    assert data['zone'] in ['Green', 'Yellow', 'Red']


def test_predict_invalid_disease(client):
    """Test prediction with invalid disease type"""
    response = client.post('/predict/invalid_disease',
                          data=json.dumps({"test": 1}),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_predict_missing_features(client):
    """Test prediction with missing required features"""
    incomplete_data = {
        "Pregnancies": 6,
        "Glucose": 148
    }
    
    response = client.post('/predict/diabetes',
                          data=json.dumps(incomplete_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'missing' in data


def test_predict_no_data(client):
    """Test prediction with no data"""
    response = client.post('/predict/diabetes',
                          data=json.dumps({}),
                          content_type='application/json')
    
    assert response.status_code == 400


def test_recommendations_endpoint(client):
    """Test recommendations endpoint"""
    response = client.get('/recommendations/diabetes?risk_score=45')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'recommendations' in data
    assert 'risk_band' in data


def test_recommendations_missing_score(client):
    """Test recommendations without risk score"""
    response = client.get('/recommendations/diabetes')
    
    assert response.status_code == 400


def test_recommendations_invalid_disease(client):
    """Test recommendations with invalid disease"""
    response = client.get('/recommendations/invalid?risk_score=50')
    
    assert response.status_code == 400


def test_404_error(client):
    """Test 404 error handling"""
    response = client.get('/nonexistent')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data


def test_expected_features_structure():
    """Test that expected features are properly defined"""
    assert 'diabetes' in EXPECTED_FEATURES
    assert 'heart' in EXPECTED_FEATURES
    assert 'kidney' in EXPECTED_FEATURES
    
    # Check diabetes features
    assert len(EXPECTED_FEATURES['diabetes']) == 8
    assert 'Glucose' in EXPECTED_FEATURES['diabetes']
    assert 'BMI' in EXPECTED_FEATURES['diabetes']
