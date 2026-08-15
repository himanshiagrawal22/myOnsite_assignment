from datetime import datetime

from app.storage import get_connection


def is_late_event(city_id: str, event_timestamp: str):
    """
    An event is considered late when its timestamp is
    older than the latest event already stored for the city.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT MAX(timestamp) AS latest_timestamp
        FROM observations
        WHERE city_id = ?
        """,
        (city_id,)
    )

    result = cursor.fetchone()

    connection.close()

    latest_timestamp = result["latest_timestamp"]

    # No previous event for this city
    if latest_timestamp is None:
        return False

    return event_timestamp < latest_timestamp


def resolve_conflict(city_id: str, timestamp: str):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM observations
        WHERE city_id = ?
        AND timestamp = ?
        ORDER BY
            reliability_score DESC,
            timestamp ASC,
            id ASC
        """,
        (city_id, timestamp)
    )

    observations = cursor.fetchall()

    if not observations:
        connection.close()
        return None

    winner = observations[0]

    cursor.execute(
        """
        INSERT INTO resolved_observations (
            city_id,
            timestamp,
            observation_id,
            brightness_value,
            reliability_score,
            resolved_at
        )
        VALUES (?, ?, ?, ?, ?, ?)

        ON CONFLICT(city_id, timestamp)
        DO UPDATE SET
            observation_id = excluded.observation_id,
            brightness_value = excluded.brightness_value,
            reliability_score = excluded.reliability_score,
            resolved_at = excluded.resolved_at
        """,
        (
            winner["city_id"],
            winner["timestamp"],
            winner["id"],
            winner["brightness_value"],
            winner["reliability_score"],
            datetime.utcnow().isoformat()
        )
    )

    connection.commit()
    connection.close()

    return winner