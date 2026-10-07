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
    # PCA: from picture to proof

    This notebook supplies the calculations for the 64-slide course.

    [Open the slides](http://localhost:2719/lesson/)

    The example uses four invented position measurements in centimeters.
    The first three observations stay fixed. Use the two controls below to change observation D.
    The results update when you change either value.

    Use **Course route** in the slides to move between six questions.
    Use **Math at this step** for a short refresher without leaving the current scene.

    The six expandable sections below contain the full argument and its equation steps.
    """)
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

    return (sandbox_lab,)


@app.cell(hide_code=True)
def pca_course_v2():
    pca_course_v2 = {'version': 2, 'title': 'PCA · from picture to proof', 'chapters': [{'start': 0, 'end': 8, 'question': 'What does PCA do?'}, {'start': 8, 'end': 20, 'question': 'How do we measure a view?'}, {'start': 20, 'end': 30, 'question': 'Why does covariance appear?'}, {'start': 30, 'end': 45, 'question': 'Why do eigenvectors solve it?'}, {'start': 45, 'end': 56, 'question': 'What can we keep and recover?'}, {'start': 56, 'end': 64, 'question': 'When does the result help?'}], 'slides': [{'id': 1, 'title': 'What is PCA?', 'action': 'Rotate one line through a measured cloud. Watch four observations become four scores.', 'claim': 'PCA finds new perpendicular axes, ordered by variance. Keeping fewer axes reduces the number of values per observation.', 'scene': 'geometry', 'steps': [], 'chapter': 0}, {'id': 2, 'title': 'One number is a position on a line', 'action': 'Select an observation. Link its point, projection, and single stored score.', 'claim': 'The point and its score refer to the same observation.', 'scene': 'geometry', 'steps': [], 'chapter': 0}, {'id': 3, 'title': 'Some views lose more than others', 'action': 'Compare 45° and 135° with the same scale in both score plots.', 'claim': 'A useful projection keeps a large part of the original squared spread.', 'scene': 'geometry', 'steps': [], 'chapter': 0}, {'id': 4, 'title': 'A projection follows a perpendicular', 'action': 'Move one point to its closest position on the chosen line.', 'claim': 'The line is the axis that we KEEP; the viewing direction is perpendicular to it.', 'scene': 'geometry', 'steps': [], 'chapter': 0}, {'id': 5, 'title': 'What does one score lose?', 'action': 'Hide the original points. Reveal the possible points that share a score.', 'claim': 'A score cannot recover movement across its axis.', 'scene': 'geometry', 'steps': [], 'chapter': 0}, {'id': 6, 'title': 'Turn the axes, then remove one', 'action': 'Switch between two rotated coordinates and one retained coordinate.', 'claim': 'Rotation alone loses nothing. Removing a coordinate can lose detail.', 'scene': 'geometry', 'steps': [], 'chapter': 0}, {'id': 7, 'title': 'What will best mean?', 'action': 'Compare kept squared spread with squared reconstruction error.', 'claim': 'These are two equivalent PCA objectives under the same Euclidean scale.', 'scene': 'geometry', 'steps': [], 'chapter': 0}, {'id': 8, 'title': 'See the whole method once', 'action': 'Step through center → find axes → keep scores → reconstruct.', 'claim': 'The next chapters explain how to compute this result.', 'scene': 'geometry', 'steps': [], 'chapter': 0}, {'id': 9, 'title': 'Measure change from a shared center', 'action': 'Translate the cloud without changing its shape.', 'claim': 'The PCA direction describes variation around the mean.', 'scene': 'center', 'steps': [], 'chapter': 1}, {'id': 10, 'title': 'Find the center of this cloud', 'action': 'Highlight one column and calculate its mean.', 'claim': 'Introduce the mean only because we need this center.', 'scene': 'center', 'steps': [{'tex': '\\mu=\\left(\\frac{8+7+5+4}{4},\\frac{7+8+4+5}{4}\\right)=(6,6)', 'why': 'Add the four values in each column. Divide each sum by four.'}], 'chapter': 1}, {'id': 11, 'title': 'Move the center to zero', 'action': 'Scrub the translation. Keep observation labels fixed.', 'claim': 'Subtract the corresponding feature mean from each observation.', 'scene': 'center', 'steps': [{'tex': 'x_A=(8,7)-(6,6)=(2,1)', 'why': 'Subtract the mean of each feature. A is two units right and one unit up from the center.'}], 'chapter': 1}, {'id': 12, 'title': 'The distances do not change', 'action': 'Select two observations before and after translation.', 'claim': 'Centering changes the origin, not the relative positions.', 'scene': 'center', 'steps': [{'tex': '(r_A-\\mu)-(r_B-\\mu)=r_A-r_B', 'why': 'The two copies of the mean cancel. The difference between observations stays the same.'}], 'chapter': 1}, {'id': 13, 'title': 'Describe the line with two numbers', 'action': 'Rotate a unit arrow. Its horizontal and vertical parts update.', 'claim': 'The vector w gives a direction and has length one.', 'scene': 'score', 'steps': [{'tex': 'w=\\begin{bmatrix}\\cos\\theta\\\\\\sin\\theta\\end{bmatrix},\\quad w_1^2+w_2^2=1', 'why': 'The angle sets the direction. The unit length fixes the scale of its scores.'}], 'chapter': 1}, {'id': 14, 'title': 'Calculate one score', 'action': 'Select A. Multiply each centered coordinate by its direction weight.', 'claim': 'The dot product gives signed distance along a unit axis.', 'scene': 'score', 'steps': [{'tex': 'z_A=w^\\top x_A=2w_1+w_2', 'why': 'Multiply matching coordinates. Add the two products. A negative score is on the other side of the center.'}], 'chapter': 1}, {'id': 15, 'title': 'Use one rule for every observation', 'action': 'Link each row of Xc to its score in Xc w.', 'claim': 'Rows are observations; columns are features. Show the matrix shapes here.', 'scene': 'score', 'steps': [{'tex': '\\underbrace{z}_{4\\times1}=\\underbrace{X_c}_{4\\times2}\\underbrace{w}_{2\\times1}', 'why': 'Apply the same weights to each row. This matrix product produces all four scores.'}], 'chapter': 1}, {'id': 16, 'title': 'Keep the ruler length fixed', 'action': 'Double the direction length without changing its angle.', 'claim': 'Without the unit constraint, scores and variance can grow without limit.', 'scene': 'score', 'steps': [{'tex': 'z_i(cw)=c z_i(w),\\quad V(cw)=c^2V(w)', 'why': 'Doubling the arrow doubles every score. The variance then becomes four times as large.'}], 'chapter': 1}, {'id': 17, 'title': 'How spread out are the scores?', 'action': 'Compare scores around zero at two angles.', 'claim': 'Centered input produces scores whose mean is zero.', 'scene': 'variance', 'steps': [{'tex': '\\bar z=w_1\\bar a+w_2\\bar b=0', 'why': 'The centered feature means are zero. Their weighted sum is also zero.'}], 'chapter': 1}, {'id': 18, 'title': 'Signs cancel; squares do not', 'action': 'Switch signed contributions to square areas.', 'claim': 'Squaring measures both directions and supports the distance identity used later.', 'scene': 'variance', 'steps': [{'tex': '\\sum_i z_i=0\\quad\\text{but}\\quad\\sum_i z_i^2\\geq0', 'why': 'Positive and negative scores can cancel. Their squares measure spread on both sides of the center.'}], 'chapter': 1}, {'id': 19, 'title': 'Give spread a number', 'action': 'Add four squared scores and divide by three.', 'claim': 'Use sample variance throughout. An optional note explains n−1; changing it to n does not change the best axis.', 'scene': 'variance', 'steps': [{'tex': 'V(w)=\\frac{z_1^2+z_2^2+z_3^2+z_4^2}{3}', 'why': 'This is sample variance for four centered scores. Its units are square centimeters.'}], 'chapter': 1}, {'id': 20, 'title': 'Search with a variance curve', 'action': 'Rotate the line. Link the angle to a point on the variance curve.', 'claim': 'The highest point gives our numerical target. We still need a general method.', 'scene': 'variance', 'steps': [{'tex': 'V(w)=\\frac{1}{n-1}\\sum_i (w^\\top x_i)^2', 'why': 'The graph evaluates this expression for each direction. Next, we derive a way to find its maximum.'}], 'chapter': 1}, {'id': 21, 'title': 'Open one squared score', 'action': 'Reveal each term in (w1 a + w2 b)².', 'claim': 'Show the two identical cross-products before replacing them with a factor of two.', 'scene': 'expansion', 'steps': [{'tex': 'z_i^2=(w_1a_i+w_2b_i)(w_1a_i+w_2b_i)', 'why': 'Write the square as a product of two identical sums.'}, {'tex': '=w_1^2a_i^2+w_1w_2a_ib_i+w_2w_1b_ia_i+w_2^2b_i^2', 'why': 'Multiply each term in the first bracket by each term in the second.'}, {'tex': '=w_1^2a_i^2+2w_1w_2a_ib_i+w_2^2b_i^2', 'why': 'The middle products are equal. Add them to get the factor two.'}], 'chapter': 2}, {'id': 22, 'title': 'Add the same terms across rows', 'action': 'Select one observation in the sum. Then group matching terms.', 'claim': 'The weights are shared by all observations, so they can leave the sum.', 'scene': 'expansion', 'steps': [{'tex': 'V=\\frac{\\sum_i(w_1^2a_i^2+2w_1w_2a_ib_i+w_2^2b_i^2)}{n-1}', 'why': 'Add the expanded square for every observation.'}, {'tex': '=w_1^2\\frac{\\sum_i a_i^2}{n-1}+2w_1w_2\\frac{\\sum_i a_ib_i}{n-1}+w_2^2\\frac{\\sum_i b_i^2}{n-1}', 'why': 'The weights do not depend on the observation. Put them outside their sums.'}], 'chapter': 2}, {'id': 23, 'title': 'Two familiar sums and one new sum', 'action': 'Link the first and last terms to the two feature variances.', 'claim': 'The middle sum measures how the two centered features vary together.', 'scene': 'expansion', 'steps': [{'tex': 'V=w_1^2s_a^2+2w_1w_2s_{ab}+w_2^2s_b^2', 'why': 'The two square sums are feature variances. Name the product sum covariance, written as s_ab.'}], 'chapter': 2}, {'id': 24, 'title': 'Build covariance from signed products', 'action': 'Select observations in each quadrant. Flip the second feature.', 'claim': 'Same signs give positive products; opposite signs give negative products.', 'scene': 'covariance', 'steps': [{'tex': 's_{ab}=\\frac{2\\cdot1+1\\cdot2+(-1)(-2)+(-2)(-1)}3=\\frac83', 'why': 'Each product is positive in this cloud. Both features tend to lie on the same side of their means.'}], 'chapter': 2}, {'id': 25, 'title': 'Variance alone cannot tell the tilt', 'action': 'Compare two clouds with the same marginal variances and opposite covariance.', 'claim': 'The cross-term distinguishes these clouds.', 'scene': 'covariance', 'steps': [{'tex': 's_a^2=s_b^2=\\frac{10}3,\\qquad s_{ab}=\\pm\\frac83', 'why': 'Changing the sign of the second feature preserves its squares. It reverses each cross-product.'}], 'chapter': 2}, {'id': 26, 'title': 'Store the three quantities in S', 'action': 'Select a covariance matrix entry to reveal its products.', 'claim': 'The diagonal stores variances. Both off-diagonal entries store the same covariance.', 'scene': 'covariance', 'steps': [{'tex': 'S=\\begin{bmatrix}s_a^2&s_{ab}\\\\s_{ab}&s_b^2\\end{bmatrix}=\\frac13\\begin{bmatrix}10&8\\\\8&10\\end{bmatrix}', 'why': 'The matrix stores the three quantities needed to calculate variance in any direction.'}], 'chapter': 2}, {'id': 27, 'title': 'Compute S with one matrix product', 'action': 'Animate a selected row of Xcᵀ meeting a column of Xc.', 'claim': 'Transpose and multiplication are compact ways to do the sums we already used.', 'scene': 'covariance', 'steps': [{'tex': '\\underbrace{X_c^\\top}_{2\\times4}\\underbrace{X_c}_{4\\times2}=\\begin{bmatrix}\\sum a_i^2&\\sum a_ib_i\\\\\\sum b_ia_i&\\sum b_i^2\\end{bmatrix}', 'why': 'A row meets a column. Multiply matching entries and add.'}, {'tex': 'S=\\frac{X_c^\\top X_c}{n-1}', 'why': 'Divide all four sums by the same sample divisor.'}], 'chapter': 2}, {'id': 28, 'title': 'Read wᵀ S w from inside out', 'action': 'Calculate Sw, then the dot product with w.', 'claim': 'The compact formula is exactly the expanded variance expression.', 'scene': 'objective', 'steps': [{'tex': 'Sw=\\begin{bmatrix}s_a^2w_1+s_{ab}w_2\\\\s_{ab}w_1+s_b^2w_2\\end{bmatrix}', 'why': 'First multiply S by w. This gives a two-coordinate vector.'}, {'tex': 'w^\\top Sw=w_1^2s_a^2+2w_1w_2s_{ab}+w_2^2s_b^2', 'why': 'Take its dot product with w. The result is our expanded variance.'}], 'chapter': 2}, {'id': 29, 'title': 'Check both routes with real numbers', 'action': 'Compare direct squared scores with wᵀ S w at any angle.', 'claim': 'The two calculations agree because we derived their identity.', 'scene': 'objective', 'steps': [{'tex': '\\frac{(X_cw)^\\top(X_cw)}{n-1}=w^\\top\\frac{X_c^\\top X_c}{n-1}w=w^\\top Sw', 'why': 'Transposing a product reverses its order. These are three forms of the same calculation.'}], 'chapter': 2}, {'id': 30, 'title': 'State the optimization problem', 'action': 'Show a unit circle of permitted directions and a variance curve.', 'claim': 'Maximize wᵀ S w with wᵀ w = 1.', 'scene': 'objective', 'steps': [{'tex': '\\max_w\\; w^\\top Sw\\qquad\\text{subject to }w^\\top w=1', 'why': 'Choose the direction with the largest score variance. Compare only arrows of unit length.'}], 'chapter': 2}, {'id': 31, 'title': 'What does S do to an arrow?', 'action': 'Move w around the unit circle. Show Sw on a common labeled scale.', 'claim': 'A matrix is also a rule that maps one vector to another.', 'scene': 'eigen', 'steps': [{'tex': 'Sw=\\frac13\\begin{bmatrix}10w_1+8w_2\\\\8w_1+10w_2\\end{bmatrix}', 'why': 'The same covariance matrix can map a direction arrow to a new arrow.'}], 'chapter': 3}, {'id': 32, 'title': 'At an optimum, turning cannot help', 'action': 'Compare a direction with small clockwise and counterclockwise turns.', 'claim': 'The allowed change runs along the circle. At an optimum its first-order gain is zero.', 'scene': 'eigen', 'steps': [{'tex': 't=\\begin{bmatrix}-w_2\\\\w_1\\end{bmatrix},\\qquad \\frac{dV}{d\\theta}=2t^\\top Sw', 'why': 'The vector t points along a small turn of w. At a stationary direction, this slope is zero.'}], 'chapter': 3}, {'id': 33, 'title': 'Find the variance slope', 'action': 'Differentiate the two-coordinate quadratic one term at a time.', 'claim': 'The gradient is (2S11w1+2S12w2, 2S12w1+2S22w2) = 2Sw.', 'scene': 'eigen', 'steps': [{'tex': 'f(w_1,w_2)=S_{11}w_1^2+2S_{12}w_1w_2+S_{22}w_2^2', 'why': 'A partial derivative changes one coordinate while the other stays fixed.'}, {'tex': '\\frac{\\partial f}{\\partial w_1}=2S_{11}w_1+2S_{12}w_2', 'why': 'Use the square rule. The term with only w2 has zero derivative.'}, {'tex': '\\frac{\\partial f}{\\partial w_2}=2S_{12}w_1+2S_{22}w_2', 'why': 'Repeat for w2. Symmetry makes the two cross-term coefficients agree.'}, {'tex': '\\nabla f=2Sw', 'why': 'The gradient collects these two slopes into one vector.'}], 'chapter': 3}, {'id': 34, 'title': 'Find the constraint direction', 'action': 'Differentiate w1²+w2². Show the normal arrow to the circle.', 'claim': 'The gradient 2w points outward; allowed small changes point perpendicular to it.', 'scene': 'eigen', 'steps': [{'tex': 'g(w)=w_1^2+w_2^2-1=0', 'why': 'This equation describes the circle of permitted directions.'}, {'tex': '\\nabla g=\\begin{bmatrix}2w_1\\\\2w_2\\end{bmatrix}=2w', 'why': 'The gradient points outward. A small allowed change is tangent to the circle.'}], 'chapter': 3}, {'id': 35, 'title': 'Match the two normal directions', 'action': 'Align the gradient arrows at a stationary point.', 'claim': '2Sw = 2λw, so Sw = λw. This finds candidates; it does not yet prove a maximum.', 'scene': 'eigen', 'steps': [{'tex': '\\nabla f=\\lambda\\nabla g', 'why': 'At a constrained optimum, the objective gradient has no component along an allowed small change.'}, {'tex': '2Sw=2\\lambda w', 'why': 'Substitute the two gradients that we just calculated.'}, {'tex': 'Sw=\\lambda w', 'why': 'Divide both sides by two. The multiplier becomes the scale factor of this direction.'}], 'chapter': 3}, {'id': 36, 'title': 'Name the equation after it appears', 'action': 'Compare w and Sw at both stationary directions.', 'claim': 'An eigenvector keeps its direction under S. Its eigenvalue is the scale factor.', 'scene': 'eigen', 'steps': [{'tex': 'Sq=\\lambda q', 'why': 'The input arrow q and its image Sq lie on the same line. This defines an eigenvector and its eigenvalue.'}], 'chapter': 3}, {'id': 37, 'title': 'Find the possible scale factors', 'action': 'Subtract λ on the diagonal. Expand the 2×2 determinant.', 'claim': 'A nonzero solution requires S−λI to be singular. Explain determinant only here.', 'scene': 'eigen', 'steps': [{'tex': '(S-\\lambda I)q=0,\\quad q\\neq0', 'why': 'Move the right side to the left. A nonzero solution requires a singular matrix.'}, {'tex': '\\det(S-\\lambda I)=\\left(\\frac{10}3-\\lambda\\right)^2-\\left(\\frac83\\right)^2=0', 'why': 'For a two-by-two matrix, the determinant is the diagonal product minus the other product.'}], 'chapter': 3}, {'id': 38, 'title': 'Solve our two eigenvalues', 'action': 'Factor (10/3−λ)²−(8/3)². Link each root to the curve.', 'claim': 'The roots are 6 and 2/3.', 'scene': 'eigen', 'steps': [{'tex': '\\left(\\frac{10}3-\\lambda-\\frac83\\right)\\left(\\frac{10}3-\\lambda+\\frac83\\right)=0', 'why': 'Factor the difference of two squares.'}, {'tex': '\\left(\\frac23-\\lambda\\right)(6-\\lambda)=0', 'why': 'A product is zero when one factor is zero.'}, {'tex': '\\lambda_1=6,\\qquad\\lambda_2=\\frac23', 'why': 'These are the two possible scale factors. We order them from largest to smallest.'}], 'chapter': 3}, {'id': 39, 'title': 'Find and normalize the directions', 'action': 'Solve w2=w1 and w2=−w1. Set each vector length to one.', 'claim': 'The directions are (1,1)/√2 and (1,−1)/√2.', 'scene': 'eigen', 'steps': [{'tex': 'q=(u,v),\\quad\\lambda=6:\\quad -8u+8v=0\\;\\Rightarrow\\;v=u', 'why': 'Substitute 6 in the first row of the eigenvector equation. Multiply that row by three.'}, {'tex': 'q_1=\\frac{(1,1)}{\\sqrt2},\\qquad q_2=\\frac{(1,-1)}{\\sqrt2}', 'why': 'Repeat for 2/3. Divide each direction by its length to make a unit vector.'}], 'chapter': 3}, {'id': 40, 'title': 'A candidate can be a minimum', 'action': 'Select each eigenvector and compare its variance.', 'claim': 'The eigenvector equation alone does not choose PC1.', 'scene': 'eigen', 'steps': [{'tex': 'V(q)=q^\\top Sq=q^\\top(\\lambda q)=\\lambda', 'why': 'A unit eigenvector has variance equal to its eigenvalue. One candidate is the maximum; the other is the minimum.'}], 'chapter': 3}, {'id': 41, 'title': 'Why are these directions perpendicular?', 'action': 'Expand q1ᵀSq2 in two ways and compare.', 'claim': 'Symmetry gives (λ1−λ2)q1ᵀq2=0. Distinct eigenvalues imply perpendicular eigenvectors.', 'scene': 'eigen', 'steps': [{'tex': 'q_1^\\top Sq_2=\\lambda_2 q_1^\\top q_2', 'why': 'Apply S to q2 first.'}, {'tex': 'q_1^\\top Sq_2=(Sq_1)^\\top q_2=\\lambda_1 q_1^\\top q_2', 'why': 'Symmetry lets S act on the other vector.'}, {'tex': '(\\lambda_1-\\lambda_2)q_1^\\top q_2=0', 'why': 'If the eigenvalues differ, the dot product must be zero. The two directions are perpendicular.'}], 'chapter': 3}, {'id': 42, 'title': 'Build any unit direction from them', 'action': 'Rotate w and show coefficients a and b on the two eigenvectors.', 'claim': 'w=aq1+bq2 and a²+b²=1. State the symmetric-matrix basis theorem for higher dimensions.', 'scene': 'maximum', 'steps': [{'tex': 'w=aq_1+bq_2,\\qquad a^2+b^2=1', 'why': 'The two unit eigenvectors form perpendicular axes. Every unit direction has coordinates a and b on these axes.'}], 'chapter': 3}, {'id': 43, 'title': 'Expand variance in the new basis', 'action': 'Open four terms. Cancel both cross-terms with orthogonality.', 'claim': 'The result is λ1a²+λ2b².', 'scene': 'maximum', 'steps': [{'tex': 'w^\\top Sw=(aq_1+bq_2)^\\top S(aq_1+bq_2)', 'why': 'Substitute the coordinates of w in the eigenvector basis.'}, {'tex': '=a^2\\lambda_1+ab\\lambda_2q_1^\\top q_2+ab\\lambda_1q_2^\\top q_1+b^2\\lambda_2', 'why': 'Expand the four products. Replace Sq1 and Sq2 with their eigenvalue forms.'}, {'tex': '=a^2\\lambda_1+b^2\\lambda_2', 'why': 'Both cross-terms contain a zero dot product. Each unit vector has squared length one.'}], 'chapter': 3}, {'id': 44, 'title': 'Prove the largest value wins', 'action': 'Move the squared-weight allocation between λ1 and λ2.', 'claim': 'A weighted average cannot exceed its largest entry. Equality at q1 proves global optimality.', 'scene': 'maximum', 'steps': [{'tex': 'V=a^2\\lambda_1+b^2\\lambda_2\\leq a^2\\lambda_1+b^2\\lambda_1', 'why': 'Because λ2 is no larger than λ1, replacing λ2 cannot decrease this expression.'}, {'tex': 'V\\leq(a^2+b^2)\\lambda_1=\\lambda_1', 'why': 'The nonnegative squared weights add to one.'}, {'tex': 'w=q_1\\quad\\Rightarrow\\quad V=\\lambda_1', 'why': 'This direction reaches the bound. It is a global maximum, not just a stationary point.'}], 'chapter': 3}, {'id': 45, 'title': 'What if the eigenvalues tie?', 'action': 'Change to an isotropic cloud. Rotate freely.', 'claim': 'All directions in a tied eigenspace give the same variance. A unique PC1 is not guaranteed.', 'scene': 'maximum', 'steps': [{'tex': '\\lambda_1=\\lambda_2=\\lambda\\quad\\Rightarrow\\quad V=\\lambda(a^2+b^2)=\\lambda', 'why': 'Equal eigenvalues give the same variance for every direction in their shared space.'}], 'chapter': 3}, {'id': 46, 'title': 'Find the next component', 'action': 'Restrict the next direction to the perpendicular space.', 'claim': 'Maximize remaining variance there. In two dimensions the remaining axis is fixed up to sign.', 'scene': 'coordinates', 'steps': [{'tex': '\\max_{\\|w\\|=1,\\;w^\\top q_1=0}w^\\top Sw', 'why': 'The next component must be perpendicular to PC1. In higher dimensions, maximize variance within that remaining space.'}], 'chapter': 4}, {'id': 47, 'title': 'Read the PCA coordinates', 'action': 'Rotate both axes, then relabel the plot as PC1 and PC2.', 'claim': 'Loadings describe axes. Scores describe observations.', 'scene': 'coordinates', 'steps': [{'tex': 'Z=X_cQ,\\qquad Q=[q_1\\ q_2]', 'why': 'Each column of Q describes an axis. Each row of Z contains the new coordinates of one observation.'}], 'chapter': 4}, {'id': 48, 'title': 'Check the new covariance', 'action': 'Select an entry of QᵀSQ. See the off-diagonal product sum vanish.', 'claim': 'The score columns are uncorrelated. This does not generally mean independent.', 'scene': 'coordinates', 'steps': [{'tex': '\\operatorname{Cov}(Z)=\\frac{Z^\\top Z}{n-1}=Q^\\top SQ', 'why': 'Substitute Z=XcQ and group the covariance matrix.'}, {'tex': 'Q^\\top SQ=\\begin{bmatrix}\\lambda_1&0\\\\0&\\lambda_2\\end{bmatrix}', 'why': 'Orthonormal eigenvectors make the off-diagonal entries zero.'}], 'chapter': 4}, {'id': 49, 'title': 'Explain the 90 percent', 'action': 'Connect eigenvalue bars to the sum of squared centered distances.', 'claim': '6/(6+2/3)=90%. This is a fraction of variance, not prediction accuracy.', 'scene': 'coordinates', 'steps': [{'tex': '\\mathrm{fraction}_1=\\frac{\\lambda_1}{\\lambda_1+\\lambda_2}=\\frac{6}{6+2/3}=0.90', 'why': 'The denominator is total variance. The ratio measures retained squared spread.'}], 'chapter': 4}, {'id': 50, 'title': 'Rebuild an observation from its score', 'action': 'Select A. Multiply its score by q1, then add the mean.', 'claim': 'The reconstructed point lies on the retained line.', 'scene': 'reconstruction', 'steps': [{'tex': '\\widehat r_A=\\mu+z_Aq_1', 'why': 'Multiply the retained score by its axis. Add the stored mean.'}, {'tex': '=(6,6)+\\frac3{\\sqrt2}\\frac{(1,1)}{\\sqrt2}=(7.5,7.5)', 'why': 'A originally measured (8,7). Its one-score reconstruction has an error in both features.'}], 'chapter': 4}, {'id': 51, 'title': 'Draw the missing part', 'action': 'Show the original vector, projection, and residual as a right triangle.', 'claim': 'Orthogonality gives original squared length = kept squared length + lost squared length.', 'scene': 'reconstruction', 'steps': [{'tex': 'x_i=z_iw+e_i,\\quad w^\\top e_i=0', 'why': 'The residual e is the difference between the original point and its projection.'}, {'tex': '\\|x_i\\|^2=z_i^2+\\|e_i\\|^2', 'why': 'The kept vector and residual are perpendicular. Apply the right-triangle identity.'}], 'chapter': 4}, {'id': 52, 'title': 'Prove the second objective', 'action': 'Add the triangle identity across all observations.', 'claim': 'Total squared length is fixed, so maximizing kept variance minimizes squared reconstruction error.', 'scene': 'reconstruction', 'steps': [{'tex': '\\sum_i\\|e_i\\|^2=\\sum_i\\|x_i\\|^2-\\sum_i z_i^2', 'why': 'Add the identity for every observation and move the kept term to the right.'}, {'tex': '\\frac{\\sum_i\\|e_i\\|^2}{n-1}=\\operatorname{tr}(S)-w^\\top Sw', 'why': 'Trace is the sum of the feature variances. The first term does not depend on the direction.'}, {'tex': '\\arg\\min_w\\sum_i\\|e_i\\|^2=\\arg\\max_w w^\\top Sw', 'why': 'The same direction solves both problems. The errors are perpendicular distances, not vertical regression errors.'}], 'chapter': 4}, {'id': 53, 'title': 'Recover both coordinates', 'action': 'Switch between k=0, k=1, and k=2.', 'claim': 'Two orthonormal coordinates recover the original centered vector.', 'scene': 'reconstruction', 'steps': [{'tex': 'x_i=z_{i1}q_1+z_{i2}q_2', 'why': 'Keeping both perpendicular coordinates recovers the original centered vector.'}], 'chapter': 4}, {'id': 54, 'title': 'Choose how much to keep', 'action': 'Set a retained-variance target and select k.', 'claim': 'The task determines an acceptable error. A percentage alone does not prove usefulness.', 'scene': 'reconstruction', 'steps': [{'tex': '\\mathrm{retained}=\\frac{\\sum_{j=1}^k\\lambda_j}{\\sum_{j=1}^p\\lambda_j},\\qquad\\mathrm{loss}=\\sum_{j=k+1}^p\\lambda_j', 'why': 'The loss uses the sample divisor n−1. Multiply it by n−1 to get the total squared error.'}], 'chapter': 4}, {'id': 55, 'title': 'Extend from two features to p', 'action': 'Keep the top k eigenvalues in a larger spectrum.', 'claim': 'For orthonormal W, retained variance is tr(WᵀSW). The top k eigenvectors maximize it; discarded eigenvalues give the loss.', 'scene': 'spectrum', 'steps': [{'tex': 'V_k=\\operatorname{tr}(W^\\top SW)=\\sum_{j=1}^p\\lambda_j\\alpha_j', 'why': 'W contains k perpendicular unit directions. Define αj as the squared length of the projection of qj into their space.'}, {'tex': '0\\leq\\alpha_j\\leq1,\\qquad\\sum_j\\alpha_j=k', 'why': 'A projection cannot increase a unit vector length. The sum equals the dimension of the retained space.'}, {'tex': 'V_k\\leq\\lambda_1+\\cdots+\\lambda_k', 'why': 'Allocate the weight to the largest eigenvalues first. Choosing their eigenvectors reaches this bound.'}], 'chapter': 4}, {'id': 56, 'title': 'Connect the result to SVD', 'action': 'Substitute Xc=UΣVᵀ into S=XcᵀXc/(n−1).', 'claim': 'The columns of V are PCA directions. Eigenvalues equal squared singular values divided by n−1.', 'scene': 'spectrum', 'steps': [{'tex': 'X_c=U\\Sigma V^\\top', 'why': 'Singular value decomposition factors the centered table. U and V have orthonormal columns in the compact form.'}, {'tex': 'S=\\frac{V\\Sigma^\\top U^\\top U\\Sigma V^\\top}{n-1}=V\\frac{\\Sigma^2}{n-1}V^\\top', 'why': 'Use UᵀU=I. The diagonal entries are the squared singular values divided by n−1.'}, {'tex': 'q_j=v_j,\\qquad\\lambda_j=\\frac{\\sigma_j^2}{n-1}', 'why': 'SVD gives the same PCA directions without explicitly forming the covariance matrix.'}], 'chapter': 4}, {'id': 57, 'title': 'Use the axes on a new observation', 'action': 'Enter a new observation and apply the training mean and axes.', 'claim': 'Fit preprocessing and PCA on training data. Reuse those values for later observations.', 'scene': 'newpoint', 'steps': [{'tex': 'z_{\\mathrm{new}}=Q_k^\\top(r_{\\mathrm{new}}-\\mu_{\\mathrm{train}})', 'why': 'Keep the training mean and learned directions fixed. New observations do not refit this model.'}], 'chapter': 5}, {'id': 58, 'title': 'Decide what units mean', 'action': 'Change one feature scale, then compare standardization.', 'claim': 'Standardization changes the question. It gives each nonconstant feature unit variance.', 'scene': 'units', 'steps': [{'tex': '\\widetilde r_{ij}=\\frac{r_{ij}-\\mu_j}{s_j}', 'why': 'Divide each centered feature by its sample standard deviation. Nonconstant features then have variance one.'}], 'chapter': 5}, {'id': 59, 'title': 'Large variance is not always useful', 'action': 'Reveal a distant observation and then category labels.', 'claim': 'Outliers can dominate squared spread. A useful label can lie in a low-variance direction.', 'scene': 'outliers', 'steps': [], 'chapter': 5}, {'id': 60, 'title': 'A line cannot follow every shape', 'action': 'Compare a ring with the elongated cloud.', 'claim': 'PCA is linear. Two components may be necessary even if a curve has one intrinsic parameter.', 'scene': 'ring', 'steps': [], 'chapter': 5}, {'id': 61, 'title': 'Change the real notebook data', 'action': 'Use native marimo controls to change an observation.', 'claim': 'Python recomputes mean, covariance, directions, scores, and reconstruction.', 'scene': 'notebook', 'steps': [], 'chapter': 5}, {'id': 62, 'title': 'Solve a fresh geometric problem', 'action': 'Choose a direction for a rotated, unseen cloud before seeing its optimum.', 'claim': 'Require a prediction and a reason; then compare with the computed result.', 'scene': 'challenge', 'steps': [], 'chapter': 5}, {'id': 63, 'title': 'Produce the calculation yourself', 'action': 'Compute a covariance entry, a score, and a reconstruction for new values.', 'claim': 'Record numeric correctness separately from the learner’s written explanation.', 'scene': 'exam', 'steps': [], 'chapter': 5}, {'id': 64, 'title': 'Teach PCA back in your own words', 'action': 'Explain purpose → objective → covariance → eigenvectors → loss.', 'claim': 'Use new examples and name one limit. Reopen the exact relevant scene after a miss.', 'scene': 'teachback', 'steps': [], 'chapter': 5}], 'refreshers': {'center': ['Mean and centering', 'The mean is the sum divided by the number of observations. Calculate one mean per feature. Subtract each feature mean from its values. Centered values describe differences from the mean.'], 'score': ['Vectors and dot products', 'A vector stores coordinates. A unit vector has length one. Its dot product with a point gives the signed projection score. Multiply matching coordinates, then add.'], 'variance': ['Variance', 'Variance measures squared spread around a mean. Here the score mean is zero. Add the squared scores and divide by n−1. Using n instead changes the scale but not the best direction.'], 'expansion': ['Expand a square', 'Multiply each term in the first bracket by each term in the second bracket. In (A+B)², the middle terms are AB and BA. They give 2AB.'], 'covariance': ['Transpose and matrix multiplication', 'Transpose swaps rows and columns. A matrix product matches one row with one column. Multiply matching entries and add. In XcᵀXc, each entry compares two feature columns.'], 'objective': ['Read the dimensions', 'Xc has n rows and p columns. w has p entries. Xc w has n scores. S has p rows and p columns. wᵀSw is one number.'], 'eigen': ['Gradients, constraints, and eigenvectors', 'A derivative measures local change. A gradient collects one derivative per coordinate. On the unit circle, allowed small changes follow the tangent. At a constrained optimum, the gradient has no tangent component. Sw=λw says that S preserves the line of w.'], 'maximum': ['The basis theorem and the bound', 'A real symmetric matrix has an orthonormal basis of eigenvectors. We use this theorem for higher dimensions. The two-dimensional example can be checked directly. Squared coordinates in this basis are nonnegative and add to one. Their weighted eigenvalue average cannot exceed the largest eigenvalue.'], 'coordinates': ['Loadings and scores', 'Loadings are the feature weights in an axis. Scores are the coordinates of observations on that axis. Sign reversal changes both signs and preserves the same projection. Zero covariance does not generally imply independence.'], 'reconstruction': ['Length, projection, and trace', 'The squared length of (a,b) is a²+b². A unit-axis projection is zw. Its residual is perpendicular to the axis. Their squared lengths add. Trace means the sum of the diagonal entries.'], 'spectrum': ['Several retained directions', 'The columns of W are perpendicular unit vectors. WᵀW=I. Projecting onto these k directions gives k scores. Keeping all directions preserves the data. Keeping fewer can lose detail.'], 'geometry': ['How to read this picture', 'Each letter is one observation. Teal marks the retained axis. The score line shows one number for each observation. Orange marks a lost part. The axis we keep is perpendicular to the direction of a shadow.']}, 'notation': [['rᵢ', 'An original observation, before centering.'], ['μ', 'The mean of each original feature.'], ['xᵢ', 'One centered observation: rᵢ−μ.'], ['Xc', 'A table of centered observations, one per row.'], ['w', 'A candidate direction of unit length.'], ['zᵢ', 'The score of observation i on w.'], ['S', 'The sample covariance matrix.'], ['qⱼ', 'A learned unit eigenvector, or PCA direction.'], ['λⱼ', 'Variance along qⱼ.'], ['k', 'The number of retained components.']]}
    None

    return (pca_course_v2,)


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


@app.cell(hide_code=True)
def notebook_results(mo, sandbox_lab):
    _r=sandbox_lab
    mo.vstack([
        mo.md("## The current model"),
        mo.ui.table([{"Observation":chr(65+i),"x (cm)":p[0],"y (cm)":p[1]} for i,p in enumerate(_r["raw"])],selection=None),
        mo.md(f"Mean: **{_r['mean']}**. PC1 angle: **{_r['angle']:.2f} degrees**. Retained variance: **{100*_r['ratio']:.2f}%**."),
        mo.md("### Covariance matrix"),
        mo.ui.table([{"Row":i+1,"Column 1":p[0],"Column 2":p[1]} for i,p in enumerate(_r["cov"])],selection=None),
        mo.md("### Eigenvalues and unit directions"),
        mo.ui.table([{"Component":i+1,"Eigenvalue":v,"x weight":_r["axes"][i][0],"y weight":_r["axes"][i][1]} for i,v in enumerate(_r["values"])],selection=None)
    ])
    return


@app.cell(hide_code=True)
def notebook_course(mo, pca_course_v2):
    _sections={}
    for _chapter in pca_course_v2['chapters']:
        _parts=[]
        for _slide in pca_course_v2['slides'][_chapter['start']:_chapter['end']]:
            _body='### '+str(_slide['id'])+'. '+_slide['title']+'\n\n'+_slide['claim']+'\n\n'
            for _step in _slide['steps']:
                _body+='$$'+_step['tex']+'$$\n\n'+_step['why']+'\n\n'
            _parts.append(mo.md(_body))
        _sections[_chapter['question']]=mo.vstack(_parts)
    mo.accordion(_sections)
    return


if __name__ == "__main__":
    app.run()
