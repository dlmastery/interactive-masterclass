from pathlib import Path
import json

story=json.loads(Path('work/redesign_storyboard.json').read_text())
# Each equation is a separate reasoned step, not a wall of notation.
E={
10:[(r'\mu=\left(\frac{8+7+5+4}{4},\frac{7+8+4+5}{4}\right)=(6,6)','Add the four values in each column. Divide each sum by four.')],
11:[(r'x_A=(8,7)-(6,6)=(2,1)','Subtract the mean of each feature. A is two units right and one unit up from the center.')],
12:[(r'(r_A-\mu)-(r_B-\mu)=r_A-r_B','The two copies of the mean cancel. The difference between observations stays the same.')],
13:[(r'w=\begin{bmatrix}\cos\theta\\\sin\theta\end{bmatrix},\quad w_1^2+w_2^2=1','The angle sets the direction. The unit length fixes the scale of its scores.')],
14:[(r'z_A=w^\top x_A=2w_1+w_2','Multiply matching coordinates. Add the two products. A negative score is on the other side of the center.')],
15:[(r'\underbrace{z}_{4\times1}=\underbrace{X_c}_{4\times2}\underbrace{w}_{2\times1}','Apply the same weights to each row. This matrix product produces all four scores.')],
16:[(r'z_i(cw)=c z_i(w),\quad V(cw)=c^2V(w)','Doubling the arrow doubles every score. The variance then becomes four times as large.')],
17:[(r'\bar z=w_1\bar a+w_2\bar b=0','The centered feature means are zero. Their weighted sum is also zero.')],
18:[(r'\sum_i z_i=0\quad\text{but}\quad\sum_i z_i^2\geq0','Positive and negative scores can cancel. Their squares measure spread on both sides of the center.')],
19:[(r'V(w)=\frac{z_1^2+z_2^2+z_3^2+z_4^2}{3}','This is sample variance for four centered scores. Its units are square centimeters.')],
20:[(r'V(w)=\frac{1}{n-1}\sum_i (w^\top x_i)^2','The graph evaluates this expression for each direction. Next, we derive a way to find its maximum.')],
21:[(r'z_i^2=(w_1a_i+w_2b_i)(w_1a_i+w_2b_i)','Write the square as a product of two identical sums.'),(r'=w_1^2a_i^2+w_1w_2a_ib_i+w_2w_1b_ia_i+w_2^2b_i^2','Multiply each term in the first bracket by each term in the second.'),(r'=w_1^2a_i^2+2w_1w_2a_ib_i+w_2^2b_i^2','The middle products are equal. Add them to get the factor two.')],
22:[(r'V=\frac{\sum_i(w_1^2a_i^2+2w_1w_2a_ib_i+w_2^2b_i^2)}{n-1}','Add the expanded square for every observation.'),(r'=w_1^2\frac{\sum_i a_i^2}{n-1}+2w_1w_2\frac{\sum_i a_ib_i}{n-1}+w_2^2\frac{\sum_i b_i^2}{n-1}','The weights do not depend on the observation. Put them outside their sums.')],
23:[(r'V=w_1^2s_a^2+2w_1w_2s_{ab}+w_2^2s_b^2','The two square sums are feature variances. Name the product sum covariance, written as s_ab.')],
24:[(r's_{ab}=\frac{2\cdot1+1\cdot2+(-1)(-2)+(-2)(-1)}3=\frac83','Each product is positive in this cloud. Both features tend to lie on the same side of their means.')],
25:[(r's_a^2=s_b^2=\frac{10}3,\qquad s_{ab}=\pm\frac83','Changing the sign of the second feature preserves its squares. It reverses each cross-product.')],
26:[(r'S=\begin{bmatrix}s_a^2&s_{ab}\\s_{ab}&s_b^2\end{bmatrix}=\frac13\begin{bmatrix}10&8\\8&10\end{bmatrix}','The matrix stores the three quantities needed to calculate variance in any direction.')],
27:[(r'\underbrace{X_c^\top}_{2\times4}\underbrace{X_c}_{4\times2}=\begin{bmatrix}\sum a_i^2&\sum a_ib_i\\\sum b_ia_i&\sum b_i^2\end{bmatrix}','A row meets a column. Multiply matching entries and add.'),(r'S=\frac{X_c^\top X_c}{n-1}','Divide all four sums by the same sample divisor.')],
28:[(r'Sw=\begin{bmatrix}s_a^2w_1+s_{ab}w_2\\s_{ab}w_1+s_b^2w_2\end{bmatrix}','First multiply S by w. This gives a two-coordinate vector.'),(r'w^\top Sw=w_1^2s_a^2+2w_1w_2s_{ab}+w_2^2s_b^2','Take its dot product with w. The result is our expanded variance.')],
29:[(r'\frac{(X_cw)^\top(X_cw)}{n-1}=w^\top\frac{X_c^\top X_c}{n-1}w=w^\top Sw','Transposing a product reverses its order. These are three forms of the same calculation.')],
30:[(r'\max_w\; w^\top Sw\qquad\text{subject to }w^\top w=1','Choose the direction with the largest score variance. Compare only arrows of unit length.')],
31:[(r'Sw=\frac13\begin{bmatrix}10w_1+8w_2\\8w_1+10w_2\end{bmatrix}','The same covariance matrix can map a direction arrow to a new arrow.')],
32:[(r't=\begin{bmatrix}-w_2\\w_1\end{bmatrix},\qquad \frac{dV}{d\theta}=2t^\top Sw','The vector t points along a small turn of w. At a stationary direction, this slope is zero.')],
33:[(r'f(w_1,w_2)=S_{11}w_1^2+2S_{12}w_1w_2+S_{22}w_2^2','A partial derivative changes one coordinate while the other stays fixed.'),(r'\frac{\partial f}{\partial w_1}=2S_{11}w_1+2S_{12}w_2','Use the square rule. The term with only w2 has zero derivative.'),(r'\frac{\partial f}{\partial w_2}=2S_{12}w_1+2S_{22}w_2','Repeat for w2. Symmetry makes the two cross-term coefficients agree.'),(r'\nabla f=2Sw','The gradient collects these two slopes into one vector.')],
34:[(r'g(w)=w_1^2+w_2^2-1=0','This equation describes the circle of permitted directions.'),(r'\nabla g=\begin{bmatrix}2w_1\\2w_2\end{bmatrix}=2w','The gradient points outward. A small allowed change is tangent to the circle.')],
35:[(r'\nabla f=\lambda\nabla g','At a constrained optimum, the objective gradient has no component along an allowed small change.'),(r'2Sw=2\lambda w','Substitute the two gradients that we just calculated.'),(r'Sw=\lambda w','Divide both sides by two. The multiplier becomes the scale factor of this direction.')],
36:[(r'Sq=\lambda q','The input arrow q and its image Sq lie on the same line. This defines an eigenvector and its eigenvalue.')],
37:[(r'(S-\lambda I)q=0,\quad q\neq0','Move the right side to the left. A nonzero solution requires a singular matrix.'),(r'\det(S-\lambda I)=\left(\frac{10}3-\lambda\right)^2-\left(\frac83\right)^2=0','For a two-by-two matrix, the determinant is the diagonal product minus the other product.')],
38:[(r'\left(\frac{10}3-\lambda-\frac83\right)\left(\frac{10}3-\lambda+\frac83\right)=0','Factor the difference of two squares.'),(r'\left(\frac23-\lambda\right)(6-\lambda)=0','A product is zero when one factor is zero.'),(r'\lambda_1=6,\qquad\lambda_2=\frac23','These are the two possible scale factors. We order them from largest to smallest.')],
39:[(r'q=(u,v),\quad\lambda=6:\quad -8u+8v=0\;\Rightarrow\;v=u','Substitute 6 in the first row of the eigenvector equation. Multiply that row by three.'),(r'q_1=\frac{(1,1)}{\sqrt2},\qquad q_2=\frac{(1,-1)}{\sqrt2}','Repeat for 2/3. Divide each direction by its length to make a unit vector.')],
40:[(r'V(q)=q^\top Sq=q^\top(\lambda q)=\lambda','A unit eigenvector has variance equal to its eigenvalue. One candidate is the maximum; the other is the minimum.')],
41:[(r'q_1^\top Sq_2=\lambda_2 q_1^\top q_2','Apply S to q2 first.'),(r'q_1^\top Sq_2=(Sq_1)^\top q_2=\lambda_1 q_1^\top q_2','Symmetry lets S act on the other vector.'),(r'(\lambda_1-\lambda_2)q_1^\top q_2=0','If the eigenvalues differ, the dot product must be zero. The two directions are perpendicular.')],
42:[(r'w=aq_1+bq_2,\qquad a^2+b^2=1','The two unit eigenvectors form perpendicular axes. Every unit direction has coordinates a and b on these axes.')],
43:[(r'w^\top Sw=(aq_1+bq_2)^\top S(aq_1+bq_2)','Substitute the coordinates of w in the eigenvector basis.'),(r'=a^2\lambda_1+ab\lambda_2q_1^\top q_2+ab\lambda_1q_2^\top q_1+b^2\lambda_2','Expand the four products. Replace Sq1 and Sq2 with their eigenvalue forms.'),(r'=a^2\lambda_1+b^2\lambda_2','Both cross-terms contain a zero dot product. Each unit vector has squared length one.')],
44:[(r'V=a^2\lambda_1+b^2\lambda_2\leq a^2\lambda_1+b^2\lambda_1','Because λ2 is no larger than λ1, replacing λ2 cannot decrease this expression.'),(r'V\leq(a^2+b^2)\lambda_1=\lambda_1','The nonnegative squared weights add to one.'),(r'w=q_1\quad\Rightarrow\quad V=\lambda_1','This direction reaches the bound. It is a global maximum, not just a stationary point.')],
45:[(r'\lambda_1=\lambda_2=\lambda\quad\Rightarrow\quad V=\lambda(a^2+b^2)=\lambda','Equal eigenvalues give the same variance for every direction in their shared space.')],
46:[(r'\max_{\|w\|=1,\;w^\top q_1=0}w^\top Sw','The next component must be perpendicular to PC1. In higher dimensions, maximize variance within that remaining space.')],
47:[(r'Z=X_cQ,\qquad Q=[q_1\ q_2]','Each column of Q describes an axis. Each row of Z contains the new coordinates of one observation.')],
48:[(r'\operatorname{Cov}(Z)=\frac{Z^\top Z}{n-1}=Q^\top SQ','Substitute Z=XcQ and group the covariance matrix.'),(r'Q^\top SQ=\begin{bmatrix}\lambda_1&0\\0&\lambda_2\end{bmatrix}','Orthonormal eigenvectors make the off-diagonal entries zero.')],
49:[(r'\mathrm{fraction}_1=\frac{\lambda_1}{\lambda_1+\lambda_2}=\frac{6}{6+2/3}=0.90','The denominator is total variance. The ratio measures retained squared spread.')],
50:[(r'\widehat r_A=\mu+z_Aq_1','Multiply the retained score by its axis. Add the stored mean.'),(r'=(6,6)+\frac3{\sqrt2}\frac{(1,1)}{\sqrt2}=(7.5,7.5)','A originally measured (8,7). Its one-score reconstruction has an error in both features.')],
51:[(r'x_i=z_iw+e_i,\quad w^\top e_i=0','The residual e is the difference between the original point and its projection.'),(r'\|x_i\|^2=z_i^2+\|e_i\|^2','The kept vector and residual are perpendicular. Apply the right-triangle identity.')],
52:[(r'\sum_i\|e_i\|^2=\sum_i\|x_i\|^2-\sum_i z_i^2','Add the identity for every observation and move the kept term to the right.'),(r'\frac{\sum_i\|e_i\|^2}{n-1}=\operatorname{tr}(S)-w^\top Sw','Trace is the sum of the feature variances. The first term does not depend on the direction.'),(r'\arg\min_w\sum_i\|e_i\|^2=\arg\max_w w^\top Sw','The same direction solves both problems. The errors are perpendicular distances, not vertical regression errors.')],
53:[(r'x_i=z_{i1}q_1+z_{i2}q_2','Keeping both perpendicular coordinates recovers the original centered vector.')],
54:[(r'\mathrm{retained}=\frac{\sum_{j=1}^k\lambda_j}{\sum_{j=1}^p\lambda_j},\qquad\mathrm{loss}=\sum_{j=k+1}^p\lambda_j','The loss uses the sample divisor n−1. Multiply it by n−1 to get the total squared error.')],
55:[(r'V_k=\operatorname{tr}(W^\top SW)=\sum_{j=1}^p\lambda_j\alpha_j','W contains k perpendicular unit directions. Define αj as the squared length of the projection of qj into their space.'),(r'0\leq\alpha_j\leq1,\qquad\sum_j\alpha_j=k','A projection cannot increase a unit vector length. The sum equals the dimension of the retained space.'),(r'V_k\leq\lambda_1+\cdots+\lambda_k','Allocate the weight to the largest eigenvalues first. Choosing their eigenvectors reaches this bound.')],
56:[(r'X_c=U\Sigma V^\top','Singular value decomposition factors the centered table. U and V have orthonormal columns in the compact form.'),(r'S=\frac{V\Sigma^\top U^\top U\Sigma V^\top}{n-1}=V\frac{\Sigma^2}{n-1}V^\top','Use UᵀU=I. The diagonal entries are the squared singular values divided by n−1.'),(r'q_j=v_j,\qquad\lambda_j=\frac{\sigma_j^2}{n-1}','SVD gives the same PCA directions without explicitly forming the covariance matrix.')],
57:[(r'z_{\mathrm{new}}=Q_k^\top(r_{\mathrm{new}}-\mu_{\mathrm{train}})','Keep the training mean and learned directions fixed. New observations do not refit this model.')],
58:[(r'\widetilde r_{ij}=\frac{r_{ij}-\mu_j}{s_j}','Divide each centered feature by its sample standard deviation. Nonconstant features then have variance one.')],
}
groups=[(1,8,'What does PCA do?'),(9,20,'How do we measure a view?'),(21,30,'Why does covariance appear?'),(31,45,'Why do eigenvectors solve it?'),(46,56,'What can we keep and recover?'),(57,64,'When does the result help?')]
def scene(i):
    if i<=8:return 'geometry'
    if i<=12:return 'center'
    if i<=16:return 'score'
    if i<=20:return 'variance'
    if i<=23:return 'expansion'
    if i<=27:return 'covariance'
    if i<=30:return 'objective'
    if i<=41:return 'eigen'
    if i<=45:return 'maximum'
    if i<=49:return 'coordinates'
    if i<=54:return 'reconstruction'
    if i<=56:return 'spectrum'
    return ['newpoint','units','outliers','ring','notebook','challenge','exam','teachback'][i-57]
