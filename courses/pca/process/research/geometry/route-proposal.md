# Proposed route: one coordinate, least regret

Status: independent research proposal, not an authored course or executed pilot. Date: 2026-10-07.

## Central question and running case

Suppose a tracker records the horizontal and vertical location of a moving point. We may store one number per observation plus a shared decoding rule. Which straight-line representation lets us recover the locations with the least total squared error? Use a deliberately constructed, labeled toy dataset; do not pretend it is a documented device deployment. The first scene shows two possible reconstructions and lets the learner identify what each loses. Show the useful result before introducing the acronym.

Keep one equal-unit two-coordinate cloud for the central derivation. All points, the center, direction, scalar score, reconstruction, and residual retain stable visual identities. Add a third coordinate only after the line problem is resolved. A real-data transfer is introduced when the learner can state what the objective promises. This construction makes variance an earned consequence, while leaving an explicit question: is squared reconstruction loss the right objective for the actual task?

Provisional core: approximately 70–85 scenes if each resolves one inference; the count is not a target to pad or a ceiling. Notebook and slides share mathematical objects and data. Notes must speak the actual displayed state, explain each operation's reason, pause at a prediction, and state the next unresolved question. No notes or runtime are authored by this proposal.

## Inference route and scene allocation

| Proposed scenes | Learner question and witness | What the learner supplies | Next need |
|---|---|---|---|
| 1–7 | How can one number describe a point with two coordinates? Show encoding and decoding on candidate lines. Explain what is lost, and why original feature deletion can be wasteful. | Predict a reconstruction and distinguish a score from a direction. | Where should the line pass? |
| 8–13 | Why center? Translate the cloud; keep relative geometry. Mean plus centered coordinates separates a shared offset from varying detail. | Reconstruct a new observation using the stored training mean. | How do we measure loss fairly? |
| 14–20 | Why perpendicular projection and squared loss? For a fixed line, the right triangle shows the nearest point. Dot product refresher gives the signed score. Unit-length constraint prevents score inflation. | Compute one score, its reconstruction and residual; explain the constraint. | Can we compare all directions without reconstructing each point? |
| 21–29 | Why preserve variance? Pythagoras makes total squared radius equal retained squared score plus residual loss. Centering makes mean score zero. | Complete the missing term and explain which part stays fixed as the line rotates. | Can the whole cloud be summarized for this objective? |
| 30–40 | Why covariance? Expand the squared score for two coordinates, exposing variances and cross-products. Equal marginal variance clouds with opposite tilt show what covariance adds. Generalize through an outer-product matrix. | Build one covariance entry, predict its sign, trace a matrix entry to the data. | How does this summary reveal the best direction? |
| 41–50 | Why eigenvectors? Interpret `Cw` as a sum of sample directions weighted by projected scores. Tangential change must vanish at a stationary direction. Introduce gradient/Lagrange machinery only here. | Explain why a sideways component means the direction can improve; identify maximum versus minimum candidates. | Which candidate wins globally? |
| 51–57 | Why global? Symmetric covariance has an orthonormal eigenbasis. Every unit direction allocates squared coefficients summing to one. Its variance cannot exceed the largest eigenvalue. | Reconstruct the bound, equality case and repeated-eigenvalue case. | What if one coordinate is not enough? |
| 58–65 | Why top k? Orthogonal projector, captured energy, trace and score covariance. Prove the subspace bound; connect reconstruction error to omitted eigenvalues. | Choose k for a stated loss tolerance and distinguish a basis from its subspace. | How do we calculate and trust it? |
| 66–73 | How does code match the model? SVD derives the same directions with `lambda = sigma²/(n−1)`. Fit/transform/inverse, shapes, signs, rank limits and train-only preprocessing. | Trace one sample through code; diagnose an implementation or leakage error. | Does optimizing this loss solve the user's problem? |
| 74–85+ | Where does PCA help or fail? Unit changes, outliers, label relevance, nonlinear structure, sampling instability; documented applications and matched alternatives. | Select, reject or qualify PCA on held-out scenarios; teach the core to another audience. | Independent reconstruction and research questions. |

Order is adaptable. Do not let the arithmetic and prerequisites consume the proof or practical judgment. Optional prerequisite detours return to the exact pending question. Expert entries can jump to the objective and use prior geometry as an explanation-back task.

## Exact mathematical spine to preserve

Use rows as observations: `X` has shape n by d, `mu` has d entries, `Xc = X - 1 muᵀ`, and `C = Xcᵀ Xc/(n−1)` for n > 1. Each centered observation is a column vector `x_i` when written individually. Define direction `w`, score `z_i = wᵀx_i`, reconstruction `xhat_i = w z_i`, and residual `r_i = x_i - xhat_i`; `||w||=1`. State this convention before any transpose.

