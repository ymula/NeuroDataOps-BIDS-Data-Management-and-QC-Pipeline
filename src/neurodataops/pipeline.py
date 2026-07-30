from __future__ import annotations

import json
import os
import platform
from datetime import datetime, timezone
from pathlib import Path

import yaml
from dotenv import load_dotenv

from .database import create_database
from .inventory import (
    build_file_inventory,
    build_session_inventory,
    load_and_clean_participants,
)
from .qc import run_qc, write_html_report


def main() -> None:
    load_dotenv()
    bids_root = Path(os.environ["BIDS_ROOT"]).expanduser().resolve()
    output_root = Path(os.getenv("OUTPUT_ROOT", "outputs"))
    db_path = Path(os.getenv("DATABASE_PATH", output_root / "neurodataops.db"))

    if not bids_root.exists():
        raise FileNotFoundError(f"BIDS_ROOT does not exist: {bids_root}")

    with Path("config/project.yaml").open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)

    required = config["project"]["required_root_files"]
    missing = [name for name in required if not (bids_root / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing required BIDS root files: {missing}")

    output_root.mkdir(parents=True, exist_ok=True)

    files = build_file_inventory(bids_root)
    participants = load_and_clean_participants(bids_root)
    sessions = build_session_inventory(files)
    qc = run_qc(
        participants,
        sessions,
        config["project"]["expected_sessions"],
    )

    files.to_csv(output_root / "file_inventory.csv", index=False)
    participants.to_csv(output_root / "participants_clean.csv", index=False)
    sessions.to_csv(output_root / "session_inventory.csv", index=False)
    qc.to_csv(output_root / "qc_summary.csv", index=False)
    write_html_report(qc, output_root / "qc_report.html")
    create_database(db_path, participants, sessions, files)

    manifest = {
        "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_root": str(bids_root),
        "participant_count": len(participants),
        "inventoried_file_count": len(files),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
    }
    (output_root / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
