from pathlib import Path
import copy, hashlib, json

path = Path('outputs/pca-studio/course-v2.json')
before_bytes = path.read_bytes()
before = json.loads(before_bytes)
course = copy.deepcopy(before)
Path('work/course-before-learner-copy.json').write_bytes(before_bytes)

# title, action, claim. Each action addresses the learner and an observable operation.
edits = {
1: ('Can two coordinates become one?', 'Select a marker. Turn the line and compare its original position with its recovered position.', 'PCA chooses new axes through the center of the data. With fewer coordinates, we can recover approximate positions and measure the errors.'),
2: ('A score is a position on a ruler', 'Select A, then B. Follow each marker to its position on the score ruler.', 'One score locates a point along the chosen axis. The shared axis and center let us turn that score into a recovered position.'),
3: ('Which line recovers the points better?', 'Compare 45° and 135°. Which direction gives smaller gaps between the original and recovered points?', 'The choice of line changes the recovery error. We will choose the line with the smallest total squared error.'),
4: ('Put each point at its closest place on the line', 'Move the selected point to the line. Notice the right angle at the point where it arrives.', 'A projection is the closest point on the line. The gap from the original point is perpendicular to the line.'),
5: ('What did one score lose?', 'Move the point across the axis. Check that its stored score stays fixed.', 'Several original positions can have the same score. The missing coordinate tells them apart.'),
6: ('Turning both axes loses nothing', 'Keep both coordinates, then remove one. Compare the recovered position in each case.', 'Two rotated coordinates still locate the point exactly. Removing one coordinate can create a recovery error.'),
7: ('Choose an axis by a clear rule', 'Turn the line. Compare the squared spread kept with the squared recovery error.', 'With the same units, the axis that keeps the most squared spread also gives the least total squared recovery error.'),
8: ('From a picture to a computation', 'Subtract the center. Search for a direction. Store the scores. Recover a point from its score.', 'We first move the mean to zero. Then we choose an axis, compute each score, and use the axis to recover positions.'),
9: (None, 'Move the whole cloud toward the origin. Watch its center and the gaps between points.', 'PCA measures how the observations differ from their shared center, the mean.'),
10: (None, 'Add the four x values and divide by four. Repeat for y.', 'The mean gives one shared center for the four observations.'),
11: (None, 'Move the mean to zero. Follow the selected point as its coordinates change.', 'Subtract each feature mean from that feature. The resulting coordinates measure differences from the shared center.'),
12: (None, 'Follow A and B as the cloud moves. Does the gap between them change?', 'Subtracting the same center from every point preserves all pairwise distances.'),
13: (None, 'Turn the unit arrow. Compare its horizontal and vertical coordinates.', 'The vector w specifies the axis direction. Its length is one, so every direction uses the same score scale.'),
14: (None, 'Select a point. Multiply its centered coordinates by the two direction weights, then add.', 'The dot product gives a signed coordinate along a unit axis.'),
15: (None, 'Select each row of Xc. Apply the same two weights to calculate its score.', 'The 4×2 data table multiplies a 2×1 direction vector to produce four scores. Each row is one observation.'),
16: (None, 'Double the direction length. Compare each score and the resulting variance.', 'A longer direction vector enlarges every score without improving the axis. Unit length prevents this arbitrary increase.'),
17: (None, 'Try two angles. Compare the positive and negative scores around zero.', 'Centering the observations also centers their scores: the mean score is zero.'),
18: (None, 'Compare each signed score with its square. Why do the signed scores add to zero?', 'Positive and negative scores can cancel. Their squares measure spread on both sides of the center.'),
19: (None, 'Add the four squared scores and divide by three.', 'Sample variance divides the squared score sum by n−1. Here n=4, so the divisor is three.'),
20: (None, 'Turn the line. Follow the matching point on the variance curve and find its highest position.', 'The curve shows which direction gives the most score variance. We need a method that also works with many features.'),
21: (None, 'Follow each product in (w1 a + w2 b)². Find the two equal cross-products.', 'Multiplying the two brackets gives four products. The two equal cross-products combine into one term with a factor of two.'),
22: (None, 'Expand each observation’s squared score. Group its terms with matching terms from the other observations.', 'Every observation uses the same direction weights. We can place these fixed weights outside the sums.'),
23: (None, 'Compare the three sums. Which use squares, and which uses products of different features?', 'The square sums give feature variances. The mixed product sum gives covariance, which measures how the centered features vary together.'),
24: (None, 'Compare Together, Opposite, and Cancellation. Follow the signs in the product table.', 'Same signs give positive products. Opposite signs give negative products. Covariance adds these contributions.'),
25: (None, 'Switch between the positive and negative tilts. Compare the variances and the covariance.', 'These clouds have the same feature variances. Their opposite covariance signs describe opposite tilts.'),
26: (None, 'Select an entry of S. Calculate its four products, their sum, and the division by three.', 'The diagonal stores the two variances. The two off-diagonal entries store the same covariance.'),
27: (None, 'Select an entry of S. Match a row of Xcᵀ with a column of Xc, then add their paired products.', 'Transposing turns feature columns into rows. Each row–column product calculates one sum needed by the covariance matrix.'),
28: (None, 'Compute Sw first. Then multiply its coordinates by the matching entries of w and add.', 'The compact expression wᵀSw is exactly the expanded score variance.'),
29: (None, 'Change the angle. Compare variance calculated from the scores with variance calculated from S.', 'Both routes give the same number at every angle because they are two forms of the same expression.'),
30: (None, 'Try several unit directions. Compare their variance and identify the largest value.', 'We want the largest value of wᵀSw. The constraint wᵀw=1 keeps every direction vector at unit length.'),
31: (None, 'Turn w. Compare its direction and length with the arrow Sw.', 'Multiplying by S maps the input vector w to the output vector Sw.'),
32: ('Find where the turning slope is zero', 'Compare a direction with a small turn to either side. Check the variance curve at both candidate axes.', 'At a stationary direction, the variance curve has zero slope. Both a maximum and a minimum can have this slope.'),
33: (None, 'Differentiate with respect to w1 while holding w2 fixed. Then exchange their roles.', 'Changing each coordinate gives one slope. Together, these slopes form the gradient 2Sw.'),
34: (None, 'Find the gradient of w1²+w2². Compare its outward direction with the circle’s tangent.', 'The vector 2w points outward from the unit circle. A tangent to the circle is perpendicular to w.'),
35: (None, 'Compare both stationary directions. Check why each has zero change along the tangent.', 'Zero slope along the tangent gives 2Sw=2λw, hence Sw=λw. This identifies candidates; we still need to find the maximum.'),
36: ('This equation defines an eigenvector', 'Compare w and Sw at 45° and 135°. How much does S scale each arrow?', 'An eigenvector is a nonzero vector that S maps to a multiple of itself. Its eigenvalue is that multiplier.'),
37: (None, 'Subtract λ from each diagonal entry. Calculate the determinant of the resulting 2×2 matrix.', 'The matrix S−λI must send a nonzero vector to zero. Its determinant must therefore be zero.'),
38: (None, 'Factor the difference of squares. Check each root in the original determinant equation.', 'The two possible eigenvalues are 6 and 2/3.'),
39: (None, 'Solve for the relation between the two coordinates. Divide each resulting vector by its length.', 'The two unit directions are (1,1)/√2 and (1,−1)/√2.'),
40: (None, 'Select each eigenvector. Compare its variance with the nearby directions on the curve.', 'The eigenvector equation finds both candidates. Their eigenvalues tell us that their variances differ.'),
41: (None, 'Calculate q1ᵀSq2 in two ways. What must its dot product be when the eigenvalues differ?', 'Symmetry gives (λ1−λ2)q1ᵀq2=0. Different eigenvalues force the dot product to be zero, so these axes are perpendicular.'),
42: (None, 'Turn w. Follow its coordinates a and b along the two eigenvector axes.', 'These two perpendicular unit vectors span the plane. Every unit direction has coordinates a and b with a²+b²=1.'),
43: (None, 'Expand the four products. Use the perpendicular axes to remove the two cross-terms.', 'The variance becomes λ1a²+λ2b²: each eigenvalue is weighted by a squared coordinate.'),
44: (None, 'Change the squared weights. Can their weighted eigenvalue average exceed λ1?', 'The squared weights are nonnegative and add to one. Their average cannot exceed λ1, and q1 reaches that bound.'),
45: (None, 'Turn the axis through the round cloud. Compare variance in different directions.', 'Tied eigenvalues give the same variance in every direction of their shared space. The best axis can therefore be non-unique.'),
46: (None, 'Keep PC1 fixed. Find a unit direction perpendicular to it.', 'PC2 maximizes variance among unit directions perpendicular to PC1. In two dimensions, only one perpendicular axis remains.'),
47: (None, 'Switch between the original axes and the PCA axes. Follow one observation’s two coordinates.', 'Loadings describe the axes. Scores describe where each observation lies along those axes.'),
48: (None, 'Compare the covariance before and after changing to PCA coordinates. Check the off-diagonal entries.', 'The score columns have zero covariance. This does not generally make them independent.'),
49: ('What does 90 percent measure?', 'Divide the PC1 variance by total variance. Explain what the resulting percentage measures.', 'PC1 keeps 6/(6+2/3)=90% of the total squared spread. This percentage does not measure prediction accuracy.'),
50: (None, 'Select an observation. Multiply its score by q1, then add the mean.', 'The recovered point lies on the line through the mean in direction q1.'),
51: (None, 'Select a point. Compare its original vector, projection, and error vector as a right triangle.', 'The original squared length equals the kept squared length plus the squared error. The right angle makes this identity possible.'),
52: (None, 'Add the right-triangle identity for all observations. Find the term that stays fixed as the axis turns.', 'Total squared distance from the center stays fixed. Maximizing score variance therefore minimizes total squared recovery error.'),
53: (None, 'Keep zero, one, and then two components. Compare the recovered positions.', 'Both perpendicular coordinates together recover the original centered vector exactly.'),
54: (None, 'Set a retained-variance target. Compare the component count and the remaining recovery error.', 'Choose an acceptable error for the task. A high retained-variance percentage alone does not establish usefulness.'),
55: (None, 'Choose k in the larger eigenvalue spectrum. Compare the sum kept with the sum discarded.', 'Choose k perpendicular unit axes. The top k eigenvectors retain the most total variance; discarded eigenvalues give the remaining loss.'),
56: (None, 'Substitute Xc=UΣVᵀ into the covariance formula. Follow the factors that cancel.', 'The columns of V give PCA directions. Each eigenvalue is a squared singular value divided by n−1.'),
57: (None, 'Enter a new observation. Apply the existing mean and axes without changing them.', 'Fit preprocessing and PCA on the training data. Reuse the same values to transform later observations.'),
58: (None, 'Rescale the second feature. Turn standardization on and compare the resulting axis.', 'Standardization gives each nonconstant feature unit variance. It changes the relative weight of the features in the PCA objective.'),
59: (None, 'Compare the original cloud, a distant observation, and the labeled example. Is the largest spread useful each time?', 'A distant observation can dominate squared spread. A direction with little variance can still separate useful categories.'),
60: (None, 'Turn a line through the ring. Check the gaps between the ring and the recovered points.', 'One straight axis cannot preserve a circle’s shape. A curve may need two PCA coordinates even when one parameter describes it.'),
61: (None, 'Move observation D. Compare the new center, covariance, and PC1 with their earlier values.', 'Changing a measurement changes the data that PCA describes. The notebook recalculates the center, covariance, axes, scores, and recovery errors.'),
62: (None, 'Choose an axis for the new cloud. Write your reason before checking the computed optimum.', 'The same PCA rule applies to a new cloud. Its best axis can differ from the one in our worked example.'),
63: (None, 'Calculate the requested covariance, score, and recovered position. Explain why each operation is needed.', 'Use the same three operations on new values: covariance, projection, and reconstruction.'),
64: (None, 'Explain why covariance leads to eigenvectors and small recovery errors. Use a new example and name one limit.', 'PCA’s axes keep the most squared spread. Their usefulness still depends on the task and the chosen units.'),
}
for slide in course['slides']:
    title, action, claim = edits[slide['id']]
    if title is not None:
        slide['title'] = title
    slide['action'], slide['claim'] = action, claim

