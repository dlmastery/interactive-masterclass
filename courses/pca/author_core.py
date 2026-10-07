"""Author-owned content source. Regenerates core.json; does not alter the notebook."""
import json
from pathlib import Path

scenes = []
def add(id, chapter, title, question, body, takeaway, kind, notes, **extra):
    scenes.append(dict(id=id, chapter=chapter, title=title, question=question,
        body=body, takeaway=takeaway, kind=kind, notes=notes, **extra))

add('purpose',0,'Two measurements. One useful coordinate.',
    'Can we store less and still recover the shape?',
    'Each dot is a position with an east and a north coordinate. We can store one number per dot, plus one shared ruler. Turn the ruler. Watch what we can recover.',
    'PCA finds directions that preserve the most variation. Keeping fewer directions gives a shorter, approximate description.', 'geometry',
    '[Start at 0°. Point to A, then its hollow copy.] These are invented positions in centimetres. Two numbers locate each dot. We want a shorter description. The decoder knows one shared ruler and its center. We send one signed distance for each point. [Turn to 45°.] The recovered points now lie closer to the originals. PCA finds this direction without guessing. It optimizes a precise reconstruction error. It does not promise to preserve every useful fact. We will build its rule, prove it, then test when to trust it.',
    mode='raw', angle=0, prompt='Try 0°, then 45°. Which ruler leaves less sideways error?')
add('promise',0,'A picture. A proof. A decision.', 'What will this lesson let you do?',
    'Build a smaller description. Derive the best direction. Decide whether its lost detail matters. The math will enter when the problem needs it.',
    'A useful explanation includes how PCA works and when its objective fits the task.', 'geometry',
    '[Compare 45° and 135°.] Both lines can encode the points. One loses much less. A picture gives a strong guess, but a guess is not a proof. Our eight questions lead from geometry to proof and practical judgment. Math help stays beside the current step. Speaker notes give the spoken explanation. The notebook link opens editable Python. Browser experiments respond instantly; the final native lab also reruns Python. Visiting a scene is not evidence that you learned it. Use the reasoning tasks to test your own explanation.', mode='raw', angle=45,
    prompt='State what a “good” shorter description should preserve.')
add('score',0,'One distance per point.', 'What is the number we send?',
    'Choose a dot. Its score is the signed distance along the ruler. The decoder puts a hollow dot at that distance. The sideways gap is lost.',
    'A direction belongs to the shared ruler. A score belongs to one observation.', 'geometry',
    '[Select A, then B, at 45°.] These points have the same score. Their original positions differ, but their shadows coincide. A shorter description can merge distinct observations. The score says how far to walk along the line from its center. It does not tell us how far to move sideways. Keep three objects separate: the shared direction, the individual score, and the reconstructed point. [Point to the score, then its hollow dot.] One is a number; the other is a location. Their difference from the original point is the residual.', mode='scores', angle=45,
    prompt='A and B share a score. Which part of their original positions is gone?')
add('decoder',0,'Save the shared rule once.', 'What else does the decoder need?',
    'Save a center and direction for the dataset. Save one score for each point. Multiply the score by the direction, then add the center.',
    'Scores alone are not enough. The decoder also needs the fitted coordinate system.', 'proof',
    '[Reveal the reconstruction rule.] The center records a shared position. The direction records how the one-dimensional code sits in the original plane. The score records an individual distance. Multiplying a score by a direction gives an offset. Adding the center gives a location. These shared quantities cost storage too. Four points make arithmetic visible; they are not a compression benchmark. With many observations and far fewer retained dimensions, the shared cost can be small relative to the saved coordinates. We still need to choose where the line passes.',
    steps=[[r'\widehat p_i=\mu+z_iw','Recover a location from a center, score, and direction.'],
           [r'nd\quad\longrightarrow\quad nk+dk+d','Typical stored numbers: scores, directions, and mean. File overhead is omitted.']],
    refresh=['Vector and scalar','A vector is an ordered list of coordinates. A scalar is one number. Multiply a vector by a scalar by multiplying every coordinate. Add vectors by adding matching coordinates.'])
add('center',0,'Move the origin to the cloud.', 'Why subtract the mean?',
    'The mean is (6, 6). Subtract it from each point. This shifts the cloud without changing gaps between points. Add the mean back when decoding.',
    'Centering separates shared position from variation. It does not rescale the axes.', 'center',
    '[Move the translation control.] Coordinates change, but shape does not. PCA should describe this shape rather than the location of the map origin. The mean east coordinate is six; the mean north coordinate is also six. A becomes two, one after centering. B becomes one, two. The centered observations sum to zero. We can now describe a line through zero and later shift it back. That is convenient, but convenience is not the full reason. We will justify this anchor after we have built the projection algebra. For now, use it as the shared center.',
    refresh=['Mean','Add the four east readings and divide by four. Do the same for north. This gives a point, (6, 6), with the average coordinate on each axis.'])