1. **Projection is nearest on the chosen line.** For any scalar a, `||x_i-aw||² = ||x_i-(wᵀx_i)w||² + (a-wᵀx_i)²`. Therefore the score supplies the least-error point on that line. The claim is restricted to Euclidean squared distance.
2. **Reconstruction and retained spread agree.** Orthogonality gives `sum ||r_i||² = sum ||x_i||² - sum (wᵀx_i)²`. The first sum is fixed as w varies; maximizing retained score energy minimizes loss. Since `sum x_i=0`, scores have mean zero, and their sample variance is the energy divided by n−1.
3. **Covariance is the needed summary.** In two coordinates, `(w1*x1+w2*x2)²` exposes both square terms and the cross term. Summing yields `var(z)=wᵀCw`. Generalize with `x_i x_iᵀ`, checking d by d dimensions. Symmetry follows by transpose; positive semidefiniteness follows from nonnegative squares.
4. **Stationarity gives candidates.** With `L(w,lambda)=wᵀCw-lambda(wᵀw-1)`, symmetry gives `gradient L = 2Cw-2lambda w`. Thus stationary directions satisfy `Cw=lambda w`; multiplying by wᵀ identifies lambda as achieved variance. This is necessary, not yet a maximum proof. A minor-axis eigenvector is a counterexample to the wrong conclusion.
5. **Global bound.** Invoke and name the finite-dimensional spectral theorem for real symmetric matrices. Let `Cq_j=lambda_j q_j`, `lambda_1 >= ... >= lambda_d >= 0`, and `w=sum a_j q_j`, with `sum a_j²=1`. Then `wᵀCw=sum lambda_j a_j² <= lambda_1`. Equality holds exactly when w lies in the top eigenspace. The weighted-average argument is verified against [Cornell's primary lecture](https://www.cs.cornell.edu/courses/cs6210/2025fa/lec/2025-11-03.html). Prove the theorem in an optional foundation branch or explicitly state it is invoked; do not silently imply the graphic proves it.
6. **Global k-dimensional guarantee.** For `WᵀW=I_k`, let `b_j=||Wᵀq_j||²`. An orthogonal projector gives `0<=b_j<=1` and `sum b_j=k`. Captured variance is `sum lambda_j b_j`. Its maximum is `sum_{j<=k} lambda_j`: any weight assigned below k while capacity remains above can be moved upward without decreasing the sum. Therefore top-k span is globally optimal. A tie across the boundary allows multiple optimal subspaces. Total residual sum of squares is `(n−1)sum_{j>k}lambda_j`.
7. **SVD connects proof to computation.** `Xc=U Sigma Vᵀ` gives `C=V Sigma² Vᵀ/(n−1)` and scores `Xc V_k=U_k Sigma_k`. Standard PCA directions are columns of V for this data orientation. Forming covariance is pedagogically useful; explicitly teach direct SVD as a computation route. Do not conflate uncentered low-rank SVD of one image matrix with PCA across centered image samples.
8. **What orthogonality means.** `cov(XcW)=WᵀCW` is diagonal for eigenvectors. Directions are perpendicular; training scores are uncorrelated. Independence needs more assumptions. Scores, direction coefficients and variance-scaled loadings have different meanings; choose one loading convention and label any biplot scaling.

These are mathematical derivations, not empirical guarantees about unseen observations or scientific meaning. The reconstruction identity, covariance construction and eigenspace facts accord with the primary course/author sources in `source-analysis.md`.

## Critical pilot that can reject this route

Build three connected pieces in native marimo-studio: opening (3 scenes), variance-to-covariance-to-eigenvector bridge with immediate context (8–12 scenes), and decision transfer (3 scenes). Pilot controls: rotate the line, change a covariance sign while preserving marginal variance, and toggle a low-variance label-bearing direction. Controls must require a prediction before an evidence reveal; the score/reconstruction labels must remain visible. Include direct reading paths and keyboard equivalents.

Neutral tasks, without exposing author diagnoses:

- Given a new direction and point, mark the scalar score, reconstruction and residual; explain why increasing score scale is not improvement.
- Given two centered clouds with equal horizontal/vertical variances but opposite slants, predict which summary entry must differ.
- Starting from squared scores, fill the two missing algebra steps to `wᵀCw`; each step must mention the same geometric objects.
- Given two eigenpairs, decide whether the equation alone proves which one maximizes variance. Then reconstruct the weighted-average bound.
- Given eigenvalues 4, 4, 1, assess whether an algorithm returning a different first direction is necessarily wrong.
- Given a long horizontal cloud whose labels split vertically, distinguish best reconstruction from best one-feature classification; propose a held-out comparison.
- Explain the method to someone who knows coordinates but not eigenvectors; retain the loss criterion and one boundary.

Reject or substantially revise this route if reviewers supplied only the declared entry knowledge cannot map score to reconstructed point, repeatedly infer that variance means predictive information after the failure case, or cannot bridge the cross term to covariance without outside PCA knowledge. A correct answer supplied from an AI reviewer's prior knowledge is insufficient: require scene-specific warrants. First comparison should match the hard bridge and audience, not claim that a full course beats a short video through added coverage. Actual human transfer and delayed retention remain unmeasured until observed.

## Strongest objection and serious competing route

**Objection:** Reconstruction makes squared Euclidean loss look inevitable and turns PCA into a compression algorithm before showing why anyone needs a new coordinate system. Novices may spend their attention on right triangles and forget scientific variation. Also, the step from a manipulable 2D angle to an eigenbasis proof may still feel like a second disconnected lesson.

**Response to test, not assume:** Open with visible reconstruction payoff and explicitly permit the learner to reject the loss. Keep a compact second view showing the same points as scores. Use the `Cw` weighted-vector operation as the bridge from the data picture into stationarity, then retain the same direction marker during the eigenbasis proof. If the pilot still fails, change the route.

**Competitor:** Measurement redundancy → change of coordinates → covariance diagonalization → ordered axes → approximation/variance equivalence. This has a natural scientific purpose and makes decorrelation central (Shlens). Its strongest weakness is that decorrelation alone does not justify truncation or which axes to retain; the global objective must still be supplied. Prefer it if the opening pilot shows that learners understand coordinate change more readily than reconstruction, not because one author is admired.

## Failure, mitigation and alternative decisions

| Mechanism and witness | Diagnostic and mitigation | Residual cost / alternative |
|---|---|---|
| Mixed units change Euclidean loss; rescale one feature | Compare covariance and correlation PCA, justify task units before fitting | Standardization amplifies small-variance noise too; domain weighting or keep interpretable variables |
| One outlier dominates squared deviations | Show fit with/without flagged observation; investigate measurement origin, use robust estimation when appropriate | Removing real extremes changes the target; robust PCA methods have different assumptions |
| Class signal lies in a small-variance direction | Evaluate downstream task on held-out data across k and baseline | More k sacrifices compression; supervised dimension reduction/regularized baseline may fit task better |
| Curved manifold folds under a linear projection | Inspect reconstruction residual structure and neighborhood distortion | Kernel/nonlinear embeddings change objectives and interpretation; no universal winner |
| Nearly tied eigenvalues yield unstable individual axes | Perturb/resample, compare subspace angles and explained variance | Axis narratives may remain unjustified; report subspace or gather more representative data |
| Train/test contamination creates optimistic workflow | Fit mean, scaling, selection and PCA only on training folds | Every pipeline variant needs fair validation; PCA alone does not prevent overfit |
| Uncorrelated mistaken for independent | Symmetric parabola example has zero covariance but deterministic relation | ICA targets stronger separation under assumptions; PCA still valid for its own loss |

Alternatives research beyond these decision roles requires a separate primary-source pass before course claims are finalized. In particular, robust PCA is not a universal synonym for resistant covariance, and UMAP/t-SNE do not supply the same reconstruction guarantee.

## Six explanation lenses, one unchanged core

Shared concept: a constrained shorter description preserves some measured variation and loses the rest; the chosen criterion determines what counts as best.

| Lens/readiness hypothesis | Representation and required translation | Check |
|---|---|---|
| Around 10, coordinates not assumed | Dots, one ruler and recovered locations; perpendicular nearest point demonstrated | Draw which ruler position loses less and name a case where lost detail matters |
| Around 15, coordinates/Pythagoras | Signed distance, squared triangles and changing spread | Explain why keeping more along the ruler leaves less sideways error |
| Undergraduate | Covariance quadratic form, constrained direction, eigenvectors and full worked example | Reconstruct derivation, then explain it without symbols |
| Graduate | Spectral bound, k-subspace trace proof, rank/ties and metric dependence | Prove or refute uniqueness and state assumptions precisely |
| PhD | Population/sample distinction, eigengap stability and objective/task mismatch | Critique an empirical PCA interpretation and propose a discriminating validation |
| Postdoc | Synthesis with representation learning, noise models and domain pipelines | Design a controlled comparison, anticipate confounds and explain stakes in ordinary language |

These are authored tasks and design hypotheses, not evidence of learning at any age. Depth-specific specialist material must be verified before authoring; titles alone are not covered content.
