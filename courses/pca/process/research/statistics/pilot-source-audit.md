# Six-scene pilot source audit

7 October 2026. Read-only review of `v/lesson/src/math.ts`, `Visuals.tsx`, and `course.ts`. No frontend edits. This is source-level mathematical/teaching review, not rendered visual inspection or runtime verification. It reviews the six-scene snapshot present at inspection, not future expanded content.

## Findings needing attention

1. **Inconsistent formula after the equal-eigenvalue toggle.** `global-pilot` fixes its scene formula at V=6a₁²+(2/3)a₂²≤6. `Mixture` changes the second eigenvalue to 6 when the tie toggle is active. Its internal formula and feedback change correctly, but the scene formula cannot follow that local state. If both are displayed, the reader sees contradictory assumptions. Make the outer formula symbolic (λ₁a₁²+λ₂a₂²≤λ₁), synchronize the state, or hide the fixed example while the tie state is active. This is a concrete source inconsistency, not a request for more styling.

2. **One missing proof warrant in global notes.** The notes say cross-terms vanish because the basis is perpendicular. They also need Cqⱼ=λⱼqⱼ, so qᵢᵀCqⱼ=λⱼqᵀqⱼ=0 for distinct basis indices. Perpendicularity by itself does not make the cross-terms of an arbitrary quadratic form vanish. Add this relation with a learner-visible connection; do not simply lengthen the spoken symbol reading.

3. **The six-scene pilot does not yet test the complete hard bridge.** It jumps from score language to covariance and then to a proof whose notes refer to a previously established stationary candidate. The needed centering→score variance, projection identity, covariance quadratic form, and stationarity scenes are absent in this snapshot. This is acceptable as a rendering probe, but it cannot establish the intended causal sequence for a fresh learner. Add immediate context to the pilot or label it explicitly as separated excerpts.

4. **Undefined variance enters the opening instrument.** The first learner-facing interaction already shows kept/lost variance in cm² before the course defines variance or the divisor. A novice can compare gaps, but may interpret the two numbers as raw average squared distances. Consider opening with recovered points and an explicit error description; reveal normalized variance quantities when earned, or explain their normalization in a small accessible detail. This is a pedagogical risk to pilot, not a numerical error.

5. **Derivative visual needs scale clarity if promoted into the core.** `Eigen` draws the unit vector with scale 85 and Cw with scale 28. Its caption says separate labeled scales, but the drawing supplies labels w (unit) and Sw without numeric scale legends. Direction comparison remains valid; a learner must not infer an eigenvalue from the apparent ratio of lengths. Use direction-only framing or explicit scale labels. Source notes alone do not verify how the rendered arrows are perceived.

## Correct mathematics in the reviewed fixture

RAW points are (8,7), (7,8), (5,4), (4,5). Their mean is (6,6). Centered points are (2,1), (1,2), (−1,−2), (−2,−1). The code correctly computes sample covariance [[10,8],[8,10]]/3, eigenvalues 6 and 2/3, and the 45° principal line. A and B have equal signed scores at 45°, so the opening collision illustrates lost detail correctly. At 135° the stationary line is the minimum-variance direction. This independently recomputed arithmetic supports the fixture, not the whole code for arbitrary input.

`model` uses cosine/sine to keep w unit length and computes projection/reconstruction/residuals consistently. Its kept variance plus loss equals trace(C), with both terms normalized by n−1. The “lost variance” label can be justified as total residual variance for centered residuals, but it should not silently be described as mean squared error with divisor n. The `bestAngle` half-angle formula is correct for this symmetric 2×2 covariance; at equal eigenvalues its returned angle is one arbitrary optimum, not a unique direction.

`Covariance` mirrors the second coordinate about the fixed mean and preserves both marginal variances while reversing covariance. Its cross-term arithmetic is correct. The signed product prediction is a genuine reasoning opportunity, though selected-product hiding does not enforce an attempt; assess learner explanation separately from clicks.

`Mixture` correctly uses nonnegative squared weights, a constant sum of one, and a weighted eigenvalue average. Its caption notes square roots and sign invariance, preventing an important “coefficient equals weight” confusion. The all-directions claim still depends on the eigenbasis argument; the slider illustrates that argument rather than proving it.

The 2D derivative formula dV/dθ=2tᵀCw is correct when t=(−sinθ,cosθ) and θ is in radians. Its sign feedback agrees with local increasing/decreasing variance. The UI's degree control is consistent because the derivative caption explicitly says per radian.

## Follow-up acceptance

After repairs, inspect the tied state, zero-weight endpoints, covariance-sign flip and score collision in the actual renderer. Verify the notebook's data/mean/control outputs agree with the plotted data, not merely the fixed JavaScript fixture. For teaching review, use the five neutral tasks in ROUTE-SYNTHESIS.md and require visible warrants. No runtime, oral pacing, accessibility or actual learning claim is made by this source audit.
