# /// script
# requires-python = ">=3.10,<3.15"
# dependencies = ["marimo-studio[deno]==0.2.3", "numpy==2.5.3"]
#
# [tool.marimo-studio]
# default = "lesson"
# view_root = "v"
#
# [tool.marimo-studio.cells]
# ///

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")


@app.cell
def imports():
    import marimo as mo
    import numpy as np

    return mo, np


@app.cell(hide_code=True)
def welcome(mo):
    mo.md("""
    # Principal component analysis
    A geometric intuition, followed by the covariance derivation.
    """)
    return


@app.cell(hide_code=True)
def centering_control(mo):
    center_amount = mo.ui.slider(0, 1, step=0.1, value=0, label="Fraction of mean subtracted", show_value=True)
    center_amount
    return (center_amount,)


@app.cell(hide_code=True)
def correlation_control(mo):
    rho = mo.ui.slider(-0.9, 0.9, step=0.05, value=0.75, label="Correlation", show_value=True)
    rho
    return (rho,)


@app.cell(hide_code=True)
def direction_control(mo):
    angle = mo.ui.slider(0, 180, step=1, value=0, label="Direction angle (degrees)", show_value=True)
    angle
    return (angle,)


@app.cell(hide_code=True)
def dimension_control(mo):
    components = mo.ui.radio({"One component": 1, "Both components": 2}, value="One component", label="Keep")
    components
    return (components,)


@app.cell(hide_code=True)
def scale_control(mo):
    scale_y = mo.ui.slider(1, 8, step=1, value=1, label="Multiply feature 2 units by", show_value=True)
    standardize = mo.ui.checkbox(value=False, label="Standardize each feature")
    mo.vstack([scale_y, standardize])
    return scale_y, standardize


@app.cell(hide_code=True)
def data_explanation(mo):
    mo.md("""
    ## A controlled point cloud
    These 48 synthetic observations have exactly zero sample mean and a chosen
    sample covariance. A fixed seed holds the observations steady as controls change.
    Feature units are arbitrary. The units experiment uses a separate copy.
    """)
    return


@app.cell(hide_code=True)
def data_model(np, rho):
    _rng = np.random.default_rng(17)
    _noise = _rng.normal(size=(48, 2))
    _noise -= _noise.mean(axis=0)
    _q, _r = np.linalg.qr(_noise)
    base_cov = np.array([[4.0, 4.0 * rho.value], [4.0 * rho.value, 4.0]])
    Xc = np.sqrt(47) * _q @ np.linalg.cholesky(base_cov).T
    mean_vector = np.array([5.0, 3.0])
    Xraw = Xc + mean_vector
    S = Xc.T @ Xc / (len(Xc) - 1)
    _vals, _vecs = np.linalg.eigh(S)
    eigenvalues = _vals[::-1]
    W = _vecs[:, ::-1]
    W = W * np.where(W[0] < 0, -1, 1)
    scores = Xc @ W
    None
    return S, W, Xc, Xraw, eigenvalues, mean_vector, scores


@app.cell(hide_code=True)
def projection_model(
    S,
    W,
    Xc,
    Xraw,
    angle,
    center_amount,
    components,
    eigenvalues,
    mean_vector,
    np,
    rho,
    scores,
):
    theta = np.deg2rad(angle.value)
    w = np.array([np.cos(theta), np.sin(theta)])
    z = Xc @ w
    Xhat = np.outer(z, w)
    projected_variance = float(w @ S @ w)
    residual_loss = float(np.sum((Xc - Xhat)**2) / (len(Xc) - 1))
    _angles = np.linspace(0, 180, 181)
    _directions = np.column_stack((np.cos(np.deg2rad(_angles)), np.sin(np.deg2rad(_angles))))
    variance_curve = np.einsum("ij,jk,ik->i", _directions, S, _directions)
    _k = components.value
    reconstruction = scores[:, :_k] @ W[:, :_k].T
    cloud = {
        "points": Xc.tolist(), "raw": Xraw.tolist(), "mean": mean_vector.tolist(),
        "centered": (Xraw - center_amount.value * mean_vector).tolist(),
        "centerAmount": center_amount.value, "cov": S.tolist(), "rho": rho.value,
        "w": w.tolist(), "sw": (S @ w).tolist(), "angle": angle.value,
        "projected": Xhat.tolist(), "z": z.tolist(),
        "variance": projected_variance, "total": float(np.trace(S)),
        "loss": residual_loss, "curve": list(zip(_angles.tolist(), variance_curve.tolist())),
        "eigenvalues": eigenvalues.tolist(), "axes": W.T.tolist(), "scores": scores.tolist(),
        "pcAngle": float(np.degrees(np.arctan2(W[1, 0], W[0, 0])) % 180),
        "reconstruction": reconstruction.tolist(), "k": _k,
        "reconstructionLoss": float(np.sum((Xc - reconstruction)**2) / 47),
        "retained": float(eigenvalues[:_k].sum() / eigenvalues.sum()),
        "degenerate": bool(np.isclose(eigenvalues[0], eigenvalues[1])),
    }
    None
    return


