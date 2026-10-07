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


@app.cell(hide_code=True)
def masterclass_model(np):
    def make_pca_case(raw, with_frames=True):
        raw = np.asarray(raw, dtype=float)
        n = len(raw)
        mu = raw.mean(0)
        xc = raw - mu
        cov = xc.T @ xc / (n - 1)
        vals, vec = np.linalg.eigh(cov)
        vals, vec = vals[::-1], vec[:, ::-1]
        vec *= np.where(vec[0] < 0, -1, 1)
        z = xc @ vec
        total = float(np.trace(cov))
        pack = lambda a: np.asarray(a).round(7).tolist()
        result = dict(raw=pack(raw), points=pack(xc), mean=pack(mu), cov=pack(cov),
            sums=pack(xc.T @ xc), values=pack(vals), axes=pack(vec.T), scores=pack(z),
            std=pack(np.sqrt(np.diag(cov))),corr=pack(cov / np.outer(np.sqrt(np.diag(cov)),np.sqrt(np.diag(cov)))),scoreCov=pack(z.T @ z / (n - 1)), scoreProducts=pack(z[:, 0] * z[:, 1]),
            total=total, ratio=float(vals[0] / total), n=n,
            angle=float(np.degrees(np.arctan2(vec[1, 0], vec[0, 0])) % 180),
            squared=pack(xc**2), signedSums=pack(xc.sum(0)), squaresSums=pack((xc**2).sum(0)),
            products=pack(np.einsum('ij,ik->ijk', xc, xc)),
            singular=pack(np.sqrt(np.maximum(vals, 0) * (n - 1))),
            recon=[], frames=[])
        for k in range(3):
            xhat = z[:, :k] @ vec[:, :k].T
            loss = np.sum((xc - xhat)**2, axis=1)
            result['recon'].append(dict(points=pack(xhat), raw=pack(xhat+mu),
                loss=pack(loss), totalLoss=float(loss.sum()/(n-1)),
                ratio=float(vals[:k].sum()/total)))
        if with_frames:
            for angle in range(181):
                theta = np.deg2rad(angle)
                w = np.array([np.cos(theta), np.sin(theta)])
                score = xc @ w
                projected = np.outer(score, w)
                residual = xc - projected
                kept = score**2
                lost = np.sum(residual**2, axis=1)
                sw = cov @ w
                tangent = np.array([-w[1], w[0]])
                result['frames'].append(dict(w=pack(w), sw=pack(sw), z=pack(score),
                    terms=pack(xc*w), projected=pack(projected), residual=pack(residual),
                    kept=pack(kept), lost=pack(lost), lengths=pack(np.sum(xc**2,axis=1)),
                    variance=float(kept.sum()/(n-1)), loss=float(lost.sum()/(n-1)),
                    sumSquares=float(kept.sum()), ratio=float(kept.sum()/(n-1)/total),
                    slope=float(2*tangent@cov@w), turn=float(tangent@sw),
                    eigen=bool(abs(tangent@sw)<1e-6)))
        return result

    None

    return (make_pca_case,)


@app.cell(hide_code=True)
def masterclass_data(make_pca_case, np):
    _base = np.array([[8,7],[7,8],[5,4],[4,5]],dtype=float)
    _centered = _base - _base.mean(0)
    _cases = [make_pca_case(_base), make_pca_case(_centered * [1,-1],False),
              make_pca_case(np.column_stack((_centered[:,0],[1,-2,2,-1])),False)]
    _centers = []
    for _i in range(21):
        _fraction = _i/20
        _shifted = _base - _fraction*_base.mean(0)
        _centers.append(dict(points=_shifted.tolist(),mean=_shifted.mean(0).tolist(),
                             fraction=_fraction))
    _scales = []
    for _factor in range(1,11):
        _scaled = _centered * [1,_factor]
        _scales.append(dict(raw=make_pca_case(_scaled,False),
            standard=make_pca_case(_scaled/_scaled.std(0,ddof=1),False),factor=_factor))
    _ruler = []
    for _length in range(1,7):
        _w = np.array([1.,1.])/np.sqrt(2)*_length
        _z = _centered@_w
        _ruler.append(dict(length=_length,w=_w.tolist(),z=_z.tolist(),
            norm2=float(_w@_w),variance=float(_z@_z/3)))
    _mix = []
    for _i in range(101):
        _p = _i/100
        _v = _p*6+(1-_p)*2/3
        _mix.append(dict(p=_p,a=float(np.sqrt(_p)),b=float(np.sqrt(1-_p)),
            variance=_v,first=_p*6,second=(1-_p)*2/3))
    _rotation = np.array([[np.cos(.41),-np.sin(.41)],[np.sin(.41),np.cos(.41)]])
    _challenge = make_pca_case(_centered@_rotation.T)
    _theta = np.linspace(0,2*np.pi,24,endpoint=False)
    _ring = make_pca_case(np.column_stack([np.cos(_theta),np.sin(_theta)])*3,False)
    _nuisance = make_pca_case([[x,y] for y in [-.5,.5] for x in [-3,-1,1,3]],False)
    _outlier = make_pca_case(np.vstack([_centered,[0,10]]),False)
    pca_lab = dict(base=_cases[0],covCases=_cases,centers=_centers,scales=_scales,
                   ruler=_ruler,mixtures=_mix,challenge=_challenge,
                   edgeCases=[make_pca_case(_centered,False),_outlier,_ring],
                   nuisance=_nuisance,people=['A','B','C','D'])
    None

    return (pca_lab,)


@app.cell(hide_code=True)
def masterclass_controls(mo):
    sandbox_a = mo.ui.slider(0,10,step=.5,value=4,show_value=True,label="Observation D · x (cm)")
    sandbox_b = mo.ui.slider(0,10,step=.5,value=5,show_value=True,label="Observation D · y (cm)")
    mo.vstack([sandbox_a,sandbox_b])

    return sandbox_a, sandbox_b


@app.cell(hide_code=True)
def masterclass_sandbox(make_pca_case, sandbox_a, sandbox_b):
    sandbox_lab = make_pca_case([[8,7],[7,8],[5,4],[sandbox_a.value,sandbox_b.value]])
    None

    return


