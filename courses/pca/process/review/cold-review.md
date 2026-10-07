# PCA cold review — first independent pass

Date: 2026-10-07. State: **revise** for the source-level delivery defects below. No numerical score.

## Provenance and limits

Reviewer: fresh-context AI subagent, same model family as the authoring agent; not an independent human expert. I did not author the course and received the audience, objective, file locations, neutral review tasks, and permission to inspect runtime source only after the learner-content pass. I have prior PCA knowledge; successful answers below do not establish that this course taught me PCA. I first read the four learner-content JSON files and reconstructed their route. I then read Visuals.tsx, LearningVisuals.tsx, PracticalVisuals.tsx, and App.tsx, plus the applicable review reference and repository instructions. No author research notes, desired verdict, or earlier review diagnoses were supplied or consulted.

Evidence is written-content review and source inspection only. I did not render the app, operate controls, listen to narration, measure duration, verify external application references, or observe a human learning. Runtime consequences below are dispatch/code inferences to verify in the browser. This report preserves the first pass; subsequent fixes require a separately dated recheck rather than silently changing these observations.

## Reconstructed route

The 84 scenes form a coherent argument with eight chapters. First, a shared ruler and a score recover approximate positions; centering supplies the anchor, and perpendicular projection supplies the best fixed-line decoder. Second, Pythagoras changes the question from minimizing lost squared distance to maximizing score variance. Third, expanding squared scores demands cross-products, which produces covariance and wᵀSw. Fourth, tangent motion and constrained calculus find eigenvector candidates, then a symmetric eigenbasis and weighted-average bound prove the global winner. Fifth, orthogonal frames extend the argument to k coordinates; capacity weights prove a global top-k bound; the eigenvalue tail and SVD connect proof to computation. Sixth, metric choice, fitting discipline, and checks make the calculation usable. Seventh, low-variance signals, outliers, curvature, duplication, instability, and applications challenge overinterpretation. Eighth, explanation and decision tasks ask learners to rebuild the argument, vary the case, and translate it back to ordinary language.

The opening problem receives a real payoff at `opening-payoff`, and the later task mismatch returns to the opening loss rather than treating limitations as unrelated warnings. The course explicitly invokes, rather than pretends to prove, the spectral and SVD existence theorems.

## Exact warrants for the central bridges

| Bridge | Learner-visible evidence in authored content | Assessment |
|---|---|---|
| Projection | `dot` computes a score and decoded point; `nearest` shows wᵀ(x−zw)=0 and ‖x−aw‖²=‖x−zw‖²+(a−z)². | Sufficient fixed-line optimality warrant under the stated unit direction and Euclidean squared loss. |
| Mean anchor | `center` gives zero-sum centered observations; `mean-proof` splits loss into centered loss plus n‖(I−P)(μ−a)‖² and states the cross term vanishes. It distinguishes moving along the same line from moving the line sideways. | Correct warrant, but presented before the required projector notation is earned; see P2-3. |
| Var(z)=wᵀSw | `score-mean` establishes zero score mean; `variance` fixes n−1; `square` supplies the cross term; `cov-matrix` traces each sum; `quadratic` expands the matrix expression; `outer` generalizes it. | This is a derivation, not a covariance recipe. Sample/population distinction and units are stated. |
| Stationarity versus global optimum | `gradient` derives 2Sw by perturbation; `lagrange` gives Sw=λw as necessary; `stationary-trap` supplies the minimum counterexample; `spectral`, `cross-vanish`, and `global` compare every unit vector with the weighted eigenvalue sum. | Mathematically sound. `cross-vanish` correctly uses both eigenvector structure and orthogonality. |
| Top-k bound | `more-projector` gives the loss split; `more-capacity-weights` defines b_j and its constraints; `more-global-k-bound` pairs below-cutoff weight with unused upper capacity, then exhibits an attaining W. | Correct proof as written, with an underexplained trace/identity bridge for this audience; see P2-2. |
| SVD | `more-svd-connection` substitutes X=UΣVᵀ into XᵀX; `more-svd-scores` supplies dimensions, scores U_kΣ_k, and reconstruction; `more-numpy-meaning` maps the objects into NumPy. | Correct algebra and orientation. The course does not claim to derive the SVD theorem or numerical algorithm. |
| Metric choice | `practice-metric` ties equal costs to physical units; `practice-units` shows squared scaling; `practice-standardize` and `practice-weighted-loss` state inverse-square weighting; `practice-whiten` separates score scaling. | The guarantee is correctly conditional on the chosen metric. |
| Task mismatch | `boundary`, `limits-small-signal`, `limits-supervised`, and `transfer-compare-objectives` distinguish reconstruction from prediction and pair the failure with extra components, original-feature baselines, supervised reduction, and held-out evaluation. | Mechanism and response are supplied. The failure is more than a general caution. |

