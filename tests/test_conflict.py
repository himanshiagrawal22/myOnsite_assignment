import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_conflict_resolution():

    unique_id = str(uuid.uuid4())

    timestamp = "2026-08-20T12:00:00"
    city_id = f"CONFLICT_TEST_CITY_{unique_id}"

    observation_a = {
        "source_id": f"SATELLITE_A_{unique_id}",
        "timestamp": timestamp,
        "city_id": city_id,
        "brightness_value": 100.0,
        "reliability_score": 0.60
    }

    observation_b = {
        "source_id": f"SATELLITE_B_{unique_id}",
        "timestamp": timestamp,
        "city_id": city_id,
        "brightness_value": 150.0,
        "reliability_score": 0.95
    }

    # Satellite A
    response_a = client.post(
        "/ingest",
        json=observation_a
    )

    assert response_a.status_code == 200
    assert response_a.json()["status"] == "accepted"

    # Satellite B
    response_b = client.post(
        "/ingest",
        json=observation_b
    )

    assert response_b.status_code == 200

    data = response_b.json()

    assert data["status"] == "accepted"

    winner = data["resolved_observation"]

    assert winner["source_id"] == observation_b["source_id"]
    assert winner["reliability_score"] == 0.95