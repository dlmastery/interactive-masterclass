# Original PCA lesson — recovered source

This folder preserves the original **14-slide lesson**, before the 54-slide and 64-slide expansions. It uses the light background, large point-cloud illustration, two-column composition, and native notebook controls shown in `../../pca-preview.png`.

**Status: recovered source only.** No native build, live execution, or browser comparison has been performed on this recovered package. It is not presented as a tested runnable release.

## What was recovered

- `v/lesson/src/Lesson.tsx`: the full original 14-slide component from native Studio's Deno cache. Only ten injected `data-marimo-studio-site` attributes were removed. Fresh Studio builds must generate their own mount IDs.
- `v/lesson/src/LessonText.tsx`, `main.tsx`, and `lib/use-marimo-value.ts`: exact source-map content from the same original build candidate.
- `v/lesson/src/lesson.css`: surviving original stylesheet, copied unchanged.
- `pca_lesson.py`: the original 32 notebook cells, through `slide_content`, extracted from the notebook backup. Later masterclass cells were removed. A standard `app.run()` entry point was retained.
- Studio declarations, HTML, view configuration, and pinned dependency files were copied from the existing project. These provide scaffolding; this is not a complete historical repository snapshot.

The recovered component was cached on 2026-10-03 at 23:57:56 and 23:58:05, before the saved original screenshot. The source uses a deterministic 48-point cloud, native correlation and projection controls, covariance calculations, a four-point worked example, reconstruction, units, SVD, and a quiz.

`recovery-manifest.json` records exact source locations, transformations, SHA-256 values, and verification status. The original build-stage component hash is `cd4aee2df30cc8863dd9b92f4af7e02f9dd2a3469b50252f55ce86f9d0ea071f`.

## Before presenting this version

1. Build this notebook's own `lesson` view with native marimo-studio, using the pinned dependencies.
2. Validate all notebook bindings and run it on separate ports from the active course.
3. Test correlation, centering, angle, component count, units, and quiz controls.
4. Compare slide 4 at angle 45 degrees and correlation 0.75 with the original screenshot. Expected retained variance: 87.5%. Expected displayed loss: 1.00.

Only Python syntax, the 32-cell extraction, the 14-slide count, and file hashes were checked during recovery. This package does not replace or change the active course. The original 14-slide sequence is an earlier baseline; it does not satisfy the later 50-plus-slide masterclass request on its own.
