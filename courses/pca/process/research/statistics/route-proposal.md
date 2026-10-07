# Independent proposal: choose what a smaller description must preserve

7 October 2026. Initial proposal developed without the other proposer's route or the coordinator's preference. Research-informed author hypothesis; no pilot has yet been delivered or learner result observed.

## Main question and promise

Two sensors give two readings for each machine state. Can we store one number per state and reconstruct both readings accurately? How do we know the direction is the best, and when would keeping that direction lose what we actually care about?

The running example uses same-unit sensor readings. It starts with a visible cloud and competing one-number encodings. We deliberately use a transparent synthetic case so the learner can inspect all points and later change the data-generating mechanism. We do not pretend synthetic sensor behavior establishes a real deployment claim. Biology and yield-change examples later test transfer.

Core claim: PCA finds an orthogonal coordinate system ordered by sample variance. Truncating it gives the best linear reconstruction for the selected squared-distance metric. The choice of metric, component count, and task still belongs to the analyst.

The first chapter establishes the goal and projection operation before naming covariance or eigenvectors. Reconstruction then earns the variance objective. Covariance is derived from the square of a projected score; it is not an unexplained intermediate table. Eigenvectors emerge from stationarity, followed immediately by a distinct proof that the largest eigenvalue gives a global maximum. The later chapters test what that guarantee does and does not mean.

## Suggested scene route

These 72 scene obligations are an allocation, not a slide-count target or ceiling. Split or merge only when the inference and attention load warrant it. Every authored scene needs exact spoken notes, a specified figure state, a transition that creates the next question, and separate notebook reasoning work. Critical proof scenes cannot be relegated to optional notes.

| Scenes | Learner question and development | Work/evidence |
|---|---|---|
| 1–4 | What can one number retain? Raw table → cloud → two proposed encodings → reconstructed points. State why compact representation is useful and what “good” will mean. | Choose the visibly smaller reconstruction loss and state the tradeoff. No eigen terminology yet. |
| 5–8 | How does a direction become a number? Unit ruler, signed projection, dot product, reconstructed point. | Calculate one point's score; distinguish score from direction and reconstruction. |
| 9–12 | Why center? Translate the cloud; show affine line through the mean. Mean plus centered residual. Distinguish centering from scaling. | Predict whether translating every point changes centered directions; explain the saved mean. |
| 13–16 | Why maximize spread? A point, its foot, residual, and right triangle; sum the identities; constant total squared length. | Fill the conserved-total argument; compare orthogonal versus vertical residuals. |
| 17–20 | Why unit length, why variance, why covariance? Scaling an unnormalized ruler gives an unbounded fake win; centered score mean is zero; square a two-feature score; expose cross-products. | Defeat the “longer arrow is better” rule; distinguish equal variances with opposite tilt. |
| 21–24 | How does the matrix encode this? Two variances plus covariance; expand wᵀCw; general n×p data; symmetry and positive semidefiniteness. | Map one covariance entry to data products; explain why a negative off-diagonal entry is allowed. |
| 25–28 | Where can an optimum be? Tangent change on the unit circle/sphere; constrained gradient; Lagrange equation; define eigenvector and eigenvalue at point of need. | Show why the gradient must have no tangential part; identify minimum and maximum stationary candidates. |
| 29–32 | Why the largest is globally best? State the symmetric spectral theorem; expand any unit direction in that basis; squared coefficients sum to one; weighted-average bound plus equality case. | Supply the inequality and equality condition without relying on a slider search. |
| 33–36 | What if several answers work? Sign freedom, equal eigenvalues, almost equal eigenvalues, subspace versus individual axis. | Perturb a round cloud; explain why unstable axes need not imply unstable retained subspace. |
| 37–40 | Why does taking k directions work? Orthonormal frame, scores and reconstruction, covariance of scores, trace objective. | Check dimensions; distinguish uncorrelated from independent with a nonlinear example. |
| 41–44 | Is the k-dimensional answer global? Projection matrix, spectral weights, sum-of-top-k bound, residual tail sum. | Explain why greedy selection happens to achieve the joint optimum for this problem. |
| 45–48 | How should software compute it? SVD, λ=σ²/(n−1), scores UΣ, rank/null-space limits. Compare direct SVD with forming covariance. | Match eigen and SVD answers up to sign/subspace; show a centered n<p case. |
| 49–52 | Which distances did we choose? Unit conversion, standardized data, reconstruction metric after rescaling, whitening. | Defend a same-unit or standardized metric for a stated task; distinguish whitening from PCA truncation. |
| 53–56 | How many components? Scree/cumulative variance, reconstruction budget, held-out error, target-relevant low-variance direction. | Choose k using a stated loss; demonstrate why a universal 95% rule cannot guarantee prediction. |
| 57–60 | What can bend or break the result? Outlier leverage, curved structure, duplicated/reweighted features, data leakage. | Diagnose the mechanism and select a specific repair with residual cost. |
| 61–64 | When would another method help? Robust model, supervised reduction/regression, nonlinear embedding, factor/latent-variable models. | Compare objectives and outputs before choosing; optional depth for assumptions not yet earned. |
| 65–68 | Does the idea transfer? Seurat rare-subset problem; yield-change patterns; time-shifted validation; one original transfer notebook task. | State data axes, preprocessing, retained objective, loss, validation, and what cannot be concluded. |
| 69–72 | Can you own the explanation? Reconstruct the proof; audit a misleading PCA claim; explain to two audiences; propose a discriminating investigation. | Unassisted derivation, changed data, audience follow-up, and later reconstruction prompt. |

## The decisive bridges

