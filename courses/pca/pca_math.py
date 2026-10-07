"""Small, JSON-ready PCA computations owned by the course notebook.

Rows are observations; columns are x and y measurements. Covariance, score
variance, and reconstruction loss all use the sample denominator n - 1.
The presentation may draw these values, but this module owns their meaning.
"""

from __future__ import annotations

import numpy as np

BASE_RAW = ((8.0, 7.0), (7.0, 8.0), (5.0, 4.0), (4.0, 5.0))


def _observations(raw) -> np.ndarray:
    values = np.asarray(raw, dtype=float)
    if values.ndim != 2 or values.shape[1] != 2 or values.shape[0] < 2:
        raise ValueError("Use at least two observations with two measurements each.")
    if not np.isfinite(values).all():
        raise ValueError("Measurements must be finite numbers.")
    return values


def pca_case(raw) -> dict:
    """Return a compact PCA result, including a consistent full SVD.

    eigenvectors has eigenvectors in columns. axes is its transpose: one
    drawable direction per row. scores has one column per principal component.
    reconstruction retains the first component in centered coordinates.
    """
    raw = _observations(raw)
    n = len(raw)
    mean = raw.mean(axis=0)
    points = raw - mean
    cov = points.T @ points / (n - 1)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = np.maximum(eigenvalues[order], 0.0)
    eigenvectors = eigenvectors[:, order]
    # Choose a reproducible sign for drawing. PCA directions are sign-invariant.
    for index in range(2):
        pivot = int(np.argmax(np.abs(eigenvectors[:, index])))
        if eigenvectors[pivot, index] < 0:
            eigenvectors[:, index] *= -1
    scores = points @ eigenvectors
    reconstruction = np.outer(scores[:, 0], eigenvectors[:, 0])
    u, singular_values, vt = np.linalg.svd(points, full_matrices=False)
    for index in range(2):
        pivot = int(np.argmax(np.abs(vt[index])))
        if vt[index, pivot] < 0:
            vt[index] *= -1
            u[:, index] *= -1
    total = float(np.trace(cov))
    return {
        "n": n,
        "denominator": n - 1,
        "raw": raw.tolist(),
        "mean": mean.tolist(),
        "points": points.tolist(),
        "cov": cov.tolist(),
        "eigenvalues": eigenvalues.tolist(),
        "eigenvectors": eigenvectors.tolist(),
        "axes": eigenvectors.T.tolist(),
        "scores": scores.tolist(),
        "reconstruction": reconstruction.tolist(),
        "rawReconstruction": (reconstruction + mean).tolist(),
        "totalVariance": total,
        "explainedRatio": (eigenvalues / total).tolist() if total > 0 else None,
        "singularValues": singular_values.tolist(),
        "svd": {"u": u.tolist(), "s": singular_values.tolist(), "vt": vt.tolist()},
    }


def projection_case(raw, angle_deg: float, outlier: float = 0.0) -> dict:
    """Project onto a chosen angle after moving the last observation in x.

    variance = sum(scores**2)/(n-1); loss = sum(residuals**2)/(n-1).
    Their sum is totalVariance. The reconstruction is centered; add the mean
    to recover the units and origin of the measured observations.
    """
    if not np.isfinite(angle_deg) or not np.isfinite(outlier):
        raise ValueError("The angle and displacement must be finite.")
    raw = _observations(raw).copy()
    raw[-1, 0] += outlier
    case = pca_case(raw)
    points = np.asarray(case["points"])
    theta = np.deg2rad(angle_deg)
    w = np.array([np.cos(theta), np.sin(theta)])
    scores = points @ w
    reconstruction = np.outer(scores, w)
    residuals = points - reconstruction
    denominator = len(points) - 1
    return {
        "angleDeg": float(angle_deg),
        "outlier": float(outlier),
        "n": len(points),
        "denominator": denominator,
        "raw": raw.tolist(),
        "mean": case["mean"],
        "points": case["points"],
        "cov": case["cov"],
        "w": w.tolist(),
        "scores": scores.tolist(),
        "reconstruction": reconstruction.tolist(),
        "rawReconstruction": (reconstruction + np.asarray(case["mean"])).tolist(),
        "residuals": residuals.tolist(),
        "variance": float(scores @ scores / denominator),
        "loss": float(np.sum(residuals**2) / denominator),
        "totalVariance": case["totalVariance"],
        "eigenvalues": case["eigenvalues"],
        "axes": case["axes"],
    }


def course_data() -> dict:
    """Fixed model and compact boundary cases; no repeated angle frames."""
    raw = np.asarray(BASE_RAW)
    outlier_raw = raw.copy()
    outlier_raw[-1, 0] += 8.0
    return {
        "schema": 1,
        "units": "cm",
        "covarianceConvention": "sample covariance: denominator n - 1",
        "base": pca_case(raw),
        "cases": {
            "isotropic": pca_case([[1, 0], [0, 1], [-1, 0], [0, -1]]),
            "rankOne": pca_case([[-3, -3], [-1, -1], [1, 1], [3, 3]]),
            "outlier": pca_case(outlier_raw),
            "scaled": pca_case(raw * [1.0, 10.0]),
        },
    }