## Findings requiring changes

### P1-1 — The discarded-tail scene delivers a different numerical problem

Scene: `more-discarded-tail`. Source: `rank-svd.json`; `PracticalVisuals.tsx` `SpectrumVisual` and `PracticalVisual`; `App.tsx`.

Observation: the scene exercise is eigenvalues (12,5,2,1), n=5, k=2 and its authored steps establish the exact eigenvalue-tail equation. Its `kind: spectrum` dispatches to a hard-coded (8,1,1) spectrum, three-component slider, 90% feedback, and no rendering of scene.steps. The caption calls this a separate fixture, so this is not a false calculation; it is an avoidable conflict in the scene whose job is to connect a specific calculation to the theorem. At k=2 the visual says 90% and discarded variance 1 while the exercise requires 85% and 3. The intended equation is not in scene.formula, so the main copy does not rescue its missing display.

Learner consequence: the learner cannot use the displayed accounting to check the exercise; the essential n−1 link is relegated to notes. This breaks the promised connection between exact loss, spectrum, and worked example.

Required change: make the spectrum take the scene's eigenvalues and n, display retained amount/fraction, normalized loss, and squared-error sum for the same selected k, and render the authored equation/steps. Keep (8,1,1) for `practice-budget` if desired.

Discriminating recheck: at `more-discarded-tail`, choose k=2 and confirm the same scene shows 17/20, 3, and 12 with the n−1 explanation. At `practice-budget`, confirm its distinct target still uses (8,1,1). State: revise; source-inferred, not browser-observed.

### P1-2 — The centered-rank derivation is dropped by the renderer

Scene: `more-centered-rank`. Source: `rank-svd.json`; `PracticalVisuals.tsx` `RankVisual`; `App.tsx`.

Observation: the scene supplies 1ᵀX=0, rank(X)≤min(n−1,d), and the null-space argument for rank(S)=rank(X). `kind: rank` dispatches to an unrelated add-retained-directions control over the (8,1,1) fixture; that component never reads the steps. Its displayed rank-one expansion does not explain why centering removes an observation-space dimension. The body gives the assertion and notes narrate the idea, but the intended displayed reasoning is absent.

Learner consequence: the learner is asked to connect centered column sums, observation space, covariance rank, and nonzero eigenvalues while the visual changes k in a different problem. This is especially costly because rank/null space are new prerequisites.

Required change: render the prepared rank derivation, define rank as the number of independent columns/directions, and give a small centered matrix whose column sums are visibly zero. An n/d control can distinguish the upper bound from the actual rank. Preserve the sparse-centering visual for `practice-sparse`.

Discriminating recheck: a reader must be able to answer the n=10,d=100 question from displayed centered columns and the bound, and explain why nine is only an upper bound. State: revise; source-inferred, not browser-observed.

### P2-1 — Several notes ask the presenter to point to objects that are not drawn

Scenes: `tangent`, `more-global-k-bound`, `more-frame-shapes`, `more-score-covariance`, `more-numpy-meaning`.

Observation: `Eigen` draws w and Sw but no tangent or sideways component although `tangent` says the tangent points along a legal turn. `more-global-k-bound` says to keep a capacity picture visible beside the inequalities, but `Proof` displays only equation cards. `more-frame-shapes` asks to trace a row through a diagram; `matrix` scenes currently share the same equation-card renderer. `more-score-covariance` asks the presenter to read dimensions before multiplying although its steps have no dimensions and the explicit W/Z dimension lesson is the next scene. `more-numpy-meaning` asks learners to write operations before revealing code, but `CodeVisual` shows all lines immediately; selecting a line only changes its annotation.

Learner consequence: notes cannot function as an exact cold-presenter script, and the visual support promised for the hardest new objects is absent. Correct equations alone do not show the movement or allocation the narration refers to.

Required change: draw and label the tangent/sideways projection; supply a small capacity-allocation view or change the script to match what is actually present; provide the shape/row flow when the script asks for one; move `more-frame-shapes` before `more-score-covariance` or add its needed dimensions there; hide the SVD recipe until the first attempt is made or remove the nonexistent reveal instruction.

