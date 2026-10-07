# Geometry route: research notes

Date: 2026-10-07. Independent proposer; research/teaching-design work, not a novice learning test. Read canonical teaching protocol 3.1 plus research-debate, lesson-design, explanation-depth, explainer-craft and content-contract. No course implementation, publishing, video playback, listening, or full third-party text retained. Candidate IDs below refer to the existing 31-item ledger; first 15 means zero-based indices 0–14.

## Deep written inspections

### G1 — Andrew Ng, CS229 PCA notes

[Primary course notes](https://cs229.stanford.edu/notes-spring2019/cs229-notes10.pdf), pp. 1–6, text inspected throughout. Related to candidate PCA-15; this is a course-family written companion, not proof that the exact video sequence was inspected.

The opening makes redundancy concrete, then uses a direction through a centered cloud to connect projection to a scalar score. The crucial bridge expands the sum of squared scores into a covariance quadratic form. Normalization and dimensions are discussed before application. Compression, visualization, preprocessing and denoising follow. The learner is invited to derive the eigenvector condition with Lagrange multipliers, but the maximum and higher-dimensional guarantee are asserted rather than fully proved here. Adopt the geometry-to-objective continuity. Supply the missing global bound and reconstruction derivation. Avoid a general equation of variance with useful information. No pacing or animation judgment.

### G2 — Jonathon Shlens, A Tutorial on PCA

[Author manuscript](https://arxiv.org/pdf/1404.1100), sections II–V inspected: pp. 1–6, including change of basis, variance/covariance and diagonalization. Additional independently discovered written source, not a video candidate.

One measurement problem persists into notation: several camera coordinates describe one underlying motion. The route asks what a better coordinate system must achieve, then diagonalizes covariance to remove linear redundancy. This gives a strong reason to discuss basis choice and identifies substantive assumptions about signal and noise. It assumes working linear algebra and changes row/column conventions; those are poor fits for a novice main route. Adapt its continuity, not its camera example or artwork. Distinguish the mathematical optimum for squared loss from the empirical hope that dominant variation is relevant signal. Deep text inspection does not establish visual or oral delivery quality. The route's diagonalization proof supports decorrelation; add a separate variational proof for global optimality.

### G3 — Biostatsquid, PCA simply explained

[Creator lesson](https://biostatsquid.com/pca-simply-explained/), opening through interpretation and summary, text inspected. Related to PCA-07. Also screened [creator single-cell lesson](https://biostatsquid.com/a-simple-explanation-of-pca/).

The useful teaching move is a task with too many measured variables to draw, followed by scores, loadings and a scree plot. It stays close to the reader's interpretation needs. However, the lifespan example equates predictor variance retained with lifespan variance explained, which is not warranted. Equal plotted distances do not automatically count more along PC1: actual score units and axis scales matter. The newer companion calls orthogonal components independent; PCA generally supplies uncorrelated scores, not statistical independence. Adopt the question-driven plot reading, but replace these claims with counterexamples. Distinguish illustrative biological interpretations from validated inference. Full video, actual illustrations and audio were not inspected.

### G4 — AssemblyAI, from-scratch PCA companion

[Official source file](https://raw.githubusercontent.com/AssemblyAI-Examples/Machine-Learning-From-Scratch/main/07%20PCA/pca.py), full 63-line file inspected, not executed. Related to PCA-06.

The compact fit/transform division makes the stored mean and reusable basis visible. The path is center, covariance, eigendecomposition, sort, project, then an Iris scatter plot. It offers a useful code-to-symbol mapping but supplies no reconstruction or mathematical warrant. This revision contains a consequential error: the assignment receives eigenvalues into a variable called eigenvectors and eigenvectors into one called eigenvalues. [NumPy's primary API documentation](https://numpy.org/doc/1.18/reference/generated/numpy.linalg.eig.html?highlight=eig) confirms return order. Therefore treat the code as an inspection case, not reusable verified implementation. Our proposed lesson uses `eigh` for covariance demonstration and SVD for a separate implementation, checking shapes, orthonormality, residual and reconstruction. No claim about whether the video itself has this error.

### G5 — Satija Lab, Seurat guided clustering tutorial

[Maintainer tutorial](https://satijalab.org/seurat/articles/pbmc3k_tutorial), compiled 2026-04-28, substantive workflow through PCA, choice of dimension, graph clustering and visualization inspected. Additional primary application source.

This route connects a preprocessing decision to downstream consequences: QC, normalization, selected variable genes, scaling, PCA, neighborhoods, clusters and UMAP. It explicitly discusses uncertainty in choosing component count, rare-cell signals in later PCs and rerunning with different counts. Use this as a decision scene: retaining more total variance is not the same as recovering a rare population, and the first two axes need not be the analysis space. Learner task: identify what was input to PCA and what test could reveal a bad cutoff. Limit: the full biological workflow requires domain knowledge; this masterclass should interpret a documented pipeline, not imply it teaches independent single-cell analysis. No code execution or reproduction was performed.

## Verification and supplementary screening

### G6 — Em Freedman, visual PCA explanation (transcript)

[Candidate PCA-02](https://www.youtube.com/watch?v=5HNr_j6LmPc). After the initial web-access failures, the documented browser transcript exporter succeeded. Read English auto-generated captions 0:02–6:34 throughout; the exported file stays in operating-system temporary storage, outside the repository. This is deep transcript analysis, not visual or oral review.

The sequence starts with a trends question but assumes eigenvector familiarity almost immediately (0:17). Signed rectangle areas connect centered coordinate products to covariance (0:51–1:58), followed by matrix entries, eigenpair ranking, axis change and SVD (2:00–4:32). A hedgehog-feature case then asks what components might mean, making interpretation a hypothesis rather than a automatic label (4:35–6:34). Adopt the cross-product construction, with signs written explicitly and its role in projected variance shown. The transcript asserts covariance eigenvectors give the right axes without deriving optimality, so it does not remove the need for our central proof. Qualify the blanket orthogonality claim: a symmetric matrix admits an orthonormal eigenbasis, but arbitrary vectors in a repeated eigenspace need not be orthogonal. No protected diagrams or script were copied.

- [David Bindel, Cornell CS6210, Variational approaches](https://www.cs.cornell.edu/courses/cs6210/2025fa/lec/2025-11-03.html): actual mathematical text inspected. It expands the Rayleigh quotient in an orthonormal eigenbasis into a weighted average and separately derives stationarity. Primary lecture source for the distinction between an eigenvector candidate and the largest-eigenvalue global maximum. Its matrix pencil and SVD extensions need not enter the beginner route.
- [DINOv2 author-hosted paper](https://pierrefdz.github.io/assets/publis/dinov2/paper.pdf), Figure 1 caption and patch-feature discussion pp. 2, 16–17 inspected as text. PCA reduces learned patch features into three displayed color channels; a preceding threshold separates foreground in their examples. This supports a documented representation-inspection application, not proof that PCA universally discovers objects or semantics. No actual figure pixels were reviewed.
- [IBM explanatory article](https://www.ibm.com/think/topics/principal-component-analysis): substantive article screened as a same-organization written alternative for PCA-10, not an exact transcript. It makes applications visible but makes overly broad benefit claims about relevance and overfitting; do not inherit these as guarantees. [IBM product documentation](https://www.ibm.com/docs/en/db2w-as-a-service?topic=procedures-principal-component-analysis-pca) more carefully states orthogonality and lack of correlation. No inference about the video's precise content.
- [Brunton/Kutz book](https://databookuw.com/databook.pdf): indexed substantive extract of section 1.5 returned, but full open failed. This is partial text screening only, not deep inspection. Its generated cloud offers a known ground truth to compare with recovered directions. No adoption of normalization or singular-vector wording without checking a full current edition.

## Access gaps

Initial YouTube web opens returned errors or tiny non-substantive pages. A later CUA transcript export succeeded for PCA-02 (G6); the same API reported no transcript available for PCA-13. The official Edinburgh Lavrenko slide PDF returned errors twice. Creator notebook directory opens for CampusX and codebasics also failed. The other candidate videos stay discovered/metadata-only in this pass even where a separate written companion was inspected. A search surfaced third-party transcript pages, but their text was not used as technical authority or treated as creator-verified captions. No popularity/learning/animation rankings were created.

The research supports a provisional geometry route and exposes missing obligations. It does not complete the requested audiovisual comparative review. See `candidate-access.json` for per-candidate access and `route-proposal.md` for the original synthesis and falsifiable pilot.

## Extended screening pass

After the independent proposal, the coordinator requested broader transcript attempts. The IAB connection was no longer available; the enabled Chrome connection supplied the same documented transcript exporter. Each remaining exact candidate URL was attempted. PCA-01 succeeded. PCA-03, 04, 05, 06, 07, 08, 09, 10, 12, 14 and 15 returned unavailable; this means unavailable through this attempt, not proof that captions cannot be accessed elsewhere. PCA-11 was not duplicated because the coordinator reported an unavailable transcript and inspected actual frames at 6:35 and 7:00. That evidence belongs to the coordinator, not this agent. PCA-02's prior success and PCA-13's prior unavailable result complete the assigned access-attempt coverage. No new audiovisual quality claim follows.

### G7 — StatQuest short PCA introduction (transcript)

[PCA-01](https://www.youtube.com/watch?v=HMOI_lkzW08). English auto-generated captions exported outside the repository and read throughout, 0:00–6:01. The initial task distinguishes externally similar cells through many gene measurements (0:27–1:23), then grows pairwise comparisons into an unwieldy many-axis problem (1:32–3:34). A PCA plot is offered as the overview. The task has visible purpose and a compact payoff, but the route does not derive a variance objective or eigenvector solution. The interpretation passage at 4:27–5:06 ranks differences along PC1 more strongly than comparable plotted distances along PC2; the course must qualify this with score units and plotting scales. Correlation language also needs care: PCA's default geometry concerns the chosen centered/scaled feature space, not a universal sample-correlation distance. Adopt the progressive failure of separate two-variable views as an optional application entry. The transcript does not establish the exact plotted scales, animation quality or delivery. It is an introductory comparator, not a full-promise competitor.
