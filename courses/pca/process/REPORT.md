# PCA rebuild: delivery and evidence report

7 October 2026. Status: **84-scene reviewed course candidate, implemented and runtime-tested**.

The course is at [courses/pca](../README.md) in the public [interactive-masterclass repository](https://github.com/dlmastery/interactive-masterclass). The prior course, retrospectives, skill deltas, and generated artifacts remain preserved. This report concerns the new course only. It does not relabel the earlier course as successful.

## What changed in the teaching

The earlier failure was a failure of route and evidence: prerequisite coverage displaced the actual PCA problem; visible activity was too easily treated as useful interaction; derivation and explanation quality were asserted without enough review of what the learner would actually see. This rebuild begins with one shared ruler and four measured points. It asks what one coordinate can preserve, what the decoder needs, and what detail is lost. The learner can rotate the ruler and inspect original and recovered points before meeting the covariance formula.

The same fixture survives the first mathematical argument. Its mean is (6,6); centered points are (2,1), (1,2), (−1,−2), and (−2,−1). Its covariance is [[10,8],[8,10]]/3. At 45 degrees, retained variance is 6 and normalized squared loss is 2/3. At zero degrees, each is 10/3. These values anchor the geometry, algebra, code, and runtime checks.

The route earns each new object:

1. A shared direction and scalar score define an encoder and decoder.
2. The perpendicular foot minimizes point-to-line error. Pythagoras makes retained and discarded squared distances add to a fixed total.
3. Centering makes the scores have zero mean. Variance becomes the retained squared-distance measure. A unit constraint prevents a fake improvement by lengthening the direction vector.
4. Expanding a squared score introduces the cross-product. Covariance is the summary needed to evaluate every direction, not an unrelated statistics chapter.
5. The quadratic form connects the visible summary to matrix notation. The affine mean proof returns after projection and matrix operations are available, and explicitly cancels the cross-term.
6. A sideways improvement introduces the tangent condition. The gradient and Lagrange argument identify eigenvector candidates. A minimum also passes that condition, so it cannot close the proof.
7. An orthonormal eigenbasis turns retained variance into a weighted average of eigenvalues. The largest eigenvalue bounds every direction. Equality, ties, and sign ambiguity are explained. This complete rank-one global argument arrives at scene 32.
8. Orthogonal frames extend the construction to k dimensions. Capacity weights lie in [0,1], sum to k, and yield the top-k bound. The discarded eigenvalue sum measures normalized reconstruction loss. SVD supplies the same directions, scores, and scaling.

The spectral theorem and existence of SVD are named background results. Their full foundational proofs are not supplied. The optimization guarantees that rely on them are derived rather than replaced by an animation or stationary-point assertion.

## Coverage and participation

The eight chapters contain 84 scenes, 31 diagnostic multiple-choice tasks, 17 open-reasoning rubric scenes, eight chapter recall tasks, and 113 authored mathematical steps. The [coverage map](COVERAGE.md) maps requirements to scenes. The [speaker notes](../SPEAKER_NOTES.md) contain exact scripts and cues for every scene, totaling approximately 8,265 words. These are content counts, not measures of learning.

Interactions include rotating the retained direction, inspecting point contributions, hiding and revealing a signed covariance product, flipping tilt while keeping marginal variances fixed, allocating eigenbasis weights, constructing a legal two-dimensional frame, changing measurement units, revealing target labels, adding an outlier, comparing linear and curved structure, diagnosing code, and reconstructing explanations. Equation reveals expose a reason for each step. They are supplemented by construction and counterexamples, rather than serving as the only interaction.

Practical scenes distinguish the proven objective from the user's actual task. They cover units, standardization, weighted error, whitening, k selection, held-out validation, leakage, reuse of a fitted mean/basis, sparse data, numerical identities, nuisance variation, outliers, robust-model assumptions, nonlinear alternatives, instability, duplicated features, and causal overinterpretation. Documented applications include Seurat's single-cell workflow and DINOv2 feature visualization. These applications were interpreted from primary material; the underlying biological or vision pipelines were not reproduced.

Six explanation lenses ask the learner to reconstruct the idea for different levels of readiness. Age labels do not determine readiness. The advanced tasks ask for proof, counterexamples, evaluation design, and claim auditing. Open responses have authored self-review rubrics and examples. They are not sent to an AI grader. Drafts persist during navigation but are lost on reload; this is stated in the interface and README.

## Research and route selection

The process considered 31 video candidates, divided between independent geometric and statistical researchers. Access records distinguish metadata discovery, transcript inspection, written companions, actual video frames, and listening. Five candidates received substantive transcript inspection across the research passes. Many others remained inaccessible beyond metadata after direct and browser attempts. Two StatQuest projection frames, around 6:35 and 7:00, were visually inspected without listening. It would be false to say that 31 complete videos were watched or that their oral delivery was compared.

Complementary written sources included Shlens, Shalizi, CS229, Cornell variational notes, NumPy and scikit-learn documentation, Seurat, and primary research on robust PCA and DINOv2. Research notes include detected weaknesses in source claims, not just admired techniques. They distinguish uncorrelated from independent, retained variance from prediction value, and mathematical optima from assumptions about signal. Prior Welch Labs teaching-pattern research remains in the version 3.1 skill bundle; it was not counted as a new full-video inspection.

Both independent proposals favored a reconstruction-led route. A covariance/decorrelation-first route was kept as a substantive alternative, and the synthesis records the tradeoff. This is convergence of AI proposals, not evidence of a blind tournament winner. The selected route fit the user's demand to begin with PCA's purpose and geometry. See [synthesis](ROUTE-SYNTHESIS.md), [geometry evidence](research/geometry/source-analysis.md), and [statistical evidence](research/statistics/source-analysis.md).

## Review findings and actual repairs

A fresh-context AI reviewer inspected the course source without having authored it. Subsequent rechecks received the repair list and were therefore targeted, supervised rechecks rather than new blind reviews. The reviewer belongs to the same model family; independence of authorship is not independence from shared model biases. The original findings and both rechecks are retained in [review/](review/).

| Finding | Repair and evidence |
|---|---|
| A tail-loss scene used a visual fixture different from its exercise | Give the scene its own spectrum (12,5,2,1), n=5, and both normalized loss and raw SSE. At k=2 these are 3 and 12. |
| Rank scenes silently lost their authored proof steps in dispatch | Route rank scenes with steps to the proof renderer. Restore the small matrix and null-space grounding. |
| Tangent improvement was described without the promised geometric object | Draw the tangent and sideways component of Sw. |
| Top-k capacity was algebra without a matching construction | Show a legal frame with weights (1,1−p,p,0), k=2, and capture 17−3p. Distinguish this example family from the general theorem. |
| The key capacity sum and trace relationship needed a warrant | Display the sum of squared basis coordinates and connect each score variance to the diagonal of WᵀSW. |
| Matrix-shape narration and notation timing disagreed with the visual | Use the actual four-by-two fixture, name the later eight-feature exercise separately, and remove the multi-direction renderer from the earlier data-matrix scene. |
| The mean proof appeared before its scaffold and omitted the zero cross-term | Move it after the outer-product/matrix discussion and display the zero-sum step. |
| A NumPy residual check compared incompatible shapes | Use scalar sums on both sides; hide the example until the learner has attempted the task. |
| Too much participation depended on reveals | Add eight chapter-specific recall tasks and retain geometry, construction, diagnosis, and transfer tasks. |
| Notebook return failed without current authentication | Start an authenticated editor, keep its generated URL in ignored local runtime files, and put the correct link in the trusted outer presentation page. |
| Narrow layouts overflowed; scene navigation retained scroll position | Stack the narrow geometry view, allow formula-local overflow, and reset scene scroll on navigation. |

Recheck 2 found no remaining P1 mathematical or dispatch blocker within its source scope. Its minor notation-timing residue was repaired afterward by restricting the multi-direction renderer. Final type checks, formula tests, and browser traversal cover that change. None of these checks establishes that every learner will follow the proof.

## Runtime and verification

This is a native marimo-studio 0.2.3 view attached to a Python notebook, using its React/Reveal provider, cell controls, and projected values. It is not a separate imitation of the Studio interface. Most controls calculate immediate illustration states from the fixed notebook fixture. Scene 71 embeds native marimo controls and receives recomputed Python values. The editor and full presentation are separate server sessions; their control values do not synchronize with each other.

Final verification on Windows/Chrome:

- **15 Python tests passed:** mathematical identities, 3,077 native control combinations, payload bounds, and notebook-link/authentication composition. Maximum combined model/live payload: 7,177 bytes.
- **Two Deno tests passed:** authored formulas render, narration/feedback contracts hold, and browser geometry agrees with 24 independently generated NumPy fixtures. These fixture comparisons are mathematical checks, not browser-automation tests.
- **Deno type checking passed.** Notebook structural check and isolated execution also passed in the earlier framework pass.
- **Production build completed with exit code 0.** Final bundle SHA-256: `4d22322902aff6dbd5e97b4881e37e7cdc7d2af2f7439e18cc948f4f41235d3a`.
- **84 final scene entry states traversed in the real browser:** each had a title, populated visual container, and zero rendered KaTeX errors. Navigation reset each scene to its top. See [raw traversal](runtime/browser-traversal.json). This is not an 84-scene screenshot or interaction audit.
- **Representative controls operated:** covariance sign/variance changes, eigenvalue ties, top-k capacity, discarded-tail accounting, unit scaling, native Python angle/outlier recomputation, notes, chapter recall, and navigation-persistent explain-back drafts. Test drafts were cleared.
- **Responsive checks:** the opening's 390-pixel viewport had scene width and scroll width both 375 pixels after repair; 760-pixel layout and normal desktop layout were also inspected. This does not establish full mobile accessibility for every scene.
- **Clean launcher test:** start hidden editor and presentation processes, open slides, follow the authenticated notebook link, observe editable cells with Studio status **Live**, then use the notebook link to reopen the presentation. Earlier restored-runtime recovery using Run all was also exercised.

Screenshots: [opening](runtime/opening.jpg), [covariance](runtime/covariance.jpg), [native notebook and Studio](runtime/native-studio.jpg). Final source hashes are in [source-hashes.json](runtime/source-hashes.json). Earlier framework receipts retain their original scope and hashes; they must not be mistaken for tests of later revisions.

The pinned framework emitted a Windows temporary-directory cleanup traceback after reporting build success and returning exit code 0. The resulting production bundle was served and tested. The launcher and README preserve this qualification. Authentication, iframe sandbox attributes, and CSP protections were not disabled to repair notebook navigation. Local login URLs and process records are excluded from publication.

## What remains unproven, and the next evaluation loop

The user asked for exceptional teaching, not merely more slides. This build is a concrete candidate toward that goal. Human comprehension, delayed retention, comparative learning against leading tutorials, spoken delivery, and audience reach remain unmeasured. There is no defensible improvement multiplier or prediction of millions of views.

The prose uses short, direct sentences, but the requested 80% ASD-STE100 compatibility target is not certified. [Mechanical measurements](language-measurements.json) are explicitly not a vocabulary or usage audit. External fonts and KaTeX CSS currently need network access. The Windows launcher was tested; cross-platform launching, full offline operation, exhaustive accessibility, and narrated audio were not.

The next evaluation should use independent learners with known starting skills. Before exposure, ask them to predict a projection, explain covariance's role, distinguish an eigenvector condition from a global proof, and select preprocessing for a practical case. Observe where they stall without prompting. After exposure, use structurally different cases rather than the memorized four-point fixture. Repeat selected tasks after a delay. Compare matched objectives and learning time against a selected source lesson; do not compare only visual polish or slide count.

The outer authoring loop changes the route when failures cross scenes or the objective itself is unclear. The inner explanation loop repairs a specific missing inference or representation, then retests a fresh case. Learner practice selection and learner step feedback remain distinct: selecting the next task is different from helping on the current attempt. This course implements authored choices, retrieval, and self-review; it is not yet an autonomous adaptive tutoring system. A future tutor can use these records, but should not claim adaptive teaching merely because a text box exists.

The delivery is complete as an authored and tested course. The educational claims remain bounded by the evidence above.
