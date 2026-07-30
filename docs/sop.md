# Standard Operating Procedure

## Dataset intake

1. Confirm authorization, scope, expected subjects, sessions, and modalities.
2. Record source, transfer method, date, sender, recipient, and checksum.
3. Place raw data in an immutable intake directory.
4. Run structural validation and inventory.
5. Reconcile participants and sessions against the delivery manifest.
6. Quarantine unexpected, duplicate, corrupted, or unauthorized files.
7. Document discrepancies and resolution.

## Routine QC

1. Run the pipeline after every delivery.
2. Review missing participant/session combinations.
3. Review zero-byte and unexpectedly small files.
4. Compare counts with the prior run.
5. Resolve discrepancies with the contributing site.
6. Approve a versioned analysis release.
7. Archive the QC report and provenance manifest.

## Change control

All scripts, schemas, and documentation changes require a Git commit. Material changes should use a pull request and reviewer approval.
