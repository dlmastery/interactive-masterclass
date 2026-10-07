# Pilot source review — first pass

7 October 2026. Inspected the then-current six scenes in `courses/pca/v/lesson/src/course.ts`, `Visuals.tsx`, and the referenced arithmetic in `math.ts`. No code edits. Rendered evidence, runtime, accessibility interaction and actual learner performance are still pending. This reviewer authored the geometry route, so this is author-informed technical and continuity review, not a truly cold novice test.

## Findings

### P1 — LaTeX literals are altered before KaTeX receives them

`course.ts` global-pilot formula and `Visuals.tsx` Covariance/Mixture/Eigen formulas contain single source backslashes in ordinary JavaScript strings/template literals. Literal `\frac`, `\tfrac`, `\begin` and `\quad` can become control characters or lose the slash before rendering. Source-character inspection confirmed single-backslash runs in these formulas; matrix separators contain only two source backslashes. `throwOnError:false` makes a silent malformed formula especially plausible. Use `String.raw` templates or correctly doubled source escapes, then inspect actual equations in every pilot state. This must be repaired before screenshots can support a math-layout claim.

### P2 — The hardest bridge is absent from the actual pilot sequence

The six-scene array jumps from `store` to `cov-pilot` to `global-pilot`. The global notes refer to a stationary candidate, but no preceding scene defines stationarity or obtains `Cw=lambda w`. `Eigen` is implemented but no scene selects it. The covariance scene shows a squared score and the final matrix, but does not show the summed/normalized identity `var(z)=wᵀCw`. Therefore the current pilot cannot test the claimed covariance-to-eigenvector bridge; an expert can fill it in from prior knowledge.

Minimal repair: add immediate context showing the centered sample variance as a sum of squared scores; collect its coefficients into C; show the constrained direction condition with the existing Eigen visualization; distinguish the minor-axis stationary direction; then enter the global bound. If these are deliberately isolated slices, each slice still needs this declared context instead of a spoken reference to unseen material.

### P2 — The global proof's cross-term warrant needs the eigenvector relation

The notes say cross terms vanish because the basis is perpendicular. In a quadratic form, orthogonality alone does not remove an arbitrary matrix's cross terms. The needed bridge is `q_iᵀCq_j=lambda_j q_iᵀq_j`, then orthonormality removes i≠j. Show this operation or say both reasons: these are eigenvectors of C and an orthonormal basis. The covariance matrix here has eigenvalues 6 and 2/3, so the numerical bound is correct; the issue is the missing general warrant.

### P2 — The slider displays an eigenvalue mixture without reconstructing its direction

The mixture control uses squared weights and correctly notes square roots/sign freedom. However, its display contains two eigenvalue cards rather than geometric q-directions or the resulting w. The transition from a rotated ruler to weights may thus feel like a new unrelated numerical exercise. Show at least one concrete choice, such as equal weights yielding `(q1+q2)/sqrt(2)`, beside the same ruler representation. The caption can preserve the other sign choices. This is a teaching hypothesis to test in rendered review, not a requirement for decorative animation.

## Correctness checks and useful details

- The four-point fixture has mean (6,6), covariance `[[10,8],[8,10]]/3`, eigenvalues 6 and 2/3, and leading direction 45 degrees. The code's sample-variance and normalized-residual denominators match.
- At 45 degrees, A and B have equal scores but different residuals, so the `store` question has a legitimate many-to-one witness.
- Reflection `y -> 12-y` preserves each marginal variance and reverses covariance. The flip control tests a meaningful insufficiency of separate variance summaries.
- Mixture tie state correctly permits every direction in this two-dimensional space; changing signs does not change variance. The final course should also distinguish a repeated top eigenvalue from a repeated eigenvalue at another index.
- The Eigen derivative is with respect to radians while the slider is labeled degrees; the caption explicitly says so. Its sign test is valid for finding a local improving direction.
- The plot labels raw mean as (6,6) unconditionally. It is correct for the current fixed raw scenes; if moved-point data later enters a raw plot, use the computed mean. The current live lab uses the centered view, so this is a future interface hazard rather than a reproduced current failure.

## Next evidence needed

After formula repair, inspect the covariance matrix, the mixed term, the unequal/equal eigenvalue formulas, and the derivative in actual rendered states. Then verify the covariance prediction/reveal, angle presets, point selection, reset, native Python control update, notes and notebook return. Do not call this current pilot a passed inference test until it contains the missing context and reviewers complete held-out reasoning tasks with visible scene warrants.
