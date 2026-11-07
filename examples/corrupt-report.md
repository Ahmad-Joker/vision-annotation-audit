# Vision Annotation Audit

Images: 2 | Annotations: 3 | Categories: 2
Errors: 8 | Warnings: 3

| Severity | Code | Location | Description |
|---|---|---|---|
| error | NEGATIVE_ORIGIN | annotations[0] | bbox origin cannot be negative |
| error | NONPOSITIVE_BBOX | annotations[0] | bbox width and height must be positive |
| error | UNKNOWN_CATEGORY | annotations[0] | Unknown category_id 99 |
| error | UNKNOWN_IMAGE | annotations[0] | Unknown image_id 99 |
| warning | AREA_MISMATCH | annotations[1] | area differs from bbox area (may be valid for segmentation) |
| error | DUPLICATE_ID | annotations[1] | Duplicate id 1 |
| error | OUT_OF_BOUNDS | annotations[1] | bbox extends outside image |
| warning | DUPLICATE_BOX | annotations[2] | Same image/category/bbox as annotations[1] |
| error | OUT_OF_BOUNDS | annotations[2] | bbox extends outside image |
| warning | EMPTY_CATEGORY | categories[1] | No annotations for this category |
| error | DUPLICATE_ID | images[1] | Duplicate id 1 |