add('mean-proof',0,'A misplaced line adds error.', 'Why is a line through the mean sufficient?',
    'For a fixed direction, separate centered error from a shared offset. The cross term sums to zero. A sideways offset from the mean adds nonnegative loss.',
    'An optimal affine line can always pass through the sample mean.', 'proof',
    '[Reveal the error split.] P maps x to w(w transpose x), the perpendicular projection we already derived. Let a be an arbitrary anchor. Write each raw point as mean plus centered point. The sideways error splits into a centered part and a shared offset. Squaring and summing gives a cross term, but it vanishes because centered points sum to zero. The extra term is n times a squared length, so it cannot improve the loss. Choosing the mean removes it. Moving the anchor along the same line changes no line, so the anchor is not unique.',
    steps=[[r'P=ww^T,\quad p_i=\mu+x_i,\quad\sum_i x_i=0','P is the projector, and I is the identity map.'],
           [r'\sum_i\|(I-P)(p_i-a)\|^2=\sum_i\|(I-P)x_i\|^2+n\|(I-P)(\mu-a)\|^2','The summed cross term is zero. The second term is an avoidable offset cost.'],
           [r'a=\mu\quad\Rightarrow\quad\text{offset cost}=0','This works for any fixed direction.']],
    refresh=['Squared length and identity','‖v‖² adds the squared coordinates of v. I leaves a vector unchanged. I−P keeps the part not kept by P. The projector keeps the component along the unit ruler.'])
add('dot',0,'Weights turn a point into a score.', 'How do we calculate the shadow?',
    'Multiply matching coordinates and add. With a unit direction, this dot product is the signed distance along the ruler.',
    'For A = (2, 1), the 45° score is 3/√2 ≈ 2.12 cm.', 'proof',
    '[Reveal the direction and coordinate calculation.] The forty-five-degree unit direction has two equal entries, each one over square root two. Their squares add to one. For A, multiply two by the east entry and one by the north entry, then add. The result is three over square root two. Geometrically, a dot product is length times cosine of the angle to the unit ruler. That is the signed adjacent side of the right triangle. Multiply the score by the direction to recover one point five, one point five, the centered shadow.',
    steps=[[r'w=(1/\sqrt2,1/\sqrt2)^T,\quad\|w\|^2=1','A unit ruler separates direction from arbitrary scale.'],
           [r'z_A=w^Tx_A=2/\sqrt2+1/\sqrt2=3/\sqrt2','Transpose turns the direction into a row. Matching entries multiply and add.'],
           [r'\widehat x_A=z_Aw=(1.5,1.5)^T','The score is one number; the reconstruction has two coordinates.']],
    refresh=['Dot product','For a=(a₁,a₂) and b=(b₁,b₂), aᵀb=a₁b₁+a₂b₂. If b has unit length, the result is the signed projection of a onto b.'])
add('nearest',0,'Why use the perpendicular foot?', 'Could another point on the line be closer?',
    'Any other point adds a squared distance along the line to the squared perpendicular gap. It cannot reduce the first gap.',
    'Orthogonal projection is the best decoder on a fixed line for Euclidean squared error.', 'proof',
    '[Reveal perpendicularity first.] Let z be the dot-product score. Dot the residual x minus zw with w. The result is z minus z, zero, because w has unit length. Any different score a moves along the line away from that foot. The moves along and across the line are perpendicular, so their squared lengths add. The extra square is zero only when a equals z. We have proved the decoder is optimal on the chosen line. We have not chosen the best line yet. The proof also depends on Euclidean distance.',
    steps=[[r'w^T(x-zw)=w^Tx-z(w^Tw)=z-z=0','The residual is perpendicular to w.'],
           [r'\|x-aw\|^2=\|x-zw\|^2+(a-z)^2','Pythagoras splits a different reconstruction error into two perpendicular parts.'],
           [r'(a-z)^2\ge0\quad\Rightarrow\quad a=z\text{ is best}','The perpendicular foot reaches the smallest error.']],
    refresh=['Pythagoras now','For perpendicular u and v, ‖u+v‖²=‖u‖²+‖v‖². The cross term 2uᵀv is zero. This is why the two squared errors add.'])
add('triangle',1,'Kept and lost make a right triangle.', 'What stays fixed as the ruler turns?',
    'The original centered point stays still. Its shadow and gap move. Original squared length equals squared score plus squared gap.',
    'A rotation changes how a fixed total is split.', 'triangle',
    '[Select A and turn the ruler.] The dark segment reaches the original point. Its length stays fixed. The teal segment lies along the ruler. The dashed segment is the residual. They meet at a right angle. Because w has unit length, the squared teal length is z squared. For A, the total is two squared plus one squared, which equals five. Do not add the unsquared lengths. This identity concerns squares. If the lost square is one half, the kept square is four and one half. Now add this reasoning across the cloud.',
    angle=20, formula=r'\|x_i\|^2=z_i^2+\|x_i-z_iw\|^2',prompt='For A, the fixed total is 5. If the squared gap is 0.5, how much is kept?')