@app.cell(hide_code=True)
def masterclass_guide(mo):
    masterclass = {
     'title':'PCA, from the ground up',
     'passTest':'On a new two-feature dataset, center the columns, compute a covariance entry, find a useful projection, reconstruct a point, and explain what was lost.',
     'chapters':['1 · Meet the data','2 · Build covariance','3 · Invent a score','4 · Find the best axis','5 · Compress & recover','6 · Break the method','7 · Prove you can use it'],
     'slides':[
     ['Can two numbers become one?', 'You have two test scores per person. Your job is to keep one number that preserves as much difference between people as possible.', 'Predict before the demonstration: what would a single score lose?', 'PCA is a choice of what to preserve: squared spread. It does not decide what makes a person successful.'],
     ['A row is a person. A column is a measurement.', 'These are four invented people, not a claim about real students. Each dot and each table row refer to the same person.', 'Select a row or a dot. Find the same person in both views.', 'A feature is simply a measured quantity. Here both features use points, so their units are comparable.'],
     ['First, find the balance point', 'The mean is the equal-share value: add the four scores, then divide by four. We do this separately for each test.', 'Switch between the two columns. Where is the balance point?', 'A large score and a large deviation are different ideas. A deviation says how far someone is from the group mean.'],
     ['Move the origin, keep the differences', 'Subtract the mean from every score in its column. Person A changes from (8, 7) to (2, 1). They are two points above average on A and one above on B.', 'Slide from raw scores to centered scores. Watch the mean move to zero.', 'Translation preserves distances and the shape of the cloud. PCA now describes variation around the group, not distance from an arbitrary zero.'],
     ['Why square the deviations?', 'The positive and negative deviations cancel. A sum of zero does not mean everyone has the same score. Squaring makes both directions contribute to spread.', 'Switch from signed deviations to squares. Select a person to inspect their contribution.', 'Sample variance is the sum of squared deviations divided by n−1. Its units are points squared.'],
     ['Why does the formula divide by n−1?', 'Once we estimated the mean, the deviations must add to zero. If three are known, the fourth is already determined. Only three deviations are free here.', 'Try the missing deviation before opening the explanation.', 'For independent observations from one distribution, dividing by n−1 corrects the average underestimate of population variance caused by estimating the mean. Using n rescales eigenvalues, not PCA directions.'],
     ['Covariance starts with one multiplication', 'For one person, multiply the deviation on test A by the deviation on test B. Same signs give a positive product; opposite signs give a negative product.', 'Select each person. Then reverse the pattern on test B.', 'Covariance adds these cross-products and divides by n−1. Positive means the deviations tend to move together; negative means they tend to move oppositely.'],
     ['Zero covariance can be cancellation', 'A zero total does not require every product to be zero. Positive and negative contributions can cancel.', 'Compare together, opposite, and cancelling patterns. Look at all four products.', 'Covariance measures a linear co-movement. Zero covariance alone does not establish independence.'],
     ['A covariance matrix is four familiar numbers', 'The diagonal entries compare a column with itself: they are variances. The off-diagonal entries compare the two columns: they are covariances.', 'Click each matrix entry to see its four products.', 'The two off-diagonal entries agree because multiplying A by B gives the same result as multiplying B by A. S is symmetric.'],
     ['Matrix multiplication is the same bookkeeping', 'Xc stores centered observations in rows. Transposing swaps rows and columns. Multiplying a row of Xcᵀ by a column of Xc adds the products you already calculated.', 'Choose an entry, then step through transpose → multiply → divide.', 'Xc has shape 4×2; Xcᵀ has shape 2×4. Their product is 2×2, so it has one entry for every pair of features.'],
     ['A score is a shadow on a line', 'Imagine dropping a perpendicular from a dot onto an axis. The signed distance along that axis is its new score. This reduces two coordinates to one.', 'Drag the orange handle to rotate the axis. Select a person.', 'Projection keeps movement along the chosen line and loses movement across it. A negative score just lies on the other side of the mean.'],
     ['You choose the axis first', 'Rotate the line and watch the shadows spread out or crowd together. PCA wants the line whose shadows have the largest variance.', 'Find the best direction without pressing “Show the best axis”.', 'We maximize variance across all people. Fitting one particular person perfectly is not the objective.'],
     ['The dot product is a weighted sum', 'A unit direction w has two weights. Multiply each centered feature by its weight, then add. This arithmetic computes exactly the shadow you just moved.', 'Change the angle and select a person. Follow both products into the final score.', 'Loadings are the shared weights. Scores are the different results for individual observations. They are not the same object.'],
     ['Derive variance from the scores you made', 'The score mean is zero because the input columns are centered. So variance is the sum of squared scores divided by n−1.', 'Turn the axis, then step through each equality. Both calculations must agree.', 'The covariance matrix is sufficient for this objective: every candidate direction can be scored using wᵀSw.'],
     ['A longer ruler is a cheat', 'Multiplying w by three triples every score and multiplies score variance by nine, even though the direction has not improved.', 'Stretch the weight vector, then normalize it again.', 'Require wᵀw = 1. We compare directions using the same unit length. Otherwise the optimization has no finite maximum.'],
     ['What does the covariance matrix do to a direction?', 'Multiply w by S. Most arrows turn as well as stretch. At special directions, Sw lies on the same line as w.', 'Rotate w until the matrix stops turning it. Try both diagonal directions.', 'A nonzero vector that only stretches under S is an eigenvector. Its stretch factor is an eigenvalue.'],
     ['Find the eigenvectors by doing the multiplication', 'For this matrix, try the simple directions (1,0), (1,1), and (−1,1). An eigenvector must use one common stretch factor for both coordinates.', 'Choose a candidate. Compare input and output component by component.', 'The long diagonal has eigenvalue 6; the perpendicular diagonal has eigenvalue 2/3. Unit versions have length one.'],
     ['Why does the largest eigenvalue win?', 'Any unit direction is a mixture of the two perpendicular eigenvectors: w = a v₁ + b v₂, with a²+b² = 1. Its variance is a weighted average of their eigenvalues.', 'Move the share assigned to v₁. Can the average exceed the larger endpoint?', 'Because the weights a² and b² are nonnegative and sum to one, a mixture cannot beat the largest eigenvalue. This proves the global maximum.'],
     ['PC2 keeps what PC1 misses', 'PC1 captures the common high-versus-low pattern. PC2 captures the contrast between the two tests. Two perpendicular axes describe the original plane completely.', 'Switch between old and new coordinates. Flip the sign of PC1.', 'The new score columns have covariance zero. Sign flips change score signs, not information. Uncorrelated still does not mean independent in general.'],
     ['What does “90% explained” actually mean?', 'Total variance is the sum of the two feature variances. In the PCA coordinates it is the sum of the eigenvalues. Rotation changes the coordinates, not this total.', 'Allocate your storage to zero, one, or two components.', '90% means 90% of total squared centered spread. It does not mean 90% accuracy, 90% of people, or 90% certainty about a prediction.'],
     ['Can you reconstruct one person?', 'A one-number record stores the score z. To rebuild the centered point, multiply z by the direction w. Add the mean to return to the original test scales.', 'Select a person, then choose how many components to keep.', 'One component gives an approximation. Two components recover both original scores, apart from numerical rounding.'],
     ['The lost part is a right-triangle side', 'The kept projection and the residual are perpendicular. Pythagoras says original squared distance = kept squared distance + lost squared distance.', 'Rotate the axis. Watch the triangle and its three squared lengths.', 'Sum this identity over every person. The total stays fixed, so keeping more squared spread leaves less reconstruction error.'],
     ['Choose k using an error budget', 'Keeping fewer components saves storage but loses detail. The acceptable loss comes from the task; a convenient percentage is not a universal law.', 'Set a required variance percentage, then choose the smallest sufficient k.', 'For general p features, keep the smallest k meeting your error or variance requirement. Validate its usefulness on your downstream task.'],
     ['Changing units changes the competition', 'Suppose test B is reported in tenths of a point. The same performance now has numbers ten times larger. Its squared deviations become one hundred times larger.', 'Increase the multiplier on B. Watch PC1 rotate toward the enlarged scale.', 'Covariance PCA gives more weight to numerically larger variation. Choosing units is part of choosing what differences matter.'],
     ['Standardizing is a modeling choice', 'Subtract each feature mean, then divide by its sample standard deviation. Each nonconstant feature now has variance one. The covariance matrix becomes the correlation matrix.', 'Toggle standardization after changing B’s units. Inspect the matrix.', 'Standardize when relative variation should receive comparable weight. Keep natural scales when their sizes are meaningful. Neither choice is automatic.'],
     ['Try to break PCA', 'A point far from the rest can dominate squared spread. A circular cloud has no unique longest axis. A single straight line also cannot follow a circle.', 'Switch between the original cloud, an outlier, and a ring.', 'PCA is sensitive to outliers, eigenvalue ties, and nonlinear structure. More variance does not guarantee a better representation for every purpose.'],
     ['High variance may hide the thing you need', 'Here the categories differ vertically, but most variation is horizontal. PCA does not see category labels when choosing a direction.', 'Reveal the categories, then keep only PC1. Can you still separate them?', 'PCA is unsupervised. A low-variance direction can be the most useful one for classification.'],
     ['A fresh cloud. Your axis.', 'This dataset has been rotated. Use the cloud and the spread meter to find its best one-dimensional representation.', 'Submit your angle and a reason before viewing the solution.', 'Transfer means using the idea when the familiar picture changes. An angle memorized from the first example will not solve this one.'],
     ['Now change the actual notebook data', 'Replace person D’s two scores. Python recomputes the mean, covariance, eigensystem, and every projection frame. Your drag control explores those newly computed results.', 'Change D’s test B score, then find the new best axis.', 'The notebook is the mathematical model; the slide is a live control surface for exploring its results.'],
     ['SVD is another route to the same answer', 'Software often factors the centered data directly as UΣVᵀ. The columns of V are the PCA directions; UΣ contains the scores.', 'Step through the substitution, then choose how many components to keep.', 'SVD avoids explicitly forming XcᵀXc. For new observations, reuse the training mean, any training scales, and the learned directions.'],
     ['Optional: the calculus derivation, unpacked', 'A gradient is a vector of slopes. At a constrained optimum, the objective cannot improve along the unit circle, so its gradient points normal to that circle.', 'Choose the a or b derivative, then advance one algebra step at a time.', 'The Lagrange multiplier enforces equal-length directions. Stationarity gives eigenvectors; the weighted-average proof tells us which stationary point is the maximum.'],
     ['Close the notes. Produce an answer.', 'This check uses fresh numbers. Answer one question at a time. A miss or an admitted guess stops the check and gives you a route back to the relevant experiment.', 'Give the number and a reason. Save your learning record when finished.', 'Numeric checks are automatic; written reasoning is saved for tutor or self-review. Passing a numeric check alone is not proof of mastery.'],
     ],
     'equations':{
     'center':r'x_{ci}=x_i-\mu',
     'variance':r's_A^2=\frac{\sum_i (x_{iA}-\mu_A)^2}{n-1}',
     'cov':r'S_{AB}=\frac{\sum_i x_{ci,A}\,x_{ci,B}}{n-1}',
     'matrix':r'S=\frac{X_c^\top X_c}{n-1}',
     'score':r'z_i=w_A x_{ci,A}+w_B x_{ci,B}=w^\top x_{ci}',
     'constraint':r'w^\top w=w_A^2+w_B^2=1',
     'eigen':r'Sw=\lambda w',
     'mix':r'w^\top Sw=\lambda_1a^2+\lambda_2b^2\leq\lambda_1',
     'recon':r'\widehat x_i=\mu+\sum_{j=1}^k z_{ij}w_j',
     'loss':r'\|x_{ci}\|^2=z_i^2+\|x_{ci}-z_iw\|^2',
     'standard':r'\widetilde x_{ij}=\frac{x_{ij}-\mu_j}{s_j}',
     },
     'varianceSteps':[
     [r'\operatorname{Var}(z)=\frac{z_1^2+\cdots+z_n^2}{n-1}', 'Square each centered score and add. The table on the right performs this calculation for the angle you choose.'],
     [r'\operatorname{Var}(z)=\frac{z^\top z}{n-1}', 'A column transposed into a row, multiplied by itself, is the same sum of squares. No new statistical idea is being introduced.'],
     [r'\frac{(X_cw)^\top(X_cw)}{n-1}', 'Every score came from the same weighted sum. Xc times w computes those scores for all people, so replace z with Xc w.'],
     [r'\frac{w^\top X_c^\top X_cw}{n-1}', 'Transposing a product reverses its order: (AB)ᵀ = BᵀAᵀ. The outside objects are the weights, and the middle compares feature columns.'],
     [r'w^\top\underbrace{\left(\frac{X_c^\top X_c}{n-1}\right)}_{S}w=w^\top Sw', 'The middle block is exactly the covariance matrix you built. Both routes must produce the same number.']
     ],
     'svdSteps':[
     [r'X_c=U\Sigma V^\top','U has orthonormal columns; V has orthonormal columns. Σ contains nonnegative singular values. Think of V as directions and UΣ as their scores.'],
     [r'S=\frac{V\Sigma U^\top U\Sigma V^\top}{n-1}','Substitute the factorization into XcᵀXc/(n−1). The order reverses when taking a transpose.'],
     [r'S=V\frac{\Sigma^2}{n-1}V^\top','Because UᵀU = I, the middle simplifies. This is an eigen-decomposition of S.'],
     [r'W=V,\qquad Z=U\Sigma,\qquad\lambda_j=\frac{\sigma_j^2}{n-1}','The directions, scores, and variances match PCA. Thin SVD suffices; zero singular values need care in rank-deficient data.']
     ],
     'calculusSteps':[
     [r'f(a,b)=S_{AA}a^2+2S_{AB}ab+S_{BB}b^2','Expand wᵀSw for w=(a,b). The cross-product appears twice because S is symmetric.'],
     [r'\frac{\partial f}{\partial a}=2S_{AA}a+2S_{AB}b,\quad\frac{\partial f}{\partial b}=2S_{AB}a+2S_{BB}b','For the a derivative, hold b fixed. For the b derivative, hold a fixed. These two slopes make the vector 2Sw.'],
     [r'\mathcal L=w^\top Sw-\lambda(w^\top w-1)','The constraint is a²+b²=1. At an optimum its normal and the objective gradient line up; λ is the factor connecting them.'],
     [r'2Sw-2\lambda w=0\quad\Rightarrow\quad Sw=\lambda w','Set the two slopes of the Lagrangian to zero. Divide by two. This yields the eigenvector equation, including both maximum and minimum candidates.']
     ],
     'exam':[
     {'prompt':'A feature has observations 2, 4, 9. What is its mean?','answer':5,'tolerance':.001,'route':2,'level':'Recall','hint':'Add all observations, then divide by their count.'},
     {'prompt':'Centered pairs are (−2,−1), (0,0), (2,1). What is their sample covariance?','answer':2,'tolerance':.001,'route':6,'level':'Apply','hint':'Multiply each pair, add the three products, then divide by n−1.'},
     {'prompt':'A covariance matrix has eigenvalues 9 and 3. What percentage of total variance does PC1 keep?','answer':75,'tolerance':.001,'route':19,'level':'Apply','hint':'Compare the largest eigenvalue with the sum of all eigenvalues.'},
     {'prompt':'Using that same matrix, what is the squared reconstruction error divided by n−1 after keeping PC1?','answer':3,'tolerance':.001,'route':21,'level':'Transfer','hint':'The error equals the sum of the discarded eigenvalues.'},
     ],
     'practices':{
     'mission':{'prompt':'If you store only the average of the two tests, can you tell which test a person was stronger at?','options':['Yes, always','No, the contrast can disappear'],'answer':1,'feedback':'A=(8,7) and B=(7,8) have the same average, yet their strengths differ. One number has discarded the contrast.'},
     'nminus':{'prompt':'Centered deviations are 3, −1, 2, and ?. What must the last deviation be?','answer':-4,'feedback':'Centered deviations sum to zero. The first three total 4, so the last must be −4. Try a fresh set after this.'},
     'nminusRedo':{'prompt':'Without the worked answer: deviations are 4, −3, 1, and ?.','answer':-2,'feedback':'Check the zero-sum condition.'}
     }
    }
    mo.md('# PCA masterclass\n54 interactive experiments. Start with means and arithmetic; finish with covariance, eigenvectors, reconstruction, transfer, and optional SVD/calculus.\n\n**Pass test:** '+masterclass['passTest'])

    # Just-in-time prerequisite bridges. These belong beside the PCA operation they unlock.
    _bridges = {
     'vector':['A vector is an ordered list', 'The pair (8,7) records test A first and test B second. A vector can represent a point or a movement. The order gives each number its meaning.', 'Switch between a point and an arrow. Select a different person.', 'Two coordinates make a two-dimensional vector. A dataset with p features uses p coordinates.',r'x_i=\begin{bmatrix}x_{iA}\\x_{iB}\end{bmatrix}'],
     'coordinates':['Read a point, one coordinate at a time', 'To locate (8,7), move eight units horizontally and seven vertically. Dropping guide lines to the axes recovers the two measurements.', 'Select a person and toggle the guide lines.', 'A scatterplot is a table drawn in space. It is not an extra dataset.',r'x_i=(x_{iA},x_{iB})'],
     'sigma':['The Σ symbol just means “add these”', 'The small i is an observation index. The limits say where to start and stop. We use the same instruction whether there are four observations or four million.', 'Reveal the sum one person at a time. Then divide by the count.', 'An index names which observation you are using; it is not a new feature or a power.',r'\mu_A=\frac14\sum_{i=1}^{4}x_{iA}=\frac{8+7+5+4}{4}'],
     'subtract':['Subtract vectors coordinate by coordinate', 'Subtracting the mean vector does two ordinary subtractions. Nothing crosses between features: test A subtracts its own mean, and test B subtracts its own mean.', 'Select a person. Reveal one coordinate subtraction at a time.', 'The center of the whole dataset becomes zero, while the differences between people stay the same.',r'\begin{bmatrix}8\\7\end{bmatrix}-\begin{bmatrix}6\\6\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix}'],
     'square':['A square measures size without sign', 'A deviation of −2 and one of +2 are equally far from zero. Each gives a squared contribution of 4. Larger deviations matter more: doubling one makes its square four times as large.', 'Choose a deviation. Inspect its signed length and square area.', 'Squaring prevents cancellation, but also makes distant points especially influential. We will return to that when an outlier breaks PCA.',r'(-2)^2=2^2=4'],
     'variancecheck':['Your turn: calculate a variance', 'Use a fresh set of centered deviations. Write the sum of squares on paper before entering your result. Do not copy a displayed worked example.', 'Submit an answer before the explanation is available.', 'A correct computation should include centering, squaring, summing, and the chosen denominator.',r's^2=\frac{\sum_i d_i^2}{n-1}'],
     'signs':['Why does a cross-product encode “together”?', 'Above average on both tests gives (+)×(+). Below average on both gives (−)×(−). Both products are positive. Opposite sides of their averages give a negative product.', 'Choose the two signs before revealing their product.', 'Covariance concerns deviations from each feature’s mean. Raw positive scores alone cannot tell you the covariance sign.',r'(+)(+)>0,\quad(-)(-)>0,\quad(+)(-)<0'],
     'shape':['Keep track of rows and columns', 'We have four observations and two features, so Xc has shape 4×2. The first number counts rows. The second counts columns. Matrix dimensions help you spot invalid operations.', 'Choose which objects can multiply to produce a 2×2 feature-pair matrix.', 'For A of shape m×n and B of shape n×p, AB has shape m×p. The inside sizes must match.',r'(m\times n)(n\times p)\longrightarrow(m\times p)'],
     'transpose':['Transpose changes the view, not the values', 'The transpose symbol ᵀ swaps rows and columns. The test A column becomes the test A row. Every value stays attached to its person and feature.', 'Toggle the transpose. Select a person to follow their two entries.', 'We transpose Xc so each feature becomes a row ready to compare with every feature column.',r'(X_c^\top)_{ji}=(X_c)_{ij}'],
     'blend':['Invent a weighted score', 'A score can combine both features. The weights answer “how much does each feature count?” A negative weight subtracts a feature, measuring a contrast instead of a shared level.', 'Choose “test A”, “together”, or “contrast”, then select a person.', 'We will compare these choices fairly by giving their weight vectors unit length.',r'z_i=a\,x_{ci,A}+b\,x_{ci,B}'],
     'unitcircle':['An angle names a unit direction', 'The unit circle has radius one. At angle θ, the horizontal coordinate is cos θ and the vertical coordinate is sin θ. Those two coordinates are the projection weights.', 'Rotate the direction. Watch the two weights change while length stays one.', 'Angles describe directions in this two-dimensional example. In many dimensions, we use a unit vector directly.',r'w=(\cos\theta,\sin\theta),\quad\cos^2\theta+\sin^2\theta=1'],
     'dotcheck':['Your turn: compute a dot product', 'No matrix machinery is needed. Multiply matching coordinates and add. The result is a single number.', 'Calculate (3,4) · (0.6,0.8), then submit.', 'When the second vector has unit length, a dot product gives the signed projection length.',r'x\cdot w=x_Aw_A+x_Bw_B'],
     'reverse':['Why does transposing reverse the order?', 'Xc w produces a 4×1 score column. Its transpose must be 1×4. The reversed product wᵀXcᵀ has exactly those shapes; keeping the original order does not.', 'Choose an order and inspect the dimensions before revealing the rule.', 'Transpose reverses the composition: (AB)ᵀ = BᵀAᵀ. It does not arbitrarily rearrange ordinary matrix multiplication.',r'(X_cw)^\top=w^\top X_c^\top'],
     'norm':['Length comes from Pythagoras', 'For a vector (a,b), the squared length is a²+b². Its length is the square root. Dividing each coordinate by this length keeps the direction and makes the length one.', 'Compare the vector (1,1) with its unit version.', 'The normalized weights are 1/√2 each, not 1/2 each. An average and a unit-vector projection have different scales.',r'\|w\|=\sqrt{a^2+b^2},\quad\widehat w=\frac{w}{\|w\|}'],
     'matvec':['A matrix times a vector: two weighted sums', 'The first output uses the first row of the matrix. The second output uses the second row. Each is the same multiply-and-add operation as a dot product.', 'Choose an output row and follow the two products.', 'A 2×2 matrix transforms a two-coordinate vector into another two-coordinate vector.',r'Sw=\begin{bmatrix}S_{AA}w_A+S_{AB}w_B\\S_{BA}w_A+S_{BB}w_B\end{bmatrix}'],
     'identity':['Solving for the stretch factors', 'I is the identity matrix: multiplying by it changes nothing. Rewrite Sw=λw as (S−λI)w=0. A nonzero solution exists when S−λI is singular, which means its determinant is zero.', 'Try the candidate λ values and check the determinant.', 'For a 2×2 matrix [[a,b],[c,d]], determinant = ad−bc. Here the two roots are 6 and 2/3.',r'\det(S-\lambda I)=\left(\frac{10}{3}-\lambda\right)^2-\left(\frac83\right)^2=0'],
     'perpendicular':['Perpendicular means zero dot product', 'The unit directions (1,1)/√2 and (−1,1)/√2 form a right angle. Their dot product is −1/2+1/2=0.', 'Compare the perpendicular axis with a duplicate of PC1.', 'A duplicate axis gives the same information twice. PC2 searches among directions perpendicular to PC1.',r'v_1^\top v_2=0,\qquad W^\top W=I'],
     'trace':['The trace adds the diagonal', 'The trace of S is simply the sum of its diagonal entries: total feature variance. In the PCA basis, the diagonal entries are the eigenvalues. Both sums agree.', 'Toggle original and PCA coordinates. Compare the two totals.', 'Rotating coordinates preserves total squared distance. That is why the variance budget stays the same.',r'\operatorname{tr}(S)=S_{AA}+S_{BB}=\lambda_1+\lambda_2'],
     'reconcheck':['Your turn: put the mean back', 'A new dataset has mean (10,20). The retained unit direction is (1,0), and a person’s score is 3. Reconstruct that person’s first coordinate.', 'Enter the first coordinate, then explain what happens to the second.', 'A projection score is measured relative to the mean. Forgetting to add the mean back gives coordinates in the wrong system.',r'\widehat x=\mu+zw'],
     'zscore':['A standardized value counts standard deviations', 'A raw value of 14, a mean of 10, and a sample standard deviation of 2 give (14−10)/2 = 2. This is two standard deviations above the mean.', 'Try the below-mean example without seeing its answer.', 'Centering changes the origin; dividing by standard deviation changes the scale. These are separate operations.',r'z=\frac{x-\mu}{s}'],
    }
    _sequence=[0,1,'vector','coordinates',2,'sigma',3,'subtract',4,'square',5,'variancecheck',6,'signs',7,8,'shape','transpose',9,'blend',10,'unitcircle',12,'dotcheck',11,13,'reverse',14,'norm',15,'matvec',16,'identity',17,'perpendicular',18,19,'trace',20,'reconcheck',21,22,23,24,'zscore',25,26,27,28,29,30,31]
    masterclass['bridges']=_bridges
    masterclass['sequence']=_sequence
    masterclass['bridgeProblems']={
     'variancecheck':{'prompt':'Centered deviations are −3, 0, 3. What is the sample variance?','answer':9,'feedback':'The squared deviations total 18. There are three observations, so divide by 2.'},
     'dotcheck':{'prompt':'Compute (3,4) · (0.6,0.8).','answer':5,'feedback':'Multiply coordinate by coordinate: 1.8 + 3.2 = 5.'},
     'reconcheck':{'prompt':'Mean (10,20), direction (1,0), score 3. What is the reconstructed first coordinate?','answer':13,'feedback':'Start at the mean and add the displacement: 10 + 3×1.'},
     'zscore':{'prompt':'Value 6, mean 10, standard deviation 2: what is the standardized value?','answer':-2,'feedback':'Subtract first, then divide: (6−10)/2. The negative sign means below the mean.'},
    }
    masterclass['examVariants']=[masterclass['exam'],[
     {'prompt':'A feature has observations 1, 6, 11. What is its mean?','answer':6,'tolerance':.001,'route':2,'level':'Recall','hint':'Add all observations, then divide by their count.'},
     {'prompt':'Centered pairs are (−3,1), (0,0), (3,−1). What is their sample covariance?','answer':-3,'tolerance':.001,'route':6,'level':'Apply','hint':'Add the products and divide by n−1.'},
     {'prompt':'Eigenvalues are 12 and 4. What percentage of total variance does PC1 keep?','answer':75,'tolerance':.001,'route':19,'level':'Apply','hint':'Divide the larger eigenvalue by their sum, then multiply by 100.'},
     {'prompt':'For eigenvalues 12 and 4, what is the squared reconstruction error divided by n−1 after retaining PC1?','answer':4,'tolerance':.001,'route':21,'level':'Transfer','hint':'Sum the discarded eigenvalues.'},
    ]]
    masterclass['glossary']={
     'Observation':'One row: the measurements for one person or object.',
     'Feature':'One column: a quantity measured for each observation.',
     'Centered':'The feature’s own mean has been subtracted from every value.',
     'Variance':'Sum of squared deviations from the mean, divided here by n−1.',
     'Covariance':'Sum of products of two features’ centered deviations, divided here by n−1.',
     'Transpose':'Rows become columns and columns become rows; written ᵀ.',
     'Dot product':'Multiply corresponding coordinates, then add the products.',
     'Unit vector':'A direction vector of length one; squared coordinates sum to one.',
     'Eigenvector':'A nonzero direction that a matrix stretches without turning.',
     'Eigenvalue':'The stretch factor for an eigenvector; for a unit PCA direction, its score variance.',
     'Loading':'One of the weights used to combine centered features into a component score.',
     'Score':'An observation’s coordinate along a chosen component direction.',
     'Orthogonal':'Perpendicular; the dot product is zero.',
     'Trace':'Sum of the diagonal entries of a matrix.',
     'Gradient':'A vector of partial derivatives: the slopes as each coordinate changes.',
    }
    masterclass['map']=[
     {'name':'Deviations & spread','depends':'Arithmetic','unlocks':'Covariance','stuck':'Signed deviations cancel','artifact':'Calculate a sample variance'},
     {'name':'Covariance & matrices','depends':'Deviations','unlocks':'Scoring directions','stuck':'Treating raw products as covariance','artifact':'Compute and locate one S entry'},
     {'name':'Projection & variance','depends':'Covariance; weighted sums','unlocks':'PCA objective','stuck':'Confusing loadings with scores','artifact':'Find a useful axis; derive its variance'},
     {'name':'Eigenvectors','depends':'Projection; unit length','unlocks':'Best axes','stuck':'Why the largest eigenvalue wins','artifact':'Verify Sw=λw and justify the maximum'},
     {'name':'Reconstruction','depends':'Axes and scores','unlocks':'Compression choices','stuck':'Forgetting the mean or residual','artifact':'Reconstruct a new point; compute loss'},
     {'name':'Modeling choices','depends':'Variance and reconstruction','unlocks':'Knowing when PCA helps','stuck':'Equating variance with usefulness','artifact':'Explain a scaling or outlier failure'},
     {'name':'Transfer','depends':'All six nodes','unlocks':'Independent use','stuck':'Recognizing examples without reproducing reasoning','artifact':'Fresh calculation plus explanation'},
    ]
    None

    masterclass['bridges']['std']=['Standard deviation puts spread back in the original units', 'Variance uses squared units. Its square root is the standard deviation: a measure of spread in the same units as the original feature. It is a root-mean-square-type size of centered deviations, with the sample correction.', 'Change the units of test B. Compare the changes in variance and standard deviation.', 'Multiply a feature by c: its variance scales by c squared, while its standard deviation scales by the absolute value of c.', r's_B=\sqrt{S_{BB}}']
    masterclass['bridges']['correlation']=['Correlation is covariance with the units divided out', 'Covariance depends on the scales of both features. Divide by the product of their standard deviations to obtain correlation: a unit-free measure between minus one and one.', 'Compare positive, negative, and cancelling patterns. Read covariance and correlation together.', 'A correlation of zero means no linear association. A correlation near one means a strong positive linear association; it does not prove causation.', r'r_{AB}=\frac{S_{AB}}{s_A s_B}']
    _seq=masterclass['sequence']
    _pos=_seq.index(24)
    _seq[_pos:_pos]=['std','correlation']
    # Define standardized values immediately before the standardization experiment.
    _seq.remove('zscore')
    _seq.insert(_seq.index(24),'zscore')

    return