@app.cell(hide_code=True)
def scale_model(Xc, np, scale_y, standardize):
    _scaled = Xc * np.array([1.0, float(scale_y.value)])
    _std = _scaled.std(axis=0, ddof=1)
    _working = _scaled / _std if standardize.value else _scaled
    _cov = _working.T @ _working / 47
    _e, _v = np.linalg.eigh(_cov)
    _e = _e[::-1]
    _v = _v[:, ::-1]
    _v *= np.where(_v[0] < 0, -1, 1)
    units = {
        "points": _working.tolist(), "cov": _cov.tolist(), "axes": _v.T.tolist(),
        "eigenvalues": _e.tolist(), "scale": scale_y.value,
        "standardized": standardize.value,
        "ratio": float(_e[0] / _e.sum()),
        "angle": float(np.degrees(np.arctan2(_v[1, 0], _v[0, 0])) % 180),
    }
    None
    return


@app.cell(hide_code=True)
def center_math(mo):
    text_center_math = r"""


    $$
    \mu=\frac{1}{n}\sum_{i=1}^{n}x_i,\qquad X_c=X-\mathbf 1\mu^\top
    $$



    Each row of $X$ is one observation. Each column is one feature.
    Subtracting the column means moves the cloud without changing its shape.
    Here $n=48$, $p=2$, and $\mu=(5,3)^\top$.
    """
    mo.md(text_center_math)
    return (text_center_math,)


@app.cell(hide_code=True)
def covariance_math(mo):
    text_covariance_math = r"""


    $$
    S_{jk}=\frac{1}{n-1}\sum_i (x_{ij}-\mu_j)(x_{ik}-\mu_k)
    $$




    $$
    S=\frac{X_c^\top X_c}{n-1}=
    \begin{bmatrix}\operatorname{Var}(x_1)&\operatorname{Cov}(x_1,x_2)\\
    \operatorname{Cov}(x_1,x_2)&\operatorname{Var}(x_2)\end{bmatrix}
    $$



    Same-sign deviations contribute positively. Opposite-sign deviations contribute negatively.
    The diagonal measures each feature's spread.
    """
    mo.md(text_covariance_math)
    return (text_covariance_math,)


@app.cell(hide_code=True)
def score_math(mo):
    text_score_math = r"""


    $$
    w=\begin{bmatrix}\cos\theta\\\sin\theta\end{bmatrix},\quad
    z_i=w^\top(x_i-\mu),\quad z=X_cw
    $$




    $$
    \hat x_i=\mu+z_iw
    $$



    The **score** $z_i$ locates a point along the axis.
    The **loading vector** $w$ combines the features.
    Perpendicular segments show the lost information.
    """
    mo.md(text_score_math)
    return (text_score_math,)


@app.cell(hide_code=True)
def variance_step1(mo):
    text_variance_step1 = r"""
    Since $X_c$ is centered, the score mean is zero.


    $$
    \operatorname{Var}(z)=\frac{1}{n-1}\sum_i z_i^2=\frac{z^\top z}{n-1}
    $$


    """
    mo.md(text_variance_step1)
    return (text_variance_step1,)


@app.cell(hide_code=True)
def variance_step2(mo):
    text_variance_step2 = r"""
    Substitute $z=X_cw$.



    $$
    \frac{(X_cw)^\top(X_cw)}{n-1}=\frac{w^\top X_c^\top X_cw}{n-1}
    $$





    $$
    =w^\top\!\underbrace{\frac{X_c^\top X_c}{n-1}}_{S}\!w=w^\top Sw
    $$


    """
    mo.md(text_variance_step2)
    return (text_variance_step2,)


@app.cell(hide_code=True)
def variance_step3(mo):
    text_variance_step3 = r"""
    PCA chooses the axis with maximum projected variance.


    $$
    \max_{w\in\mathbb R^p} w^\top Sw\quad\text{subject to }w^\top w=1
    $$


    The constraint fixes the ruler's length. Otherwise scaling $w$ makes the variance arbitrarily large.
    """
    mo.md(text_variance_step3)
    return (text_variance_step3,)


@app.cell(hide_code=True)
def eigen_step1(mo):
    text_eigen_step1 = r"""
    Introduce a multiplier for the unit-length constraint.


    $$
    \mathcal L(w,\lambda)=w^\top Sw-\lambda(w^\top w-1)
    $$


    """
    mo.md(text_eigen_step1)
    return (text_eigen_step1,)


