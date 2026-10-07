"""Numerical acceptance for the notebook model, independent of its diagrams.

Run: uv run --no-project --with numpy==2.5.3 python -m unittest test_pca_math -v
"""

import json
import unittest

import numpy as np

from pca_math import BASE_RAW, course_data, pca_case, projection_case


class PcaMathematics(unittest.TestCase):
    def test_fixed_example_matches_hand_calculation(self):
        base = pca_case(BASE_RAW)
        np.testing.assert_allclose(base["mean"], [6, 6])
        np.testing.assert_allclose(base["points"], [[2, 1], [1, 2], [-1, -2], [-2, -1]])
        np.testing.assert_allclose(base["cov"], [[10/3, 8/3], [8/3, 10/3]])
        np.testing.assert_allclose(base["eigenvalues"], [6, 2/3])
        np.testing.assert_allclose(base["explainedRatio"], [0.9, 0.1])
        at_optimum = projection_case(BASE_RAW, 45)
        self.assertAlmostEqual(at_optimum["variance"], 6)
        self.assertAlmostEqual(at_optimum["loss"], 2/3)

    def test_eigendecomposition_and_svd_recover_every_case(self):
        data = course_data()
        for case in [data["base"], *data["cases"].values()]:
            x = np.asarray(case["points"])
            q = np.asarray(case["eigenvectors"])
            values = np.asarray(case["eigenvalues"])
            cov = np.asarray(case["cov"])
            np.testing.assert_allclose(x.mean(axis=0), 0, atol=1e-12)
            np.testing.assert_allclose(q.T @ q, np.eye(2), atol=1e-12)
            np.testing.assert_allclose(cov @ q, q * values, atol=1e-12)
            np.testing.assert_allclose(q @ np.diag(values) @ q.T, cov, atol=1e-12)
            np.testing.assert_allclose(np.asarray(case["scores"]) @ q.T, x, atol=1e-12)
            svd = case["svd"]
            np.testing.assert_allclose(np.asarray(svd["u"]) @ np.diag(svd["s"]) @ svd["vt"], x, atol=1e-12)
            np.testing.assert_allclose(np.square(svd["s"]) / (case["n"]-1), values, atol=1e-12)
            residual = x - np.asarray(case["reconstruction"])
            self.assertAlmostEqual(np.sum(residual**2)/(case["n"]-1), values[1])

    def test_native_control_grid_obeys_projection_and_global_bound(self):
        # Every offered integer angle and half-centimeter displacement.
        for outlier in np.arange(0, 8.01, 0.5):
            for angle in range(181):
                result = projection_case(BASE_RAW, angle, outlier)
                x = np.asarray(result["points"])
                w = np.asarray(result["w"])
                cov = np.asarray(result["cov"])
                z = np.asarray(result["scores"])
                residuals = np.asarray(result["residuals"])
                np.testing.assert_allclose(w @ w, 1, atol=1e-12)
                np.testing.assert_allclose(z, x @ w, atol=1e-12)
                np.testing.assert_allclose(residuals @ w, 0, atol=1e-12)
                self.assertAlmostEqual(result["variance"], float(w @ cov @ w))
                self.assertAlmostEqual(result["variance"] + result["loss"], result["totalVariance"])
                self.assertLessEqual(result["variance"], result["eigenvalues"][0] + 1e-10)
                np.testing.assert_allclose(result["raw"][-1], [4 + outlier, 5])

    def test_axis_sign_changes_scores_but_not_reconstruction(self):
        a = projection_case(BASE_RAW, 23, 3)
        b = projection_case(BASE_RAW, 203, 3)
        np.testing.assert_allclose(a["scores"], -np.asarray(b["scores"]), atol=1e-12)
        np.testing.assert_allclose(a["reconstruction"], b["reconstruction"], atol=1e-12)
        self.assertAlmostEqual(a["variance"], b["variance"])

    def test_translation_changes_mean_but_not_centered_pca(self):
        base = pca_case(BASE_RAW)
        moved = pca_case(np.asarray(BASE_RAW) + [101, -44])
        np.testing.assert_allclose(moved["cov"], base["cov"])
        np.testing.assert_allclose(moved["eigenvalues"], base["eigenvalues"])
        np.testing.assert_allclose(moved["rawReconstruction"], np.asarray(base["rawReconstruction"]) + [101, -44])

    def test_degenerate_cases_are_mathematically_honest(self):
        cases = course_data()["cases"]
        np.testing.assert_allclose(cases["isotropic"]["eigenvalues"], [2/3, 2/3])
        self.assertAlmostEqual(cases["rankOne"]["eigenvalues"][1], 0)
        constant = pca_case([[2, 2], [2, 2]])
        self.assertEqual(constant["totalVariance"], 0)
        self.assertIsNone(constant["explainedRatio"])

    def test_bad_measurements_are_rejected(self):
        for raw in [[[1, 2]], [[1, 2, 3], [4, 5, 6]], [[1, 2], [np.nan, 3]]]:
            with self.assertRaises(ValueError):
                pca_case(raw)

    def test_all_native_states_stay_under_transport_budget(self):
        data = course_data()
        max_bytes = 0
        for outlier in np.arange(0, 8.01, 0.5):
            for angle in range(181):
                payload = {"values": {"pca_data": data, "pca_live": projection_case(BASE_RAW, angle, outlier)}, "errors": {}}
                size = len(json.dumps(payload, allow_nan=False, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
                max_bytes = max(max_bytes, size)
        self.assertLess(max_bytes, 100_000)
        print(f"\nMaximum combined model/live JSON response: {max_bytes:,} bytes across 3,077 native control states.")


if __name__ == "__main__":
    unittest.main()