why = {
10: ['Add the four values in each feature column. Divide each sum by four to get that feature’s mean.'],
11: ['Subtract the corresponding feature mean. The centered coordinates tell us how far the selected observation is from the shared center.'],
12: ['Both observations lose the same mean. Those two copies cancel when we subtract one observation from the other.'],
13: ['The angle sets the direction. Unit length gives every axis the same score scale.'],
14: ['Multiply matching coordinates, then add. A negative result locates the projection on the opposite side of the center.'],
15: ['Each row contains one observation’s two centered coordinates. Multiplying that row by w gives its score.'],
16: ['Multiplying w by c multiplies each score by c. Squaring the scores therefore multiplies their variance by c².'],
17: ['Each centered feature has mean zero. Any fixed weighted sum of these features also has mean zero.'],
18: ['The positive and negative scores sum to zero. Their nonnegative squares measure distance from zero without cancellation.'],
19: ['Four centered scores give four squared distances. Their sum divided by n−1=3 is the sample variance, measured in square centimeters.'],
20: ['Each position on the curve is the score variance at one angle. Its highest value is the target of our search.'],
21: ['A square multiplies an expression by itself. Here each copy contains two terms.', 'Each of the two terms multiplies both terms in the other bracket. This produces four products.', 'The middle products contain the same four factors. Adding them gives twice either product.'],
22: ['Variance adds the squared score of every observation, then divides by n−1.', 'The direction weights stay fixed across observations. Factor them out, leaving three sums that depend only on the data.'],
23: ['Each sum is divided by n−1. The square sums give variances; the mixed product sum gives covariance.'],
24: ['Multiply the selected centered feature values for each observation. Add the four products, then divide by n−1=3.'],
25: ['Reversing the second feature leaves its squared values unchanged. Every cross-product changes sign, so the covariance changes sign.'],
26: ['These entries store both feature variances and their covariance. Together, they determine score variance at every angle.'],
27: ['Transposing makes each feature column a row. Its dot product with a feature column adds four paired products.', 'Divide each sum by n−1. The diagonal gives variances; the other two entries give covariance.'],
28: ['Each row of S takes a dot product with w. The two results form the vector Sw.', 'Multiply the two entries of Sw by the matching weights and add. The two equal cross-products combine.'],
29: ['Transposing Xc w gives wᵀXcᵀ. Grouping XcᵀXc/(n−1) then replaces it with S.'],
30: ['The objective is score variance. The constraint compares only unit vectors, so changing vector length cannot inflate the result.'],
31: ['Each row of S combines the two input coordinates. The two resulting coordinates locate the tip of Sw.'],
32: ['The unit tangent t points along a small increase in angle. Its dot product with the gradient gives the turning slope.'],
33: ['A partial derivative measures the local change in one coordinate while holding the other fixed.', 'Differentiating w1² gives 2w1. The mixed term gives 2S12w2; the term containing only w2 stays constant.', 'Exchange the roles of w1 and w2. The mixed term now contributes 2S12w1.', 'The gradient contains both partial derivatives. Their shared matrix form is 2Sw.'],
34: ['The equation restricts w to length one, so its tip lies on the unit circle.', 'The gradient 2w points outward. The tangent gives the allowed change to first order and is perpendicular to this gradient.'],
35: ['At a stationary point, the objective gradient has zero tangent component. It must lie along the constraint’s outward direction.', 'The objective gradient is 2Sw. The constraint gradient is 2w, so proportional gradients give this equation.', 'Cancel the common factor two. S maps w to a scalar multiple of w.'],
36: ['The vector q must be nonzero. S multiplies it by λ without sending it off its axis; λ may also be zero.'],
37: ['Subtract λq from both sides. The matrix S−λI must collapse a nonzero direction to zero, so it is singular.', 'A 2×2 determinant is the main diagonal product minus the other diagonal product. A singular matrix has determinant zero.'],
38: ['Use A²−B²=(A−B)(A+B), with A=10/3−λ and B=8/3.', 'The simplified factors must have a zero product. Set each factor to zero in turn.', 'These two roots are the eigenvalues. Number them from largest to smallest.'],
39: ['Set λ=6 in the first row, then multiply by three. The resulting equation requires the two coordinates to be equal.', 'For λ=2/3, the first row requires v=−u. Each displayed direction has length √2 before division, so dividing makes its length one.'],
40: ['For a unit eigenvector, Sq=λq and qᵀq=1. Substitution makes its score variance equal to λ.'],
41: ['Since q2 is an eigenvector, replace Sq2 with λ2q2.', 'Symmetry means Sᵀ=S, so q1ᵀS=(Sq1)ᵀ. Now replace Sq1 with λ1q1.', 'The same expression has two values that must agree. Distinct eigenvalues force q1ᵀq2=0, which means perpendicular directions.'],
42: ['The two perpendicular unit axes give coordinates a and b for w. Since w has length one, Pythagoras gives a²+b²=1.'],
43: ['Replace each copy of w with its two components along the eigenvector axes.', 'Multiply all four pairs. Use Sq1=λ1q1 and Sq2=λ2q2 in each term.', 'Perpendicular axes have dot product zero, so both mixed terms vanish. Unit lengths leave a²λ1+b²λ2.'],
44: ['Replacing λ2 with the larger λ1 cannot reduce the sum because b² is nonnegative.', 'The squared weights add to one. Therefore the variance cannot exceed λ1 for any unit direction.', 'Choosing w=q1 reaches λ1. Since no unit direction can exceed it, this is a global maximum.'],
45: ['Equal eigenvalues make the result independent of the squared weights. Every unit direction in this shared space has variance λ.'],
46: ['The next axis must have unit length and be perpendicular to q1. It maximizes variance among the directions that meet both conditions.'],
47: ['Each column of Q is a unit PCA direction. Multiplying each data row by Q gives that observation’s new coordinates.'],
48: ['Substitute Z=XcQ and transpose the product. The middle factor XcᵀXc/(n−1) is S.', 'Applying S scales each eigenvector by its eigenvalue. The perpendicular unit eigenvectors then make the off-diagonal entries zero.'],
49: ['The eigenvalues add to total variance. Since both variances use the same divisor, their ratio also measures the fraction of squared spread kept.'],
50: ['The score gives distance along q1 from the center. Multiplying by q1 and adding the mean returns to the original coordinate system.', 'Compare the recovered coordinates with the original coordinates. Their difference is the reconstruction error.'],
51: ['The residual e fills the gap from the projection to the original centered point. Its dot product with w is zero.', 'The projection and residual form a right angle. Pythagoras adds their squared lengths; the projection’s squared length is z² because w is unit length.'],
52: ['Add the right-triangle identity for all observations. Move the total kept squared length to the other side.', 'The total squared distance divided by n−1 is tr(S), the sum of feature variances. It stays fixed while w changes.', 'With unit directions and fixed data, reducing the error means increasing score variance. The measured gaps are perpendicular to the chosen line.'],
53: ['The two perpendicular components add to the original centered vector. Add the mean to recover the original observation.'],
54: ['The displayed loss divides total squared error by n−1. It equals the sum of discarded eigenvalues in the same units.'],
55: ['W contains k perpendicular unit directions. Each αj is the squared length of eigenvector qj projected onto their shared space.', 'Projection cannot lengthen a unit vector, so each αj lies from zero to one. Their sum is k, the number of retained axes.', 'With total weight k and each weight at most one, the largest sum uses the k largest eigenvalues. Their eigenvectors attain this bound.'],
56: ['SVD factors the centered data matrix into U, Σ, and Vᵀ. In compact SVD, U and V have perpendicular unit columns.', 'Substitution gives UᵀU=I, which removes the middle pair. The resulting diagonal values are squared singular values divided by n−1.', 'The columns of V therefore satisfy the covariance eigenvector equation. SVD computes them without explicitly forming S.'],
57: ['Subtract the training mean, then take the dot product with the learned direction. This transforms the new observation without fitting new axes.'],
58: ['Divide each centered feature by its sample standard deviation. Every nonconstant feature then has sample variance one.'],
}
for slide in course['slides']:
    if slide['id'] in why:
        assert len(why[slide['id']]) == len(slide['steps']), slide['id']
        for step, explanation in zip(slide['steps'], why[slide['id']]):
            step['why'] = explanation