add('total',1,'Keeping more means losing less.', 'Does the whole cloud obey the same rule?',
    'Add the right-triangle identities. The total squared radius is fixed. Loss is that constant minus the sum of squared scores.',
    'Minimum reconstruction error and maximum retained squared length select the same line.', 'proof',
    '[Reveal the sum, then rearrange.] Every point has its own right triangle. Add the original totals, the retained squares, and the lost squares. The data stay fixed while we choose a ruler, so the total on the left is constant. Loss is therefore a constant minus retained squared length. Maximizing the retained term minimizes the loss. This earns the spread objective from the original reconstruction problem. It does not declare spread useful for all tasks. Before calling the retained term variance, we must verify that the scores are centered.',
    steps=[[r'\sum_i\|x_i\|^2=\sum_i z_i^2+\sum_i\|x_i-z_iw\|^2','Add one Pythagoras identity per observation.'],
           [r'\text{loss}=\underbrace{\sum_i\|x_i\|^2}_{\text{fixed}}-\sum_i z_i^2','The unit direction changes; the original centered data do not.'],
           [r'\arg\min_w\text{loss}=\arg\max_w\sum_i z_i^2','The same direction solves both objectives.']],
    refresh=['Arg max','“Max” is the largest value. “Arg max” is the input that reaches it. We want a direction w, not only a variance value.'])
add('score-mean',1,'Centered points give centered scores.', 'Why measure spread from zero?',
    'The average centered point is zero. Projecting that average gives zero. Thus the average score is zero too.',
    'Squared scores measure squared deviations from the score mean.', 'proof',
    '[Reveal the averaging step.] Variance measures spread about a mean, not distance from an arbitrary zero. The same direction weights apply to every point. We can therefore take the direction outside the average. The average score equals the direction dotted with the average centered vector, which is zero. This is a small but essential link. Squared score energy now measures spread rather than location. If we used raw points without centering, the energy could be large simply because the cloud sits far from the origin. Our geometry would solve a different problem.',
    steps=[[r'\bar z=\frac1n\sum_i w^Tx_i=w^T\left(\frac1n\sum_i x_i\right)','Projection with fixed weights commutes with averaging.'],
           [r'\sum_i x_i=0\quad\Rightarrow\quad\bar z=0','Centering made the sum of observation offsets zero.'],
           [r'\sum_i(z_i-\bar z)^2=\sum_i z_i^2','No further score-mean subtraction is needed.']],
    refresh=['Linearity','Using the same weights, projecting a sum equals summing its projections. Distributing multiplication through the sum shows why.'])
add('variance',1,'Variance gives spread a scale.', 'Why squares, and why n − 1?',
    'Signed offsets cancel. Squares count distance on either side. Sample variance divides their sum by n − 1. This fixed divisor does not change the winning direction.',
    'Use the same divisor for kept variance, lost variance, and total variance.', 'proof',
    '[Reveal the scores at forty-five degrees.] Two scores are positive and two negative. Adding them gives zero, even though the points are spread out. Their squared scores sum to eighteen. Divide by three to get sample variance six, in square centimetres. The n minus one convention compensates for estimating a mean in the usual sample variance estimator. That statistical motivation is separate from our optimization: division by n instead would scale every candidate equally. Keep the convention consistent so covariance eigenvalues, singular values, and reconstruction losses agree.',
    steps=[[r'z=(3/\sqrt2,3/\sqrt2,-3/\sqrt2,-3/\sqrt2)','These scores have mean zero.'],
           [r'\operatorname{var}(z)=\frac{\sum_i z_i^2}{n-1}=18/3=6','Squared score units are cm².'],
           [r'\text{total}=20/3,\quad\text{kept}=6,\quad\text{lost}=2/3','The normalized kept and lost amounts add to the normalized total.']],
    refresh=['Sample and population','The sample is our observed set. A population is the broader distribution of interest. We first solve the exact sample optimization. Broader claims need sampling assumptions and validation.'])
add('unit',1,'A longer arrow is a fake win.', 'Why constrain the direction length?',
    'Doubling w doubles all dot-product scores and multiplies their variance by four. The line itself has not changed. Compare only unit directions.',
    'PCA chooses orientation, not an arbitrary ruler scale.', 'proof',
    '[Reveal w and then two w.] Without a length constraint, we can inflate the objective without changing the line. Whenever variance is positive, make the vector longer and the dot-product scores grow without bound. Our decoder formula assumed a unit vector, so each score was a distance. With a nonunit vector, a correct projection coefficient would require division by its squared length. We keep the geometry simple by fixing the squared length to one. This constraint is why our optimization will move around a circle or sphere instead of through all vectors freely.',
    steps=[[r'z_i(2w)=2z_i(w)','The weights and every score double.'],[r'V(2w)=4V(w)','Variance squares the scale change.'],[r'\max_{w^Tw=1}V(w)','Fix length; choose only the orientation.']],
    refresh=['Unit vector','A unit vector has squared entries that add to one. Normalize a nonzero vector v by dividing every coordinate by its length ‖v‖.'])
