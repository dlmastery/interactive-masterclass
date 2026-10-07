# Statistical route research

Researcher: fresh-context route proposer, 7 October 2026. This is research and a teaching hypothesis, not novice learning evidence. No video pixels or audio were reviewed. Text evidence cannot support claims about animation, pacing, or voice. Notes below are brief paraphrases. No protected visual assets or full transcripts are copied here.

## Access record

Read the canonical skill and its research-debate, lesson-design, explanation-depth, and explainer-craft references. Assigned zero-based candidate indices 15–30: PCA-16 through PCA-31. The other 15 entries retain metadata-only status for this pass. Primary YouTube direct opens for 14 assigned candidates returned fetch errors, throttling, or empty page shells. Browser transcript fallback recovered PCA-18; the other 13 returned no transcript available and remain discovered, not screened. Three video candidates received substantive transcript inspection: PCA-18, PCA-24, and PCA-28. Separate written sources fill subject coverage; they do not increase the video-review count. See `candidate-access.json` for individual results.

Serrano access used an existing local auto-generated transcript export, not a fresh caption retrieval. Inspected 0:00–1:00, 6:48–11:46, 14:16–26:30; intervening returned output was incomplete and is not claimed as read. MIT transcript inspection covered PDF pages 1–11, focusing on pages 1–7 and 9–11; the later pages were not deeply inspected. Other PDFs were read through extracted text. PPCA PDF text was corrupt; screenshot fallback failed, so only its abstract is substantiated here.

Local export identifiers, retained outside the public research package: Serrano `youtube-g-Hb26agBFg-5064ddee-d61f-4fd1-b89c-4693a808e3fa.txt`; Krohn `youtube-t5UA3xWDGZI-ace15aea-9f49-40df-83b2-077405aa7ceb.txt`. Both reside in the browser-use temporary exports folder. Export success is not video playback. Browser fallback was sequential in a separate hidden research tab and did not use the coordinator's tab.

## Deep source analyses

### S1 — A geometric need for covariance

