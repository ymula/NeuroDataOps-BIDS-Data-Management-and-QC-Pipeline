from __future__ import annotations

from pathlib import Path
import pandas as pd


def run_qc(
    participants: pd.DataFrame,
    sessions: pd.DataFrame,
    expected_sessions: list[str],
) -> pd.DataFrame:
    """Produce participant-level completeness and consistency metrics."""
    observed = (
        sessions.groupby("subject_id")["session_id"]
        .apply(lambda x: sorted(set(x) - {"no-session"}))
        .to_dict()
    )
    rows = []
    for participant_id in participants["participant_id"]:
        actual = observed.get(participant_id, [])
        missing = sorted(set(expected_sessions) - set(actual))
        rows.append({
            "participant_id": participant_id,
            "observed_session_count": len(actual),
            "expected_session_count": len(expected_sessions),
            "missing_sessions": ";".join(missing),
            "is_complete": len(missing) == 0,
        })
    return pd.DataFrame(rows)


def write_html_report(qc: pd.DataFrame, output_path: Path) -> None:
    complete = int(qc["is_complete"].sum())
    total = len(qc)
    rate = (complete / total * 100) if total else 0
    html = f"""
    <html>
      <head><title>NeuroDataOps QC Report</title></head>
      <body>
        <h1>NeuroDataOps QC Report</h1>
        <p>Participants: {total}</p>
        <p>Complete longitudinal records: {complete}</p>
        <p>Completeness rate: {rate:.1f}%</p>
        {qc.to_html(index=False)}
      </body>
    </html>
    """
    output_path.write_text(html, encoding="utf-8")