add('seek',1,'Find a good line before the formula.', 'Can you explain why it wins?',
    'Seek the largest retained variance. Compare your choice with the optimum. Explain what stays fixed and what changes.',
    'A numerical search checks a guess. It does not replace a general proof.', 'geometry',
    '[Start at twenty degrees.] Predict which way the ruler should turn before you move it. Increase the kept part while shrinking the lost part. Then compare your choice with the computed optimum. Explain why the two goals agree for the same centered dataset. Do not rely only on the phrase “the dots line up.” Name the fixed total and the changing split. In two dimensions, a slider is useful. In a thousand dimensions, it is not a practical solver. We need a compact data summary and an algebraic rule. The squared-score formula tells us what summary to build.',
    mode='predict',angle=20,prompt='Complete: “This line loses less because the total is fixed and …”')
add('new-point',1,'Decode a point you have not seen.', 'Can you run the saved rule yourself?',
    'A new position is (9, 6). Keep the learned mean (6, 6) and 45° direction. Center, score, reconstruct, then add the mean.',
    'Use the training mean and directions for new observations. Do not refit them for each point.', 'proof',
    '[Pause before revealing each result.] Subtract the saved mean to get three, zero. Dot that offset with the learned direction to get three over square root two. Multiply back to obtain one point five, one point five. Add the mean and recover seven point five, seven point five. This is a new observation, but the coordinate system is the one we already fitted. Recomputing a separate mean for this single point would erase its offset. Later, we will extend this rule to honest validation: fit preprocessing and PCA only on training data, then freeze them for evaluation.',
    steps=[[r'x_{new}=(9,6)^T-(6,6)^T=(3,0)^T','Subtract the saved training mean.'],[r'z_{new}=3/\sqrt2,\quad\widehat x_{new}=(1.5,1.5)^T','Encode, then reconstruct the centered offset.'],[r'\widehat p_{new}=(7.5,7.5)^T','Add the saved mean back.']],
    prompt='Write all three results before revealing them.')
add('boundary',1,'Most spread is not always most useful.', 'Useful for which task?',
    'A small sideways signal may mark a fault, a rare group, or an outcome we need. Our proof will protect squared reconstruction, not every downstream goal.',
    'State the task before treating small variance as safe to discard.', 'decision',
    '[Read the scenario before revealing feedback.] Suppose large sensor variation is harmless drift, while a tiny second signal marks a fault. One-component PCA may retain the drift. It can be optimal for input reconstruction and poor for fault detection at the same time. There is no contradiction: the tasks reward different things. Keep this boundary in mind throughout the proof. A theorem helps most when we know exactly what it promises. After the derivation, we will build this counterexample and compare alternatives. For now, reject the idea that retained variance is a percentage of all useful information.',
    mode='objective',prompt='A small-variance direction perfectly identifies faults. What does retaining 95% variance guarantee?',choices=['At least 95% fault accuracy','95% of the chosen sample variance','The discarded direction is noise'],correct=1,
    feedback=['Input spread does not measure fault accuracy.','Correct. Evaluate the fault task separately.','Small variation can carry a decisive signal. Noise needs evidence.'])
add('square',2,'Square the score. Keep every term.', 'Where does covariance come from?',
    'A tilted score combines both coordinates. Its square contains two square terms and one cross term. All three affect its spread.',
    'Separate feature variances do not describe how the features move together.', 'proof',
    '[Reveal the product, then distribute.] Multiply the sum by itself. Each term in the first factor multiplies each term in the second, giving four products. The two mixed products are equal, so they combine with a factor of two. Omitting them loses the cloud tilt. This is why covariance appears. We are not inserting a matrix because a recipe says so. Our reconstruction objective led to squared scores, and their expansion asks for products of different coordinates. Next we collect those products across observations and see what their signs mean.',
    steps=[[r'z^2=(w_1x+w_2y)(w_1x+w_2y)','Each term multiplies both terms in the other factor.'],[r'z^2=w_1^2x^2+w_1w_2xy+w_2w_1yx+w_2^2y^2','The mixed products are equal real numbers.'],[r'z^2=w_1^2x^2+2w_1w_2xy+w_2^2y^2','Keep the cross term.']],
    refresh=['Square of a sum','(a+b)²=a²+2ab+b², not a²+b². Set a=b=1: four is not two.'])
add('products',2,'Signed products remember the tilt.', 'What does each point contribute?',
    'Multiply the centered offsets. Same signs give a positive product; opposite signs give a negative one. Sum and divide by n − 1.',
    'Covariance measures joint linear variation about the mean.', 'covariance',
    '[Select A before revealing its product.] A is two east and one north of the mean, so the product is positive two. A point below and left has two negative offsets; its product is positive too. Both support a positive tilt. [Flip the tilt.] Separate squared columns remain unchanged, but the mixed products change sign. Covariance detects the change that the marginal variances miss. Zero covariance does not prove no relationship: positive and negative products can cancel. We will later test that boundary with a curved, deterministic relationship.',
    prompt='Predict a product sign. Flip the cloud and explain what stays unchanged.',refresh=['Covariance','For centered pairs (xᵢ,yᵢ), sample covariance is Σxᵢyᵢ/(n−1). Pairing a coordinate with itself gives its variance.'])
