# PCA · from picture to proof

A 64-slide interactive course in native marimo-studio, with 79 equation steps. The 6 October 2026 repair restores the first version's light background, large geometric pictures, and readable two-column layout while retaining the full derivation.

## Open the course

- [Interactive slides](http://localhost:2719/lesson/)
- [Notebook and Studio](http://localhost:2718/studio/lesson/) — open this address in **Chrome or Edge** for authoring. Chrome was verified with the notebook, preview, and code-mode session running.
- [Teaching strategy and storyboard](PCA-TEACHING-PLAN.html)
- [Original 14-slide source recovery](original-first-version/README.md)

The in-app browser can show the slides, but native notebook authoring fails there. Its sandbox blocks access to `navigator.serviceWorker`; the browser reports a `SecurityError`. Open the Studio address in an external browser instead. No CSP or sandbox protection was weakened.

Inside Studio, enable **Show Notebook** when that checkbox is present. In a narrow layout, use **Visible surface** to choose **Notebook** or **Preview**. The notebook contains the Python model, live data controls, results, and the complete lesson text and derivation.

To restart after closing the servers, open two PowerShell terminals in this folder:

```powershell
# First terminal: notebook editor on port 2718
.\Start-Lesson.ps1 -Edit
```

```powershell
# Second terminal: slides on port 2719
.\Start-Lesson.ps1
```

Keep both processes running. The launchers require `uv` and use pinned packages. Keep the notebook, view source, and lockfile together. KaTeX styles and fonts load from jsDelivr on first use.

## The teaching route

| Slides | Question |
|---|---|
| 1–8 | What does PCA do? |
| 9–20 | How do we measure a view? |
| 21–30 | Why does covariance appear? |
| 31–45 | Why do eigenvectors solve it? |
| 46–56 | What can we keep and recover? |
| 57–64 | When does the result help? |

The opening gives the picture a concrete purpose: store one number for each marker, recover its position, and measure the gap. The shared example uses A(8,7), B(7,8), C(5,4), and D(4,5), in centimeters. Its mean is (6,6), covariance is [[10,8],[8,10]]/3, and eigenvalues are 6 and 2/3. Keeping PC1 preserves 90% of squared spread; this is not a measure of prediction accuracy.

The repair adds four linked teaching mechanisms:

- **Compression and recovery:** connect each marker, its one stored score, recovered position, and error. Move across an axis to see positions that share one score.
- **Covariance calculation:** follow a row of Xcᵀ and a column of Xc through paired products, an accumulating sum, division by three, and the destination matrix entry.
- **Stationary directions:** compare the gradient with the circle's tangent. Both the maximum and minimum have zero turning slope; a finite turn distinguishes their behavior.
- **Global maximum:** express a direction in the signed eigenvector basis. Its squared weights give a weighted eigenvalue average bounded by 6, reached at PC1.

The remaining route derives reconstruction, the minimum-error identity, multiple components, and SVD, then tests units, outliers, new observations, and limits. **Math at this step**, **Symbols**, and **Course route** provide local help and direct navigation.

Learner inputs and proof/scene state now survive navigation away from a slide and back during the same page session. **Reloading resets that state.** There is no persistent learner record, and written explanations still need human review.

## Source and recovery

`pca_lesson.py` owns the mathematics, data, lesson prose, and native controls. `course-v2.json` is its reviewable content snapshot. The view uses `PcaCourse.tsx`, `PcaScenes.tsx`, and `pca.css` under `v/lesson/src`. Six named projections carry Python results into the native view; slide 61 embeds actual marimo controls.

`serve_lesson.py` wraps Studio's native ASGI application to put notebook navigation in the outer page. The presentation keeps Studio's original sandbox.

`original-first-version/` preserves the recovered 14-slide source, original stylesheet and renderer, and 32 original notebook cells. Its manifest records source-map provenance and file hashes. That recovery package has not been separately built or run; it does not replace this 64-slide course.

## Checks and limits · 6 October 2026

- Production build passed.
- All 64 slides passed browser navigation, math-rendering, and input-pointer checks at the actual 870×668 viewport.
- Interaction checks passed for covariance 8÷3; zero slope at both extrema; finite 3° turns of approximately −0.0146 variance at the maximum and +0.0146 at the minimum; signed basis reversal; the upper bound 6; and state retained across slide navigation.
- Numerical checks passed for 1,629 projection frames and 2,880 additional direction cases. The combined projection payload is 946,805 bytes.
- Native Studio runtime validation passed with no issues: all 10 notebook cells parsed, the embedded native cell completed, and all six projected values resolved.

The prose uses short sentences and consistent mathematical terms. The copy pass checked all 64 claims/actions and 79 equation reasons; 394 slide-copy sentences met the simple 20/25-word limits. This does **not** establish 80% ASD-STE100 vocabulary or meaning compliance. No learner mastery or teaching-effectiveness claim follows from software checks.

Supported delivery is a local Python server. Static export, WASM, public hosting, and offline fonts have not been verified. Studio may report a temporary-directory cleanup warning on Windows after a successful build; build and runtime results are assessed separately.

The teaching sequence draws on the transcripts of [Luis Serrano](https://www.youtube.com/watch?v=g-Hb26agBFg), [StatQuest](https://www.youtube.com/watch?v=FgakZw6K1QQ), and [Shlens's PCA tutorial](https://arxiv.org/abs/1404.1100). Scenes and prose are original. The user's AI Learn Loop guidance informed prediction, calculation, explanation, and feedback.

Pinned environment: marimo-studio 0.2.3, marimo 0.25.0, NumPy 2.5.3, Deno 2.9.7.
