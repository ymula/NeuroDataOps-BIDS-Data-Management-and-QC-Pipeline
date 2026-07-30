# NeuroDataOps: Reproducible BIDS Data Management and QC

A portfolio project demonstrating end-to-end research data management for a longitudinal, multi-site-style neuroimaging program using the public OpenNeuro dataset **ds008477**.

## Job-aligned capabilities

- BIDS-aware data inventory and metadata harmonization
- Relational SQLite research database
- Automated validation, consistency checks, and QC metrics
- Reproducible Python command-line workflows
- SLURM batch submission example for HPC
- Git/GitHub version control and CI
- FAIR-oriented documentation and provenance
- Secure-data design patterns without publishing raw data

> The raw dataset is not committed to this repository. Store it outside the repo and configure its path through `.env`.

## Architecture

```text
OpenNeuro BIDS dataset
        |
        v
01 inventory + checks
        |
        v
standardized manifests / QC tables
        |
        v
SQLite relational database
        |
        v
HTML/CSV summary deliverables
        |
        +--> SLURM batch execution
        +--> GitHub Actions tests
```

## Repository structure

```text
.
├── config/
│   └── project.yaml
├── docs/
│   ├── data_dictionary.md
│   ├── governance.md
│   └── sop.md
├── slurm/
│   └── run_pipeline.sbatch
├── src/neurodataops/
│   ├── __init__.py
│   ├── inventory.py
│   ├── database.py
│   ├── qc.py
│   └── pipeline.py
├── tests/
│   └── test_core.py
├── .github/workflows/
│   └── ci.yml
├── .env.example
├── .gitignore
├── pyproject.toml
└── requirements.txt
```

## 1. Clone the public dataset

From a folder outside this project:

```powershell
cd C:\Users\yuvas\Documents
git clone https://github.com/OpenNeuroDatasets/ds008477.git
```

OpenNeuro GitHub repositories may use DataLad/git-annex. A normal clone can contain metadata or annex pointers rather than all large imaging content. The management pipeline still inventories what is locally available; downloading all image content is optional for the metadata-focused stages.

## 2. Create the environment

```powershell
cd C:\Users\yuvas\Documents\yale-neuro-data-manager-portfolio
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Configure the dataset path

```powershell
Copy-Item .env.example .env
```

Edit `.env`:

```text
BIDS_ROOT=C:/Users/yuvas/Documents/ds008477
OUTPUT_ROOT=outputs
DATABASE_PATH=outputs/neurodataops.db
```

Use forward slashes in the Windows path.

## 4. Run the end-to-end pipeline

```powershell
python -m neurodataops.pipeline
```

Expected outputs:

- `outputs/file_inventory.csv`
- `outputs/participants_clean.csv`
- `outputs/session_inventory.csv`
- `outputs/qc_summary.csv`
- `outputs/qc_report.html`
- `outputs/neurodataops.db`
- `outputs/run_manifest.json`

## 5. Inspect the relational database

```powershell
python -c "import sqlite3; c=sqlite3.connect('outputs/neurodataops.db'); print(c.execute('SELECT group_name, COUNT(*) FROM participants GROUP BY group_name').fetchall())"
```

## 6. Run tests

```powershell
pytest
```

## 7. Run on SLURM

Edit paths and resource directives in `slurm/run_pipeline.sbatch`, then submit:

```bash
sbatch slurm/run_pipeline.sbatch
```

## 8. Publish your code to your GitHub account

Do **not** push from inside the cloned OpenNeuro dataset. Create a separate GitHub repository named:

```text
neurodataops-bids-qc
```

Then run from this project folder:

```powershell
git init
git add .
git commit -m "Initial end-to-end BIDS data management pipeline"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/neurodataops-bids-qc.git
git push -u origin main
```

## Suggested portfolio description

Built an end-to-end Python research data management platform for a longitudinal BIDS neuroimaging dataset, including metadata harmonization, relational database creation, automated QC audits, FAIR-aligned documentation, provenance manifests, GitHub CI, and SLURM-ready HPC execution.

## Privacy and compliance note

This demonstration uses a public animal dataset and does not claim HIPAA or IRB-regulated processing. The governance documents show how the same architecture should be adapted for controlled human research data using least-privilege access, approved storage, audit logs, encrypted transfer, and documented IRB/DUA requirements.
