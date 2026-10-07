# PCA, from the ground up

A **54-slide interactive masterclass** built as the native Reveal.js slide view of a marimo-studio notebook. It assumes arithmetic and introduces the required statistics and linear algebra immediately before use.

## Open the masterclass

- Presentation: <http://localhost:2719/>
- Notebook and Studio Preview: <http://localhost:2718/studio/lesson/>

These are local servers. To relaunch later, open PowerShell in this project folder:

```powershell
.\Start-Lesson.ps1
```

For the editable notebook and Studio view:

```powershell
.\Start-Lesson.ps1 -Edit -Port 2718
```

The launcher uses `uv` and pinned isolated dependencies. Keep the notebook, `v/lesson`, manifests, and lockfiles together. A short extraction path helps on Windows. KaTeX styling and fonts load from pinned jsDelivr URLs on first use, so network access is needed then.

## How the lesson teaches

The main thread follows four invented people taking two short tests. The same person, table row, plotted point, covariance contribution, score, and reconstructed observation are connected throughout. The centered example is `(2,1), (1,2), (−1,−2), (−2,−1)`; its covariance matrix is `[[10,8],[8,10]]/3`, and PC1 retains 90% of its total variance.

The foundations are interleaved with the PCA steps they unlock:

1. **Deviations and spread:** vectors and coordinates, mean, summation notation, centering, signs, squares, variance, and the sample denominator.
2. **Covariance and matrices:** individual cross-products, cancellation, diagonal/off-diagonal entries, matrix shapes, transpose, and multiplication.
3. **Projection and variance:** weighted scores, shadows, dot products, trigonometric unit directions, the score-variance derivation, and normalization.
4. **Best axes:** matrix-vector multiplication, eigenvectors/eigenvalues, identity and determinant, a global maximum argument, perpendicular directions, PC2, and explained variance.
5. **Reconstruction:** adding the mean back, residuals, the Pythagorean identity, and choosing a component count against a budget.
6. **Modeling choices:** units, standard deviation, correlation, standardized values, outliers, circular data, and variance unrelated to a category.
7. **Transfer:** a rotated cloud, live edits to notebook data, optional SVD/calculus connections, and a fresh assessment.

See **TEACHING-MAP.md** for every slide's explanation, action, and connection.

## Interactions

- Select a person in the table or illustration; the same selection carries into later experiments.
- Rotate a projection using the orange handle or the keyboard-accessible angle slider. Scores, projections, squared distances, and variance are notebook-computed frames.
- Click a covariance entry to inspect the products behind it.
- Change covariance patterns, ruler length, component count, scale, and standardization.
- Step through individual equations with plain-language explanations.
- Use the native notebook playground to change person D's actual scores. Python rebuilds the mean, covariance, eigensystem, and projection frames.
- Submit an answer and reasoning before opening a practice explanation.
- The final assessment asks one fresh question at a time and stops after a miss or admitted guess. A separate action opens help; another starts an alternate-number check.
- Save the learner's original attempts and reasons as JSON. No account, upload, external grading service, or automatic reminder is involved. The record is held in memory, so save it before reloading.

Slides can be explored freely; navigating to the end is not treated as a learning pass. Numerical answers are checked automatically. Written reasoning is deliberately labeled as requiring tutor or self-review, rather than being falsely presented as AI-graded mastery.

## Teaching guidance used

The user supplied `ai-learn-skills.zip` and explanatory notes. This revision draws on its `ai-learn-loop`, `learn-mapmaker`, `learn-calibrator`, `learn-explainer`, and `learn-examiner` guidance: a concrete pass test, a dependency map, an appropriate starting level, production before feedback, separate explanation and examination, and a fresh retry after a miss. The pack was read as design guidance; it was not installed globally. This is an interactive teaching artifact, not a complete implementation of every role in that pack or an autonomous LLM tutor.

## Where marimo-studio is doing the work

The notebook owns the mathematical model, datasets, teaching text, native data controls, and NumPy calculations. The slide view consumes `pca_lab`, `masterclass`, and `sandbox_lab` through explicit `mo-value` projections. `marimo-cell` embeds the notebook's native playground controls.

For smooth exploration, Python calculates 181 angle frames for each interactive cloud. The browser selects a frame while the learner drags, with no server round trip per pixel. Changing the native notebook inputs recomputes the sandbox frames in Python. These are actual model outputs, not independently reimplemented front-end PCA or canned screenshots.

The native Reveal.js deck supplies slide navigation. React/SVG supplies linked illustrations, local selection, proof steps, and learning interactions. A narrow layout stacks the explanation and experiment; longer panels scroll. The learning map, term explanations, slide picker, and attempt record remain available throughout.

## Reuse for another topic

- `pca_lesson.py`: all notebook computation and teaching data. New `masterclass_*` cells define this revision; earlier derivation cells remain as reference material.
- `v/lesson/src/Masterclass.tsx`: course shell, navigation, map, glossary, and learning record.
- `v/lesson/src/LabComponents.tsx`: linked diagrams, tables, matrices, sliders, proof steps, and practice components.
- `v/lesson/src/CoreLabs.tsx`: PCA experiments.
- `v/lesson/src/BridgeLabs.tsx`: prerequisites introduced as needed.
- `v/lesson/src/Assessment.tsx`: attempt/stop/help/retry assessment states.
- `v/lesson/src/masterclass.css`: presentation and narrow-screen layouts.

For another subject, keep the course shell and learning interactions, replace the notebook model and examples, and place prerequisite bridges directly before the operations that require them. This is a reusable pattern, not yet a general course generator.

## Verification and delivery limits

The mathematical checks cover the exact covariance and eigenvalues, all 543 angle frames across the baseline, transfer, and default sandbox clouds, unit-length directions, orthogonal projections, variance-plus-loss conservation, and complete reconstruction. All projected values stay below Studio's 1 MB per-value limit.

The supported delivery here is the live local Python runtime. WASM, prepared static export, and public hosting have not been verified. Studio 0.2.3 on this Windows installation can report temporary-directory cleanup warnings after successful builds; build JSON is checked for success and source revision.

Tested dependencies: marimo-studio 0.2.3, marimo 0.25.0, NumPy 2.5.3, and Deno 2.9.7.

Official references: [Studio overview](https://marimo-team.github.io/marimo-studio/), [native Reveal.js starter](https://marimo-team.github.io/marimo-studio/guide/frontend-options#reveal-js-slides), [notebook projections](https://marimo-team.github.io/marimo-studio/reference/projections), and [runtime choices](https://marimo-team.github.io/marimo-studio/guide/run-and-share).
