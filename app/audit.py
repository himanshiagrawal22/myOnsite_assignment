import json
from datetime import datetime

from app.storage import get_connection


def create_audit_log(
    event_id,
    city_id,
    event_timestamp,
    action,
    decision,
    reason,
    input_data,
    output_data=None
):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO audit_logs (
            event_id,
            city_id,
            event_timestamp,
            action,
            decision,
            reason,
            input_data,
            output_data,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            event_id,
            city_id,
            event_timestamp,
            action,
            decision,
            reason,

            # Convert datetime and other non-JSON objects to strings
            json.dumps(input_data, default=str),

            json.dumps(output_data, default=str)
            if output_data is not None
            else None,

            datetime.utcnow().isoformat()
        )
    )

    connection.commit()
    connection.close()