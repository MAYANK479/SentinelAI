import pytest
from fastapi.testclient import TestClient
from app.api.router import router
from fastapi import FastAPI
from app.db import init_db

app = FastAPI()
app.include_router(router, prefix="/api/v1")

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()
    
@pytest.fixture
def client():
    return TestClient(app)

def test_predict_endpoint(client):
    payload = {
        "customer_id": "CUST_TEST",
        "Amount": 100.0,
        "MerchantCategoryRisk": 0.5,
        "NightTime": 0,
        "Velocity": 2,
        "GeographicJump": 0,
        "NewDevice": 0,
        "VPNUsed": 0,
        "SpendDeviation": 1.0,
        "FailedAttempts": 0
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "ml_probability" in data
    assert "composite_score" in data
    assert "risk_band" in data
    
def test_drift_check_endpoint(client):
    response = client.get("/api/v1/drift-check")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "drift_detected" in data
