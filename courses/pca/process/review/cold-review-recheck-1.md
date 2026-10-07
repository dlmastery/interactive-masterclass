# PCA repair recheck 1

Date: 2026-10-07. This is a **supervised repair recheck**, not a new blind review. The first-pass report, `cold-review.md`, is preserved unchanged. Reviewer: the same AI subagent that performed that pass, with prior topic knowledge and now with the author's repair summary. No human learner, rendered app, live control, audio, or notebook execution was observed here.

Scope: reread affected current scene content, `Visuals.tsx`, `LearningVisuals.tsx`, `PracticalVisuals.tsx`, `App.tsx`, `course.ts`, `checkpoints.ts`, and relevant styles. Conclusions concern written/source delivery and mathematical reasoning only.

## Result

The two original **P1 source delivery defects are repaired**. No outstanding P1 mathematical or dispatch blocker was found in this scoped recheck. Several P2 details remain below. Browser readability and working controls still require the author's separate runtime evidence; this report does not establish them.

| First-pass issue | Recheck evidence | Status |
|---|---|---|
| P1-1, `more-discarded-tail` | `SpectrumVisual` now selects (12,5,2,1), n=5, starts k=2, and computes 17/20=85%, normalized loss 3, and raw SSE 12. Its slider supports all four components. The prepared steps are rendered. `practice-budget` retains its separate (8,1,1) fixture and 90% target. | Repaired in source. |
| P1-2, `more-centered-rank` | `Visual` sends a rank scene with steps to `Proof`. The steps now begin with an explicit 4×2 centered matrix whose columns each sum to zero, then the observation-space constraint, rank bound, and covariance rank equality. A rank/null-space refresher is present. `practice-sparse` still goes to its storage example. | Repaired in source. |
| P2-1, missing referents | `Eigen` draws the unit-circle tangent and the sideways component of Sw. `Capacity` now supplies a real legal two-direction frame with a moving weight. `ShapeFlow` supplies an inspectable row through XW=Z. `more-frame-shapes` precedes `more-score-covariance`. The authored NumPy example is hidden behind a reveal button. | Substantially repaired; fixture/script mismatches remain below. |
| P2-2, trace/completeness | `more-capacity-weights` now has a local refresher explaining reconstruction by a complete orthonormal basis and cyclic trace via summed indices. | Improved; captured-variance and capacity sums still warrant two explicit elementary lines. |
| P2-3, early mean proof | `mean-proof` now follows `outer`, after dot product, projection, unit length, and outer product. `center` explicitly treats the anchor provisionally until its later proof. | Ordering repaired; old refresher and hidden cross term remain below. |
| P2-4, burden/notation | Raw x is explicitly reintroduced in standardization/new-observation practice, and sparse S is explicitly distinguished from covariance. Eight chapter-specific `Pause & recall` tasks are accessible through App, use an explanation input, withhold example answers, and return to the current scene. | Material improvement; d/p shift remains undeclared in general code/practice. Human burden remains unmeasured. |

## Outstanding P2 changes

### R1 — The authored NumPy check still sums only one axis

Scene: `more-numpy-meaning`, final example comment. Current text is `sum((A - A_hat)**2)/(len(A)-1) agrees with np.sum(lam[k:])`. Python's built-in sum iterates the array's rows and produces a d-entry vector; the right side is one scalar. The code panel annotation says both sides are scalar and instructs use of `np.sum`, so the displayed recipe contradicts its own explanation.

Required change: use `np.sum((A - A_hat)**2)` on the left as well. Recheck with a residual matrix with unequal column sums, such as squared entries [[1,4],[9,16]]: the required total is 30, whereas the built-in sum gives [10,20]. This is a correctness defect in an example check, not a defect in the PCA theorem. The reveal itself is repaired.

### R2 — New instructional visuals need matching scene fixtures and narration

Scenes: `more-global-k-bound`, `more-frame-shapes`, and `data-matrix`.

`Capacity` is a valid subspace example with eigenvalues (9,4,1), weights (1,1−p,p), and objective 13−3p. But `more-global-k-bound` immediately asks for (12,5,2,1), weights (1,.5,.5,0), and the optimum 17. Unlike the repaired tail scene, the new caption does not explicitly say this is a different fixture. Prefer parameterizing the capacity example with (12,5,2,1), an always-zero fourth weight, and objective 17−3p so the same visual checks the task. An explicit separate-example declaration is acceptable if the transition has a teaching purpose.

