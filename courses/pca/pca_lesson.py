# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = ["marimo-studio[deno]==0.2.3", "numpy==2.5.3"]
#
# [tool.marimo-studio]
# default = "lesson"
# view_root = "v"
# ///

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")


@app.cell
def imports():
    import marimo as mo
    from pca_math import BASE_RAW, course_data, projection_case

    return BASE_RAW, course_data, mo, projection_case


@app.cell(hide_code=True)
def welcome(mo):
    mo.md(r"""
    # PCA: keep the useful variation

    We measured four positions in centimeters. Suppose we can store only one
    number for each position. Which direction should that number measure?
    Principal component analysis finds the direction that keeps the most
    variation. For this squared-distance problem, it also loses the least.

    This notebook contains the data, live controls, calculations, and argument.
    In the native Studio shell, use the notebook surface and the **lesson**
    view together. For the separate presentation process, open
    [the slides on port 2729](http://localhost:2729/lesson/).

    Rows below are observations A–D. Columns are the x and y measurements.
    The fixed main example is A=(8,7), B=(7,8), C=(5,4), D=(4,5).
    The sandbox changes only D's x coordinate. Its results are shown separately
    from the fixed example so you can compare them.
    """)
    return


@app.cell
def fixed_model(course_data):
    pca_data = course_data()
    return (pca_data,)


@app.cell(hide_code=True)
def fixed_example(mo, pca_data):
    _base = pca_data["base"]
    mo.vstack([
        mo.md("## The fixed measurements"),
        mo.ui.table([
            {"Observation": chr(65 + i), "x (cm)": row[0], "y (cm)": row[1]}
            for i, row in enumerate(_base["raw"])
        ], selection=None),
        mo.md(r"""
        The mean is (6,6). Subtract it from every row to get the centered
        matrix $X$: (2,1), (1,2), (−1,−2), (−2,−1). Each column now sums to zero.
        Centering makes PCA describe variation around the cloud's center.
        Without it, a large offset from the origin can dominate the result.

        A candidate direction is a unit vector $w$. The signed coordinate of
        row $x_i$ along that direction is $z_i=x_i^T w$. Collect the scores in
        $z=Xw$. The point on the line is $\hat{x}_i=z_iw$. A score is one number;
        a projected point still has two coordinates.
        """),
    ])
    return


@app.cell(hide_code=True)
def sandbox_controls(mo):
    angle_control = mo.ui.slider(
        start=0, stop=180, step=1, value=45,
        label="Direction angle (degrees)", show_value=True,
    )
    outlier_control = mo.ui.slider(
        start=0, stop=8, step=0.5, value=0,
        label="Add to D's x coordinate (cm)", show_value=True,
    )
    mo.vstack([angle_control, outlier_control])
    return angle_control, outlier_control


@app.cell
def live_model(BASE_RAW, angle_control, outlier_control, projection_case):
    pca_live = projection_case(BASE_RAW, angle_control.value, outlier_control.value)
    return (pca_live,)


@app.cell(hide_code=True)
def live_results(mo, pca_live):
    _live = pca_live
    mo.vstack([
        mo.md(f"""
        ## Your current projection

        Angle **{_live['angleDeg']:.0f}°**; D's x displacement **{_live['outlier']:.1f} cm**.

        Score variance: **{_live['variance']:.6f} cm²**. Lost variation:
        **{_live['loss']:.6f} cm²**. Total: **{_live['totalVariance']:.6f} cm²**.

        Both quantities divide by n−1=3. The lost variation is the sum of
        squared perpendicular residual lengths divided by 3. It is not the
        raw sum of squared errors. Move the angle to trade kept variation for
        lost variation; their sum stays fixed for one dataset.
        """),
        mo.ui.table([
            {"Observation": chr(65 + i), "Centered x": point[0], "Centered y": point[1],
             "Score": _live["scores"][i], "Projected x": _live["reconstruction"][i][0],
             "Projected y": _live["reconstruction"][i][1]}
            for i, point in enumerate(_live["points"])
        ], selection=None),
        mo.md("The covariance matrix for the current data is:"),
        mo.ui.table([
            {"Row": i + 1, "Column 1": row[0], "Column 2": row[1]}
            for i, row in enumerate(_live["cov"])
        ], selection=None),
    ])
    return


