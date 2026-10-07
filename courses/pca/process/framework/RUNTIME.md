# PCA notebook runtime

Implemented 2026-10-07 after the read-only framework investigation was expanded to authorize a new runtime. All files here belong to `courses/pca/`; historical output files remain untouched.

## Start and return

Prerequisites: `uv` on PATH and network access on a machine where the pinned packages are not cached. The launcher selects Python 3.12 because NumPy 2.5.3 requires it. It uses normal uv dependency resolution/cache reuse and contains no machine-specific cache path. The frontend view and frozen Deno lockfile must exist before the presentation build can succeed.

From `courses/pca/`, open a PowerShell terminal:

```powershell
./Start-Lesson.ps1 -Edit
```

This starts the native marimo Studio editor on port 2728, with file watching. Use the browser URL opened by marimo; the native workspace route is `http://localhost:2728/studio/lesson/`. The notebook surface remains editable. The `lesson` view uses the same notebook runtime when viewed in this shell.

For a separate full-page presentation, keep the first terminal running and use a second:

```powershell
./Start-Lesson.ps1
```

This builds the view for production, then serves native Studio on `http://localhost:2729/lesson/`. Its outer-page **Back to editable notebook** link points to `http://localhost:2728/studio/lesson/`. The editor must already be running and authenticated in the browser if marimo requires a token. Native controls on the presentation recompute in its own Python session. The separate editor and presentation processes do not share in-memory control state.

Use `-EditorPort 2738` in both commands and `-Port 2739` on the presentation command to choose different ports. The launcher checks for a conflict and reports it; it does not terminate or reuse an unknown server. Stop only the terminal/process you started with Ctrl+C. Start commands have been syntax-checked but not launched by the runtime implementation agent. Clean-start and actual browser return acceptance are pending the parent pilot.

After Python source edits, the editor's `--watch` reloads its notebook. A standalone run-mode process requires a deliberate restart for source changes. For frontend source edits, rebuild the production view and verify the reported revision. A refresh displaying a prior artifact is not evidence that a failed build succeeded.

## Projection contract

Both projected values are finite, JSON-compatible Python dictionaries. All points are arrays `[x,y]` and rows are observations. No angle-frame array is projected.

`pca_data`:

```text
schema: 1
units: "cm"
covarianceConvention: text
base: PcaCase
cases: {isotropic: PcaCase, rankOne: PcaCase, outlier: PcaCase, scaled: PcaCase}

PcaCase:
  n, denominator
  raw: number[N][2]
  mean: number[2]
  points: number[N][2]            # centered raw data
  cov: number[2][2]              # X.T @ X / (n-1)
  eigenvalues: number[2]         # descending
  eigenvectors: number[2][2]     # eigenvectors are columns
  axes: number[2][2]             # eigenvectors are rows
  scores: number[N][2]           # X @ eigenvectors
  reconstruction: number[N][2]   # centered, first PC only
  rawReconstruction: number[N][2]
  totalVariance: number
  explainedRatio: number[2] | null  # null when totalVariance is zero
  singularValues: number[2]
  svd: {u: number[N][2], s: number[2], vt: number[2][2]}
```

`pca_live`:

```text
angleDeg, outlier, n, denominator
raw, mean, points, cov                 # same meaning as above
w: number[2]                          # unit vector at angleDeg
scores: number[N]                     # X @ w; one score per row
reconstruction: number[N][2]           # outer(scores,w), centered
rawReconstruction: number[N][2]        # add mean
residuals: number[N][2]                # points - reconstruction
variance: number                      # sum(scores**2)/(n-1)
loss: number                          # sum(residuals**2)/(n-1)
totalVariance, eigenvalues, axes
```

The named cell `sandbox_controls` displays `angle_control` (0–180 degrees, step 1, default 45) and `outlier_control` (0–8 cm, step 0.5, default 0). The latter adds to observation D's x coordinate before recomputing the mean and covariance. Mount it using:

```tsx
<marimo-cell name="sandbox_controls" />
```

The reactive `live_model` cell depends on both controls' `.value` and defines `pca_live`. Native Studio projection hosts are `mo-value="pca_data"` and `mo-value="pca_live"`. Use the supplied hook so the view responds to updates and errors. Changing a custom browser control may calculate geometry from this compact data, but label that behavior as a browser calculation rather than Python recomputation.

Variance and loss use the same denominator, n−1; `variance + loss = totalVariance`. A reconstructed point is centered until its mean is added back. `pca_data.base` is always the fixed example. The two native controls change `pca_live`, not `pca_data.base`.

## Verification performed

The complete cached environment used for evidence is recorded in `REPORT.md`. Equivalent portable test command:

```powershell
uv run --python 3.12 --no-project --with 'marimo-studio[deno]==0.2.3' --with 'numpy==2.5.3' python -m unittest test_pca_math test_navigation -v
uvx --python 3.12 --with 'marimo-studio[deno]==0.2.3' marimo check pca_lesson.py
```

- Eight numerical tests passed. They check the hand-calculated baseline, covariance/eigendecomposition, SVD reconstruction, every native control combination, the eigenvalue global bound, orthogonal residuals, translation and sign invariance, degeneracy, and invalid inputs.
- Every offered angle/outlier combination was checked: 181 × 17 = 3,077 states. The largest combined serialized `pca_data` and `pca_live` response was **7,177 bytes**, including a simple values/errors envelope. The bound is below the assigned 100,000 bytes and the installed transport's 1,000,000-byte aggregate limit. Additional projections need their own measurement.
- Isolated `pca_lesson.app.run()` succeeded: 10 displayed outputs; exports included both controls and both projected models. Native defaults were 45 and 0; variance was 6.000000000000001 and loss 0.6666666666666666.
- `marimo check pca_lesson.py` passed. Studio's static notebook inventory finds `sandbox_controls` with `has_output_expression=True`.
- Four ASGI composition tests passed: return link, existing CSP nonce and iframe sandbox preservation, root-route link, asset passthrough, error passthrough, and unexpected compression passthrough.
- PowerShell parser found no launcher syntax errors.

This is numerical/source/isolated-execution evidence. It does not establish a real pointer-driven native-control update, final artifact build, actual browser navigation, notes layout, offline export, or learner understanding. Those are separate pilot checks.
