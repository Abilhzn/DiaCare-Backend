import pytest
from flask import Flask
from app import create_app  # pastikan ini dari app/__init__.py
import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_recommendation_with_normal_data(client):
    payload = {
        "age": 30,
        "glucose": 95,
        "condition": "sebelum",
        "category": "sehat"
    }
    response = client.post('/api/recommendations/get_recommendation',
                           data=json.dumps(payload),
                           content_type='application/json')
    
    data = response.get_json()
    assert response.status_code == 200
    assert data['status'] == "none"
    assert data['message'] is None

def test_recommendation_with_high_glucose(client):
    payload = {
        "age": 30,
        "glucose": 150,
        "condition": "sesudah",
        "category": "sehat"
    }
    response = client.post('/api/recommendations/get_recommendation',
                           data=json.dumps(payload),
                           content_type='application/json')
    
    data = response.get_json()
    assert response.status_code == 200
    assert data['status'] == "success"
    assert "Gula darah Anda tinggi" in data['message']
