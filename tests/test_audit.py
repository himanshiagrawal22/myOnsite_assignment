import sqlite3
import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_audit_log_created():

    unique_id = str(uuid.uuid4())

    payload = {
        "source_id": f"AUDIT_TEST_SATELLITE_{unique_id}",
        "timestamp": "2026-08-21T12:00:00",
        "city_id": f"AUDIT_TEST_CITY_{unique_id}",
        "brightness_value": 180.0,
        "reliability_score": 0.92
    }

    response = client.post(
        "/ingest",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "accepted"

    event_id = data["event_id"]

    # Connect to database
    connection = sqlite3.connect("data/satellite.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    # Find audit record
    cursor.execute(
        """
        SELECT *
        FROM audit_logs
        WHERE event_id = ?
        """,
        (event_id,)
    )

    audit_record = cursor.fetchone()

    connection.close()

    # Verify audit record exists
    assert audit_record is not None

    assert audit_record["event_id"] == event_id
    assert audit_record["city_id"] == payload["city_id"]
    assert audit_record["action"] == "INGEST"
    assert audit_record["decision"] == "ACCEPTED"