Discriminating recheck: perform a cold presenter pass and identify the precise on-screen referent for each bracketed instruction. For the code task, confirm the first-attempt state actually withholds the answer. State: revise; code and notes inspected only.

### P2-2 — The top-k proof conceals two new algebraic prerequisites

Scenes: `more-capacity-weights`, `more-global-k-bound`.

Observation: the capacity idea is useful, but the equation for Σb_j introduces the resolution Σq_jq_jᵀ=I and trace rearrangements without a derivation. Trace was previously only defined as adding diagonal entries. Captured variance tr(WᵀSW) is asserted without first showing it sums the k score-column variances. No scene-specific refresher exists, so App's “Math at this step” falls back to the opening two-dimensional point/ruler text.

Learner consequence: an interested learner who followed the one-direction proof can repeat the top-k bound while not knowing why every genuine subspace satisfies its decisive capacity constraints. AI prior knowledge can conceal this gap.

Required change: add the elementary sum argument b_j=Σ_l(w_lᵀq_j)², exchange the finite sums, and use unit length of each w_l in the eigenbasis to get k. Likewise show captured variance =Σ_l w_lᵀSw_l. Explain Σq_jq_jᵀ=I as rebuilding any vector from all its basis coordinates if retaining that notation. Add local help for frame, projector, trace, and rank.

Discriminating recheck: without invoking a memorized trace rule, explain why Σb_j=k for a rotated two-dimensional frame in three dimensions and why each b_j≤1. State: revise for explanatory support; no false inequality found.

### P2-3 — The mean proof arrives before its notation and has no concrete intermediate expansion

Scenes: `mean-proof`, `dot`, `nearest`.

Observation: `mean-proof` introduces P=wwᵀ before dot-product, transpose, and unit-vector explanations, and states the summed cross term is zero without showing that term. Notes candidly promise projection justification shortly, but a novice must temporarily accept several new objects to justify the anchor before learning the simpler projection operation.

Learner consequence: the sixth scene interrupts the physical story with its densest notation so far. This is a route-burden risk, not a mathematical contradiction.

Required change: put `dot` and `nearest` before the formal anchor proof, or keep the early centering picture and defer the proof until those objects are defined. Show the cross term as a fixed vector dotted with Σx_i, and state ‖w‖=1 directly beside P=wwᵀ.

Discriminating recheck: ask why sideways anchor displacement adds loss and why movement along the line does not; require the reader to identify the canceled sum. State: revise for audience scaffolding.

### P2-4 — Notation changes and repeated display patterns add avoidable burden

Scenes: `practice-standardize`, `practice-frozen-transform`, `practice-svd`, `limits-robust`, `more-numpy-meaning`, `more-projector` through `more-global-k-bound`.

Observation: core notation uses p_i for raw points and x_i for centered points, but practice uses x for raw values without an explicit reset. Feature count changes from d in the derivation to p in the SVD code and body. S means covariance before meaning sparse corruption in M=L+S. These are conventional locally but need short declarations. The central rigorous route also has long runs of identically presented “reveal next reason” cards, including the projector/capacity/global proof. The route offers chapter jumping but no chapter-specific stopping/retrieval task until after the whole top-k/SVD chapter; 84 scenes imply a substantial study route even without a measured duration.

Learner consequence: symbol tracking and reveal-clicking can substitute for reconstructing the argument. This is an attention/learning risk inferred from source, not observed boredom.

Required change: keep d and the raw/centered distinction consistent, label the sparse term as a new local symbol, and replace at least the hardest capacity transition with a construct/predict/check operation. Offer explicit chapter pause points and short reconstruction checks. Preserve the full derivation rather than shortening scope to meet an arbitrary scene cap.

Discriminating recheck: after `global`, and separately after `more-global-k-bound`, have a fresh reader explain what each symbol refers to and supply the bound before opening the next card. State: revise for clarity; engagement unverified.

## Fresh assessment attempts with course warrants

These cases were created after the learner-content pass and before the author received this report. They are AI attempts using existing topic knowledge; pointers establish that the needed warrant is present, not that learning occurred.

### Case A — A negative tilt, a new point, and a stationary trap

Task: six training observations have mean μ=(10,−3) and sample covariance S=[[5,−2],[−2,2]]. Candidate unit directions are q=(2,−1)/√5 and r=(1,2)/√5. Encode the new raw point (12,−3) using q. Recover it, calculate its squared gap, and determine which candidate gives the globally best training line. Does moving the anchor one unit north help?