@app.cell(hide_code=True)
def covariance_argument(mo):
    mo.md(r"""
    ## Why covariance appears

    The centered scores also sum to zero, so their sample variance is the
    average squared score with denominator $n-1$:

    $$\operatorname{Var}(z)=\frac{1}{n-1}\sum_i(x_i^T w)^2
       =\frac{(Xw)^T(Xw)}{n-1}
       =w^T\left(\frac{X^TX}{n-1}\right)w=w^TSw.$$

    The first equality measures spread along the chosen line. The second
    collects every squared score in a dot product. The third uses
    $(Xw)^T=w^TX^T$. Define $S=X^TX/(n-1)$ once; now we can compare directions
    without repeating a separate sum over observations.

    Each diagonal entry $S_{jj}$ is a feature's variance. An off-diagonal
    entry averages products of paired deviations: do the features tend to
    move in the same direction? For the fixed example,

    $$S=\frac13\begin{bmatrix}10&8\\8&10\end{bmatrix}.$$

    The off-diagonal value is $8/3$: the four products are 2, 2, 2, 2.
    Covariance keeps units: these entries have units cm². Changing one
    feature's scale changes the problem that PCA solves.
    """)
    return


@app.cell(hide_code=True)
def eigenvector_argument(mo):
    mo.md(r"""
    ## From the best direction to an eigenvector

    Maximize $w^TSw$ subject to $w^Tw=1$. Without that constraint, multiplying
    $w$ by a large number would increase the score variance without finding
    a better direction.

    Use $L(w,\lambda)=w^TSw-\lambda(w^Tw-1)$. Since $S$ is symmetric,
    $\nabla_w(w^TSw)=2Sw$ and $\nabla_w(w^Tw)=2w$. At a constrained stationary
    point, $2Sw-2\lambda w=0$, hence $Sw=\lambda w$.

    This makes $w$ an eigenvector. Multiplying by $w^T$ gives
    $w^TSw=\lambda w^Tw=\lambda$: its eigenvalue is its score variance.
    A stationary point alone does not prove we found the largest variance.

    ## Why the largest eigenvalue is a global maximum

    A real symmetric matrix has an orthonormal eigenbasis $q_1,\ldots,q_d$.
    Order its eigenvalues $\lambda_1\ge\cdots\ge\lambda_d$ and write any unit
    vector as $w=\sum_j a_jq_j$. Orthonormality gives $\sum_j a_j^2=1$.
    Substitute into the objective:

    $$w^TSw=\sum_j\lambda_j a_j^2
       \le\lambda_1\sum_j a_j^2=\lambda_1.$$

    The cross terms vanish because different basis vectors are perpendicular.
    The remaining terms form a weighted average of the eigenvalues. No such
    average can exceed the largest entry. Choosing $w=q_1$ reaches the bound,
    which proves a global maximum. If the largest eigenvalue is repeated,
    several directions can reach it; a unique first axis is not guaranteed.

    For the fixed example, $q_1=(1,1)/\sqrt2$ has eigenvalue 6 and
    $q_2=(1,-1)/\sqrt2$ has eigenvalue $2/3$. The first direction keeps
    $6/(6+2/3)=90\%$ of the total sample variance. Either sign of an axis
    describes the same line; its scores change sign too.
    """)
    return


@app.cell(hide_code=True)
def reconstruction_and_svd(mo):
    mo.md(r"""
    ## Why keeping variation also minimizes squared error

    For unit $w$, the residual $r_i=x_i-(x_i^Tw)w$ is perpendicular to $w$.
    Pythagoras therefore gives
    $\|x_i\|^2=(x_i^Tw)^2+\|r_i\|^2$. Sum over observations and divide by
    $n-1$: total variation = kept score variance + lost variation.
    The total is fixed for a fixed centered dataset, so maximizing what we
    keep minimizes what we lose. Add the mean back to a reconstructed point
    to return to the original measurement coordinates.

    For several components, collect the first $k$ orthonormal eigenvectors
    in $Q_k$. Scores are $Z=XQ_k$ and the centered reconstruction is
    $\hat X=ZQ_k^T=XQ_kQ_k^T$. Keeping all available components recovers $X$;
    keeping fewer generally loses information.

    ## The same result through SVD

    Let $X=U\Sigma V^T$ be a singular value decomposition. Then
    $X^TX=V\Sigma^2V^T$, because $U^TU=I$. The right singular vectors are
    covariance eigenvectors and $\lambda_j=\sigma_j^2/(n-1)$. Computing PCA
    through SVD avoids explicitly forming $X^TX$ and is often a useful
    numerical route. The notebook exposes both results so they can be checked.

    ## Before using PCA on another problem

    Decide what distances should mean. A feature measured on a much larger
    scale can dominate covariance PCA; standardization changes that metric.
    Outliers can rotate the chosen axes because squared deviations give them
    high weight. Equal eigenvalues make individual axes ambiguous. Low
    variance does not imply low predictive value for a target. Fit the mean,
    scaling, and axes on training data, then apply those fitted operations to
    held-out data. PCA is a linear approximation; a curved structure can need
    a different representation.

    Try this without the display: explain why the diagonal axis is best in
    the fixed example, why swapping its sign is harmless, and why the proof
    above does more than finding a stationary point.
    """)
    return


if __name__ == "__main__":
    app.run()
