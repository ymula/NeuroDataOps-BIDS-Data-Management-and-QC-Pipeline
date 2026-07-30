# Data Dictionary

## participants

| Field | Description |
|---|---|
| participant_id | BIDS-compatible pseudonymous subject identifier |
| group_name | Experimental group from participant metadata |
| sex | Biological sex recorded in source metadata |
| species | Scientific species name |
| strain | Animal strain |

## sessions

| Field | Description |
|---|---|
| participant_id | Foreign key to participants |
| session_id | Longitudinal visit/timepoint |
| file_count | Number of files inventoried for the subject/session |
| total_bytes | Total locally available bytes |

## files

| Field | Description |
|---|---|
| relative_path | Dataset-relative file location |
| participant_id | Parsed BIDS subject identifier |
| session_id | Parsed BIDS session identifier |
| suffix | File extension(s) |
| size_bytes | File size |
| sha256 | Integrity checksum for files up to 100 MB |
