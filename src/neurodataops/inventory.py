from __future__ import annotations

import hashlib
from pathlib import Path
import pandas as pd


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Return SHA-256 for regular, locally available files."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_file_inventory(bids_root: Path) -> pd.DataFrame:
    """Create an auditable file-level inventory."""
    rows: list[dict] = []
    for path in sorted(bids_root.rglob("*")):
        if not path.is_file() or ".git" in path.parts or ".datalad" in path.parts:
            continue
        relative = path.relative_to(bids_root)
        stat = path.stat()
        parts = relative.parts
        subject = next((p for p in parts if p.startswith("sub-")), None)
        session = next((p for p in parts if p.startswith("ses-")), None)
        rows.append(
            {
                "relative_path": relative.as_posix(),
                "subject_id": subject,
                "session_id": session,
                "suffix": "".join(path.suffixes),
                "size_bytes": stat.st_size,
                "sha256": sha256_file(path) if stat.st_size <= 100_000_000 else None,
            }
        )
    return pd.DataFrame(rows)


def load_and_clean_participants(bids_root: Path) -> pd.DataFrame:
    """Load participants.tsv and standardize column names and values."""
    path = bids_root / "participants.tsv"
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    frame = pd.read_csv(path, sep="\t", dtype=str)
    frame.columns = [c.strip().lower().replace(" ", "_") for c in frame.columns]
    frame = frame.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
    if "participant_id" not in frame.columns:
        raise ValueError("participants.tsv must contain participant_id")
    if frame["participant_id"].duplicated().any():
        duplicates = frame.loc[frame["participant_id"].duplicated(), "participant_id"].tolist()
        raise ValueError(f"Duplicate participant IDs: {duplicates}")
    return frame


def build_session_inventory(file_inventory: pd.DataFrame) -> pd.DataFrame:
    """Summarize file counts and bytes by subject and session."""
    usable = file_inventory.dropna(subset=["subject_id"]).copy()
    usable["session_id"] = usable["session_id"].fillna("no-session")
    return (
        usable.groupby(["subject_id", "session_id"], as_index=False)
        .agg(file_count=("relative_path", "count"), total_bytes=("size_bytes", "sum"))
        .sort_values(["subject_id", "session_id"])
    )
