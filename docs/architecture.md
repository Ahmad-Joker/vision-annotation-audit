# Architecture and decisions

No external runtime dependency. `core.audit()` is pure and deterministic. The CLI handles JSON input, output and exit codes. Tests exercise each failure family and the sample command. Input files are never modified. Reports preserve issue location and severity for triage. The quality gate fails on structural/geometric errors, not subjective warnings. Future: optional image existence checks, segmentation validation, IoU-based suspicious duplicates, dataset stratification reports and HTML gallery.
