# PCA derivation audit

Original proof checklist for the proposed course, 7 October 2026. This specifies what the explanation must establish; it does not certify slides not yet authored. Foundational cross-checks: [Shalizi's lecture](https://stat.cmu.edu/~cshalizi/dm/19/lectures/05/lecture-05.html), [Shlens's tutorial](https://www.cs.cmu.edu/~11755/lectures/pca.pdf), and [scikit-learn's current PCA definition](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html). Use the course's notation consistently even when a reference transposes observations and features or uses a different variance divisor.

## Objects and purpose

- [ ] Real data A has n rows (observations) and p columns (features), n≥2. The mean μ is p-dimensional. Center X=A−1μᵀ; column sums vanish. A point xᵢ is written as a column when discussing geometry, while its transpose is row i of X. State this once visibly.
- [ ] Define sample covariance C=XᵀX/(n−1), shape p×p. Dividing by n changes eigenvalues and sample-variance normalization, not directions. Distinguish empirical optimization from estimating a population covariance; unbiasedness of entries is not the reason the eigenvectors solve the finite-data problem.
- [ ] A direction w is p×1, with wᵀw=1. Scores z=Xw are n×1. Reconstructed centered points form Xwwᵀ, n×p. Restore μ for raw-unit reconstructions. “Component” may mean direction or score in references; the course should say which.
- [ ] State the actual objective and units. Squared Euclidean error is meaningful only relative to the chosen feature scaling. PCA is not automatically a measure of semantic, causal, or target-relevant information.

## Projection and reconstruction

- [ ] Derive the closest point tw on a fixed line: ||x−tw||²=||x||²−2t(xᵀw)+t²; its unique minimizer is t=xᵀw for a unit w. This earns orthogonal projection, rather than assuming it merely because the picture looks good.
- [ ] Show the residual x−(xᵀw)w is perpendicular to w. Then ||x||²=(xᵀw)²+||x−(xᵀw)w||². The identity is pointwise and does not require a probability model.
- [ ] Sum over observations to obtain ||X−Xwwᵀ||²_F=||X||²_F−||Xw||². The first term is fixed when w changes; minimizing one term maximizes the other.
- [ ] Explain centering: the score mean is zero, so ||Xw||²/(n−1) is its sample variance. Without centering, the same norm is a second moment about the origin, not the centered variance.
- [ ] For an affine subspace, optimizing the offset permits a subspace through the mean. One proof decomposes total residual into centered residual plus n times the squared residual of μ−a. Do not imply every optimal offset parameter a is uniquely μ: shifts within the retained subspace describe the same affine set.

## Why covariance appears

- [ ] In 2D expand (w₁xᵢ₁+w₂xᵢ₂)² before matrix shorthand. Averaging yields w₁²C₁₁+2w₁w₂C₁₂+w₂²C₂₂. Explain the cross-term as co-movement, including its sign. Marginal variances alone cannot decide between opposite tilts.
- [ ] In p dimensions, derive Var(z)=(Xw)ᵀ(Xw)/(n−1)=wᵀCw with every transpose/dimension justified. This is an identity, not an approximation.
- [ ] Show C is symmetric and positive semidefinite: vᵀCv=||Xv||²/(n−1)≥0. Covariance off-diagonals can be negative. Nonnegative eigenvalues do not require every entry to be positive.
- [ ] Show why w needs a length constraint: replacing w by aw multiplies variance by a². Unit length compares directions on an equal scale. It is a coordinate normalization, not an empirical claim that the real mechanism has unit size.

## Stationarity is necessary, not the global proof

- [ ] Give a geometric constrained-change interpretation: a tangent perturbation h satisfies hᵀw=0. A stationary direction has hᵀCw=0 for every tangent h, so Cw is parallel to w.
- [ ] Derive ∇(wᵀCw)=(C+Cᵀ)w=2Cw; use symmetry explicitly. For L=wᵀCw−λ(wᵀw−1), stationarity gives Cw=λw. The unit sphere's constraint gradient is nonzero, so the multiplier condition applies at its extrema.
- [ ] Multiply by wᵀ to show the stationary variance equals λ. This identifies the value at a stationary direction; it does not yet select the global maximum.
- [ ] Use C=diag(9,1) as the discriminating example: both coordinate directions satisfy the equation, but one is the minimum. In three dimensions an intermediate eigenvector can be a saddle. An eigensolver output alone is not a proof of the optimization claim.

## Global one-direction guarantee

- [ ] State the real symmetric spectral theorem explicitly: C has an orthonormal eigenbasis q₁,…,qₚ with real λ₁≥…≥λₚ≥0. Either prove its required portion in an optional branch or label it as the theorem invoked; do not pretend the current illustration proves it.
- [ ] Write any unit w=Σⱼaⱼqⱼ, with Σⱼaⱼ²=1. Orthogonality removes cross-terms, yielding wᵀCw=Σⱼλⱼaⱼ²≤λ₁Σⱼaⱼ²=λ₁. A unit vector in the top eigenspace achieves equality. This bounds all feasible directions and supplies the global proof.
- [ ] Explain equality: positive weight may occur only on eigenvalues equal to λ₁. If λ₁>λ₂, the direction is unique up to sign. If λ₁=λ₂, every unit direction in that repeated top eigenspace is a maximizer. If C=0, every direction gives zero and explained-variance ratios need special handling.
- [ ] Connect the bound back to reconstruction: the minimum squared residual is ||X||²_F−(n−1)λ₁. Do not end the proof with symbols detached from the opening's lost distances.

## Joint k-direction guarantee

- [ ] Let W be p×k with WᵀW=Iₖ, k≤p. P=WWᵀ is symmetric and idempotent. Scores are Z=XW; reconstruction is XP. Retained variance is tr(WᵀCW); residual is ||X||²_F−(n−1)tr(WᵀCW).
- [ ] In the eigenbasis, define bⱼ=||Wᵀqⱼ||². Then 0≤bⱼ≤1 and Σⱼbⱼ=k. The retained variance is Σⱼλⱼbⱼ. Prove the upper bound Σⱼ≤kλⱼ by moving weight from a smaller eigenvalue to an unfilled larger one, or show the explicit inequality using λₖ. This is a joint bound, not merely repeated one-direction stationarity.
- [ ] W=[q₁,…,qₖ] achieves the bound. The residual is (n−1)Σⱼ>kλⱼ. Successively maximizing under orthogonality produces this solution, which is why the greedy procedure is globally optimal here.
- [ ] For the selected eigenbasis, ZᵀZ/(n−1)=diag(λ₁,…,λₖ). Thus score coordinates are uncorrelated in the sample. Uncorrelated does not generally mean statistically independent. A rotation inside the same optimal subspace preserves reconstruction; to keep diagonal score covariance when eigenvalues differ, use the eigenbasis.
- [ ] If λₖ>λₖ₊₁, the retained top-k subspace is unique although its arbitrary orthonormal representation need not be. A tie crossing the cutoff allows multiple optimal subspaces. Near ties can destabilize individual estimated vectors; distinguish that from stability of a larger subspace that has a gap at its boundary.

## SVD and rank

- [ ] For X=UΣVᵀ, use compatible full or reduced shapes. Then C=VΣᵀΣVᵀ/(n−1) in the full convention; nonzero eigenvalues are σⱼ²/(n−1), principal directions are right singular vectors, and retained scores are XVₖ=UₖΣₖ.
- [ ] The truncated reconstruction Xₖ=UₖΣₖVₖᵀ equals XVₖVₖᵀ. Explain the link to the Eckart–Young–Mirsky theorem and name the norm. The course's reconstruction objective is Frobenius squared error; a theorem about operator norm must not silently be substituted for it.
- [ ] With centered columns, rank(X)≤min(n−1,p). Scores beyond rank are zero; null-space directions are arbitrary. SVD can compute PCA without explicitly forming C. Numerical sign flips and rotations of degenerate eigenspaces are not failures.
- [ ] Do not teach characteristic-polynomial roots as the practical algorithm for large data. Solver choice, sparse centering, and approximate methods are computational branches; their error/stability claims need actual environment checks.

## Metric, degeneracy, and task relevance

- [ ] For standardized Y=XD⁻¹, PCA minimizes standardized residuals. If transformed reconstruction is mapped back to original units, the implied error is weighted by inverse scale squared. It does not in general minimize raw-unit Euclidean error. Handle zero-variance features before dividing.
- [ ] Unit conversion can change covariance PCA when features are rescaled differently. Common scaling of all features preserves directions. Standardization is a defensible metric choice in some tasks, not a law that always improves PCA.
- [ ] Whitening rescales retained scores to unit variance and changes their relative scale. It is not the same action as centering, standardizing raw features, rotating, or truncating. Zero eigenvalues prevent ordinary inverse-square-root whitening.
- [ ] Retained variance fraction is Σⱼ≤kλⱼ/Σⱼλⱼ when total variance is positive. It quantifies this representation's squared variation, not percent accuracy, labels retained, causal information, or universal denoising quality.
- [ ] Fit mean, scales, feature filters, and PCA only on the training split when assessing a predictive pipeline. Apply stored transformations to later observations. Component-count selection belongs inside the validation procedure. Choose splits that respect temporal/group structure when relevant.
- [ ] Distinguish exact finite-sample optimization from estimating a population subspace, discovering latent causes, denoising, preserving rare groups, or predicting outcomes. Those additional claims require assumptions and external evidence.
- [ ] Demand a failure/mitigation pair with a cost: outlier influence → inspect provenance/robust method with assumptions; curved data → nonlinear model with validation; weak eigengap → report subspace/stability; target in small direction → task-aware k/model; drift → temporal evaluation and refitting policy. No method name alone closes the reasoning.

## Evidence hierarchy for the notebook

Numerical tests illustrate and catch code errors; they do not prove the universal theorem. Use separate held-out reasoning tasks for learning: compute one fresh projection, derive the two-feature cross-term, identify a stationary minimum, reconstruct the eigenbasis bound, handle a repeated eigenvalue, select the metric, and explain an optimum that loses target information. Record assistance and prior knowledge. An AI expert solving these tasks does not establish novice learning.