add('cov-matrix',2,'Three numbers summarize our objective.', 'How should we organize these products?',
    'Put the two variances on the diagonal. Put covariance in both off-diagonal positions. This symmetric matrix is S.',
    'Covariance retains the second-order information for this objective, not the full dataset.', 'proof',
    '[Reveal the data sums.] East squares are four, one, one, four. North squares reverse that order. Both sums are ten. Every mixed product is two, so that sum is eight. Divide by three. The off-diagonal entries match because x times y equals y times x. We can now evaluate any direction from three numbers. This is a useful summary, not a complete description of the cloud. Different datasets may have identical covariance. Later, nonlinearity and outliers will expose facts that these second-order numbers cannot resolve by themselves.',
    steps=[[r'\sum x_i^2=10,\quad\sum y_i^2=10,\quad\sum x_iy_i=8','Sum across the four centered observations.'],[r'S=\frac13\begin{bmatrix}10&8\\8&10\end{bmatrix}','Rows and columns both label features.'],[r'S_{11}=\operatorname{var}(x),\quad S_{22}=\operatorname{var}(y),\quad S_{12}=S_{21}=\operatorname{cov}(x,y)','All entries have units cm² in this same-unit example.']],
    refresh=['Matrix at this step','A matrix is a table with a defined operation. Its labels matter. In S, both axes label features. They do not label observations.'])
add('quadratic',2,'wᵀSw is the sum we already know.', 'What does the matrix product do?',
    'Multiply S by w, then dot the result with w. Expanding gives the two variance terms and the cross term from squared scores.',
    'Compact notation does not change the objective.', 'proof',
    '[Reveal S times w.] Each matrix row makes a weighted sum. Dot the resulting vector with w and expand again. The two diagonal terms use squared weights. Symmetry combines the two cross terms. That expression matches the squared-score expansion after averaging over the data. If the compact notation feels opaque, return to the three terms rather than memorizing a symbol chain. Check the shapes too: row direction, square covariance, column direction. Their product is a scalar, as variance must be. Now we can evaluate every direction without rereading every observation.',
    steps=[[r'Sw=\begin{bmatrix}S_{11}w_1+S_{12}w_2\\S_{21}w_1+S_{22}w_2\end{bmatrix}','Each row gives one weighted sum.'],[r'w^TSw=w_1^2S_{11}+2w_1w_2S_{12}+w_2^2S_{22}','Symmetry combines the cross terms.'],[r'\operatorname{var}(z)=w^TSw','Shapes: (1×d)(d×d)(d×1) gives one number.']],
    refresh=['Matrix dimensions','Inner dimensions must match for a matrix product. The remaining outer dimensions give the result shape. A 1×1 result represents a scalar.'])
add('outer',2,'One point contributes one small matrix.', 'How do we extend this to many features?',
    'The outer product xᵢxᵢᵀ lists every coordinate pair for one observation. Add those matrices and divide by n − 1.',
    'The same construction works in any number of dimensions.', 'proof',
    '[Reveal A’s outer product.] Multiplying its column by its row produces four coordinate pairs. This is different from the dot product: row times column would yield the scalar squared length. Add these outer products across observations and every feature pair has its required sum. With d features, the result is d by d. Multiplying on the left and right by a direction extracts the average squared score. This generalizes the two-coordinate calculation without inventing a new objective. The matrix is simply a compact store of the products that squared projection needs.',
    steps=[[r'x_Ax_A^T=\begin{bmatrix}2\\1\end{bmatrix}\begin{bmatrix}2&1\end{bmatrix}=\begin{bmatrix}4&2\\2&1\end{bmatrix}','Column times row gives all coordinate pairs.'],[r'S=\frac1{n-1}\sum_i x_ix_i^T','Sum one contribution per observation.'],[r'w^TSw=\frac1{n-1}\sum_i(w^Tx_i)^2','Each term becomes the square of a scalar score.']],
    refresh=['Inner versus outer product','xᵀx is a scalar squared length. xxᵀ is a matrix of pairwise coordinate products. Order matters.'])
add('data-matrix',2,'Rows are observations. Columns are features.', 'Why does XᵀX appear in code?',
    'Stack centered observations as rows of X. XᵀX sums products down each pair of feature columns. These are covariance numerators.',
    'S=XᵀX/(n−1) is the same summary in data-matrix notation.', 'matrix',
    '[Trace the upper-right product.] The first feature column contains east offsets; the second contains north offsets. Their dot product is the upper-right entry of X transpose X. It sums the paired products over observations and gives eight. Each diagonal pairs a column with itself, giving a sum of squares. We use rows for observations in code. When writing a single x i in the derivation, we treat it as a column. Stating that convention prevents transpose mistakes. All scores at once form X w, one score per observation.',
    steps=[[r'X=\begin{bmatrix}2&1\\1&2\\-1&-2\\-2&-1\end{bmatrix}\in\mathbb R^{4\times2}','Each row is one centered observation.'],[r'X^TX=\begin{bmatrix}10&8\\8&10\end{bmatrix},\quad S=X^TX/3','Pair columns and sum over observations.'],[r'z=Xw\in\mathbb R^{n\times1}','One score per row.']],refresh=['Transpose','Transpose swaps rows and columns. It does not invert or undo a matrix.'])
