from __future__ import annotations

import sqlite3
from pathlib import Path
import pandas as pd


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS participants (
    participant_id TEXT PRIMARY KEY,
    group_name TEXT,
    sex TEXT,
    species TEXT,
    strain TEXT
);

CREATE TABLE IF NOT EXISTS sessions (
    participant_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    file_count INTEGER NOT NULL,
    total_bytes INTEGER NOT NULL,
    PRIMARY KEY (participant_id, session_id),
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id)
);

CREATE TABLE IF NOT EXISTS files (
    relative_path TEXT PRIMARY KEY,
    participant_id TEXT,
    session_id TEXT,
    suffix TEXT,
    size_bytes INTEGER,
    sha256 TEXT,
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id)
);
"""


def _find_column(frame: pd.DataFrame, candidates: list[str]) -> str | None:
    return next((name for name in candidates if name in frame.columns), None)


def create_database(
    db_path: Path,
    participants: pd.DataFrame,
    sessions: pd.DataFrame,
    files: pd.DataFrame,
) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)

    group_col = _find_column(participants, ["group", "group_name"])
    sex_col = _find_column(participants, ["sex"])
    species_col = _find_column(participants, ["species"])
    strain_col = _find_column(participants, ["strain"])

    normalized = pd.DataFrame({
        "participant_id": participants["participant_id"],
        "group_name": participants[group_col] if group_col else None,
        "sex": participants[sex_col] if sex_col else None,
        "species": participants[species_col] if species_col else "Rattus norvegicus",
        "strain": participants[strain_col] if strain_col else "Wistar",
    })

    db_files = files.rename(columns={"subject_id": "participant_id"})
    db_sessions = sessions.rename(columns={"subject_id": "participant_id"})

    with sqlite3.connect(db_path) as connection:
        connection.executescript(SCHEMA)
        connection.execute("DELETE FROM files")
        connection.execute("DELETE FROM sessions")
        connection.execute("DELETE FROM participants")
        normalized.to_sql("participants", connection, if_exists="append", index=False)
        valid_ids = set(normalized["participant_id"])
        db_sessions = db_sessions[db_sessions["participant_id"].isin(valid_ids)]
        db_files = db_files[
            db_files["participant_id"].isna() | db_files["participant_id"].isin(valid_ids)
        ]
        db_sessions.to_sql("sessions", connection, if_exists="append", index=False)
        db_files[
            ["relative_path", "participant_id", "session_id", "suffix", "size_bytes", "sha256"]
        ].to_sql("files", connection, if_exists="append", index=False)