# The local refreshers use the same learner-facing terminology as the route.
course['refreshers']['geometry'][1] = 'Each letter marks one observation. The green axis is a shared ruler through the center. Its score is one signed coordinate. The closest point on the axis is the projection. The gap to the original point is the recovery error.'
course['refreshers']['score'][1] = 'A vector stores coordinates. A unit vector has length one. Its dot product with a centered observation gives the signed projection score. Multiply matching coordinates, then add.'
course['refreshers']['eigen'][1] = 'A derivative measures local change. A gradient collects one derivative per coordinate. On the unit circle, the tangent gives an allowed change to first order. A stationary direction has zero turning slope. It can be a maximum or a minimum. Sw=λw says that S maps w to a multiple of itself.'

assert len(course['slides']) == 64
assert [s['id'] for s in course['slides']] == [s['id'] for s in before['slides']]
assert course['chapters'] == before['chapters']
assert course['notation'] == before['notation']
for old,new in zip(before['slides'],course['slides']):
    assert old['scene'] == new['scene'] and old['chapter'] == new['chapter']
    assert [x['tex'] for x in old['steps']] == [x['tex'] for x in new['steps']]
assert sum(len(s['steps']) for s in course['slides']) == 79
path.write_text(json.dumps(course, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('Updated 64 learner-facing claims and actions; reviewed all 79 equation reasons. All equations, IDs, scenes, and chapter ranges preserved.')
print('Before SHA256:',hashlib.sha256(before_bytes).hexdigest())
print('After SHA256:',hashlib.sha256(path.read_bytes()).hexdigest())