add('psd',2,'Two properties make the proof possible.', 'What is special about covariance?',
    'S is symmetric. Also, wᵀSw is nonnegative because it is an average of squared scores. This property is called positive semidefinite.',
    'Negative off-diagonal entries are allowed. A direction cannot have negative variance.', 'proof',
    '[Reveal symmetry, then nonnegativity.] Covariance is symmetric because opposite entries contain the same products. Positive semidefinite has a concrete meaning: no direction has negative variance. The sum-of-squares expression proves it. Negative covariance is still allowed; it records opposite signs occurring together. These properties will let us invoke a theorem for real symmetric matrices. The theorem provides real eigenvalues and a perpendicular eigenbasis. Nonnegative quadratic forms make covariance eigenvalues nonnegative. We will derive why those eigenvalues are exactly the variances of special directions.',
    steps=[[r'S^T=S','Feature pairing is symmetric.'],[r'w^TSw=\frac{\|Xw\|^2}{n-1}\ge0','Squared length cannot be negative.'],[r'Sq=\lambda q,\ \|q\|=1\quad\Rightarrow\quad\lambda=q^TSq\ge0','The eigenvector notation will be derived shortly.']],prompt='Can covariance have negative off-diagonal entries? Explain why this does not give negative variance.')
add('objective',2,'State the problem we have earned.', 'Which unit direction loses least?',
    'Maximize wᵀSw subject to wᵀw=1. This retains the most score variance and therefore gives the least squared reconstruction error.',
    'We have an objective and constraint. We still need a global solution.', 'proof',
    '[Read the optimization in ordinary words.] Among all unit directions, choose the one with the largest projected sample variance. S is fixed; w is our choice. Unit length prevents artificial score inflation. Pythagoras connected maximum variance to minimum reconstruction loss. Rebuild that chain without formulas: choose a ruler, send distances, recover points, add squared gaps, and retain as much of a fixed total as possible. The trace is the sum of feature variances, which supplies that fixed total. Next we turn the direction slightly to discover the equation an optimum must satisfy.',
    steps=[[r'\max_{w\in\mathbb R^d}w^TSw\quad\text{subject to }w^Tw=1','Known: centered data and S. Unknown: unit direction w.'],[r'L(w)=\operatorname{tr}(S)-w^TSw','Normalized reconstruction loss is total variance minus kept variance.']],refresh=['Trace','Trace adds diagonal entries. For S it adds original feature variances, equal to total squared centered radius divided by n−1.'])
add('tangent',3,'A sideways push means we can improve.', 'Where could an optimum occur?',
    'A legal move turns the unit direction without changing its length. If Sw has a sideways part, a small turn can raise variance.',
    'At a stationary direction, Sw must be parallel to w.', 'eigen',
    '[Start at twenty degrees.] We may turn the ruler but cannot lengthen it. The tangent points along a small legal turn. Twice its dot product with Sw gives the rate of variance change per radian. Positive means turn one way; negative means the other. At a stationary direction, this sideways change is zero. In a plane, Sw must then be parallel to w. In more dimensions, it must have zero component along every tangent. This geometric condition is why eigenvectors appear. The calculus will express this same restriction, not replace the picture with an unrelated trick.',
    formula=r'w(\theta)=(\cos\theta,\sin\theta)^T,\quad t=(-\sin\theta,\cos\theta)^T',refresh=['Derivative','A derivative gives the first-order rate of change for a small move. Here it measures how variance changes as the ruler turns, with angle in radians.'])
add('gradient',3,'Expand one small change.', 'Why is the gradient 2Sw?',
    'Replace w by w+εh. Expand the quadratic form. Symmetry combines the two first-order terms into 2εhᵀSw.',
    'At a constrained stationary point, the gradient cannot improve the objective along a tangent.', 'proof',
    '[Reveal the perturbation expansion.] Substitute w plus epsilon h into both copies of the direction. Distribute the products. Symmetry makes the two first-order cross terms equal. The epsilon-squared term vanishes faster than epsilon as epsilon approaches zero. The first-order rate is therefore twice h transpose S w. The gradient is the vector that dots with h to give this rate, so it is two S w. A first-order motion on the unit sphere has h transpose w equal to zero. At stationarity, every such legal tangent must have zero first-order gain.',
    steps=[[r'(w+\varepsilon h)^TS(w+\varepsilon h)=w^TSw+2\varepsilon h^TSw+\varepsilon^2h^TSh','Expand and use Sᵀ=S.'],[r'D_hV=2h^TSw,\quad\nabla V=2Sw','The first-order rate is the coefficient of ε.'],[r'h^Tw=0\quad\Rightarrow\quad h^TSw=0\text{ at stationarity}','No tangent has a first-order improvement.']],refresh=['Gradient','The gradient collects partial derivatives. Its dot product with a small change gives the first-order change in a scalar objective.'])