[Luis Serrano, PCA](https://www.youtube.com/watch?v=g-Hb26agBFg), PCA-24; local auto-caption export. The camera question gives projection a purpose. At 8:29–10:40, equal marginal variances fail to distinguish opposite tilts; signed coordinate products supply the missing measurement. At 14:16–20:14, a concrete transformation precedes the eigenvector name. At 20:50–26:02 the pieces form the PCA procedure.

Teaching adaptation: retain the insufficiency contrast, then derive the cross-term from a projected score's square so covariance is both motivated and necessary. Ask learners to distinguish opposite tilts before calculation. Prerequisite: coordinates, signed multiplication, and averages. The mathematical bottleneck is why eigenvectors optimize the stated goal; the transcript gives useful direction language but does not furnish our required global proof. Its broad information-retention wording needs qualification. The analogy also risks confusing camera sightline with the retained axis. We should explicitly mark them perpendicular. No claims about the video's actual visual execution or narration quality are supported by this inspection.

### S2 — Reconstruction earns the variance objective

[Cosma Shalizi, Principal Components Analysis, 2019 lecture](https://stat.cmu.edu/~cshalizi/dm/19/lectures/05/lecture-05.html). Inspected projection/reconstruction sections, optimization, covariance properties, score interpretation, low-rank approximation, and cautions about interpretation; page sections through low-rank approximation, including extracted lines 20–172 and 368–377.

The key sequence asks for the closest linear approximation, expands squared residuals, drops a fixed term, then identifies projected variance and the covariance quadratic form. This earns the objective rather than equating spread with usefulness by fiat. The derivation assumes centered data and uses divisor n. It then applies Lagrange multipliers and identifies the leading eigenvector.

Adaptation: keep the reconstruction accounting, but show explicitly that stationarity does not select the maximum; follow with a spectral-basis bound. Ask the learner to supply why the fixed term can be ignored, and why all stationary directions cannot be maxima. Add the centered rank bound min(n−1,p), which is sharper than the lecture's stated at-most-n bound. The interpretation caution is valuable: domain meaning and uncertainty do not follow from a decomposition alone. The whole route still presumes more algebra than the novice opening.

### S3 — A scientific measurement story, with visible assumptions

[Jonathon Shlens, A Tutorial on Principal Component Analysis](https://www.cs.cmu.edu/~11755/lectures/pca.pdf). Inspected PDF pages 1–3 and 5–9: spring/camera motivation, change of basis, covariance diagonalization, assumptions, SVD construction, and nonlinear failure example. Did not inspect the appendix proofs in full or actual rendered figures.

The tutorial asks how redundant measurements can reveal a simple underlying motion. It develops a basis change, decorrelation, ordered variance, and then SVD. The SVD discussion carefully connects a scalar relation to stacked matrices. Its explicit large-variance-means-interesting-structure assumption creates a useful later challenge. It uses features as rows, unlike the proposed course; copy no formulas without translating dimensions.

Adaptation: use an original two-sensor measurement example, maintain one row convention, and show the SVD identity next to dimensions. Learners predict what a duplicated sensor and a rescaled sensor will do. Do not import the empirical assumption as a mathematical requirement for PCA's finite-sample optimum: that optimum needs no Gaussian/noise model. The failure case motivates nonlinear alternatives, but manifold choice needs additional evidence and assessment. Its assumed working linear algebra makes it a substance reference, not the opening's prerequisite contract.

### S4 — Stability, units, and a consequential application

[MIT OCW, Stefan Andreev, Lecture 9 transcript](https://ocw.mit.edu/courses/18-642-topics-in-mathematics-with-applications-in-finance-fall-2024/1W7E-UsRG0zyYe1J1vHunh3QNejR5wd7v_transcript.pdf), [video](https://www.youtube.com/watch?v=CechARGinR4), PCA-28. Inspected printed pages 1–11, particularly geometric examples, eigenvalue proximity, centering/scaling, temporal windows, and yield-change loadings.

A perturbed point distinguishes a stable elongated cloud from an unstable nearly round cloud. The lecture connects this to eigenvalue gaps, then to repeated estimation through time. Yield changes give same-unit variables, interpretable loading shapes, and a practical reason to preserve relative volatility. It assumes the class already had PCA mathematics.

Adaptation: after proving the optimum, shrink the eigenvalue gap and ask what can remain stable when individual directions move. Introduce out-of-sample reconstruction and temporal validation. Do not turn the lecture's preferred gap heuristic into a universal threshold. Transcript slips include product instead of sum for total variance and a claim that PCA is not optimization, contradicted by later distance-minimization discussion. These require correction, not repetition. Lecture-era interest rates and reported variance shares are historical context, not current market facts. A PCA factor is descriptive, not a causal mechanism or investment recommendation.

### S5 — Current application with a useful counterexample to automatic k

[Satija Lab, Seurat guided clustering tutorial](https://satijalab.org/seurat/articles/pbmc3k_tutorial.html), page compiled 28 April 2026; accessed 7 October 2026. Read normalization/feature selection context, scaling, RunPCA, loading inspection, component-count discussion, and graph clustering sections. This is a primary current workflow, separate from candidate PCA-20's inaccessible video.

The workflow uses scaled selected features, inspects gene loadings and score heatmaps, then uses PCA coordinates downstream. Component count is an uncertain decision: the example notes rare immune subsets in later PCs and asks users to vary the count. This is much stronger teaching evidence than a generic claim that PCA is used in biology.

Adaptation: a domain transfer scene presents a high explained-variance cutoff alongside a rare group lost by that cutoff. The learner must request marker/feature evidence and a sensitivity analysis. Prerequisites include what cells, genes, and the matrix axes represent; teach only enough domain context to decide. Limits: this is a worked workflow, not a universal guarantee that high variance is biological signal. Scaling, normalization, and feature selection change the question. We did not run Seurat or validate a biological conclusion.

### S6 — Optimal compression can lose predictive information

[scikit-learn, PCR versus PLS example](https://scikit-learn.org/stable/auto_examples/cross_decomposition/plot_pcr_vs_pls.html), accessed 7 October 2026. Read purpose, data construction, train/test pipeline, one-component comparison, and two-component resolution. No code execution or figure-pixel review in this pass.

The example constructs a target aligned with a low-variance direction. PCA ignores target values; truncation can remove the direction the regression needs. PLS provides a supervised comparison, while retaining both PCs resolves this particular loss. This is a deliberate counterexample, not evidence that PLS generally wins.

Adaptation: use a new deterministic sensor fixture with a small but target-relevant contrast. Ask which objective each method sees, then compare held-out target loss with held-out reconstruction loss. This closes the opening's promise without making variance synonymous with information. The strongest learner work is explaining why a mathematically correct algorithm can answer the wrong question. The source assumes regression and model validation, so those need brief in-place refreshers. Its plotted component arrow lengths encode variance; our geometric directions should stay unit length and use a separate variance scale.

## Focused primary checks and limits

### Additional candidate screening — Jon Krohn, PCA-18

[Topic 40, Principal Component Analysis](https://www.youtube.com/watch?v=t5UA3xWDGZI). A fresh CUA export supplied auto-generated English captions; read the full returned 0:00–8:24 transcript. The lesson explicitly delegates derivation to Goodfellow et al. section 2.12, then demonstrates Iris matrix shapes, a two-component fit, and a score plot. At 6:19 onward it reveals labels only to color the already-computed representation. Useful adaptation: make “labels were not input” visible, and check rows remain observations while feature count changes. Learner obligation: distinguish exploratory separation from a trained classifier. It assumes earlier linear-algebra lessons; it cannot supply this course's missing proof. Its equation of variance with importance/data structure must be task-qualified. No visual, oral, or code-execution claim follows from the transcript. This is screened rather than counted among the six deep source analyses above.

- [Candès et al., Robust Principal Component Analysis?](https://arxiv.org/pdf/0912.3599): read introduction and sections 1.3–1.4, including low-rank/sparse identifiability and theorem assumptions. Low-rank plus sparse decomposition is one mitigation for gross corruption. Recovery claims require conditions, including incoherence and a suitable corruption pattern; a matrix that is both sparse and low rank makes the split ambiguous. Do not label any outlier procedure “RPCA” or promise universal denoising. Full proof and later experiments not deeply reviewed.
- [PCA API](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html): primary current solver/preprocessing reference; page reports version 1.9.1. Current documentation is not the installed-runtime version. Course code must verify its actual environment. Centering and feature scaling are separate choices. Use SVD identity checks and avoid teaching a covariance matrix as a mandatory implementation step.
- [Common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html): primary reference for learning preprocessing only on training data and composing transformations in a pipeline. Validation must match the task; time-dependent data may need temporal splits.
- [Tipping and Bishop, PPCA](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/bishop-ppca-jrss.pdf): abstract accessed. Full extracted PDF text is corrupt; screenshots unavailable. Its probabilistic latent-variable formulation is identified, but detailed assumptions, EM derivation, and likelihood proof require another readable primary copy before a research-depth branch is authored.
- StatLect PCA URL and Data Driven Science & Engineering PDF opens failed. No deep-reading claim for either. Primary papers and lectures above supplied the audited route's evidence instead.

## Research changed the proposed design

1. S1 motivates covariance with an insufficiency; our own projected-square expansion then explains why that exact quantity appears.
2. S2 replaces “spread means information” with an explicit error criterion, followed by a separate global bound.
3. S3 makes SVD an equivalent computation and makes assumptions visible; preserve row conventions throughout.
4. S4 moves stability and units into the main story, immediately after optimality.
5. S5 and S6 prevent component-count heuristics from masquerading as task guarantees.

Unresolved evidence: no oral/visual review of these video candidates, 13 assigned videos lack substantive access, no human learning or comparative preference observations, no executed notebook/application claims. These are precise limits, not inferred source-quality judgments.
