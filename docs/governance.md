# Research Data Governance Plan

## Demonstration scope

This portfolio uses a public animal neuroimaging dataset. It contains no human PHI and is not represented as HIPAA-regulated work.

## Controlled-data adaptation

For human high-risk research data:

1. Store data only in institution-approved encrypted systems.
2. Enforce role-based, least-privilege access.
3. Separate identifiers from research IDs and maintain the linkage key in a restricted location.
4. Confirm IRB approval and DUA permissions before ingestion, use, or transfer.
5. Use approved encrypted transfer mechanisms; never email research datasets.
6. Log data receipt, sender, date, checksum, authorization, and disposition.
7. Keep raw data immutable; write transformations to versioned derived-data locations.
8. Do not commit data, credentials, tokens, linkage files, or PHI to GitHub.
9. Apply retention and destruction requirements from the IRB/DUA.
10. Perform periodic access reviews and incident-response exercises.

## FAIR mapping

- Findable: accession, searchable manifests, standardized IDs
- Accessible: documented authorized access pathway
- Interoperable: BIDS naming, TSV/JSON metadata, relational schema
- Reusable: provenance, data dictionary, code versioning, QC reports