add('lagrange',3,'Enforce the constraint in one equation.', 'How does the unit sphere become algebra?',
    'Subtract a multiplier times the length constraint. Set the gradient to zero. S must stretch the direction without turning it.',
    'Stationary directions satisfy Sw=λw. This gives candidates, not yet a maximum proof.', 'proof',
    '[Reveal the Lagrangian.] Lambda is an unknown multiplier that lets the objective gradient align with the constraint gradient. The gradient of squared length is two w. Set their difference to zero and cancel two. The result is S w equals lambda w, the same parallel-vector condition we saw geometrically. Lambda is solved with w; it is not a tuning knob. The constraint gradient is nonzero on the unit sphere, so this necessary condition applies to a smooth constrained optimum. Necessary matters: some solutions will be minima. We will explicitly reject that trap.',
    steps=[[r'\mathcal L=w^TSw-\lambda(w^Tw-1)','λ is the unknown constraint multiplier.'],[r'\nabla_w\mathcal L=2Sw-2\lambda w=0','The gradients align at a stationary constrained point.'],[r'Sw=\lambda w,\quad w^Tw=1','An eigenvector equation plus unit length.']],refresh=['Lagrange multiplier','At a smooth constrained optimum, the objective gradient is normal to the constraint surface. A multiplier expresses that alignment; it does not establish a global maximum.'])
add('eigenvalue',3,'The eigenvalue is the variance.', 'What do the new names mean?',
    'An eigenvector is a nonzero direction a matrix preserves. The eigenvalue is its scale factor. For unit covariance eigenvectors, that scale equals score variance.',
    'Eigenvector: direction. Eigenvalue: variance along that direction.', 'proof',
    '[Read the matrix equation as a geometric action.] Multiplying by S may turn a general vector. An eigenvector stays on its own line. Multiply the equation on the left by w transpose. The left side becomes our variance objective. The right becomes lambda times squared length, which is one. Therefore lambda equals the projected sample variance. Our toy covariance scales the long diagonal by six and the short diagonal by two thirds. Both are legitimate eigenvectors. Naming them has not yet proved which one is the best representation. The next contrast makes that distinction visible.',
    steps=[[r'Sw=\lambda w\quad\Rightarrow\quad w^TSw=\lambda w^Tw','Dot both sides with w.'],[r'\|w\|=1\quad\Rightarrow\quad V(w)=\lambda','The covariance eigenvalue equals achieved score variance.']],refresh=['Eigenvector','A nonzero q is an eigenvector of S when Sq=λq for a scalar λ. It is a direction preserved by that matrix action.'])
add('stationary-trap',3,'The worst line passes that test too.', 'Does zero turning rate prove a maximum?',
    'Both diagonals are eigenvectors. One keeps 6; the other keeps 2/3. Both have zero first-order turning gain.',
    'A necessary condition is not a sufficient global guarantee.', 'eigen',
    '[Choose forty-five degrees, then one hundred thirty-five.] At both positions, the derivative is zero and Sw is parallel to w. Yet one is the best line and the other the worst in this plane. A zero slope can mark a maximum, a minimum, or another stationary point in a more general problem. We need a bound that applies to every unit direction, not just candidates. Choosing the largest eigenvalue feels plausible. The next steps prove it by expressing every direction in a basis the covariance matrix preserves.',
    prompt='What does a zero tangent derivative justify?',choices=['This is the best line','This is a stationary candidate','The coordinates are independent'],correct=1,
    feedback=['The minor eigenvector is a counterexample.','Correct. A global comparison still remains.','Stationarity gives no independence claim.'])
add('spectral',3,'Use a basis the matrix preserves.', 'Can we compare every direction at once?',
    'The spectral theorem gives a real symmetric matrix an orthonormal eigenbasis. Express any unit direction in that basis. We invoke this theorem here; we do not prove the theorem itself.',
    'The optimization becomes a comparison of eigenvalues and squared weights.', 'proof',
    '[Reveal the basis properties.] A basis can build every vector from its directions. Orthonormal means those directions are perpendicular and have unit length. The finite-dimensional spectral theorem supplies an eigenbasis with these properties for a real symmetric matrix. This is an explicitly invoked foundation, not something proved by an ellipse drawing. Expand any candidate w in that basis. The matrix scales each basis vector by its eigenvalue. Unit length says the squared coefficients sum to one. We now have a way to compare every possible direction through its coefficients.',
    steps=[[r'Sq_j=\lambda_jq_j,\quad q_i^Tq_j=\delta_{ij}','δ is one for matching indices and zero otherwise.'],[r'w=\sum_j a_jq_j','Every direction has coordinates in this basis.'],[r'\|w\|^2=\sum_j a_j^2=1','Perpendicular unit basis vectors make squared lengths add.']],
    refresh=['Basis','A basis is a set of independent directions that builds every vector in a space. The coefficients are coordinates. Changing basis changes coordinates, not the vector itself.'],source='https://www.cs.cornell.edu/courses/cs6210/2025fa/lec/2025-11-03.html')
