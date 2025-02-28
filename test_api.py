import pytest
from fastapi.testclient import TestClient
from main import app  # Assure-toi que `app` est bien l'objet FastAPI dans `main.py`

client = TestClient(app)

def test_home():
    """Teste si la page d'accueil charge bien."""
    response = client.get("/")
    assert response.status_code == 200

def test_weather():
    """Teste l'API météo avec une ville valide."""
    response = client.get("/weather?city=Paris&days=1")
    assert response.status_code == 200
    assert "forecasts" in response.json()