@app.cell(hide_code=True)
def eigen_step2(mo):
    text_eigen_step2 = r"""
    Because $S=S^\top$, the gradient is $2Sw$.


    $$
    \nabla_w\mathcal L=2Sw-2\lambda w=0\quad\Longrightarrow\quad Sw=\lambda w
    $$


    """
    mo.md(text_eigen_step2)
    return (text_eigen_step2,)


@app.cell(hide_code=True)
def eigen_step3(mo):
    text_eigen_step3 = r"""
    At an eigenvector, $w^\top Sw=\lambda w^\top w=\lambda$.
    The largest eigenvalue gives the maximum.

    Why global? Write $w=\sum_j a_jv_j$ in an orthonormal eigenbasis.


    $$
    w^\top Sw=\sum_j\lambda_j a_j^2\leq\lambda_1\sum_j a_j^2=\lambda_1
    $$


    """
    mo.md(text_eigen_step3)
    return (text_eigen_step3,)


@app.cell(hide_code=True)
def worked_data(mo, np):
    example_X = np.array([[2.,1.],[1.,2.],[-1.,-2.],[-2.,-1.]])
    example_S = example_X.T @ example_X / 3
    _ev, _ew = np.linalg.eigh(example_S)
    example = {"cov": example_S.tolist(), "values": _ev[::-1].tolist(),
               "ratio": float(_ev[-1] / _ev.sum())}
    text_worked_data = r"""


    $$
    X_c=\begin{bmatrix}2&1\\1&2\\-1&-2\\-2&-1\end{bmatrix},\qquad
    X_c^\top X_c=\begin{bmatrix}10&8\\8&10\end{bmatrix}
    $$




    $$
    S=\frac13\begin{bmatrix}10&8\\8&10\end{bmatrix}
    $$


    For example, the off-diagonal sum is $2\cdot1+1\cdot2+(-1)(-2)+(-2)(-1)=8$.
    """
    mo.md(text_worked_data)
    return (text_worked_data,)


@app.cell(hide_code=True)
def worked_solution(mo):
    text_worked_solution = r"""


    $$
    \det(S-\lambda I)=\left(\frac{10}{3}-\lambda\right)^2-\left(\frac83\right)^2=0
    $$




    $$
    \lambda_1=6,\quad\lambda_2=\frac23,\qquad
    w_1=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix},\quad
    w_2=\frac{1}{\sqrt2}\begin{bmatrix}-1\\1\end{bmatrix}
    $$




    $$
    z_1=X_cw_1=\frac{1}{\sqrt2}(3,3,-3,-3)^\top,\qquad
    \frac{\lambda_1}{\lambda_1+\lambda_2}=90\%
    $$


    Four points, one component, 90% of sample variance retained.
    """
    mo.md(text_worked_solution)
    return (text_worked_solution,)


@app.cell(hide_code=True)
def orthogonal_math(mo):
    text_orthogonal_math = r"""


    $$
    W=[w_1\;\cdots\;w_p],\quad W^\top W=I,\quad Z=X_cW
    $$




    $$
    \operatorname{Cov}(Z)=W^\top SW=\operatorname{diag}(\lambda_1,\ldots,\lambda_p)
    $$


    PC2 maximizes the remaining variance subject to being orthogonal to PC1.
    Scores are **uncorrelated**. Independence does not follow in general.
    Flipping an eigenvector's sign changes score signs but preserves its axis.
    """
    mo.md(text_orthogonal_math)
    return (text_orthogonal_math,)


@app.cell(hide_code=True)
def reconstruction_math(mo):
    text_reconstruction_math = r"""


    $$
    Z_k=X_cW_k,\qquad \widehat X_c=Z_kW_k^\top
    $$





    $$
    \text{loss}=\frac{\lVert X_c-\widehat X_c\rVert_F^2}{n-1}
    $$





    $$
    =\operatorname{tr}(S)-\sum_{j=1}^k\lambda_j=\sum_{j>k}\lambda_j
    $$



    Add the mean back for original coordinates. Keeping all components preserves the data, up to rounding.
    """
    mo.md(text_reconstruction_math)
    return (text_reconstruction_math,)


@app.cell(hide_code=True)
def loss_proof(mo):
    text_loss_proof = r"""
    For one unit vector, the projection and residual are perpendicular.


    $$
    \|x_{ci}-w w^\top x_{ci}\|^2=\|x_{ci}\|^2-(w^\top x_{ci})^2
    $$


    Sum over observations and divide by $n-1$:


    $$
    \text{loss}=\operatorname{tr}(S)-w^\top Sw
    $$


    Total spread stays fixed, so maximizing retained variance minimizes squared reconstruction error.
    The displayed loss uses $n-1$; per-observation mean squared distance uses $n$.
    """
    mo.md(text_loss_proof)
    return (text_loss_proof,)