add('cross-vanish',3,'Why do mixed terms disappear?', 'Perpendicularity alone is not enough.',
    'First use Sqⱼ=λⱼqⱼ. Then orthogonality removes cross terms between different basis vectors. Both properties matter.',
    'In the eigenbasis, variance is a sum of eigenvalues times squared coefficients.', 'proof',
    '[Reveal the mixed entry before the sum.] A general matrix can mix a perpendicular basis. We specifically need an eigenbasis. Apply S to q j and replace it with lambda j q j. Now dot with q i. The result is zero when the indices differ, and lambda j when they match. Expand both copies of w in the quadratic form. Every mixed pair vanishes for this reason, leaving the diagonal sum. This is the exact algebraic bridge to the weighted-average proof. It should not be skipped behind the phrase “by orthogonality.”',
    steps=[[r'q_i^TSq_j=\lambda_jq_i^Tq_j','Use the eigenvector property first.'],[r'w^TSw=\sum_i\sum_j a_i a_j q_i^TSq_j','Expand both direction vectors.'],[r'w^TSw=\sum_j\lambda_j a_j^2','Only matching indices survive.']],refresh=['Double sum','Choose a basis term from the left vector and a term from the right. The eigenvector and orthogonality properties cancel all pairs with different indices.'])
add('global',3,'No mixture beats the best ingredient.', 'Why is the largest eigenvalue globally best?',
    'Squared coefficients are nonnegative and sum to one. Variance is their weighted average of eigenvalues. No average exceeds the largest ingredient.',
    'The largest eigenvalue bounds every unit direction. Its eigenvector reaches that bound.', 'mixture',
    '[Put all squared weight on the first direction, then move some away.] With unequal eigenvalues, assigning weight to the smaller one lowers the average. In any dimension, each eigenvalue is at most lambda one. Replacing all of them by lambda one cannot decrease the sum. The weights sum to one, leaving lambda one as an upper bound. The first eigenvector reaches it. Equality also holds for any unit direction entirely inside a tied largest eigenspace. This compares every candidate direction, not just a finite slider search. We now have the promised global proof.',
    formula=r'V(w)=\sum_j\lambda_j a_j^2\le\lambda_1\sum_j a_j^2=\lambda_1',prompt='Explain the bound without referring to the slider.')
add('ties',3,'Sometimes several answers are right.', 'Is the best direction unique?',
    'A sign flip changes scores but not reconstruction. Equal top eigenvalues allow many optimal directions. Near ties can make individual axes sensitive to small data changes.',
    'A line or subspace can be meaningful even when a particular signed axis is not.', 'mixture',
    '[Toggle equal eigenvalues.] Every mixture now has the same variance. No line in this plane is preferred by our objective. With a strict top eigenvalue, the leading line is unique, but its arrow sign is still arbitrary. Replace w by minus w and every score also changes sign, leaving their product unchanged. Near ties are different from exact ties: small perturbations may rotate axes strongly. For a multi-direction representation, stability depends on separation at the retained boundary. Later we will distinguish an unstable individual axis from a stable retained subspace.',
    prompt='If software flips all PC1 score signs, which reconstructed points change?',refresh=['Eigenspace','An eigenspace contains all vectors with a given eigenvalue, plus zero. A repeated eigenvalue can support multiple independent eigenvectors and many valid bases.'])
add('opening-payoff',3,'Return to the opening ruler.', 'Did the proof recover our geometric guess?',
    'The long diagonal has eigenvalue 6. The short diagonal has eigenvalue 2/3. The first keeps 90% of this sample variance and loses 10%.',
    'Our 45° guess is now a proved optimum for the stated squared loss.', 'proof',
    '[Reveal each matrix multiplication.] The long diagonal is scaled by six; the short by two thirds. Normalize both to unit length. Their eigenvalues sum to twenty thirds, the total variance and trace. Six divided by twenty thirds is ninety percent. The remaining two thirds is the normalized reconstruction error. These numbers are the same kept and lost pieces we saw in the opening. We can now draw, calculate, and justify the answer. Ninety percent is about this metric and sample, not ninety percent of all information or ninety percent prediction accuracy. Next, keep more than one direction.',
    steps=[[r'S\frac{(1,1)^T}{\sqrt2}=6\frac{(1,1)^T}{\sqrt2}','The long diagonal is the first PC direction.'],[r'S\frac{(1,-1)^T}{\sqrt2}=\frac23\frac{(1,-1)^T}{\sqrt2}','The perpendicular diagonal records the remaining spread.'],[r'\frac{6}{6+2/3}=0.90,\quad L=2/3','Retained ratio and normalized loss describe the same split.']],prompt='Explain why “90% of variance” is not “90% of everything useful.”')

# Make the zero cross term explicit before the affine loss split.
next(s for s in scenes if s['id']=='mean-proof')['steps'].insert(1,[r'\sum_i(I-P)x_i=(I-P)\sum_i x_i=0', 'The common offset dots with this zero sum, so the total cross term vanishes.'])
# Defer the affine proof until outer-product notation has been earned.
mean_scene=next(s for s in scenes if s['id']=='mean-proof')
scenes.remove(mean_scene)
mean_scene['chapter']=2
scenes.insert(1+next(i for i,s in enumerate(scenes) if s['id']=='outer'),mean_scene)

if __name__ == '__main__':
    path=Path(__file__).parent/'v/lesson/src/core.json'
    path.write_text(json.dumps(scenes,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(scenes)} core scenes; global proof at scene {1+next(i for i,s in enumerate(scenes) if s["id"]=="global")}')
