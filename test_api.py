from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
headers = {"X-ESG-API-KEY": "dev-secret-key"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

def test_get_carbon_intensity_unauthorized():
    response = client.get("/api/v1/carbon/FR")
    assert response.status_code == 401

def test_get_carbon_intensity_authorized():
    response = client.get("/api/v1/carbon/FR", headers=headers)
    assert response.status_code == 200
    assert response.json()["region"] == "FR"
    assert "intensity_gco2_kwh" in response.json()


def test_get_batch_carbon_intensity_authorized():
    payload = {"regions": ["FR", "DE"]}
    response = client.post("/api/v1/carbon/batch", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    regions_returned = [item["region"] for item in data]
    assert "FR" in regions_returned
    assert "DE" in regions_returned