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
