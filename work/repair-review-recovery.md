# Original PCA recovery review

The original 14-slide frontend is recoverable from native Studio's Deno source-map cache. This is recovered source, not a recreation from the screenshot. No active lesson files, server, or browser were changed by this investigation.

## Recoverable pieces

- `work/recovered-original/Lesson-cd4aee2df30c.tsx`: complete 14-slide component, recovered from inline `sourcesContent` in cached `Lesson.tsx.js`. SHA-256 of recovered bytes: `cd4aee2df30cc8863dd9b92f4af7e02f9dd2a3469b50252f55ce86f9d0ea071f`.
- `work/recovered-original/manifest.json`: all candidate cache paths, modification times, source hashes, and counts. The matching candidate existed by 2026-10-03 23:57:56, before the 23:59 original screenshot.
- `outputs/pca-studio/v/lesson/src/lesson.css`: original light/cream/teal stylesheet, last modified 2026-10-03 23:55:28, 9,212 bytes. Includes responsive layout and projected KaTeX proof controls.
- `outputs/pca-studio/v/lesson/src/LessonText.tsx`: original notebook-owned prose/KaTeX renderer plus `StepProof`.
- `outputs/pca-studio/archive-v1/pca_lesson-before-cleanup.py`: original notebook cells are still present at the start. Keep through `slide_content` (before the decorator for `masterclass_model` around line 640), then retain `if __name__ == "__main__": app.run()`. These cells hold the 48-point cloud, correlation, centering, angle, retained-dimension and units controls, formulas, and quiz.
- Current `deno.json`, `deno.lock`, `marimo-studio.d.ts`, `lib/use-marimo-value.ts`, `index.html`, and `view.toml` provide the pinned native Studio scaffolding. Set `main.tsx` to import the recovered component and `lesson.css`.

## Which version is which

1. **14 slides, original:** headline “How much can one number tell us?”, 48-point cloud, cream background, broad plot next to text, native notebook controls. `outputs/pca-preview.png` shows slide 4/14. The recovered component includes this exact slide structure and wording.
2. **54 slides, prerequisite-heavy expansion:** `archive-v1/Masterclass.tsx`, `CoreLabs.tsx`, `BridgeLabs.tsx`, `Assessment.tsx`, and `masterclass.css`. The directory name `archive-v1` does **not** mean this is the original 14-slide frontend.
3. **64 slides, current:** `PcaCourse.tsx`, `PcaScenes.tsx`, `pca.css`. The current source ZIP also points to this version. Current `.artifacts/revisions/` retains only two builds of this version; changing a publication pointer cannot restore the original.

Three unique full-size cached `Lesson.tsx` versions were found. `90182957b033…` is the earlier native-math-cell form; `695f66a6d749…` uses the improved projected KaTeX text; `cd4aee2df30c…` additionally reads the center from `d.mean` instead of fixed `[5,3]`. All have 14 slides. Use the last variant.

## Minimum safe recovery

1. Preserve the current 64-slide notebook and view before mutation. Do not call the 54-slide archive the original.
2. Create a separate comparison/recovery notebook and view from the original cells and recovered component. Retain native Studio, its bridge, and the same pinned dependencies.
3. Remove recovered `data-marimo-studio-site="site-…"` attributes. They were injected into Studio's build-stage source; fresh builds must generate their own mount IDs. Keep `mo-value`, `<marimo-cell name=…>`, and the ordinary lens metadata.
4. Import only `lesson.css` for this view. Do not include `pca.css` or `masterclass.css`. Do not leave the unrelated course components in the new view root: Studio scans source files for mounts even when imports are unused.
5. Build development and production profiles, validate native bindings, and exercise the correlation, angle, centering, dimensions, units, and quiz controls. Compare slide 4 at 45°, rho=0.75 to the screenshot (87.5% variance retained; loss 1.00).

## Limits

The recovered TSX is exact build-stage source, including injected mount metadata, not a complete historical Git checkout. The original CSS and notebook cells survive separately. The native builds must be regenerated, and no reconstructed original has been executed or visually verified in this read-only review. Restoring the 14-slide baseline recovers the earlier design; it does not by itself meet the later 50+ slide masterclass requirement.

## Durable package created after the forensic review

At the parent's request, a source-only recovery package now exists at `outputs/pca-studio/original-first-version/`. It contains the cleaned original 14-slide component, original source-map main entry, renderer and bridge, original stylesheet, pinned scaffolding, the first 32 notebook cells, and provenance notes. Only ten injected mount IDs were removed from the recovered lesson component. No active source or server was changed.

- Clean component SHA-256: `475b2a783ea753533d7da0cb789fdbe1284989e7486f7a22b15d66fd5f7f66ef`.
- Recovered notebook SHA-256: `5963c9033ea4928f2c1b972ee6d702969b6eb5d87cc5a70f8486076cb855f9dd`.
- Full per-file hashes and origins: `outputs/pca-studio/original-first-version/recovery-manifest.json`.
- Notebook scratch copy: `work/recovered-original/pca_lesson.py`.

The package has not been built or run. Python AST parsing and extraction counts passed; these are source integrity checks only.
