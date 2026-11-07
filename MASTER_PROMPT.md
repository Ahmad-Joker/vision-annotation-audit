# MASTER PROMPT — Vision Annotation Audit

Build a free, offline COCO object-detection annotation quality auditor for students, CV engineers, and dataset curators. Ground the project in 2026-27 CV internship requirements for dataset curation, failure analysis, reproducible Python tools and testing. Scope: COCO JSON (images, categories, annotations), no image pixel loading, no model training, no cloud. Validate schema, duplicate IDs, broken image/category references, invalid bbox dimensions or boundaries, segmentation omission is not an error, area disagreement, category imbalance, and near-duplicate annotation boxes per image/category. Output deterministic JSON and human-readable Markdown; nonzero exit on errors. Include CLI, fixture data, stdlib-only package, pytest-compatible unittest tests, CI, README, architecture, limitations, and explanatory PDF. Use synthetic fixtures, never claim real dataset performance. Implement -> test -> inspect -> fix. Acceptance: clean sample exits zero; corrupt sample flags at least six issues; unit tests and compile succeed; reproducible from fresh directory. GitHub: dedicated Ahmad-Joker/vision-annotation-audit repo, feature branch feat/vision-annotation-audit-mvp, PR against main, no merge. If repository creation is unsupported, preserve complete ZIP/PDF and report the blocker honestly.

## Architecture
COCO JSON -> parser -> structural and geometric validators -> issue records -> JSON / Markdown reporters -> CLI exit status.

## Error cases
Unreadable file, malformed JSON, wrong root types, missing required records, duplicate identifiers, missing referenced images/categories, zero/negative/outside-image boxes, suspicious area discrepancies, duplicated boxes, empty category populations. No network or credentials. Deterministic ordering and configurable tolerance.

## Research
- https://jobs.lever.co/SimbeRobotics/d8e862ca-212d-4a88-af74-de400b0c6bf8
- https://jobs.lever.co/zoox/85c6aec7-8da2-445d-9c4d-812365dbce97
- https://www.amazon.jobs/en/jobs/10593521/software-development-engineer-intern-machine-learning-automated-reasoning-summer-2027
- https://job-boards.greenhouse.io/graphcore/jobs/8894574002
