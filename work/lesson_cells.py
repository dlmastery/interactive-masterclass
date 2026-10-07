import marimo._code_mode as cm
import textwrap

cells = {
"centering_control": '''
center_amount = mo.ui.slider(0, 1, step=0.1, value=0, label="Fraction of mean subtracted", show_value=True)
center_amount
''',
"correlation_control": '''
rho = mo.ui.slider(-0.9, 0.9, step=0.05, value=0.75, label="Correlation", show_value=True)
rho
''',
"direction_control": '''
angle = mo.ui.slider(0, 180, step=1, value=0, label="Direction angle (degrees)", show_value=True)
angle
''',
"dimension_control": '''
components = mo.ui.radio({"One component": 1, "Both components": 2}, value="One component", label="Keep")
components
''',
"scale_control": '''
scale_y = mo.ui.slider(1, 8, step=1, value=1, label="Multiply feature 2 units by", show_value=True)
standardize = mo.ui.checkbox(value=False, label="Standardize each feature")
mo.vstack([scale_y, standardize])
''',
"data_explanation": '''
mo.md("""## A controlled point cloud
These 48 synthetic observations have exactly zero sample mean and a chosen
sample covariance. A fixed seed holds the observations steady as controls change.
Feature units are arbitrary. The units experiment uses a separate copy.
""")
''',
"data_model": '''
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
''',
"projection_model": '''
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
''',
"scale_model": '''
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
''',
"center_math": r'''
mo.md(r"""
$$\mu=\frac{1}{n}\sum_{i=1}^{n}x_i,\qquad X_c=X-\mathbf 1\mu^\top$$

Each row of $X$ is one observation. Each column is one feature.
Subtracting the column means moves the cloud without changing its shape.
Here $n=48$, $p=2$, and $\mu=(5,3)^\top$.
""")
''',
"covariance_math": r'''
mo.md(r"""
$$S_{jk}=\frac{1}{n-1}\sum_i (x_{ij}-\mu_j)(x_{ik}-\mu_k)$$
$$S=\frac{X_c^\top X_c}{n-1}=
\begin{bmatrix}\operatorname{Var}(x_1)&\operatorname{Cov}(x_1,x_2)\\
\operatorname{Cov}(x_1,x_2)&\operatorname{Var}(x_2)\end{bmatrix}$$

Same-sign deviations contribute positively. Opposite-sign deviations contribute negatively.
The diagonal measures each feature's spread.
""")
''',
"score_math": r'''
mo.md(r"""
$$w=\begin{bmatrix}\cos\theta\\\sin\theta\end{bmatrix},\quad
z_i=w^\top(x_i-\mu),\quad z=X_cw$$
$$\hat x_i=\mu+z_iw$$

The **score** $z_i$ is a signed coordinate along the axis.
The **loading vector** $w$ tells us how to combine the original features.
The perpendicular segments show what a one-number representation loses.
""")
''',
"variance_step1": r'''
mo.md(r"""Since $X_c$ is centered, the score mean is zero.
$$\operatorname{Var}(z)=\frac{1}{n-1}\sum_i z_i^2=\frac{z^\top z}{n-1}$$""")
''',
"variance_step2": r'''
mo.md(r"""Substitute $z=X_cw$ and group the middle terms.
$$\frac{(X_cw)^\top(X_cw)}{n-1}
=w^\top\!\underbrace{\frac{X_c^\top X_c}{n-1}}_{S}\!w=w^\top Sw$$""")
''',
"variance_step3": r'''
mo.md(r"""PCA chooses the axis with maximum projected variance.
$$\max_{w\in\mathbb R^p} w^\top Sw\quad\text{subject to }w^\top w=1$$
The constraint fixes the ruler's length. Otherwise scaling $w$ makes the variance arbitrarily large.""")
''',
"eigen_step1": r'''
mo.md(r"""Introduce a multiplier for the unit-length constraint.
$$\mathcal L(w,\lambda)=w^\top Sw-\lambda(w^\top w-1)$$""")
''',
"eigen_step2": r'''
mo.md(r"""Because $S=S^\top$, the gradient is $2Sw$.
$$\nabla_w\mathcal L=2Sw-2\lambda w=0\quad\Longrightarrow\quad Sw=\lambda w$$""")
''',
"eigen_step3": r'''
mo.md(r"""At an eigenvector, $w^\top Sw=\lambda w^\top w=\lambda$.
The largest eigenvalue gives the maximum.

Why global? Write $w=\sum_j a_jv_j$ in an orthonormal eigenbasis.
$$w^\top Sw=\sum_j\lambda_j a_j^2\leq\lambda_1\sum_j a_j^2=\lambda_1$$""")
''',
"worked_data": r'''
example_X = np.array([[2.,1.],[1.,2.],[-1.,-2.],[-2.,-1.]])
example_S = example_X.T @ example_X / 3
_ev, _ew = np.linalg.eigh(example_S)
example = {"cov": example_S.tolist(), "values": _ev[::-1].tolist(),
           "ratio": float(_ev[-1] / _ev.sum())}
mo.md(r"""
$$X_c=\begin{bmatrix}2&1\\1&2\\-1&-2\\-2&-1\end{bmatrix},\qquad
X_c^\top X_c=\begin{bmatrix}10&8\\8&10\end{bmatrix}$$
$$S=\frac13\begin{bmatrix}10&8\\8&10\end{bmatrix}$$
For example, the off-diagonal sum is $2\cdot1+1\cdot2+(-1)(-2)+(-2)(-1)=8$.
""")
''',
"worked_solution": r'''
mo.md(r"""
$$\det(S-\lambda I)=\left(\frac{10}{3}-\lambda\right)^2-\left(\frac83\right)^2=0$$
$$\lambda_1=6,\quad\lambda_2=\frac23,\qquad
w_1=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix},\quad
w_2=\frac{1}{\sqrt2}\begin{bmatrix}-1\\1\end{bmatrix}$$
$$z_1=X_cw_1=\frac{1}{\sqrt2}(3,3,-3,-3)^\top,\qquad
\frac{\lambda_1}{\lambda_1+\lambda_2}=90\%$$
Four points, one component, 90% of sample variance retained.
""")
''',
"orthogonal_math": r'''
mo.md(r"""
$$W=[w_1\;\cdots\;w_p],\quad W^\top W=I,\quad Z=X_cW$$
$$\operatorname{Cov}(Z)=W^\top SW=\operatorname{diag}(\lambda_1,\ldots,\lambda_p)$$
PC2 maximizes the remaining variance subject to being orthogonal to PC1.
Scores are **uncorrelated**. Independence does not follow in general.
Flipping an eigenvector's sign changes score signs but preserves its axis.
""")
''',
"reconstruction_math": r'''
mo.md(r"""
$$Z_k=X_cW_k,\qquad \widehat X_c=Z_kW_k^\top$$
$$\frac{\|X_c-\widehat X_c\|_F^2}{n-1}
=\operatorname{tr}(S)-\sum_{j=1}^k\lambda_j
=\sum_{j>k}\lambda_j$$
Add the mean back to return to original coordinates.
All components preserve the data (up to rounding).
""")
''',
"loss_proof": r'''
mo.md(r"""
For one unit vector, the projection and residual are perpendicular.
$$\|x_{ci}-w w^\top x_{ci}\|^2=\|x_{ci}\|^2-(w^\top x_{ci})^2$$
Sum over observations and divide by $n-1$:
$$\text{loss}=\operatorname{tr}(S)-w^\top Sw$$
Total spread stays fixed, so maximizing retained variance minimizes squared reconstruction error.
The displayed loss uses $n-1$; per-observation mean squared distance uses $n$.
""")
''',
"units_math": r'''
mo.md(r"""
$$\widetilde X_{ij}=\frac{X_{ij}-\mu_j}{s_j},\qquad
S_{\mathrm{standardized}}=\operatorname{Corr}(X)$$
Covariance PCA depends on feature units. Standardizing gives each nonconstant
feature unit sample variance, changing the optimization's metric.
Choose the metric to match the problem. Standardizing is a choice, not a universal rule.
""")
''',
"svd_math": r'''
mo.md(r"""
$$X_c=U\Sigma V^\top\quad\Longrightarrow\quad
S=V\frac{\Sigma^2}{n-1}V^\top$$
$$W=V,\qquad Z=U\Sigma,\qquad\lambda_j=\frac{\sigma_j^2}{n-1}$$
SVD computes the same principal directions without explicitly forming $X_c^\top X_c$.
For new observations, reuse the training mean, scales (if any), and loading vectors.
""")
''',
"quiz_control": '''
quiz = mo.ui.radio(["Choose an answer", "Keep the direction with greatest variance", "Keep the original feature with largest values", "Choose the direction that best predicts a label"], value="Choose an answer", label="What does PC1 optimize?")
quiz
''',
"quiz_feedback": '''
if quiz.value == "Choose an answer":
    _answer = "Make a prediction, then test it on the projection slide."
elif quiz.value == "Keep the direction with greatest variance":
    _answer = "Correct. Under a unit-length constraint, PC1 maximizes projected sample variance. It also minimizes squared reconstruction error for a one-dimensional linear subspace."
elif quiz.value == "Keep the original feature with largest values":
    _answer = "Try again. A component can combine every feature. Centering removes offsets, so large raw values alone do not determine PC1."
else:
    _answer = "Try again. PCA uses no target labels. High variance can be irrelevant to a prediction task."
mo.md(_answer)
''',
"cautions": '''
mo.md("""
- **Equal eigenvalues:** there is no unique preferred axis in that eigenspace.
- **Large variance:** may reflect signal, nuisance variation, or outliers.
- **Curved structure:** a straight subspace may need many components.
- **Component count:** use the error or retained variance your task can tolerate.

Explain back: Why does covariance need centering? Why must the direction have unit length?
Why does losing less variance mean reconstructing better?
""")
''',
"implementation": '''
mo.md(r"""## Reusable calculation
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
""")
''',
}

async with cm.get_context() as ctx:
    existing = {c.name: c for c in ctx.cells}
    for name, code in cells.items():
        code = textwrap.dedent(code).strip()
        if name in existing:
            old_code = existing[name].code
            cid = existing[name].id
            ctx.edit_cell(cid, code, name=name)
        else:
            cid = ctx.create_cell(code, name=name)
        ctx.run_cell(cid)

print("Created and ran", len(cells), "lesson cells")