Attempt: centered new point is (2,0), score 4/√5, recovered offset (8/5,−4/5), raw reconstruction (11.6,−3.8), and residual (0.4,0.8), with squared gap 0.8. Sq=6q while Sr=r, so both are stationary but q attains the global variance bound 6. The training normalized loss is tr(S)−6=1; training squared-error sum is 5, distinct from the new point's error. Moving the anchor north has perpendicular squared displacement 4/5, adding 6×4/5=4.8 to training loss, so it cannot improve this fixed-direction fit.

Warrants: `new-point`/`nearest` for frozen encoding and projection; `mean-proof` for anchor cost; `eigenvalue` and `stationary-trap` for candidate versus winner; `spectral`/`cross-vanish`/`global` for the bound; `variance` and `objective` for n−1 accounting. The anchor calculation requires the notation repair in P2-3 for this audience, though the identity is supplied.

### Case B — A boundary tie with an unused zero direction

Task: n=7,d=4, covariance eigenvalues (9,4,4,0). Compare k=2 and k=3. Can two correct programs retain different two-dimensional subspaces? Give loss, squared-error sum, singular values, and actual rank.

Attempt: at k=2, capture 13, discard 4, retain 13/17, and squared-error sum is 6×4=24. Both programs can keep q₁ and different unit choices within the tied eigenvalue-4 plane; the two-dimensional subspace itself need not match. At k=3, capture 17 and discard zero; the whole positive eigenspace is the unique leading three-dimensional subspace, though its basis may rotate inside the tied plane. Singular values are (√54,√24,√24,0). Actual centered rank is 3, below the bound min(6,4)=4. U alone omits singular-value scale and therefore does not give the ordinary PCA scores.

Warrants: `more-capacity-weights`/`more-global-k-bound` for optimal capture; `more-discarded-tail` for the factor n−1; `transfer-tied-subspace` for cutoff ties; `more-svd-connection`/`more-svd-scores` for singular values and scores; `more-centered-rank` for rank. P1-1 and P1-2 are runtime delivery gaps for these warrants even though the JSON contains them.

### Case C — Accurate compression with the wrong operational loss

Task: an archive uses feature scales 20 and 2. One candidate reconstruction has raw errors (10,1). An engineer says these unequal errors prove the standardized fit ignored feature 2, copies feature 2 five times to improve fairness, then chooses k after inspecting fault errors on the final future test period. Faults live mainly in a low-variance contrast. Diagnose the argument and propose a fair comparison.

Attempt: the scaled squared costs are (10/20)²=(1/2)²=0.25, so the unequal raw errors have equal cost under the stated metric. Copying a feature repeats its contribution and changes the metric; it adds no independent evidence. Small variance does not show that the fault contrast is disposable. Use earlier training periods to fit means/scales/PCA, validation periods to choose k and predictor settings, and an untouched later period for final assessment. Compare one PC, more PCs, and a regularized original-feature predictor under the same storage/operational constraints. Report reconstruction in the declared metric and an appropriate fault-prediction loss separately. A worsening fault result despite a good retained fraction would support more coordinates or a task-specific representation; any repair has a storage/modeling cost.

Warrants: `practice-weighted-loss`, `limits-duplicate`, `limits-small-signal`, `practice-validation`, `practice-pipeline`, `application-temporal`, and `transfer-compare-objectives`. Plain-language translation from `transfer-explain-back`: the long ruler recovers the big movements well, but a small sideways fault movement can vanish; keeping the sideways change instead may help faults while losing more of the large movements. The task decides the tradeoff.

## Coverage and remaining evidence

No central false covariance, eigenvector, global-bound, or SVD statement was found in this pass. The strongest issues concern delivery of prepared arguments and local prerequisite burden. The practical section includes mechanisms, diagnostics, mitigations with costs, fair alternatives, and modern applications, though its external source accuracy was outside this pass. Explanation across depths is exercised by actual learner prompts with follow-ups, rather than merely six canned summaries; human success on those prompts remains unverified.

After repairs, repeat the affected source/DOM checks and a cold walkthrough from projection to mean anchor, and from frame to capacity to tail/SVD. Browser rendering, mobile readability, native notebook behavior, listening, genuine learner performance, retention, and comparative quality all remain separate unverified claims here.
