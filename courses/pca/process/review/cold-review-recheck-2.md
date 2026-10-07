# PCA repair recheck 2

Date: 2026-10-07. Reviewer: the same AI subagent as the initial cold review and recheck 1. This is a **targeted supervised source recheck**, not another blind review. Both earlier reports remain unchanged. The author provided the repair list before this pass.

## Outcome

The substantive remaining repairs from recheck 1 are present and correct in the inspected source. **No remaining P1 mathematical or dispatch blocker was found within this review's scope.** One minor notation-timing residue is documented below; it does not invalidate the argument or prevent the affected task from being completed.

| Recheck-1 item | Current evidence and reasoning | Status |
|---|---|---|
| R1: scalar NumPy residual check | `more-numpy-meaning` now displays `np.sum((A - A_hat)**2)/(len(A)-1)` against `np.sum(lam[k:])`. Both are scalars. For squared entries [[1,4],[9,16]], the numerator is 30, not the former per-column vector [10,20]. The authored example still starts hidden. | Repaired in source. |
| R2: capacity fixture mismatch | `Capacity` now explicitly uses eigenvalues (12,5,2,1), k=2, and four weights (1,1−p,p,0). Its legal frame is q1 together with sqrt(1−p)q2+sqrt(p)q3. Captured variance is 17−3p, matching `more-global-k-bound` and the tail scene. At p=.5 the visual formula gives 15.5; at p=0 it attains 17. | Repaired in source. |
| R2: shape narration mismatch | `more-frame-shapes` notes now trace the displayed four-by-two example, change the row, and switch between one/two scores before explicitly moving to the separate eight-feature exercise. | Repaired in source. |
| R3: capacity and captured-variance warrants | `more-capacity-weights` now displays Σ_j b_j = Σ_l Σ_j(w_lᵀq_j)² = Σ_l‖w_l‖² = k, with the explanation that each retained unit direction has squared basis coordinates summing to one. It also displays captured variance = Σ_l w_lᵀSw_l = tr(WᵀSW), and identifies each diagonal entry as one score variance. The trace/completeness form remains available afterward. | Repaired; no memorized trace rearrangement is needed to justify the key capacity constraint. |
| R4: moved mean-proof scaffold | `mean-proof` displays Σ_i(I−P)x_i=(I−P)Σ_i x_i=0 and explains that the common offset dots with this zero sum. Its refresher refers to the already-derived projection and identifies the unit ruler. The loss split and anchor nonuniqueness remain correct. | Repaired; the zero cross-term now has an explicit learner-visible warrant. |
| R4: p/d shift | `more-numpy-meaning` explicitly states that p in code denotes the same feature count called d in the derivation. This declaration precedes the later generic practice recipes. | Repaired for the sequential route. |

The original P1 repairs remain in dispatch: a rank scene with steps goes to `Proof`, and `more-discarded-tail` uses its own spectrum and renders its authored equations. This pass did not repeat unrelated earlier checks merely for reassurance.

## Minor residue

`LearningVisuals.tsx` still mounts `ShapeFlow` on `data-matrix`, where the formal lesson uses the single-direction notation z=Xw and W/k have not yet been introduced. The component labels its columns “one unit direction” or “two perpendicular directions” and its dimensions visibly communicate the count, so the learner is not confronted with an entirely unexplained object. However, its caption could directly say “W stores direction columns; k counts them,” or the multi-direction view could be restricted to `more-frame-shapes` and `more-score-covariance`. This is a nonblocking clarity refinement to the previously reported R2, not a new mathematical requirement.

## Route and evidence limits

The revisions preserve the original argument: perpendicular decoding earns squared reconstruction loss; Pythagoras and centering earn score variance; expanding the score earns covariance; stationary candidates are separated from a global eigenbasis bound; orthogonal frames and explicit capacity sums extend the proof to k; SVD returns the same directions and correctly scaled scores. Metric choice and downstream task limitations remain attached to that exact guarantee.

The capacity control now provides a constructive example whose numbers match the exercise, while its caption and proof distinguish that one family of frames from the theorem covering every legal frame. The shape narration now distinguishes its concrete fixture from the later generalization. These changes address the original source-level learning-route objections without shortening the requested derivation.

This reviewer inspected source and written reasoning only. I did not render the current app, operate controls, run Python, listen to notes, observe a human learner, or evaluate retention. The author's separate browser traversal and native-runtime checks must stand on their own recorded evidence. Source repair is not proof of readable rendering, teaching efficacy, or comparative superiority. No numerical score or universal ready claim is supplied.

SHA-256 hashes captured for the principal changed content during this pass:

| File | Hash |
|---|---|
| core.json | 228392ED19F5D85F931B8B439D75D4A85FC9BFFD4FAB8A443B7F17B2405F8148 |
| rank-svd.json | 0308D4B674D3F8F3208BF94F4EE67EAAD01C21AA66AB1665FA3AD66B0C347822 |
| LearningVisuals.tsx | 9A5B1B2A5D18A522BC5F4AE599917AB8E68F5247FCFDFBF5086C3F82C02D2E5F |
