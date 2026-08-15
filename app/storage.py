import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/satellite.db")


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            city_id TEXT NOT NULL,
            brightness_value REAL NOT NULL,
            reliability_score REAL NOT NULL,
            event_id TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            received_at TEXT NOT NULL
        )
    """)

    try:
        cursor.execute(
            "ALTER TABLE observations ADD COLUMN received_at TEXT"
        )
    except sqlite3.OperationalError:
        pass

    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS resolved_observations (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         city_id TEXT NOT NULL,
    #         timestamp TEXT NOT NULL,
    #         observation_id INTEGER NOT NULL,
    #         brightness_value REAL NOT NULL,
    #         reliability_score REAL NOT NULL,
    #         resolved_at TEXT NOT NULL,
    #         UNIQUE(city_id, timestamp)
    #     )
    # """)
    
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id TEXT NOT NULL,
            city_id TEXT NOT NULL,
            event_timestamp TEXT NOT NULL,
            action TEXT NOT NULL,
            decision TEXT NOT NULL,
            reason TEXT NOT NULL,
            input_data TEXT NOT NULL,
            output_data TEXT,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()