import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_late_event():

    unique_id = str(uuid.uuid4())

    city_id = f"LATE_TEST_CITY_{unique_id}"

    # First: newer observation
    newer_observation = {
        "source_id": f"SATELLITE_NEW_{unique_id}",
        "timestamp": "2026-08-20T14:00:00",
        "city_id": city_id,
        "brightness_value": 200.0,
        "reliability_score": 0.90
    }

    response_new = client.post(
        "/ingest",
        json=newer_observation
    )

    assert response_new.status_code == 200
    assert response_new.json()["status"] == "accepted"

    # Second: older observation arrives later
    late_observation = {
        "source_id": f"SATELLITE_LATE_{unique_id}",
        "timestamp": "2026-08-20T12:00:00",
        "city_id": city_id,
        "brightness_value": 150.0,
        "reliability_score": 0.80
    }

    response_late = client.post(
        "/ingest",
        json=late_observation
    )

    assert response_late.status_code == 200

    data = response_late.json()

    assert data["status"] == "accepted"
    assert data["late_event"] is True