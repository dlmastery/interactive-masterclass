# PCA route synthesis

7 October 2026. Provisional authoring decision based on independent source research and crosscritique. No human learning study, comparative preference result, or full-course runtime result is claimed. The initial six-scene native pilot is a delivery/bridge prototype, not fulfillment of the full course.

## Decision

Use a stable same-unit geometric case and make reconstruction error the explicit opening criterion. Derive retained variance from a pointwise right triangle, covariance from squared scores, eigenvectors from constrained stationarity, and global optimality from a spectral-basis bound. Reach the complete one-direction global proof by approximately scene 35. Preserve 84–100 scenes as the current full-course planning scope, with room to split or revise where the learning obligations require it; count is not the acceptance test.

The geometry and statistics proposals independently converged on this main route. They are two research perspectives on substantially the same strategy, not two materially different routes that were experimentally compared. Their agreement supplies reviewable reasoning, not learning evidence. Both strongest objections remain open: reconstruction may overemphasize compression, and a chosen squared-distance metric may look inevitable unless the lesson explicitly earns and later challenges it.

Research basis and source-access limits are in [geometry analysis](research/geometry/source-analysis.md) and [statistics analysis](research/statistics/source-analysis.md). The detailed initial proposals and objections remain intact in [geometry route](research/geometry/route-proposal.md), [statistics route](research/statistics/route-proposal.md), and [statistics crosscritique](research/statistics/crosscritique.md). The [derivation audit](research/statistics/derivation-audit.md) specifies proof obligations without claiming they are already authored.

## A serious competing route

The covariance/decorrelation route begins with redundant scientific measurements: a simpler coordinate system may separate variation that the original sensors mix. It develops covariance, finds an orthogonal basis with diagonal score covariance, orders those axes, and then establishes variance/reconstruction equivalence.

Its advantage is that coordinate change and scientific measurement are the first-class purpose; it does not make compression the only motivation. Its strongest weakness is that decorrelation alone does not justify dropping dimensions or establish which approximation is best. It still owes the complete objective, unit constraint, global proof, and task-relevance qualifications. Shlens's tutorial provides substantive support for this alternative; it is not a hypothetical straw route.

Current selection is provisional. If opening pilots show that readers understand measurement redundancy and coordinate change but do not see the point of reconstruction, test this competitor on the same audience, prerequisites, learning obligation, and bounded time. Do not call a full course better than a short introduction because it contains more topics. No such comparison has yet been executed.

## Main route and protected attention

| Planning scenes | Inference obligations | Exit evidence |
|---|---|---|
| 1–7 | One coordinate encodes a point using a shared ruler and center; show original, score, reconstruction, residual. State the practical payoff and chosen loss. | Decode a fresh point; distinguish direction from score. |
| 8–14 | Centering, closest-point projection, unit length, fixed total squared length, and retained/lost split. Define variance when the centered score energy makes it useful. | Explain why an arbitrary longer arrow is not a fair improvement and why translation does not change centered directions. |
| 15–22 | Expand a two-feature squared score, expose its cross-term, build covariance entries, generalize to XᵀX/(n−1), justify symmetry and nonnegative quadratic forms. | Rebuild a covariance entry and explain opposite tilts with equal marginal variances. |
| 23–28 | Relate a small rotation to the tangential component of Cw. Introduce gradients/Lagrange multipliers in place; identify eigenpairs as stationary candidates. | Reject the minor eigenvector as a maximum despite satisfying Cw=λw. |
| 29–35 | Invoke the symmetric spectral theorem explicitly; expand any unit direction; derive the weighted-average bound and equality cases; return to minimum reconstruction. | Reconstruct the general bound, not merely manipulate a two-value slider. |
| 36–47 | Sign/ties/eigengaps, several directions, orthogonal projectors, joint top-k bound, omitted-eigenvalue error. | Distinguish basis and subspace; prove why the joint optimum is obtained. |
| 48–57 | SVD identity, shapes, score/loadings convention, finite rank, train/transform/inverse, numerical and code verification. | Trace one observation through implementation and diagnose a sign or orientation mismatch. |
| 58–68 | Scaling changes the metric, whitening changes relative score scale, component-count criteria, validation, small but relevant directions. | Defend a loss and metric; reject a universal explained-variance threshold as a task guarantee. |
| 69–80 | Outliers, curved data, sample/population distinction, instability, duplicate features, leakage/drift; qualified repairs and objective-matched alternatives. | Name a mechanism, diagnostic, mitigation and residual cost for each proposed decision. |
| 81–90 | Documented contemporary workflows and held-out transfer: biological feature/PC inspection, yield changes and temporal evaluation, a new notebook case. | State what data axes mean, what was fit, what was validated and what cannot be inferred. |
| 91–100 as needed | Six-lens translation, proof reconstruction, comparative-method judgment and research-design branches. | Explain upward into justification and back in ordinary language, on changed examples with reduced assistance. |

This allocation moves the global proof forward relative to the geometry proposal's initial 51–57 placement. That change is a planning judgment responding to the user's derivation emphasis, not measured superiority. Keep the visual construction; use focused refresher branches and remove repeated exposition before removing mathematical warrants.

## Hardest bridge and representation rules

Maintain stable identities for x, w, z=xᵀw, reconstructed point zw, and residual x−zw. Teach each as an operation before using it as shorthand. A drawn arrow length must state whether it is unit direction, standard deviation, eigenvalue, or a rescaled display; those are not interchangeable.

Test Cw as a sum of data directions weighted by their projected scores. If that adds too many simultaneous objects, isolate one contribution and then sum. A tangential component explains the possibility of improvement. The Lagrange condition then names the same restriction. Do not claim it establishes maximality.

For global optimality, show qᵢᵀCqⱼ=λⱼqᵢᵀqⱼ before deleting cross-terms. Perpendicularity alone does not diagonalize an arbitrary quadratic form. Explain that squared eigenbasis coefficients are nonnegative and sum to one because w has unit length. Equality describes the top eigenspace, including ties. This explanation must be visible in the core and spoken notes; it cannot live only in a hidden appendix.

## Native pilot and remaining evidence

The root's initial prototype in `v/lesson/src/course.ts` contains opening, covariance, global-bound, and notebook-interaction scenes. It can test rendering, interactions, terminology and local explanatory moves. As written, separated pilot scenes omit intermediate context, including projection/variance derivation and stationarity. Supply their immediate context before treating any learner response as a test of the whole inference chain.

A falsifying pilot asks neutral tasks: encode and decode a new point; derive the mixed term; identify a stationary minimum; reconstruct the eigenbasis inequality and equality case; choose a criterion when target signal lies in a small-variance direction. Require scene-specific warrants from expert or AI reviewers. Record assistance, prior knowledge, navigation, task time, correctness and confidence separately. A slider result is not learner reasoning. Human transfer, delayed retention and comparative preference remain unmeasured.

The complete package still requires all native slides and editable notebook, synchronized exact speaker notes, source-linked application/alternative claims, full visual/oral review where claimed, actual runtime verification, and final coverage/continuity audits. Video metadata discovery is distinct from substantive transcript, pixel and audio access. Unavailable media remains an explicit research gap. Research reopens if a pilot exposes an unsupported bridge or practical claim.