`ShapeFlow` traces four observations with two features and one/two scores. `more-frame-shapes` notes still instruct the presenter to trace the diagram beginning with eight measured values and three scores. Change the script to first trace its actual 2-feature fixture, then generalize to the 100×8, k=3 prompt; or make the diagram implement the prompt. The new `data-matrix` shape visual also introduces W/k before their formal chapter; briefly define W as one or more direction columns there, or restrict that early view to Xw.

Recheck: for each instructed point/row/weight, match the exact displayed dimensions and numerical values, then perform the task using the same fixture. No browser rendering claim is made.

### R3 — Finish the local derivation rather than moving its prerequisite into prose

Scene: `more-capacity-weights`. The new help panel improves disclosure, but the learner still jumps from a single b_j to a trace rearrangement and then to captured variance. Add the short ordinary-sum route:

`b_j = sum_l (w_l^T q_j)^2`, hence `sum_j b_j = sum_l sum_j (w_l^T q_j)^2 = sum_l ||w_l||^2 = k`.

Each inner sum is the squared length of a unit frame column expressed in the complete orthonormal eigenbasis. Also state `tr(W^T S W) = sum_l w_l^T S w_l`: the diagonal entries are precisely the k score variances. This directly connects the multi-score objective to already-earned scalar variance and closes the original hidden-prerequisite concern without requiring memorized trace manipulation.

Recheck: for W=[q1, sqrt(1−p)q2+sqrt(p)q3], explain both b=(1,1−p,p) and why its total is two; then generalize the sum to an arbitrary orthonormal W. The present proof is mathematically valid; this request concerns the stated interested-novice audience.

### R4 — Clean the moved mean proof and remaining notation transition

Scene: `mean-proof`. Its refresher still says “The main projection argument follows next,” although projection is now earlier. Replace that with a backward reference. State `||w||=1` beside P=wwᵀ and expose the canceled cross term, e.g. `2 [(I−P)(mu−a)]^T (I−P) sum_i x_i = 0`. The course otherwise still asks the learner to trust the sentence that it vanishes.

Scenes: `practice-svd`, `practice-pipeline`, general SVD code. The derivation uses d features while the generic recipe uses p without declaration. Use d throughout, or explicitly say p is another conventional name for the feature count. This is a small clarity repair, not a mathematical blocker.

## Rechecked transfer and route

The new sequence preserves the purpose → fixed-line projection → variance → covariance → mean-anchor proof → constrained candidates → global eigenbasis bound chain. Deferring the formal anchor proof does not make the early use circular: `center` now identifies it as provisional, and the proof is supplied before the final optimization statement.

For the first report's Case B, the repaired tail display now supplies the missing normalized/SSE warrant, and the repaired rank scene supplies its missing algebra. For a fresh capacity perturbation, p=0.25 in the current (9,4,1) example gives b=(1,.75,.25) and captured variance 12.25; moving p to zero raises it to 13. The explicit legal frame in the caption supports these weights. The general top-k inequalities still establish the guarantee beyond that one family.

The pause panel makes chapter-level retrieval available without removing content. It is an optional control, not evidence that learners use it, pause at the right time, or succeed unaided. It should remain described as authored self-review rather than automatic mastery assessment.

## Evidence boundary and revision record

The author received R1–R4 during this recheck. Any later source edits require a targeted verification; they are not silently included as passes in this report. No new AI assessment success is evidence of human learning. No numerical quality score or unqualified release-ready judgment is supplied.

Inspected file hashes captured during this recheck (SHA-256; source could change afterward):

| File | Hash |
|---|---|
| core.json | 4FA68E1CCA570AA26204672ECD486542783431DD977598C1E3669B178775423C |
| rank-svd.json | FB20673EDD9937F38E61DFF79E9DE28416FD6C69896333A53C35C81ADA8A4F6E |
| Visuals.tsx | 0AAA1DABF007BBAB74A8FEFE5345B6C48EB45A37E407F39CFBECB138296F4BE9 |
| LearningVisuals.tsx | CF233221F027D485A475B5888754F4D513D8DEE43D7485B5E129558599A4040F |
| PracticalVisuals.tsx | 2CD4E6714CBF5B853F86172751481658F0EF1DC9B32F4DC64D509F70BCD9D46E |
| App.tsx | 8ABBFF1B9A5A2BF36D09BDB620316574E880A16ABEB0582CE9456B0A94E1123E |
| checkpoints.ts | 2A8303E3CEC7EDF5B3F78298ED2BA6D5E39E0DE958882548F13E24894D370026 |