**B1: Compression to projection.** Entering model: drop a column. Witness: correlated sensors need neither raw column alone. Show an encoder z=xᵀw and decoder zw; the same direction is reused. Prompt the learner to reconstruct one unseen point. Wrong rule: projection is a line drawn near points, with no encoding. Feedback compares score, reconstruction, and residual as three different objects.

**B2: Reconstruction to variance.** Need: select among unit directions. Show one fixed vector as the diagonal of a right triangle, with retained and discarded parts perpendicular. Hold its total squared length fixed while the ruler rotates. Then sum over points. Only after centering identify retained squared length with (n−1) times sample variance. Fresh exit: a translated dataset and a question about whether the identity still has the same variance interpretation.

**B3: Covariance to eigenvector.** Need: stop searching angles and solve in any dimension. Expand a two-variable square before matrix shorthand. Make a tangent direction h satisfy hᵀw=0; the first-order variance change is 2hᵀCw. If Cw has a tangential part, move to improve the objective. At a stationary point Cw must be parallel to w. Lagrange multipliers formalize the same restriction. Ask the learner to reject the claim that this proves maximality.

**B4: Stationarity to global optimum.** Need: several eigenvectors survived. State the symmetric spectral theorem as a named input; explain why C satisfies its condition. Express every candidate using eigenbasis coordinates; their squared weights are nonnegative and total one. Variance is a weighted average of eigenvalues and cannot exceed the largest. Equality identifies the entire top eigenspace, not just one arbitrarily signed vector. This is the central proof, not optional enrichment.

**B5: Guarantee to judgment.** Witness: let a tiny contrast predict a fault while a large shared swing is irrelevant. PCA remains optimal for reconstructing readings, yet one-component regression loses the fault signal. Ask for the task loss and an appropriate held-out test before displaying software results. The repair changes k or method; it does not declare the eigensolver broken.

## Six lenses on the same core

| Recipient preparation | Added precision and teach-back |
|---|---|
| Around age 10, using rulers/points | One position on a well-chosen ruler can approximate two readings; draw original, foot, and missed distance. Explain why a small missed change might still matter. |
| Around age 15, coordinates/algebra | Signed weighted scores, mean, squared distance, and unit length. Explain why shrinking average reconstruction error means keeping spread in this centered example. |
| Undergraduate | Derive covariance quadratic form, constrained stationarity, and global bound. Translate each step back to the ruler and reconstruct a new point. |
| Graduate | Joint k-subspace optimum, degeneracy, metric/scaling choice, SVD, finite-sample versus population claim. Supply a counterexample to independence or uniqueness. |
| PhD | Separate deterministic optimum from signal recovery or useful representation. Design an uncertainty/stability or task-validation test; critique unsupported latent-factor interpretation. |
| Postdoc | Compare objectives and assumptions across supervised, robust, probabilistic, and nonlinear approaches. Defend a research comparison, revise it under an identifiability objection, and explain its stakes plainly. |

These are readiness/recipient contracts, not developmental claims. A technically advanced learner can enter later while retaining access to the concrete core. Teach-back checks meaning and changed-case prediction, not script imitation. Research lenses are proposed branches; deep PPCA likelihood and asymptotic theory are not yet fully researched here.

## Alternatives must answer a changed need

- Gross corruptions: inspect influential points and provenance; robust covariance or a specified low-rank/sparse model may help. It adds assumptions and can erase legitimate rare events.
- Prediction: preserve useful small directions, validate k against target loss, compare regularized regression or supervised reduction such as PLS. Label information and validation are now required.
- Curved geometry: kernel PCA/manifold methods/autoencoders can represent different structure. Their objective, out-of-sample behavior, reconstruction, tuning, and stability differ; no blanket ranking.
- Interpretable latent causes: factor analysis/PPCA add probability/noise assumptions; ICA targets independence rather than decorrelation. None alone confers causal interpretation.
- Huge or sparse matrices: partial/randomized/incremental methods address computation. Truncated SVD without centering solves a different objective; do not call it identical PCA.

## Strongest objection

The reconstruction-first route may feel like a long justification of a loss the learner never wanted. The sensor example could imply compression is PCA's only purpose, and the complete proof could overwhelm the practical route. It might also delay the user's requested covariance-to-eigenvector connection if every foundation expands.

Response to test, not assume: show an actual reconstruction decision in the first four scenes, reserve fixed attention for the central derivation, and preview the later “right optimum, wrong task” challenge. Keep the same physical quantities through the proof and move refresher detail into optional native notebook detours. If learners can manipulate the picture but cannot explain the objective, replace the opening rather than add more decorations.

## Falsifying pilot

Build three native marimo-studio slices before expansion: scenes 1–8, 25–32 with immediate covariance context, and 53–56. Record actual learner time; no course-length ceiling follows. Neutral tasks: (1) encode/reconstruct a fresh point and distinguish axis from camera view; (2) explain why wᵀCw is variance; (3) reject a stationary minimum; (4) complete the weighted-average bound and equality condition; (5) choose between reconstruction and prediction metrics on a fresh small-variance signal.

Reject or materially revise this route if fresh reviewers can cite only displayed answer text, if the unit constraint appears arbitrary, if covariance is remembered as a recipe without the cross-term, if the maximum proof is explained only as “the biggest eigenvalue is biggest,” or if the learner claims 95% variance guarantees 95% predictive information. A matched-time comparison against a strong transcript-supported bridge can assess explanation burden; only a properly designed human study can support comparative learning claims. Runtime checks, expert correctness, simulated teach-back, actual human attempts, delayed retention, and preference are separate evidence.