@app.cell(hide_code=True)
def pca_course_v2():
    pca_course_v2 = {'version': 2, 'title': 'PCA · from picture to proof', 'chapters': [{'start': 0, 'end': 8, 'question': 'What does PCA do?'}, {'start': 8, 'end': 20, 'question': 'How do we measure a view?'}, {'start': 20, 'end': 30, 'question': 'Why does covariance appear?'}, {'start': 30, 'end': 45, 'question': 'Why do eigenvectors solve it?'}, {'start': 45, 'end': 56, 'question': 'What can we keep and recover?'}, {'start': 56, 'end': 64, 'question': 'When does the result help?'}], 'slides': [{'id': 1, 'title': 'What is PCA?', 'action': 'Rotate one line through a measured cloud. Watch four observations become four scores.', 'claim': 'PCA finds new perpendicular axes, ordered by variance. Keeping fewer axes reduces the number of values per observation.', 'scene': 'geometry', 'steps': [], 'chapter': 0}, {'id': 2, 'title': 'One number is a position on a line', 'action': 'Select an observation. Link its point, projection, and single stored score.', 'claim': 'The point and its score refer to the same observation.', 'scene': 'geometry', 'steps': [], 'chapter': 0}, {'id': 3, 'title': 'Some views lose more than others', 'action': 'Compare 45° and 135° with the same scale in both score plots.', 'claim': 'A useful projection keeps a large part of the original squared spread.', 'scene': 'geometry', 'steps': [], 'chapter': 0}, {'id': 4, 'title': 'A projection follows a perpendicular', 'action': 'Move one point to its closest position on the chosen line.', 'claim': 'The line is the axis that we KEEP; the viewing direction is perpendicular to it.', 'scene': 'geometry', 'steps': [], 'chapter': 0}, {'id': 5, 'title': 'What does one score lose?', 'action': 'Hide the original points. Reveal the possible points that share a score.', 'claim': 'A score cannot recover movement across its axis.', 'scene': 'geometry', 'steps': [], 'chapter': 0}, {'id': 6, 'title': 'Turn the axes, then remove one', 'action': 'Switch between two rotated coordinates and one retained coordinate.', 'claim': 'Rotation alone loses nothing. Removing a coordinate can lose detail.', 'scene': 'geometry', 'steps': [], 'chapter': 0}, {'id': 7, 'title': 'What will best mean?', 'action': 'Compare kept squared spread with squared reconstruction error.', 'claim': 'These are two equivalent PCA objectives under the same Euclidean scale.', 'scene': 'geometry', 'steps': [], 'chapter': 0}, {'id': 8, 'title': 'See the whole method once', 'action': 'Step through center → find axes → keep scores → reconstruct.', 'claim': 'The next chapters explain how to compute this result.', 'scene': 'geometry', 'steps': [], 'chapter': 0}, {'id': 9, 'title': 'Measure change from a shared center', 'action': 'Translate the cloud without changing its shape.', 'claim': 'The PCA direction describes variation around the mean.', 'scene': 'center', 'steps': [], 'chapter': 1}, {'id': 10, 'title': 'Find the center of this cloud', 'action': 'Highlight one column and calculate its mean.', 'claim': 'Introduce the mean only because we need this center.', 'scene': 'center', 'steps': [{'tex': '\\mu=\\left(\\frac{8+7+5+4}{4},\\frac{7+8+4+5}{4}\\right)=(6,6)', 'why': 'Add the four values in each column. Divide each sum by four.'}], 'chapter': 1}, {'id': 11, 'title': 'Move the center to zero', 'action': 'Scrub the translation. Keep observation labels fixed.', 'claim': 'Subtract the corresponding feature mean from each observation.', 'scene': 'center', 'steps': [{'tex': 'x_A=(8,7)-(6,6)=(2,1)', 'why': 'Subtract the mean of each feature. A is two units right and one unit up from the center.'}], 'chapter': 1}, {'id': 12, 'title': 'The distances do not change', 'action': 'Select two observations before and after translation.', 'claim': 'Centering changes the origin, not the relative positions.', 'scene': 'center', 'steps': [{'tex': '(r_A-\\mu)-(r_B-\\mu)=r_A-r_B', 'why': 'The two copies of the mean cancel. The difference between observations stays the same.'}], 'chapter': 1}, {'id': 13, 'title': 'Describe the line with two numbers', 'action': 'Rotate a unit arrow. Its horizontal and vertical parts update.', 'claim': 'The vector w gives a direction and has length one.', 'scene': 'score', 'steps': [{'tex': 'w=\\begin{bmatrix}\\cos\\theta\\\\\\sin\\theta\\end{bmatrix},\\quad w_1^2+w_2^2=1', 'why': 'The angle sets the direction. The unit length fixes the scale of its scores.'}], 'chapter': 1}, {'id': 14, 'title': 'Calculate one score', 'action': 'Select A. Multiply each centered coordinate by its direction weight.', 'claim': 'The dot product gives signed distance along a unit axis.', 'scene': 'score', 'steps': [{'tex': 'z_A=w^\\top x_A=2w_1+w_2', 'why': 'Multiply matching coordinates. Add the two products. A negative score is on the other side of the center.'}], 'chapter': 1}, {'id': 15, 'title': 'Use one rule for every observation', 'action': 'Link each row of Xc to its score in Xc w.', 'claim': 'Rows are observations; columns are features. Show the matrix shapes here.', 'scene': 'score', 'steps': [{'tex': '\\underbrace{z}_{4\\times1}=\\underbrace{X_c}_{4\\times2}\\underbrace{w}_{2\\times1}', 'why': 'Apply the same weights to each row. This matrix product produces all four scores.'}], 'chapter': 1}, {'id': 16, 'title': 'Keep the ruler length fixed', 'action': 'Double the direction length without changing its angle.', 'claim': 'Without the unit constraint, scores and variance can grow without limit.', 'scene': 'score', 'steps': [{'tex': 'z_i(cw)=c z_i(w),\\quad V(cw)=c^2V(w)', 'why': 'Doubling the arrow doubles every score. The variance then becomes four times as large.'}], 'chapter': 1}, {'id': 17, 'title': 'How spread out are the scores?', 'action': 'Compare scores around zero at two angles.', 'claim': 'Centered input produces scores whose mean is zero.', 'scene': 'variance', 'steps': [{'tex': '\\bar z=w_1\\bar a+w_2\\bar b=0', 'why': 'The centered feature means are zero. Their weighted sum is also zero.'}], 'chapter': 1}, {'id': 18, 'title': 'Signs cancel; squares do not', 'action': 'Switch signed contributions to square areas.', 'claim': 'Squaring measures both directions and supports the distance identity used later.', 'scene': 'variance', 'steps': [{'tex': '\\sum_i z_i=0\\quad\\text{but}\\quad\\sum_i z_i^2\\geq0', 'why': 'Positive and negative scores can cancel. Their squares measure spread on both sides of the center.'}], 'chapter': 1}, {'id': 19, 'title': 'Give spread a number', 'action': 'Add four squared scores and divide by three.', 'claim': 'Use sample variance throughout. An optional note explains n−1; changing it to n does not change the best axis.', 'scene': 'variance', 'steps': [{'tex': 'V(w)=\\frac{z_1^2+z_2^2+z_3^2+z_4^2}{3}', 'why': 'This is sample variance for four centered scores. Its units are square centimeters.'}], 'chapter': 1}, {'id': 20, 'title': 'Search with a variance curve', 'action': 'Rotate the line. Link the angle to a point on the variance curve.', 'claim': 'The highest point gives our numerical target. We still need a general method.', 'scene': 'variance', 'steps': [{'tex': 'V(w)=\\frac{1}{n-1}\\sum_i (w^\\top x_i)^2', 'why': 'The graph evaluates this expression for each direction. Next, we derive a way to find its maximum.'}], 'chapter': 1}, {'id': 21, 'title': 'Open one squared score', 'action': 'Reveal each term in (w1 a + w2 b)².', 'claim': 'Show the two identical cross-products before replacing them with a factor of two.', 'scene': 'expansion', 'steps': [{'tex': 'z_i^2=(w_1a_i+w_2b_i)(w_1a_i+w_2b_i)', 'why': 'Write the square as a product of two identical sums.'}, {'tex': '=w_1^2a_i^2+w_1w_2a_ib_i+w_2w_1b_ia_i+w_2^2b_i^2', 'why': 'Multiply each term in the first bracket by each term in the second.'}, {'tex': '=w_1^2a_i^2+2w_1w_2a_ib_i+w_2^2b_i^2', 'why': 'The middle products are equal. Add them to get the factor two.'}], 'chapter': 2}, {'id': 22, 'title': 'Add the same terms across rows', 'action': 'Select one observation in the sum. Then group matching terms.', 'claim': 'The weights are shared by all observations, so they can leave the sum.', 'scene': 'expansion', 'steps': [{'tex': 'V=\\frac{\\sum_i(w_1^2a_i^2+2w_1w_2a_ib_i+w_2^2b_i^2)}{n-1}', 'why': 'Add the expanded square for every observation.'}, {'tex': '=w_1^2\\frac{\\sum_i a_i^2}{n-1}+2w_1w_2\\frac{\\sum_i a_ib_i}{n-1}+w_2^2\\frac{\\sum_i b_i^2}{n-1}', 'why': 'The weights do not depend on the observation. Put them outside their sums.'}], 'chapter': 2}, {'id': 23, 'title': 'Two familiar sums and one new sum', 'action': 'Link the first and last terms to the two feature variances.', 'claim': 'The middle sum measures how the two centered features vary together.', 'scene': 'expansion', 'steps': [{'tex': 'V=w_1^2s_a^2+2w_1w_2s_{ab}+w_2^2s_b^2', 'why': 'The two square sums are feature variances. Name the product sum covariance, written as s_ab.'}], 'chapter': 2}, {'id': 24, 'title': 'Build covariance from signed products', 'action': 'Select observations in each quadrant. Flip the second feature.', 'claim': 'Same signs give positive products; opposite signs give negative products.', 'scene': 'covariance', 'steps': [{'tex': 's_{ab}=\\frac{2\\cdot1+1\\cdot2+(-1)(-2)+(-2)(-1)}3=\\frac83', 'why': 'Each product is positive in this cloud. Both features tend to lie on the same side of their means.'}], 'chapter': 2}, {'id': 25, 'title': 'Variance alone cannot tell the tilt', 'action': 'Compare two clouds with the same marginal variances and opposite covariance.', 'claim': 'The cross-term distinguishes these clouds.', 'scene': 'covariance', 'steps': [{'tex': 's_a^2=s_b^2=\\frac{10}3,\\qquad s_{ab}=\\pm\\frac83', 'why': 'Changing the sign of the second feature preserves its squares. It reverses each cross-product.'}], 'chapter': 2}, {'id': 26, 'title': 'Store the three quantities in S', 'action': 'Select a covariance matrix entry to reveal its products.', 'claim': 'The diagonal stores variances. Both off-diagonal entries store the same covariance.', 'scene': 'covariance', 'steps': [{'tex': 'S=\\begin{bmatrix}s_a^2&s_{ab}\\\\s_{ab}&s_b^2\\end{bmatrix}=\\frac13\\begin{bmatrix}10&8\\\\8&10\\end{bmatrix}', 'why': 'The matrix stores the three quantities needed to calculate variance in any direction.'}], 'chapter': 2}, {'id': 27, 'title': 'Compute S with one matrix product', 'action': 'Animate a selected row of Xcᵀ meeting a column of Xc.', 'claim': 'Transpose and multiplication are compact ways to do the sums we already used.', 'scene': 'covariance', 'steps': [{'tex': '\\underbrace{X_c^\\top}_{2\\times4}\\underbrace{X_c}_{4\\times2}=\\begin{bmatrix}\\sum a_i^2&\\sum a_ib_i\\\\\\sum b_ia_i&\\sum b_i^2\\end{bmatrix}', 'why': 'A row meets a column. Multiply matching entries and add.'}, {'tex': 'S=\\frac{X_c^\\top X_c}{n-1}', 'why': 'Divide all four sums by the same sample divisor.'}], 'chapter': 2}, {'id': 28, 'title': 'Read wᵀ S w from inside out', 'action': 'Calculate Sw, then the dot product with w.', 'claim': 'The compact formula is exactly the expanded variance expression.', 'scene': 'objective', 'steps': [{'tex': 'Sw=\\begin{bmatrix}s_a^2w_1+s_{ab}w_2\\\\s_{ab}w_1+s_b^2w_2\\end{bmatrix}', 'why': 'First multiply S by w. This gives a two-coordinate vector.'}, {'tex': 'w^\\top Sw=w_1^2s_a^2+2w_1w_2s_{ab}+w_2^2s_b^2', 'why': 'Take its dot product with w. The result is our expanded variance.'}], 'chapter': 2}, {'id': 29, 'title': 'Check both routes with real numbers', 'action': 'Compare direct squared scores with wᵀ S w at any angle.', 'claim': 'The two calculations agree because we derived their identity.', 'scene': 'objective', 'steps': [{'tex': '\\frac{(X_cw)^\\top(X_cw)}{n-1}=w^\\top\\frac{X_c^\\top X_c}{n-1}w=w^\\top Sw', 'why': 'Transposing a product reverses its order. These are three forms of the same calculation.'}], 'chapter': 2}, {'id': 30, 'title': 'State the optimization problem', 'action': 'Show a unit circle of permitted directions and a variance curve.', 'claim': 'Maximize wᵀ S w with wᵀ w = 1.', 'scene': 'objective', 'steps': [{'tex': '\\max_w\\; w^\\top Sw\\qquad\\text{subject to }w^\\top w=1', 'why': 'Choose the direction with the largest score variance. Compare only arrows of unit length.'}], 'chapter': 2}, {'id': 31, 'title': 'What does S do to an arrow?', 'action': 'Move w around the unit circle. Show Sw on a common labeled scale.', 'claim': 'A matrix is also a rule that maps one vector to another.', 'scene': 'eigen', 'steps': [{'tex': 'Sw=\\frac13\\begin{bmatrix}10w_1+8w_2\\\\8w_1+10w_2\\end{bmatrix}', 'why': 'The same covariance matrix can map a direction arrow to a new arrow.'}], 'chapter': 3}, {'id': 32, 'title': 'At an optimum, turning cannot help', 'action': 'Compare a direction with small clockwise and counterclockwise turns.', 'claim': 'The allowed change runs along the circle. At an optimum its first-order gain is zero.', 'scene': 'eigen', 'steps': [{'tex': 't=\\begin{bmatrix}-w_2\\\\w_1\\end{bmatrix},\\qquad \\frac{dV}{d\\theta}=2t^\\top Sw', 'why': 'The vector t points along a small turn of w. At a stationary direction, this slope is zero.'}], 'chapter': 3}, {'id': 33, 'title': 'Find the variance slope', 'action': 'Differentiate the two-coordinate quadratic one term at a time.', 'claim': 'The gradient is (2S11w1+2S12w2, 2S12w1+2S22w2) = 2Sw.', 'scene': 'eigen', 'steps': [{'tex': 'f(w_1,w_2)=S_{11}w_1^2+2S_{12}w_1w_2+S_{22}w_2^2', 'why': 'A partial derivative changes one coordinate while the other stays fixed.'}, {'tex': '\\frac{\\partial f}{\\partial w_1}=2S_{11}w_1+2S_{12}w_2', 'why': 'Use the square rule. The term with only w2 has zero derivative.'}, {'tex': '\\frac{\\partial f}{\\partial w_2}=2S_{12}w_1+2S_{22}w_2', 'why': 'Repeat for w2. Symmetry makes the two cross-term coefficients agree.'}, {'tex': '\\nabla f=2Sw', 'why': 'The gradient collects these two slopes into one vector.'}], 'chapter': 3}, {'id': 34, 'title': 'Find the constraint direction', 'action': 'Differentiate w1²+w2². Show the normal arrow to the circle.', 'claim': 'The gradient 2w points outward; allowed small changes point perpendicular to it.', 'scene': 'eigen', 'steps': [{'tex': 'g(w)=w_1^2+w_2^2-1=0', 'why': 'This equation describes the circle of permitted directions.'}, {'tex': '\\nabla g=\\begin{bmatrix}2w_1\\\\2w_2\\end{bmatrix}=2w', 'why': 'The gradient points outward. A small allowed change is tangent to the circle.'}], 'chapter': 3}, {'id': 35, 'title': 'Match the two normal directions', 'action': 'Align the gradient arrows at a stationary point.', 'claim': '2Sw = 2λw, so Sw = λw. This finds candidates; it does not yet prove a maximum.', 'scene': 'eigen', 'steps': [{'tex': '\\nabla f=\\lambda\\nabla g', 'why': 'At a constrained optimum, the objective gradient has no component along an allowed small change.'}, {'tex': '2Sw=2\\lambda w', 'why': 'Substitute the two gradients that we just calculated.'}, {'tex': 'Sw=\\lambda w', 'why': 'Divide both sides by two. The multiplier becomes the scale factor of this direction.'}], 'chapter': 3}, {'id': 36, 'title': 'Name the equation after it appears', 'action': 'Compare w and Sw at both stationary directions.', 'claim': 'An eigenvector keeps its direction under S. Its eigenvalue is the scale factor.', 'scene': 'eigen', 'steps': [{'tex': 'Sq=\\lambda q', 'why': 'The input arrow q and its image Sq lie on the same line. This defines an eigenvector and its eigenvalue.'}], 'chapter': 3}, {'id': 37, 'title': 'Find the possible scale factors', 'action': 'Subtract λ on the diagonal. Expand the 2×2 determinant.', 'claim': 'A nonzero solution requires S−λI to be singular. Explain determinant only here.', 'scene': 'eigen', 'steps': [{'tex': '(S-\\lambda I)q=0,\\quad q\\neq0', 'why': 'Move the right side to the left. A nonzero solution requires a singular matrix.'}, {'tex': '\\det(S-\\lambda I)=\\left(\\frac{10}3-\\lambda\\right)^2-\\left(\\frac83\\right)^2=0', 'why': 'For a two-by-two matrix, the determinant is the diagonal product minus the other product.'}], 'chapter': 3}, {'id': 38, 'title': 'Solve our two eigenvalues', 'action': 'Factor (10/3−λ)²−(8/3)². Link each root to the curve.', 'claim': 'The roots are 6 and 2/3.', 'scene': 'eigen', 'steps': [{'tex': '\\left(\\frac{10}3-\\lambda-\\frac83\\right)\\left(\\frac{10}3-\\lambda+\\frac83\\right)=0', 'why': 'Factor the difference of two squares.'}, {'tex': '\\left(\\frac23-\\lambda\\right)(6-\\lambda)=0', 'why': 'A product is zero when one factor is zero.'}, {'tex': '\\lambda_1=6,\\qquad\\lambda_2=\\frac23', 'why': 'These are the two possible scale factors. We order them from largest to smallest.'}], 'chapter': 3}, {'id': 39, 'title': 'Find and normalize the directions', 'action': 'Solve w2=w1 and w2=−w1. Set each vector length to one.', 'claim': 'The directions are (1,1)/√2 and (1,−1)/√2.', 'scene': 'eigen', 'steps': [{'tex': 'q=(u,v),\\quad\\lambda=6:\\quad -8u+8v=0\\;\\Rightarrow\\;v=u', 'why': 'Substitute 6 in the first row of the eigenvector equation. Multiply that row by three.'}, {'tex': 'q_1=\\frac{(1,1)}{\\sqrt2},\\qquad q_2=\\frac{(1,-1)}{\\sqrt2}', 'why': 'Repeat for 2/3. Divide each direction by its length to make a unit vector.'}], 'chapter': 3}, {'id': 40, 'title': 'A candidate can be a minimum', 'action': 'Select each eigenvector and compare its variance.', 'claim': 'The eigenvector equation alone does not choose PC1.', 'scene': 'eigen', 'steps': [{'tex': 'V(q)=q^\\top Sq=q^\\top(\\lambda q)=\\lambda', 'why': 'A unit eigenvector has variance equal to its eigenvalue. One candidate is the maximum; the other is the minimum.'}], 'chapter': 3}, {'id': 41, 'title': 'Why are these directions perpendicular?', 'action': 'Expand q1ᵀSq2 in two ways and compare.', 'claim': 'Symmetry gives (λ1−λ2)q1ᵀq2=0. Distinct eigenvalues imply perpendicular eigenvectors.', 'scene': 'eigen', 'steps': [{'tex': 'q_1^\\top Sq_2=\\lambda_2 q_1^\\top q_2', 'why': 'Apply S to q2 first.'}, {'tex': 'q_1^\\top Sq_2=(Sq_1)^\\top q_2=\\lambda_1 q_1^\\top q_2', 'why': 'Symmetry lets S act on the other vector.'}, {'tex': '(\\lambda_1-\\lambda_2)q_1^\\top q_2=0', 'why': 'If the eigenvalues differ, the dot product must be zero. The two directions are perpendicular.'}], 'chapter': 3}, {'id': 42, 'title': 'Build any unit direction from them', 'action': 'Rotate w and show coefficients a and b on the two eigenvectors.', 'claim': 'w=aq1+bq2 and a²+b²=1. State the symmetric-matrix basis theorem for higher dimensions.', 'scene': 'maximum', 'steps': [{'tex': 'w=aq_1+bq_2,\\qquad a^2+b^2=1', 'why': 'The two unit eigenvectors form perpendicular axes. Every unit direction has coordinates a and b on these axes.'}], 'chapter': 3}, {'id': 43, 'title': 'Expand variance in the new basis', 'action': 'Open four terms. Cancel both cross-terms with orthogonality.', 'claim': 'The result is λ1a²+λ2b².', 'scene': 'maximum', 'steps': [{'tex': 'w^\\top Sw=(aq_1+bq_2)^\\top S(aq_1+bq_2)', 'why': 'Substitute the coordinates of w in the eigenvector basis.'}, {'tex': '=a^2\\lambda_1+ab\\lambda_2q_1^\\top q_2+ab\\lambda_1q_2^\\top q_1+b^2\\lambda_2', 'why': 'Expand the four products. Replace Sq1 and Sq2 with their eigenvalue forms.'}, {'tex': '=a^2\\lambda_1+b^2\\lambda_2', 'why': 'Both cross-terms contain a zero dot product. Each unit vector has squared length one.'}], 'chapter': 3}, {'id': 44, 'title': 'Prove the largest value wins', 'action': 'Move the squared-weight allocation between λ1 and λ2.', 'claim': 'A weighted average cannot exceed its largest entry. Equality at q1 proves global optimality.', 'scene': 'maximum', 'steps': [{'tex': 'V=a^2\\lambda_1+b^2\\lambda_2\\leq a^2\\lambda_1+b^2\\lambda_1', 'why': 'Because λ2 is no larger than λ1, replacing λ2 cannot decrease this expression.'}, {'tex': 'V\\leq(a^2+b^2)\\lambda_1=\\lambda_1', 'why': 'The nonnegative squared weights add to one.'}, {'tex': 'w=q_1\\quad\\Rightarrow\\quad V=\\lambda_1', 'why': 'This direction reaches the bound. It is a global maximum, not just a stationary point.'}], 'chapter': 3}, {'id': 45, 'title': 'What if the eigenvalues tie?', 'action': 'Change to an isotropic cloud. Rotate freely.', 'claim': 'All directions in a tied eigenspace give the same variance. A unique PC1 is not guaranteed.', 'scene': 'maximum', 'steps': [{'tex': '\\lambda_1=\\lambda_2=\\lambda\\quad\\Rightarrow\\quad V=\\lambda(a^2+b^2)=\\lambda', 'why': 'Equal eigenvalues give the same variance for every direction in their shared space.'}], 'chapter': 3}, {'id': 46, 'title': 'Find the next component', 'action': 'Restrict the next direction to the perpendicular space.', 'claim': 'Maximize remaining variance there. In two dimensions the remaining axis is fixed up to sign.', 'scene': 'coordinates', 'steps': [{'tex': '\\max_{\\|w\\|=1,\\;w^\\top q_1=0}w^\\top Sw', 'why': 'The next component must be perpendicular to PC1. In higher dimensions, maximize variance within that remaining space.'}], 'chapter': 4}, {'id': 47, 'title': 'Read the PCA coordinates', 'action': 'Rotate both axes, then relabel the plot as PC1 and PC2.', 'claim': 'Loadings describe axes. Scores describe observations.', 'scene': 'coordinates', 'steps': [{'tex': 'Z=X_cQ,\\qquad Q=[q_1\\ q_2]', 'why': 'Each column of Q describes an axis. Each row of Z contains the new coordinates of one observation.'}], 'chapter': 4}, {'id': 48, 'title': 'Check the new covariance', 'action': 'Select an entry of QᵀSQ. See the off-diagonal product sum vanish.', 'claim': 'The score columns are uncorrelated. This does not generally mean independent.', 'scene': 'coordinates', 'steps': [{'tex': '\\operatorname{Cov}(Z)=\\frac{Z^\\top Z}{n-1}=Q^\\top SQ', 'why': 'Substitute Z=XcQ and group the covariance matrix.'}, {'tex': 'Q^\\top SQ=\\begin{bmatrix}\\lambda_1&0\\\\0&\\lambda_2\\end{bmatrix}', 'why': 'Orthonormal eigenvectors make the off-diagonal entries zero.'}], 'chapter': 4}, {'id': 49, 'title': 'Explain the 90 percent', 'action': 'Connect eigenvalue bars to the sum of squared centered distances.', 'claim': '6/(6+2/3)=90%. This is a fraction of variance, not prediction accuracy.', 'scene': 'coordinates', 'steps': [{'tex': '\\mathrm{fraction}_1=\\frac{\\lambda_1}{\\lambda_1+\\lambda_2}=\\frac{6}{6+2/3}=0.90', 'why': 'The denominator is total variance. The ratio measures retained squared spread.'}], 'chapter': 4}, {'id': 50, 'title': 'Rebuild an observation from its score', 'action': 'Select A. Multiply its score by q1, then add the mean.', 'claim': 'The reconstructed point lies on the retained line.', 'scene': 'reconstruction', 'steps': [{'tex': '\\widehat r_A=\\mu+z_Aq_1', 'why': 'Multiply the retained score by its axis. Add the stored mean.'}, {'tex': '=(6,6)+\\frac3{\\sqrt2}\\frac{(1,1)}{\\sqrt2}=(7.5,7.5)', 'why': 'A originally measured (8,7). Its one-score reconstruction has an error in both features.'}], 'chapter': 4}, {'id': 51, 'title': 'Draw the missing part', 'action': 'Show the original vector, projection, and residual as a right triangle.', 'claim': 'Orthogonality gives original squared length = kept squared length + lost squared length.', 'scene': 'reconstruction', 'steps': [{'tex': 'x_i=z_iw+e_i,\\quad w^\\top e_i=0', 'why': 'The residual e is the difference between the original point and its projection.'}, {'tex': '\\|x_i\\|^2=z_i^2+\\|e_i\\|^2', 'why': 'The kept vector and residual are perpendicular. Apply the right-triangle identity.'}], 'chapter': 4}, {'id': 52, 'title': 'Prove the second objective', 'action': 'Add the triangle identity across all observations.', 'claim': 'Total squared length is fixed, so maximizing kept variance minimizes squared reconstruction error.', 'scene': 'reconstruction', 'steps': [{'tex': '\\sum_i\\|e_i\\|^2=\\sum_i\\|x_i\\|^2-\\sum_i z_i^2', 'why': 'Add the identity for every observation and move the kept term to the right.'}, {'tex': '\\frac{\\sum_i\\|e_i\\|^2}{n-1}=\\operatorname{tr}(S)-w^\\top Sw', 'why': 'Trace is the sum of the feature variances. The first term does not depend on the direction.'}, {'tex': '\\arg\\min_w\\sum_i\\|e_i\\|^2=\\arg\\max_w w^\\top Sw', 'why': 'The same direction solves both problems. The errors are perpendicular distances, not vertical regression errors.'}], 'chapter': 4}, {'id': 53, 'title': 'Recover both coordinates', 'action': 'Switch between k=0, k=1, and k=2.', 'claim': 'Two orthonormal coordinates recover the original centered vector.', 'scene': 'reconstruction', 'steps': [{'tex': 'x_i=z_{i1}q_1+z_{i2}q_2', 'why': 'Keeping both perpendicular coordinates recovers the original centered vector.'}], 'chapter': 4}, {'id': 54, 'title': 'Choose how much to keep', 'action': 'Set a retained-variance target and select k.', 'claim': 'The task determines an acceptable error. A percentage alone does not prove usefulness.', 'scene': 'reconstruction', 'steps': [{'tex': '\\mathrm{retained}=\\frac{\\sum_{j=1}^k\\lambda_j}{\\sum_{j=1}^p\\lambda_j},\\qquad\\mathrm{loss}=\\sum_{j=k+1}^p\\lambda_j', 'why': 'The loss uses the sample divisor n−1. Multiply it by n−1 to get the total squared error.'}], 'chapter': 4}, {'id': 55, 'title': 'Extend from two features to p', 'action': 'Keep the top k eigenvalues in a larger spectrum.', 'claim': 'For orthonormal W, retained variance is tr(WᵀSW). The top k eigenvectors maximize it; discarded eigenvalues give the loss.', 'scene': 'spectrum', 'steps': [{'tex': 'V_k=\\operatorname{tr}(W^\\top SW)=\\sum_{j=1}^p\\lambda_j\\alpha_j', 'why': 'W contains k perpendicular unit directions. Define αj as the squared length of the projection of qj into their space.'}, {'tex': '0\\leq\\alpha_j\\leq1,\\qquad\\sum_j\\alpha_j=k', 'why': 'A projection cannot increase a unit vector length. The sum equals the dimension of the retained space.'}, {'tex': 'V_k\\leq\\lambda_1+\\cdots+\\lambda_k', 'why': 'Allocate the weight to the largest eigenvalues first. Choosing their eigenvectors reaches this bound.'}], 'chapter': 4}, {'id': 56, 'title': 'Connect the result to SVD', 'action': 'Substitute Xc=UΣVᵀ into S=XcᵀXc/(n−1).', 'claim': 'The columns of V are PCA directions. Eigenvalues equal squared singular values divided by n−1.', 'scene': 'spectrum', 'steps': [{'tex': 'X_c=U\\Sigma V^\\top', 'why': 'Singular value decomposition factors the centered table. U and V have orthonormal columns in the compact form.'}, {'tex': 'S=\\frac{V\\Sigma^\\top U^\\top U\\Sigma V^\\top}{n-1}=V\\frac{\\Sigma^2}{n-1}V^\\top', 'why': 'Use UᵀU=I. The diagonal entries are the squared singular values divided by n−1.'}, {'tex': 'q_j=v_j,\\qquad\\lambda_j=\\frac{\\sigma_j^2}{n-1}', 'why': 'SVD gives the same PCA directions without explicitly forming the covariance matrix.'}], 'chapter': 4}, {'id': 57, 'title': 'Use the axes on a new observation', 'action': 'Enter a new observation and apply the training mean and axes.', 'claim': 'Fit preprocessing and PCA on training data. Reuse those values for later observations.', 'scene': 'newpoint', 'steps': [{'tex': 'z_{\\mathrm{new}}=Q_k^\\top(r_{\\mathrm{new}}-\\mu_{\\mathrm{train}})', 'why': 'Keep the training mean and learned directions fixed. New observations do not refit this model.'}], 'chapter': 5}, {'id': 58, 'title': 'Decide what units mean', 'action': 'Change one feature scale, then compare standardization.', 'claim': 'Standardization changes the question. It gives each nonconstant feature unit variance.', 'scene': 'units', 'steps': [{'tex': '\\widetilde r_{ij}=\\frac{r_{ij}-\\mu_j}{s_j}', 'why': 'Divide each centered feature by its sample standard deviation. Nonconstant features then have variance one.'}], 'chapter': 5}, {'id': 59, 'title': 'Large variance is not always useful', 'action': 'Reveal a distant observation and then category labels.', 'claim': 'Outliers can dominate squared spread. A useful label can lie in a low-variance direction.', 'scene': 'outliers', 'steps': [], 'chapter': 5}, {'id': 60, 'title': 'A line cannot follow every shape', 'action': 'Compare a ring with the elongated cloud.', 'claim': 'PCA is linear. Two components may be necessary even if a curve has one intrinsic parameter.', 'scene': 'ring', 'steps': [], 'chapter': 5}, {'id': 61, 'title': 'Change the real notebook data', 'action': 'Use native marimo controls to change an observation.', 'claim': 'Python recomputes mean, covariance, directions, scores, and reconstruction.', 'scene': 'notebook', 'steps': [], 'chapter': 5}, {'id': 62, 'title': 'Solve a fresh geometric problem', 'action': 'Choose a direction for a rotated, unseen cloud before seeing its optimum.', 'claim': 'Require a prediction and a reason; then compare with the computed result.', 'scene': 'challenge', 'steps': [], 'chapter': 5}, {'id': 63, 'title': 'Produce the calculation yourself', 'action': 'Compute a covariance entry, a score, and a reconstruction for new values.', 'claim': 'Record numeric correctness separately from the learner’s written explanation.', 'scene': 'exam', 'steps': [], 'chapter': 5}, {'id': 64, 'title': 'Teach PCA back in your own words', 'action': 'Explain purpose → objective → covariance → eigenvectors → loss.', 'claim': 'Use new examples and name one limit. Reopen the exact relevant scene after a miss.', 'scene': 'teachback', 'steps': [], 'chapter': 5}], 'refreshers': {'center': ['Mean and centering', 'The mean is the sum divided by the number of observations. Calculate one mean per feature. Subtract each feature mean from its values. Centered values describe differences from the mean.'], 'score': ['Vectors and dot products', 'A vector stores coordinates. A unit vector has length one. Its dot product with a point gives the signed projection score. Multiply matching coordinates, then add.'], 'variance': ['Variance', 'Variance measures squared spread around a mean. Here the score mean is zero. Add the squared scores and divide by n−1. Using n instead changes the scale but not the best direction.'], 'expansion': ['Expand a square', 'Multiply each term in the first bracket by each term in the second bracket. In (A+B)², the middle terms are AB and BA. They give 2AB.'], 'covariance': ['Transpose and matrix multiplication', 'Transpose swaps rows and columns. A matrix product matches one row with one column. Multiply matching entries and add. In XcᵀXc, each entry compares two feature columns.'], 'objective': ['Read the dimensions', 'Xc has n rows and p columns. w has p entries. Xc w has n scores. S has p rows and p columns. wᵀSw is one number.'], 'eigen': ['Gradients, constraints, and eigenvectors', 'A derivative measures local change. A gradient collects one derivative per coordinate. On the unit circle, allowed small changes follow the tangent. At a constrained optimum, the gradient has no tangent component. Sw=λw says that S preserves the line of w.'], 'maximum': ['The basis theorem and the bound', 'A real symmetric matrix has an orthonormal basis of eigenvectors. We use this theorem for higher dimensions. The two-dimensional example can be checked directly. Squared coordinates in this basis are nonnegative and add to one. Their weighted eigenvalue average cannot exceed the largest eigenvalue.'], 'coordinates': ['Loadings and scores', 'Loadings are the feature weights in an axis. Scores are the coordinates of observations on that axis. Sign reversal changes both signs and preserves the same projection. Zero covariance does not generally imply independence.'], 'reconstruction': ['Length, projection, and trace', 'The squared length of (a,b) is a²+b². A unit-axis projection is zw. Its residual is perpendicular to the axis. Their squared lengths add. Trace means the sum of the diagonal entries.'], 'spectrum': ['Several retained directions', 'The columns of W are perpendicular unit vectors. WᵀW=I. Projecting onto these k directions gives k scores. Keeping all directions preserves the data. Keeping fewer can lose detail.'], 'geometry': ['How to read this picture', 'Each letter is one observation. Teal marks the retained axis. The score line shows one number for each observation. Orange marks a lost part. The axis we keep is perpendicular to the direction of a shadow.']}, 'notation': [['rᵢ', 'An original observation, before centering.'], ['μ', 'The mean of each original feature.'], ['xᵢ', 'One centered observation: rᵢ−μ.'], ['Xc', 'A table of centered observations, one per row.'], ['w', 'A candidate direction of unit length.'], ['zᵢ', 'The score of observation i on w.'], ['S', 'The sample covariance matrix.'], ['qⱼ', 'A learned unit eigenvector, or PCA direction.'], ['λⱼ', 'Variance along qⱼ.'], ['k', 'The number of retained components.']]}
    None

    return


