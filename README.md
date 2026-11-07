# Vision Annotation Audit

Offline, stdlib-only COCO object-detection annotation quality checks. Detects broken references, duplicate IDs, bad image dimensions, invalid/out-of-bounds boxes, mismatched areas, duplicate boxes and empty categories. All examples are **synthetic**. No image pixels are read and no model is trained.

## Install and run
```bash
python -m pip install -e .
python -m vision_audit examples/clean.json --json-out clean-report.json --md-out clean-report.md
python -m vision_audit examples/corrupt.json --json-out corrupt-report.json --md-out corrupt-report.md
python -m unittest discover -s tests -v
```
Exit codes: 0 no errors (warnings allowed); 2 validation errors; 3 I/O/JSON error.

## Architecture
COCO JSON -> parser -> schema/reference/geometry/duplicate checks -> deterministic issue records -> JSON/Markdown reports -> CI gate.

## Limitations
This is a heuristic annotation auditor, not a COCO compliance certification or image-visualization tool. COCO `area` can represent segmentation area and differ legitimately from bbox area; mismatch is a warning. Duplicate-box warnings can be legitimate overlapping instances. Does not inspect image bytes, verify file existence, segmentations, keypoints, polygons, or near-duplicates with non-identical coordinates. Designed for offline review, not a replacement for FiftyOne, CVAT, or Datumaro.

## Hiring evidence (official employers)
- Simbe Robotics 2027 CV intern: https://jobs.lever.co/SimbeRobotics/d8e862ca-212d-4a88-af74-de400b0c6bf8
- Zoox 2027 data science intern: https://jobs.lever.co/zoox/85c6aec7-8da2-445d-9c4d-812365dbce97
- Amazon 2027 ML/automated reasoning SDE intern: https://www.amazon.jobs/en/jobs/10593521/software-development-engineer-intern-machine-learning-automated-reasoning-summer-2027
- Graphcore 2027 QA graduate: https://job-boards.greenhouse.io/graphcore/jobs/8894574002

## Tests
Run `python -m unittest discover -s tests -v`. See `docs/verification.md` for observed results.
