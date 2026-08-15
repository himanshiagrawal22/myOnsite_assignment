import uuid

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_ingest_observation():

    unique_id = str(uuid.uuid4())

    payload = {
        "source_id": f"TEST_SATELLITE_{unique_id}",
        "timestamp": "2026-08-15T12:00:00",
        "city_id": f"TEST_CITY_{unique_id}",
        "brightness_value": 125.5,
        "reliability_score": 0.95
    }

    response = client.post(
        "/ingest",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "accepted"
    assert "event_id" in data
    assert "resolved_observation" in data


def test_duplicate_observation():

    unique_id = str(uuid.uuid4())

    payload = {
        "source_id": f"DUPLICATE_TEST_SATELLITE_{unique_id}",
        "timestamp": "2026-08-15T13:00:00",
        "city_id": f"DUPLICATE_TEST_CITY_{unique_id}",
        "brightness_value": 150.0,
        "reliability_score": 0.90
    }

    # First request
    response1 = client.post(
        "/ingest",
        json=payload
    )

    assert response1.status_code == 200
    assert response1.json()["status"] == "accepted"

    # Same request again
    response2 = client.post(
        "/ingest",
        json=payload
    )

    assert response2.status_code == 200

    data = response2.json()

    assert data["status"] == "duplicate"
    assert "event_id" in data