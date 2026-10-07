"""Verify new derivation visual mathematics against notebook-owned PCA cases.

This checks the mathematical contracts used by the new views. It does not
execute React or inspect rendered geometry, typography, or learner outcomes.
"""
from pathlib import Path
import importlib.util
import numpy as np

source = Path(__file__).resolve().parents[1] / "outputs/pca-studio/pca_lesson.py"
spec = importlib.util.spec_from_file_location("pca_derivation_test", source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
_, values = module.app.run()
lab = values["pca_lab"]
cases = [lab["base"], lab["challenge"], *values["pca_cov_v2"], *values["pca_edges_v2"]]
checks = 0
for case in cases:
    x = np.asarray(case["points"], dtype=float)
    s = np.asarray(case["cov"], dtype=float)
    axes = np.asarray(case["axes"], dtype=float)
    lambdas = np.asarray(case["values"], dtype=float)
    # Independent data-table route to every covariance destination entry.
    np.testing.assert_allclose(s, np.cov(x, rowvar=False, ddof=1), atol=2e-6)
    for row in range(2):
        for col in range(2):
            accumulator = 0.0
            for i in range(case["n"]):
                accumulator += x[i, row] * x[i, col]
            np.testing.assert_allclose(accumulator / (case["n"] - 1), s[row, col], atol=2e-6)
    np.testing.assert_allclose(axes @ axes.T, np.eye(2), atol=2e-6)
    for degrees in range(360):
        theta = np.deg2rad(degrees)
        w = np.array([np.cos(theta), np.sin(theta)])
        t = np.array([-w[1], w[0]])
        g = 2 * s @ w
        radial = np.dot(g, w) * w
        tangent = np.dot(g, t) * t
        np.testing.assert_allclose(g, radial + tangent, atol=1e-10)
        np.testing.assert_allclose(np.dot(radial, tangent), 0, atol=1e-8)
        # Check the tangent derivative against a central finite difference of
        # directly computed projection-score variance, independent of S.
        h = 1e-5
        w_plus = np.array([np.cos(theta + h), np.sin(theta + h)])
        w_minus = np.array([np.cos(theta - h), np.sin(theta - h)])
        fd = (np.var(x @ w_plus, ddof=1) - np.var(x @ w_minus, ddof=1)) / (2 * h)
        np.testing.assert_allclose(np.dot(g, t), fd, rtol=1e-6, atol=3e-6)
        # Signed coordinates must work in every quadrant, not only a,b >= 0.
        a, b = axes @ w
        np.testing.assert_allclose(a * axes[0] + b * axes[1], w, atol=2e-6)
        np.testing.assert_allclose(a * a + b * b, 1, atol=2e-6)
        v = lambdas[0] * a * a + lambdas[1] * b * b
        np.testing.assert_allclose(v, np.var(x @ w, ddof=1), atol=3e-6)
        assert v <= lambdas[0] + 3e-6, (degrees, v, lambdas)
        np.testing.assert_allclose(variance_reversed := np.var(x @ (-w), ddof=1), v, atol=3e-6)
        checks += 1
    # Both eigenvectors have zero first-order turning gain. Distinct
    # eigenvalues have opposite signs of finite turning change at the extrema.
    for j, w in enumerate(axes):
        t = np.array([-w[1], w[0]])
        np.testing.assert_allclose(2 * t @ s @ w, 0, atol=3e-6)
        step = np.deg2rad(3)
        turned = np.cos(step) * w + np.sin(step) * t
        delta = np.var(x @ turned, ddof=1) - np.var(x @ w, ddof=1)
        if abs(lambdas[0] - lambdas[1]) > 1e-5:
            assert delta < 0 if j == 0 else delta > 0
        else:
            np.testing.assert_allclose(delta, 0, atol=3e-6)

print(f"PASS: {len(cases)} notebook cases; {checks} full-circle directions.")
print("Verified covariance accumulators, gradient decomposition, finite-difference turning slopes,")
print("signed eigenbasis coordinates, the global bound, sign reversal, and both stationary candidates.")
print("Rendered UI and teaching efficacy are outside this check.")
