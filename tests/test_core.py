import pandas as pd
from neurodataops.inventory import build_session_inventory
from neurodataops.qc import run_qc


def test_session_inventory():
    files = pd.DataFrame([
        {"relative_path": "sub-01/ses-s0/a.json", "subject_id": "sub-01",
         "session_id": "ses-s0", "size_bytes": 10},
        {"relative_path": "sub-01/ses-s0/a.nii.gz", "subject_id": "sub-01",
         "session_id": "ses-s0", "size_bytes": 20},
    ])
    result = build_session_inventory(files)
    assert result.iloc[0]["file_count"] == 2
    assert result.iloc[0]["total_bytes"] == 30


def test_qc_missing_session():
    participants = pd.DataFrame({"participant_id": ["sub-01"]})
    sessions = pd.DataFrame({
        "subject_id": ["sub-01"],
        "session_id": ["ses-s0"],
        "file_count": [2],
        "total_bytes": [30],
    })
    result = run_qc(participants, sessions, ["ses-s0", "ses-s1"])
    assert not bool(result.iloc[0]["is_complete"])
    assert result.iloc[0]["missing_sessions"] == "ses-s1"
