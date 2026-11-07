# Verification evidence — 2026-11-07

## Local verification
- Runtime: Python 3.13 in a Linux container. Source is a `src/` package layout; invoke `python -m pip install -e .` first or set `PYTHONPATH=src` for direct execution without installation.
- `PYTHONPATH=src python -m unittest discover -s tests -v`: **20 tests passed**.
- `python -m compileall -q src tests`: **passed**.
- `PYTHONPATH=src python -m vision_audit examples/clean.json`: **exit 0**, 0 errors and 0 warnings.
- `PYTHONPATH=src python -m vision_audit examples/corrupt.json`: **exit 2**, 8 errors and 3 warnings.
- All sample annotations are synthetic; results are not a measured real-world quality improvement.

## GitHub publication and CI
- Repository: https://github.com/Ahmad-Joker/vision-annotation-audit
- Feature branch: `feat/vision-annotation-audit-mvp` (based on repository `main`, which contained an initial README commit).
- Pull request: https://github.com/Ahmad-Joker/vision-annotation-audit/pull/1 — open and unmerged.
- Verified source commit: `93e23725269b10602dc7ebf350e8f6d7cad2d0ce`.
- Remote Python CI workflow run: https://github.com/Ahmad-Joker/vision-annotation-audit/actions/runs/42370345652 — **success**.
- The explanatory PDF has been revised after publication to include the verified GitHub links and CI evidence.
- Subsequent documentation commits can create additional CI runs; inspect the PR checks for the current head.

## Limitations
- No Docker execution or public deployment.
- No real-world COCO dataset benchmarks or image-pixel integrity verification.
- Heuristic checks only; the COCO `area` field may legitimately describe segmentation area instead of bounding-box area.