@app.cell(hide_code=True)
def pca_alternatives_v2(make_pca_case, np, pca_lab):
    _alt_packs = []
    _circle=np.linspace(0,2*np.pi,12,endpoint=False)
    _small_ring=make_pca_case(np.column_stack([np.cos(_circle),np.sin(_circle)])*3,False)
    for _source in [pca_lab['covCases'], [pca_lab['edgeCases'][1],_small_ring,pca_lab['nuisance']]]:
        _alt_list=[]
        for _old in _source:
            _case=make_pca_case(_old['raw'])
            for _frame in _case['frames']:
                for _key in ['terms','residual','turn','eigen','lengths','kept','lost']:
                    _frame.pop(_key,None)
            _alt_list.append(_case)
        _alt_packs.append(_alt_list)
    pca_cov_v2=_alt_packs[0]
    # Base-case triangles need the three squared lengths. Other examples do not.
    pca_cov_v2[0]=pca_lab['base']
    pca_edges_v2=_alt_packs[1]
    pca_model_v2={'challenge':pca_lab['challenge']}
    pca_scales_v2=[]
    for _scale in pca_lab['scales']:
        _pack={}
        for _kind in ['raw','standard']:
            _case=make_pca_case(_scale[_kind]['raw'],False)
            _w=np.asarray(_case['axes'][0])
            _pts=np.asarray(_case['points'])
            _z=_pts@_w
            _pr=np.outer(_z,_w)
            _kept=_z**2
            _lost=((_pts-_pr)**2).sum(1)
            _case['frames']=[dict(w=_w.tolist(),sw=(np.asarray(_case['cov'])@_w).tolist(),z=_z.tolist(),projected=_pr.tolist(),kept=_kept.tolist(),lost=_lost.tolist(),lengths=(_pts**2).sum(1).tolist(),variance=_case['values'][0],loss=_case['values'][1],ratio=_case['ratio'],slope=0,sumSquares=float(_kept.sum()))]
            _pack[_kind]=_case
        pca_scales_v2.append(_pack)
    None

    return


if __name__ == "__main__":
    app.run()