course={'version':2,'title':'PCA · from picture to proof','chapters':[{'start':a-1,'end':b,'question':c} for a,b,c in groups], 'slides':[]}
for i,(title,action,claim) in enumerate(story,1):
    course['slides'].append(dict(id=i,title=title,action=action,claim=claim,scene=scene(i),steps=[{'tex':t,'why':w} for t,w in E.get(i,[])],chapter=next(j for j,(a,b,_) in enumerate(groups) if a<=i<=b)))
course['refreshers']={
 'center':['Mean and centering','The mean is the sum divided by the number of observations. Calculate one mean per feature. Subtract each feature mean from its values. Centered values describe differences from the mean.'],
 'score':['Vectors and dot products','A vector stores coordinates. A unit vector has length one. Its dot product with a point gives the signed projection score. Multiply matching coordinates, then add.'],
 'variance':['Variance','Variance measures squared spread around a mean. Here the score mean is zero. Add the squared scores and divide by n−1. Using n instead changes the scale but not the best direction.'],
 'expansion':['Expand a square','Multiply each term in the first bracket by each term in the second bracket. In (A+B)², the middle terms are AB and BA. They give 2AB.'],
 'covariance':['Transpose and matrix multiplication','Transpose swaps rows and columns. A matrix product matches one row with one column. Multiply matching entries and add. In XcᵀXc, each entry compares two feature columns.'],
 'objective':['Read the dimensions','Xc has n rows and p columns. w has p entries. Xc w has n scores. S has p rows and p columns. wᵀSw is one number.'],
 'eigen':['Gradients, constraints, and eigenvectors','A derivative measures local change. A gradient collects one derivative per coordinate. On the unit circle, allowed small changes follow the tangent. At a constrained optimum, the gradient has no tangent component. Sw=λw says that S preserves the line of w.'],
 'maximum':['The basis theorem and the bound','A real symmetric matrix has an orthonormal basis of eigenvectors. We use this theorem for higher dimensions. The two-dimensional example can be checked directly. Squared coordinates in this basis are nonnegative and add to one. Their weighted eigenvalue average cannot exceed the largest eigenvalue.'],
 'coordinates':['Loadings and scores','Loadings are the feature weights in an axis. Scores are the coordinates of observations on that axis. Sign reversal changes both signs and preserves the same projection. Zero covariance does not generally imply independence.'],
 'reconstruction':['Length, projection, and trace','The squared length of (a,b) is a²+b². A unit-axis projection is zw. Its residual is perpendicular to the axis. Their squared lengths add. Trace means the sum of the diagonal entries.'],
 'spectrum':['Several retained directions','The columns of W are perpendicular unit vectors. WᵀW=I. Projecting onto these k directions gives k scores. Keeping all directions preserves the data. Keeping fewer can lose detail.'],
 'geometry':['How to read this picture','Each letter is one observation. Teal marks the retained axis. The score line shows one number for each observation. Orange marks a lost part. The axis we keep is perpendicular to the direction of a shadow.'],
}
course['notation']=[['rᵢ','An original observation, before centering.'],['μ','The mean of each original feature.'],['xᵢ','One centered observation: rᵢ−μ.'],['Xc','A table of centered observations, one per row.'],['w','A candidate direction of unit length.'],['zᵢ','The score of observation i on w.'],['S','The sample covariance matrix.'],['qⱼ','A learned unit eigenvector, or PCA direction.'],['λⱼ','Variance along qⱼ.'],['k','The number of retained components.']]
code='pca_course_v2 = '+repr(course)+'\nNone\n'
Path('work/pca_course_v2.py').write_text(code,encoding='utf-8')
(Path('outputs/pca-studio')/'course-v2.json').write_text(json.dumps(course,ensure_ascii=False,indent=2),encoding='utf-8')
print('Wrote 64 scene specifications and',sum(len(s['steps']) for s in course['slides']),'reasoned equation steps.')
