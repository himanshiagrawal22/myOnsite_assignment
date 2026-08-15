from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import hashlib

from app.prediction import predict_population
from app.audit import create_audit_log
from app.storage import get_connection, initialize_database
from app.conflict_engine import resolve_conflict, is_late_event
from pydantic import BaseModel, Field


app = FastAPI(
    title="Real-Time Satellite Population Estimator",
    description="Satellite brightness based population estimation system",
    version="1.0.0"
)


class SatelliteObservation(BaseModel):
    source_id: str = Field(..., min_length=1)
    timestamp: datetime
    city_id: str = Field(..., min_length=1)
    brightness_value: float = Field(..., ge=0)
    reliability_score: float = Field(..., ge=0, le=1)

class PopulationPredictionRequest(BaseModel):
    average_masked_mean: float = Field(..., ge=0)
    average_masked_max: float = Field(..., ge=0)
    average_masked_min: float = Field(..., ge=0)
    average_masked_stdDev: float = Field(..., ge=0)


initialize_database()


@app.get("/")
def root():
    return {
        "message": "Satellite Population Estimator API is running"
    }


def generate_event_id(observation: SatelliteObservation):

    raw_data = (
        f"{observation.source_id}|"
        f"{observation.timestamp.isoformat()}|"
        f"{observation.city_id}|"
        f"{observation.brightness_value}|"
        f"{observation.reliability_score}"
    )

    return hashlib.sha256(
        raw_data.encode()
    ).hexdigest()


@app.post("/ingest")
def ingest_observation(observation: SatelliteObservation):

    # --------------------------------------------------
    # 1. Generate unique event ID
    # --------------------------------------------------

    event_id = generate_event_id(observation)

    event_timestamp = observation.timestamp.isoformat()


    # --------------------------------------------------
    # 2. Check whether this is a late event
    # --------------------------------------------------

    late_event = is_late_event(
        observation.city_id,
        event_timestamp
    )


    # --------------------------------------------------
    # 3. Connect to database
    # --------------------------------------------------

    connection = get_connection()

    cursor = connection.cursor()


    # --------------------------------------------------
    # 4. Check for exact duplicate
    # --------------------------------------------------

    cursor.execute(
        """
        SELECT *
        FROM observations
        WHERE event_id = ?
        """,
        (event_id,)
    )

    existing_observation = cursor.fetchone()


    if existing_observation:

        connection.close()

        create_audit_log(
            event_id=event_id,
            city_id=observation.city_id,
            event_timestamp=event_timestamp,
            action="INGEST",
            decision="DUPLICATE",
            reason="Identical event_id was already processed",
            input_data=observation.model_dump(),
            output_data={
                "status": "duplicate"
            }
        )

        return {
            "status": "duplicate",
            "message": "Observation already processed",
            "event_id": event_id,
            "late_event": False
        }


    # --------------------------------------------------
    # 5. Store raw observation
    # --------------------------------------------------

    received_at = datetime.utcnow().isoformat()

    cursor.execute(
        """
        INSERT INTO observations (
            source_id,
            timestamp,
            city_id,
            brightness_value,
            reliability_score,
            event_id,
            created_at,
            received_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            observation.source_id,
            event_timestamp,
            observation.city_id,
            observation.brightness_value,
            observation.reliability_score,
            event_id,
            received_at,
            received_at
        )
    )


    connection.commit()
    connection.close()


    # --------------------------------------------------
    # 6. Resolve conflict
    # --------------------------------------------------

    winner = resolve_conflict(
        observation.city_id,
        event_timestamp
    )


    # --------------------------------------------------
    # 7. Create audit log
    # --------------------------------------------------

    create_audit_log(
        event_id=event_id,
        city_id=observation.city_id,
        event_timestamp=event_timestamp,
        action="INGEST",
        decision="ACCEPTED",
        reason=(
            "Late event detected"
            if late_event
            else "New observation accepted"
        ),
        input_data=observation.model_dump(),
        output_data={
            "winner_observation_id": winner["id"],
            "winner_source_id": winner["source_id"],
            "winner_brightness": winner["brightness_value"],
            "winner_reliability": winner["reliability_score"],
            "late_event": late_event
        }
    )


    # --------------------------------------------------
    # 8. Return result
    # --------------------------------------------------

    return {
        "status": "accepted",
        "message": "Observation stored and conflict resolved",
        "event_id": event_id,
        "late_event": late_event,
        "resolved_observation": {
            "observation_id": winner["id"],
            "source_id": winner["source_id"],
            "city_id": winner["city_id"],
            "timestamp": winner["timestamp"],
            "brightness_value": winner["brightness_value"],
            "reliability_score": winner["reliability_score"]
        }
    }
    
@app.post("/predict")
def predict_population_endpoint(
    request: PopulationPredictionRequest
):

    mean = request.average_masked_mean
    maximum = request.average_masked_max
    minimum = request.average_masked_min

    # Calculate derived features
    brightness_range = maximum - minimum

    brightness_ratio = (
        maximum / (mean + 1e-6)
    )

    brightness_product = (
        mean * maximum
    )

    features = {
        "average_masked_mean": mean,
        "average_masked_max": maximum,
        "average_masked_min": minimum,
        "average_masked_stdDev": request.average_masked_stdDev,
        "Brightness_Range": brightness_range,
        "Brightness_Ratio": brightness_ratio,
        "Brightness_Product": brightness_product
    }

    result = predict_population(features)

    return {
        "status": "success",
        "message": "Population prediction generated",
        "input_features": {
            "average_masked_mean": mean,
            "average_masked_max": maximum,
            "average_masked_min": minimum,
            "average_masked_stdDev": request.average_masked_stdDev
        },
        "derived_features": {
            "Brightness_Range": brightness_range,
            "Brightness_Ratio": brightness_ratio,
            "Brightness_Product": brightness_product
        },
        "prediction": result
    }