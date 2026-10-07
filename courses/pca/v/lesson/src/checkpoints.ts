export const checkpoints = [
  [
    "Rebuild the encoder and decoder.",
    "A friend gives you a new point. Explain what is stored once, what is stored per point, why the foot is perpendicular, and what can be lost.",
    [
      "Distinguish direction, score, reconstruction, and residual.",
      "Use the saved mean and a unit direction.",
      "Explain why moving along the line away from the foot adds error.",
    ],
  ],
  [
    "Earn the variance objective.",
    "Without equations on screen, explain why minimizing reconstruction error is the same as maximizing score variance for a fixed centered dataset.",
    [
      "Use a right triangle and squared lengths.",
      "Name the fixed total.",
      "Explain why the score mean is zero.",
      "Explain why a common n−1 divisor does not choose the winner.",
    ],
  ],
  [
    "Build covariance from a score.",
    "Expand a squared two-feature score. Explain why the cross term belongs there and how S stores its data sums.",
    [
      "Keep the factor of two.",
      "Explain covariance signs with centered offsets.",
      "Map wᵀSw back to the expanded scalar sum.",
      "State the shapes and units.",
    ],
  ],
  [
    "Prove the winner, not just a candidate.",
    "Why does the minor eigenvector also pass the stationary test? Then bound every unit direction using an eigenbasis.",
    [
      "Separate necessary stationarity from global optimality.",
      "Use the spectral theorem explicitly.",
      "Use Sqⱼ=λⱼqⱼ and orthogonality to remove cross terms.",
      "Use nonnegative squared weights that sum to one.",
      "State the equality condition, including ties.",
    ],
  ],
  [
    "Reconstruct the top-k guarantee.",
    "Show why each eigen-direction has at most one unit of retained weight, why those weights sum to k, and why the top-k allocation wins. Then connect to SVD.",
    [
      "Explain projection weight and capacity.",
      "Supply the trace/completeness step.",
      "Bound the weighted eigenvalue sum and exhibit a legal winner.",
      "Relate discarded eigenvalues to squared error and n−1.",
      "Distinguish V directions, UΣ scores, and σ²/(n−1) variances.",
    ],
  ],
  [
    "Design a fit you can evaluate honestly.",
    "Choose an error metric, a component count, and a train/validation/test procedure. Explain why each choice fits the task.",
    [
      "Fit means, scales, and PCA on training data only.",
      "Distinguish centering, feature scaling, and whitening.",
      "Choose k using the stated task and constraint.",
      "Keep an untouched final evaluation set.",
    ],
  ],
  [
    "Diagnose a misleading success.",
    "A PCA plot looks clean and keeps 95% variance. Give two reasons the intended task can still fail, with a test and a repair for each.",
    [
      "Explain a concrete mechanism, such as nuisance spread or a rare signal.",
      "Propose evidence that could reject the claim.",
      "State a mitigation and its residual cost.",
      "Compare an alternative under the same task.",
    ],
  ],
  [
    "Teach it without losing its boundaries.",
    "Explain PCA to a listener who knows a ruler but not vectors. Then expand the same explanation into a proof and a practical decision.",
    [
      "Preserve purpose and the lost detail.",
      "Connect geometry to the formal objective.",
      "State assumptions and the exact guarantee.",
      "Answer a new example without copying a script.",
    ],
  ],
] as const;