@app.cell(hide_code=True)
def units_math(mo):
    text_units_math = r"""


    $$
    \widetilde X_{ij}=\frac{X_{ij}-\mu_j}{s_j},\qquad
    S_{\mathrm{standardized}}=\operatorname{Corr}(X)
    $$


    Covariance PCA depends on feature units. Standardizing gives each nonconstant
    feature unit sample variance, changing the optimization's metric.
    Choose the metric to match the problem. Standardizing is a choice, not a universal rule.
    """
    mo.md(text_units_math)
    return (text_units_math,)


@app.cell(hide_code=True)
def svd_math(mo):
    text_svd_math = r"""


    $$
    X_c=U\Sigma V^\top\quad\Longrightarrow\quad
    S=V\frac{\Sigma^2}{n-1}V^\top
    $$




    $$
    W=V,\qquad Z=U\Sigma,\qquad\lambda_j=\frac{\sigma_j^2}{n-1}
    $$


    SVD computes the same principal directions without explicitly forming $X_c^\top X_c$.
    For new observations, reuse the training mean, scales (if any), and loading vectors.
    """
    mo.md(text_svd_math)
    return (text_svd_math,)


@app.cell(hide_code=True)
def quiz_control(mo):
    quiz = mo.ui.radio(["Choose an answer", "Keep the direction with greatest variance", "Keep the original feature with largest values", "Choose the direction that best predicts a label"], value="Choose an answer", label="What does PC1 optimize?")
    quiz
    return (quiz,)


@app.cell(hide_code=True)
def quiz_feedback(mo, quiz):
    if quiz.value == "Choose an answer":
        _answer = "Make a prediction, then test it on the projection slide."
    elif quiz.value == "Keep the direction with greatest variance":
        _answer = "Correct. Under a unit-length constraint, PC1 maximizes projected sample variance. It also minimizes squared reconstruction error for a one-dimensional linear subspace."
    elif quiz.value == "Keep the original feature with largest values":
        _answer = "Try again. A component can combine every feature. Centering removes offsets, so large raw values alone do not determine PC1."
    else:
        _answer = "Try again. PCA uses no target labels. High variance can be irrelevant to a prediction task."
    mo.md(_answer)
    return


@app.cell(hide_code=True)
def cautions(mo):
    text_cautions = """
    - **Equal eigenvalues:** there is no unique preferred axis in that eigenspace.
    - **Large variance:** may reflect signal, nuisance variation, or outliers.
    - **Curved structure:** a straight subspace may need many components.
    - **Component count:** use the error or retained variance your task can tolerate.

    Explain back: Why does covariance need centering? Why must the direction have unit length?
    Why does losing less variance mean reconstructing better?
    """
    mo.md(text_cautions)
    return (text_cautions,)


@app.cell(hide_code=True)
def implementation(mo):
    text_implementation = r"""
    ## Reusable calculation
    ```python
    mu = X.mean(axis=0)
    Xc = X - mu
    U, singular_values, Vt = np.linalg.svd(Xc, full_matrices=False)
    Wk = Vt[:k].T
    scores = Xc @ Wk
    Xhat = scores @ Wk.T + mu
    variance = singular_values**2 / (len(X) - 1)
    ```
    Columns of $W_k$ are loadings. Rows of `scores` describe observations in the new coordinates.
    """
    mo.md(text_implementation)
    return (text_implementation,)


@app.cell(hide_code=True)
def slide_content(
    text_cautions,
    text_center_math,
    text_covariance_math,
    text_eigen_step1,
    text_eigen_step2,
    text_eigen_step3,
    text_implementation,
    text_loss_proof,
    text_orthogonal_math,
    text_reconstruction_math,
    text_score_math,
    text_svd_math,
    text_units_math,
    text_variance_step1,
    text_variance_step2,
    text_variance_step3,
    text_worked_data,
    text_worked_solution,
):
    lesson_content = {
    'center_math': text_center_math,
    'covariance_math': text_covariance_math,
    'score_math': text_score_math,
    'variance_step1': text_variance_step1,
    'variance_step2': text_variance_step2,
    'variance_step3': text_variance_step3,
    'eigen_step1': text_eigen_step1,
    'eigen_step2': text_eigen_step2,
    'eigen_step3': text_eigen_step3,
    'worked_data': text_worked_data,
    'worked_solution': text_worked_solution,
    'orthogonal_math': text_orthogonal_math,
    'reconstruction_math': text_reconstruction_math,
    'loss_proof': text_loss_proof,
    'units_math': text_units_math,
    'svd_math': text_svd_math,
    'cautions': text_cautions,
    'implementation': text_implementation,
    }
    None
    return


if __name__ == "__main__":
    app.run()
