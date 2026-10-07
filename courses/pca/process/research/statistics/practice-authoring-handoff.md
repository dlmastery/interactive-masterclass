# Practice and limitations content handoff

7 October 2026. Authored `courses/pca/v/lesson/src/practice.json`: 26 scenes, chapter 5 has 12 and chapter 6 has 14. All fields use the current Scene contract. Every scene has a three-choice diagnostic with indexed feedback, source URL, prompt and exact event-cued spoken notes. Notes contain 100–109 whitespace-delimited words including cues. JSON syntax, fields, IDs, chapters, kinds, answer arrays, note length and TeX control characters were checked; see `practice-validation.json` for the content hash. No frontend or course.ts changes by this author. The content has not been rendered or learner-tested.

## Interaction contracts for the frontend owner

Modes describe intended figure states, not already verified implementations. Do not silently render the same generic cloud for all modes while leaving the specific notes unchanged.

| Kind/mode | Needed representation or operation |
|---|---|
| decision/metric | Same-unit task statement and explicit error criterion; choices are sufficient interaction. |
| scale/units | Change one coordinate's unit multiplier, compare covariance directions, restore. |
| scale/standardize | Compare raw and standardized geometry; distinguish centering from scaling. |
| scale/weighted-loss | Compare contributions from raw errors divided by scales; fixture uses scales 10 and 1. |
| scale/whiten | Show component-score variances before/after positive-eigenvalue rescaling. Do not use raw-feature scaling as a substitute. |
| spectrum/budget | Fixture spectrum 8,1,1; k=2 retains exactly 90%. Keep this fixture consistent with choices. |
| spectrum/validation | Separate task validation loss from reconstruction/storage tradeoff. Synthetic curves must be labeled as illustrative, not an executed benchmark. |
| code/pipeline | Training-fit and held-out-transform arrows; no invented runnable output. |
| code/frozen-transform | One new point with stored training mean/directions; formula is the unscaled case. |
| code/svd | Matrix orientation, dimensions and variance relationship; distinguish right singular directions. |
| rank/sparse | Sparse zeros becoming nonzero under explicit centering; compare objectives with uncentered SVD. |
| code/checks | Show invariant checks; opposite signs with matching reconstruction. |
| nuisance/low-variance | Long horizontal spread, small vertical label-bearing coordinate; labels revealed after geometry. |
| decision/choose-method | Task-based comparison choices. No made-up performance scores. |
| outlier/influence | Move one point; show direction/variance changes and compare with original. |
| outlier/robust | Low-rank plus sparse diagram and one-nonzero-entry ambiguity; do not imply ordinary outlier slider executes robust decomposition. |
| curve/linear-failure | Circle with two points sharing a projection; demonstrate collision. |
| curve/nonlinear | Objective comparison schematic; no implied execution of UMAP/kernel PCA/autoencoder. |
| mixture/stability | Equal-eigenvalue toggle; static formulas must remain consistent with tie state. Prompt's 5,5,1 case is a separate stated example. |
| nuisance/duplicate | Repeated feature adds repeated loss terms; distinct from adding an independent observation. |
| decision/latent-model | Descriptive versus latent versus causal claims; choice interaction is sufficient. |
| decision/seurat | Cells → selected/scaled genes → PCA scores → downstream analysis. Use a sourced schematic, not a fabricated biological result. |
| decision/dinov2 | Image patches → pretrained encoder features → PCA projection → color mapping. No claim the course ran DINOv2. |
| decision/temporal | Earlier fit window and later evaluation window; changing window is a tradeoff, not an investment recommendation. |
| live/diagnose | Native controls change a point and angle; ensure Python values and plotted data share the same state. Total may change when data changes. |
| decision/decision-final | Purpose, evidence and boundary of the result; choices challenge an overclaim. |

## New source checks for the application scenes

The [DINOv2 primary paper](https://arxiv.org/html/2304.07193v2) was read at Figure 1 and section 7.5, especially its patch-feature PCA procedure. It supports a documented modern use, not a claim that DINOv2 is the latest model. The scene separates encoder training from later PCA inspection and qualifies sign/color interpretation. No model, dataset, media asset or demo was executed or copied.

The [Seurat primary tutorial](https://satijalab.org/seurat/articles/pbmc3k_tutorial.html), compiled April 2026, supports the rare-component sensitivity example. The scene avoids claiming biological validation or importing a generic “variance equals biological signal” rule.

Read relevant primary documentation for [StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html), [TruncatedSVD](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html), [FactorAnalysis](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.FactorAnalysis.html), [KernelPCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.KernelPCA.html) and [UMAP parameters](https://umap-learn.readthedocs.io/en/latest/parameters.html). Exact installed package behavior remains the frontend/notebook implementation's responsibility. No unsupported numerical comparison is supplied.

The remaining sources and their access limits are in `source-analysis.md`. Statements based on examples are not generalized into universal winners. The final source audit should retain that distinction after visual implementation.
