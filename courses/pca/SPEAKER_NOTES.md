# PCA: a shorter description — presenter script

84 authored scenes. Brackets are visual cues; remaining notes are the spoken script. This is not a recorded or rehearsed audio track. Match live control states to the conditional cues.

## 1. Two measurements. One useful coordinate.
`purpose` · Chapter 1

**Question:** Can we store less and still recover the shape?

[Start at 0°. Point to A, then its hollow copy.] These are invented positions in centimetres. Two numbers locate each dot. We want a shorter description. The decoder knows one shared ruler and its center. We send one signed distance for each point. [Turn to 45°.] The recovered points now lie closer to the originals. PCA finds this direction without guessing. It optimizes a precise reconstruction error. It does not promise to preserve every useful fact. We will build its rule, prove it, then test when to trust it.

**Learner task:** Try 0°, then 45°. Which ruler leaves less sideways error?

## 2. A picture. A proof. A decision.
`promise` · Chapter 1

**Question:** What will this lesson let you do?

[Compare 45° and 135°.] Both lines can encode the points. One loses much less. A picture gives a strong guess, but a guess is not a proof. Our eight questions lead from geometry to proof and practical judgment. Math help stays beside the current step. Speaker notes give the spoken explanation. The notebook link opens editable Python. Browser experiments respond instantly; the final native lab also reruns Python. Visiting a scene is not evidence that you learned it. Use the reasoning tasks to test your own explanation.

**Learner task:** State what a “good” shorter description should preserve.

## 3. One distance per point.
`score` · Chapter 1

**Question:** What is the number we send?

[Select A, then B, at 45°.] These points have the same score. Their original positions differ, but their shadows coincide. A shorter description can merge distinct observations. The score says how far to walk along the line from its center. It does not tell us how far to move sideways. Keep three objects separate: the shared direction, the individual score, and the reconstructed point. [Point to the score, then its hollow dot.] One is a number; the other is a location. Their difference from the original point is the residual.

**Learner task:** A and B share a score. Which part of their original positions is gone?

## 4. Save the shared rule once.
`decoder` · Chapter 1

**Question:** What else does the decoder need?

[Reveal the reconstruction rule.] The center records a shared position. The direction records how the one-dimensional code sits in the original plane. The score records an individual distance. Multiplying a score by a direction gives an offset. Adding the center gives a location. These shared quantities cost storage too. Four points make arithmetic visible; they are not a compression benchmark. With many observations and far fewer retained dimensions, the shared cost can be small relative to the saved coordinates. We still need to choose where the line passes.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 5. Move the origin to the cloud.
`center` · Chapter 1

**Question:** Why subtract the mean?

[Move the translation control.] Coordinates change, but shape does not. PCA should describe this shape rather than the location of the map origin. The mean east coordinate is six; the mean north coordinate is also six. A becomes two, one after centering. B becomes one, two. The centered observations sum to zero. We can now describe a line through zero and later shift it back. That is convenient, but convenience is not the full reason. We will justify this anchor after we have built the projection algebra. For now, use it as the shared center.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 6. Weights turn a point into a score.
`dot` · Chapter 1

**Question:** How do we calculate the shadow?

[Reveal the direction and coordinate calculation.] The forty-five-degree unit direction has two equal entries, each one over square root two. Their squares add to one. For A, multiply two by the east entry and one by the north entry, then add. The result is three over square root two. Geometrically, a dot product is length times cosine of the angle to the unit ruler. That is the signed adjacent side of the right triangle. Multiply the score by the direction to recover one point five, one point five, the centered shadow.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 7. Why use the perpendicular foot?
`nearest` · Chapter 1

**Question:** Could another point on the line be closer?

[Reveal perpendicularity first.] Let z be the dot-product score. Dot the residual x minus zw with w. The result is z minus z, zero, because w has unit length. Any different score a moves along the line away from that foot. The moves along and across the line are perpendicular, so their squared lengths add. The extra square is zero only when a equals z. We have proved the decoder is optimal on the chosen line. We have not chosen the best line yet. The proof also depends on Euclidean distance.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 8. Kept and lost make a right triangle.
`triangle` · Chapter 2

**Question:** What stays fixed as the ruler turns?

[Select A and turn the ruler.] The dark segment reaches the original point. Its length stays fixed. The teal segment lies along the ruler. The dashed segment is the residual. They meet at a right angle. Because w has unit length, the squared teal length is z squared. For A, the total is two squared plus one squared, which equals five. Do not add the unsquared lengths. This identity concerns squares. If the lost square is one half, the kept square is four and one half. Now add this reasoning across the cloud.

**Learner task:** For A, the fixed total is 5. If the squared gap is 0.5, how much is kept?

## 9. Keeping more means losing less.
`total` · Chapter 2

**Question:** Does the whole cloud obey the same rule?

[Reveal the sum, then rearrange.] Every point has its own right triangle. Add the original totals, the retained squares, and the lost squares. The data stay fixed while we choose a ruler, so the total on the left is constant. Loss is therefore a constant minus retained squared length. Maximizing the retained term minimizes the loss. This earns the spread objective from the original reconstruction problem. It does not declare spread useful for all tasks. Before calling the retained term variance, we must verify that the scores are centered.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 10. Centered points give centered scores.
`score-mean` · Chapter 2

**Question:** Why measure spread from zero?

[Reveal the averaging step.] Variance measures spread about a mean, not distance from an arbitrary zero. The same direction weights apply to every point. We can therefore take the direction outside the average. The average score equals the direction dotted with the average centered vector, which is zero. This is a small but essential link. Squared score energy now measures spread rather than location. If we used raw points without centering, the energy could be large simply because the cloud sits far from the origin. Our geometry would solve a different problem.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 11. Variance gives spread a scale.
`variance` · Chapter 2

**Question:** Why squares, and why n − 1?

[Reveal the scores at forty-five degrees.] Two scores are positive and two negative. Adding them gives zero, even though the points are spread out. Their squared scores sum to eighteen. Divide by three to get sample variance six, in square centimetres. The n minus one convention compensates for estimating a mean in the usual sample variance estimator. That statistical motivation is separate from our optimization: division by n instead would scale every candidate equally. Keep the convention consistent so covariance eigenvalues, singular values, and reconstruction losses agree.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 12. A longer arrow is a fake win.
`unit` · Chapter 2

**Question:** Why constrain the direction length?

[Reveal w and then two w.] Without a length constraint, we can inflate the objective without changing the line. Whenever variance is positive, make the vector longer and the dot-product scores grow without bound. Our decoder formula assumed a unit vector, so each score was a distance. With a nonunit vector, a correct projection coefficient would require division by its squared length. We keep the geometry simple by fixing the squared length to one. This constraint is why our optimization will move around a circle or sphere instead of through all vectors freely.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 13. Find a good line before the formula.
`seek` · Chapter 2

**Question:** Can you explain why it wins?

[Start at twenty degrees.] Predict which way the ruler should turn before you move it. Increase the kept part while shrinking the lost part. Then compare your choice with the computed optimum. Explain why the two goals agree for the same centered dataset. Do not rely only on the phrase “the dots line up.” Name the fixed total and the changing split. In two dimensions, a slider is useful. In a thousand dimensions, it is not a practical solver. We need a compact data summary and an algebraic rule. The squared-score formula tells us what summary to build.

**Learner task:** Complete: “This line loses less because the total is fixed and …”

## 14. Decode a point you have not seen.
`new-point` · Chapter 2

**Question:** Can you run the saved rule yourself?

[Pause before revealing each result.] Subtract the saved mean to get three, zero. Dot that offset with the learned direction to get three over square root two. Multiply back to obtain one point five, one point five. Add the mean and recover seven point five, seven point five. This is a new observation, but the coordinate system is the one we already fitted. Recomputing a separate mean for this single point would erase its offset. Later, we will extend this rule to honest validation: fit preprocessing and PCA only on training data, then freeze them for evaluation.

**Learner task:** Write all three results before revealing them.

## 15. Most spread is not always most useful.
`boundary` · Chapter 2

**Question:** Useful for which task?

[Read the scenario before revealing feedback.] Suppose large sensor variation is harmless drift, while a tiny second signal marks a fault. One-component PCA may retain the drift. It can be optimal for input reconstruction and poor for fault detection at the same time. There is no contradiction: the tasks reward different things. Keep this boundary in mind throughout the proof. A theorem helps most when we know exactly what it promises. After the derivation, we will build this counterexample and compare alternatives. For now, reject the idea that retained variance is a percentage of all useful information.

**Learner task:** A small-variance direction perfectly identifies faults. What does retaining 95% variance guarantee?

## 16. Square the score. Keep every term.
`square` · Chapter 3

**Question:** Where does covariance come from?

[Reveal the product, then distribute.] Multiply the sum by itself. Each term in the first factor multiplies each term in the second, giving four products. The two mixed products are equal, so they combine with a factor of two. Omitting them loses the cloud tilt. This is why covariance appears. We are not inserting a matrix because a recipe says so. Our reconstruction objective led to squared scores, and their expansion asks for products of different coordinates. Next we collect those products across observations and see what their signs mean.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 17. Signed products remember the tilt.
`products` · Chapter 3

**Question:** What does each point contribute?

[Select A before revealing its product.] A is two east and one north of the mean, so the product is positive two. A point below and left has two negative offsets; its product is positive too. Both support a positive tilt. [Flip the tilt.] Separate squared columns remain unchanged, but the mixed products change sign. Covariance detects the change that the marginal variances miss. Zero covariance does not prove no relationship: positive and negative products can cancel. We will later test that boundary with a curved, deterministic relationship.

**Learner task:** Predict a product sign. Flip the cloud and explain what stays unchanged.

## 18. Three numbers summarize our objective.
`cov-matrix` · Chapter 3

**Question:** How should we organize these products?

[Reveal the data sums.] East squares are four, one, one, four. North squares reverse that order. Both sums are ten. Every mixed product is two, so that sum is eight. Divide by three. The off-diagonal entries match because x times y equals y times x. We can now evaluate any direction from three numbers. This is a useful summary, not a complete description of the cloud. Different datasets may have identical covariance. Later, nonlinearity and outliers will expose facts that these second-order numbers cannot resolve by themselves.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 19. wᵀSw is the sum we already know.
`quadratic` · Chapter 3

**Question:** What does the matrix product do?

[Reveal S times w.] Each matrix row makes a weighted sum. Dot the resulting vector with w and expand again. The two diagonal terms use squared weights. Symmetry combines the two cross terms. That expression matches the squared-score expansion after averaging over the data. If the compact notation feels opaque, return to the three terms rather than memorizing a symbol chain. Check the shapes too: row direction, square covariance, column direction. Their product is a scalar, as variance must be. Now we can evaluate every direction without rereading every observation.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 20. One point contributes one small matrix.
`outer` · Chapter 3

**Question:** How do we extend this to many features?

[Reveal A’s outer product.] Multiplying its column by its row produces four coordinate pairs. This is different from the dot product: row times column would yield the scalar squared length. Add these outer products across observations and every feature pair has its required sum. With d features, the result is d by d. Multiplying on the left and right by a direction extracts the average squared score. This generalizes the two-coordinate calculation without inventing a new objective. The matrix is simply a compact store of the products that squared projection needs.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 21. A misplaced line adds error.
`mean-proof` · Chapter 3

**Question:** Why is a line through the mean sufficient?

[Reveal the error split.] P maps x to w(w transpose x), the perpendicular projection we already derived. Let a be an arbitrary anchor. Write each raw point as mean plus centered point. The sideways error splits into a centered part and a shared offset. Squaring and summing gives a cross term, but it vanishes because centered points sum to zero. The extra term is n times a squared length, so it cannot improve the loss. Choosing the mean removes it. Moving the anchor along the same line changes no line, so the anchor is not unique.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 22. Rows are observations. Columns are features.
`data-matrix` · Chapter 3

**Question:** Why does XᵀX appear in code?

[Trace the upper-right product.] The first feature column contains east offsets; the second contains north offsets. Their dot product is the upper-right entry of X transpose X. It sums the paired products over observations and gives eight. Each diagonal pairs a column with itself, giving a sum of squares. We use rows for observations in code. When writing a single x i in the derivation, we treat it as a column. Stating that convention prevents transpose mistakes. All scores at once form X w, one score per observation.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 23. Two properties make the proof possible.
`psd` · Chapter 3

**Question:** What is special about covariance?

[Reveal symmetry, then nonnegativity.] Covariance is symmetric because opposite entries contain the same products. Positive semidefinite has a concrete meaning: no direction has negative variance. The sum-of-squares expression proves it. Negative covariance is still allowed; it records opposite signs occurring together. These properties will let us invoke a theorem for real symmetric matrices. The theorem provides real eigenvalues and a perpendicular eigenbasis. Nonnegative quadratic forms make covariance eigenvalues nonnegative. We will derive why those eigenvalues are exactly the variances of special directions.

**Learner task:** Can covariance have negative off-diagonal entries? Explain why this does not give negative variance.

## 24. State the problem we have earned.
`objective` · Chapter 3

**Question:** Which unit direction loses least?

[Read the optimization in ordinary words.] Among all unit directions, choose the one with the largest projected sample variance. S is fixed; w is our choice. Unit length prevents artificial score inflation. Pythagoras connected maximum variance to minimum reconstruction loss. Rebuild that chain without formulas: choose a ruler, send distances, recover points, add squared gaps, and retain as much of a fixed total as possible. The trace is the sum of feature variances, which supplies that fixed total. Next we turn the direction slightly to discover the equation an optimum must satisfy.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 25. A sideways push means we can improve.
`tangent` · Chapter 4

**Question:** Where could an optimum occur?

[Start at twenty degrees.] We may turn the ruler but cannot lengthen it. The tangent points along a small legal turn. Twice its dot product with Sw gives the rate of variance change per radian. Positive means turn one way; negative means the other. At a stationary direction, this sideways change is zero. In a plane, Sw must then be parallel to w. In more dimensions, it must have zero component along every tangent. This geometric condition is why eigenvectors appear. The calculus will express this same restriction, not replace the picture with an unrelated trick.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 26. Expand one small change.
`gradient` · Chapter 4

**Question:** Why is the gradient 2Sw?

[Reveal the perturbation expansion.] Substitute w plus epsilon h into both copies of the direction. Distribute the products. Symmetry makes the two first-order cross terms equal. The epsilon-squared term vanishes faster than epsilon as epsilon approaches zero. The first-order rate is therefore twice h transpose S w. The gradient is the vector that dots with h to give this rate, so it is two S w. A first-order motion on the unit sphere has h transpose w equal to zero. At stationarity, every such legal tangent must have zero first-order gain.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 27. Enforce the constraint in one equation.
`lagrange` · Chapter 4

**Question:** How does the unit sphere become algebra?

[Reveal the Lagrangian.] Lambda is an unknown multiplier that lets the objective gradient align with the constraint gradient. The gradient of squared length is two w. Set their difference to zero and cancel two. The result is S w equals lambda w, the same parallel-vector condition we saw geometrically. Lambda is solved with w; it is not a tuning knob. The constraint gradient is nonzero on the unit sphere, so this necessary condition applies to a smooth constrained optimum. Necessary matters: some solutions will be minima. We will explicitly reject that trap.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 28. The eigenvalue is the variance.
`eigenvalue` · Chapter 4

**Question:** What do the new names mean?

[Read the matrix equation as a geometric action.] Multiplying by S may turn a general vector. An eigenvector stays on its own line. Multiply the equation on the left by w transpose. The left side becomes our variance objective. The right becomes lambda times squared length, which is one. Therefore lambda equals the projected sample variance. Our toy covariance scales the long diagonal by six and the short diagonal by two thirds. Both are legitimate eigenvectors. Naming them has not yet proved which one is the best representation. The next contrast makes that distinction visible.

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 29. The worst line passes that test too.
`stationary-trap` · Chapter 4

**Question:** Does zero turning rate prove a maximum?

[Choose forty-five degrees, then one hundred thirty-five.] At both positions, the derivative is zero and Sw is parallel to w. Yet one is the best line and the other the worst in this plane. A zero slope can mark a maximum, a minimum, or another stationary point in a more general problem. We need a bound that applies to every unit direction, not just candidates. Choosing the largest eigenvalue feels plausible. The next steps prove it by expressing every direction in a basis the covariance matrix preserves.

**Learner task:** What does a zero tangent derivative justify?

## 30. Use a basis the matrix preserves.
`spectral` · Chapter 4

**Question:** Can we compare every direction at once?

[Reveal the basis properties.] A basis can build every vector from its directions. Orthonormal means those directions are perpendicular and have unit length. The finite-dimensional spectral theorem supplies an eigenbasis with these properties for a real symmetric matrix. This is an explicitly invoked foundation, not something proved by an ellipse drawing. Expand any candidate w in that basis. The matrix scales each basis vector by its eigenvalue. Unit length says the squared coefficients sum to one. We now have a way to compare every possible direction through its coefficients.

**Learner task:** Predict the next operation and explain its reason before revealing it.

[Primary reference](https://www.cs.cornell.edu/courses/cs6210/2025fa/lec/2025-11-03.html)

## 31. Why do mixed terms disappear?
`cross-vanish` · Chapter 4

**Question:** Perpendicularity alone is not enough.

[Reveal the mixed entry before the sum.] A general matrix can mix a perpendicular basis. We specifically need an eigenbasis. Apply S to q j and replace it with lambda j q j. Now dot with q i. The result is zero when the indices differ, and lambda j when they match. Expand both copies of w in the quadratic form. Every mixed pair vanishes for this reason, leaving the diagonal sum. This is the exact algebraic bridge to the weighted-average proof. It should not be skipped behind the phrase “by orthogonality.”

**Learner task:** Predict the next operation and explain its reason before revealing it.

## 32. No mixture beats the best ingredient.
`global` · Chapter 4

**Question:** Why is the largest eigenvalue globally best?

[Put all squared weight on the first direction, then move some away.] With unequal eigenvalues, assigning weight to the smaller one lowers the average. In any dimension, each eigenvalue is at most lambda one. Replacing all of them by lambda one cannot decrease the sum. The weights sum to one, leaving lambda one as an upper bound. The first eigenvector reaches it. Equality also holds for any unit direction entirely inside a tied largest eigenspace. This compares every candidate direction, not just a finite slider search. We now have the promised global proof.

**Learner task:** Explain the bound without referring to the slider.

## 33. Sometimes several answers are right.
`ties` · Chapter 4

**Question:** Is the best direction unique?

[Toggle equal eigenvalues.] Every mixture now has the same variance. No line in this plane is preferred by our objective. With a strict top eigenvalue, the leading line is unique, but its arrow sign is still arbitrary. Replace w by minus w and every score also changes sign, leaving their product unchanged. Near ties are different from exact ties: small perturbations may rotate axes strongly. For a multi-direction representation, stability depends on separation at the retained boundary. Later we will distinguish an unstable individual axis from a stable retained subspace.

**Learner task:** If software flips all PC1 score signs, which reconstructed points change?

## 34. Return to the opening ruler.
`opening-payoff` · Chapter 4

**Question:** Did the proof recover our geometric guess?

[Reveal each matrix multiplication.] The long diagonal is scaled by six; the short by two thirds. Normalize both to unit length. Their eigenvalues sum to twenty thirds, the total variance and trace. Six divided by twenty thirds is ninety percent. The remaining two thirds is the normalized reconstruction error. These numbers are the same kept and lost pieces we saw in the opening. We can now draw, calculate, and justify the answer. Ninety percent is about this metric and sample, not ninety percent of all information or ninety percent prediction accuracy. Next, keep more than one direction.

**Learner task:** Explain why “90% of variance” is not “90% of everything useful.”

## 35. The next coordinate must add something.
`more-pc2` · Chapter 5

**Question:** Why must the second direction be perpendicular to the first?

[Point back to the first reconstructed point.] One coordinate has already used the leading direction. A second copy would not recover the sideways detail. That is why we restrict the next search to the perpendicular space. Project a residual onto a direction in that space: the removed first-component part contributes zero. We can therefore reuse the covariance objective with one new constraint. Expand the candidate in the same eigenbasis. Its first coefficient must vanish, so the largest available eigenvalue is now the second. If eigenvalues tie, choose an orthonormal set within the tied eigenspace.

**Learner task:** If we removed the perpendicular constraint, which direction would the maximization choose again? Explain why that would not add a second coordinate.

## 36. Encode k numbers and recover d features.
`more-frame-shapes` · Chapter 5

**Question:** Which matrix stores the shared directions?

[Trace row A through the displayed four-by-two example.] Two measured offsets become one score on the first direction. Select another row and observe the score change. Then keep both directions and count the two resulting scores. The decoder combines the shared directions with those scores and restores the center. Now generalize to the separate exercise with eight features and three scores. Shapes tell us which dimensions must match. Keeping three coordinates is not simply choosing three original columns: each direction can combine all eight features. The shared directions and mean must also be stored.

**Learner task:** For 100 observations, 8 features, and k = 3, give the shapes of X, W, Z, and the decoded matrix. Which objects must be retained to decode a future score vector?

## 37. What changes in the score covariance?
`more-score-covariance` · Chapter 5

**Question:** Does a diagonal covariance mean independent coordinates?

[Read the matrix dimensions before multiplying.] Each score is a new column, so its covariance is built in exactly the same way as the original covariance. The eigenvector relation supplies the diagonal entries; orthonormality removes the cross terms. Now test an overstatement of that result. The parabola example has zero covariance, but knowing the first coordinate fixes the second. Ask the learner to predict that second coordinate before naming dependence. PCA removes this linear summary of dependence. It does not turn arbitrary data into independent sources, and it does not by itself identify causes.

**Learner task:** Let A be equally likely to be −2, −1, 0, 1, or 2, and let B = A² − 2. Their covariance is zero. If A = 0, what must B be? Does knowing A tell us nothing about B?

## 38. The decoder is an orthogonal projector.
`more-projector` · Chapter 5

**Question:** Why does projecting twice change nothing?

[Return to a point that already lies on the retained plane.] Projecting it again leaves it where it is. That geometric fact is idempotence. The algebra verifies it using the orthonormal columns of W. Symmetry then lets us show that the recovered part has zero dot product with the residual. This is the same right triangle from the one-line case, now in any dimension. Summing its squared lengths gives the matrix error identity. The Frobenius norm is simply the square root of the sum of squared entries. No new kind of error has been introduced.

**Learner task:** Explain P² = P without symbols. Then state which step would fail if the columns of W were not orthonormal.

## 39. Describe every possible k-dimensional choice.
`more-capacity-weights` · Chapter 5

**Question:** How much of each eigenvector can a subspace retain?

[Introduce one weight before the whole list.] Take a unit eigenvector and project it onto the candidate subspace. The squared retained length is its weight. It cannot be negative or exceed the original unit length. Now total these weights over a complete orthonormal basis. The result is the dimension of the retained subspace, k. This is a capacity constraint: each eigenvector can contribute at most one unit, and the total capacity is k. Every genuine subspace satisfies these constraints. We will use them to bound all possible choices, then exhibit a subspace that attains the bound.

**Learner task:** Why are weights b = (2, 0, 0, …) illegal for k = 2, even though they sum to two? Explain how the bound b_j ≤ 1 prevents counting the same direction twice.

## 40. No subspace can beat the top-k total.
`more-global-k-bound` · Chapter 5

**Question:** Why does the whole k-dimensional choice win globally?

[Keep the capacity picture visible beside the inequalities.] Any weight placed below the cutoff must leave the same amount of unused capacity above it. Moving that weight upward cannot lower the objective, because the upper eigenvalue is at least as large. The displayed inequalities total all those exchanges at once. This bounds every subspace, not just the directions a particular algorithm tried. Finally, choose the top eigenvectors: they form a legal orthonormal frame and attain the bound. That last construction closes the proof. A tie at the cutoff can permit several optimal subspaces; the best value remains the same.

**Learner task:** For eigenvalues (12, 5, 2, 1) and k = 2, compare weights (1, 0.5, 0.5, 0) with (1, 1, 0, 0). Where did the improvement come from? What if the two eigenvalues at the cutoff tie?

## 41. The discarded eigenvalues measure the loss.
`more-discarded-tail` · Chapter 5

**Question:** How much error does truncation leave?

[Point to the omitted end of the spectrum.] Each discarded eigenvalue is a variance contribution we no longer reconstruct. The sum gives loss divided by n minus one, because we used sample covariance. Multiply back when you want the unnormalized squared-error sum. Have the learner distinguish those two quantities before calculating a percentage. The percentage summarizes this chosen metric on the fitted data. It does not say that eighty-five percent of useful information, class separation, or future predictive accuracy survives. If all observations are identical, the total variance is zero and a retained-variance percentage is undefined.

**Learner task:** For eigenvalues (12, 5, 2, 1), five observations, and k = 2, calculate the retained fraction, normalized loss, and unnormalized squared-error sum. Which of these claims tells you fault-prediction accuracy?

## 42. Compute the same directions without forming S.
`more-svd-connection` · Chapter 5

**Question:** Where does singular value decomposition enter?

[State that the existence of this factorization is a theorem we are invoking.] We are not proving the SVD algorithm in this course. We are proving why its output solves our PCA problem. Substitute the factorization into X transpose X and cancel the orthogonal middle factor. The remaining expression is a covariance eigendecomposition. That identifies both the directions and their variances. Keep the orientation visible: our observations are rows, so V lives in feature space. A source using transposed data can name the other factor instead. Direct SVD also avoids explicitly forming the covariance matrix.

**Learner task:** Why would taking the left singular vectors as feature directions be a shape error here? What changes if the data matrix has features in rows instead?

[Primary reference](https://arxiv.org/pdf/1404.1100)

## 43. The scores are already inside the factorization.
`more-svd-scores` · Chapter 5

**Question:** Why do U and Σ appear together?

[Trace the retained columns with the same indices in all three factors.] The scores are not U alone. Its columns have unit length; the singular values restore how much variation each score column carries. Multiplying the centered data by the retained feature directions gives exactly U times those singular values. Decoding then uses the same feature directions again. Ask the learner what forgetting the scale would do to the score covariance. Finally, flip one direction and its score together. Their outer product stays unchanged. This explains why two valid numerical runs can differ in signs without disagreeing about reconstructed data.

**Learner task:** A program returns U[:, :k] as PCA scores but forgets the singular values. What changes? Explain why multiplying both a direction and its corresponding score by −1 preserves the reconstruction.

## 44. Centering limits how many directions can vary.
`more-centered-rank` · Chapter 5

**Question:** Can ten observations support ten nonzero centered components?

[Point to one centered feature column and sum its entries.] Its entries must cancel. Every feature column therefore lives perpendicular to the same all-ones vector, which removes one possible observation-space dimension. There can also be no more independent columns than the number of features. Those two facts give the rank bound. The singular-value and covariance views agree because their zero directions have the same null-space condition. Ask whether the upper bound must be reached. Repeated observations or dependent features can lower the actual rank. Keep this fitted-data statement separate from assumptions about what future observations may do.

**Learner task:** With n = 10 and d = 100, how many covariance eigenvalues can be nonzero? If only three features vary independently, is that upper bound necessarily attained?

## 45. Read the code as the argument.
`more-numpy-meaning` · Chapter 5

**Question:** Which line stores the mean, directions, scores, and reconstruction?

[Let the learner write the operations before opening the example.] The code is short because the library supplies a numerical factorization, not because the reasoning disappeared. Ask what each returned array means before slicing it. NumPy calls its third output Vt: the transpose is part of the return convention. The retained rows therefore become our direction columns after another transpose. Check the score identity using U and the singular values, and check the residual tail independently. Small floating-point differences need a suitable tolerance. For new data, reuse the learned mean and directions. Refitting would define a different representation.

**Learner task:** Before revealing the code, write these six operations yourself. Then annotate every array shape for n = 100, d = 8, k = 3. For a new observation, which fitted quantities are reused? Propose a check that could reveal a mistaken transpose or missing mean.

[Primary reference](https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html)

## 46. Reconstruct the whole multi-coordinate chain.
`more-chain-reconstruction` · Chapter 5

**Question:** Can you justify the result without calling an eigensolver?

[Hide earlier equations for the first attempt.] This is the chapter's reconstruction check. The learner should explain why the constraints exist, not only repeat the final top-two rule. If they claim to store the leading direction twice, return to the projector weights. If they know the bound but cannot attain it, ask for an actual legal W. If they recite SVD letters, ask which dimension contains observations and which contains features. Give targeted help, then ask for a changed spectrum. Record supported and unsupported steps honestly. A correct answer after hints is useful progress, but it is not the same evidence as an unaided reconstruction.

**Learner task:** Start with a blank response. Why can a candidate not allocate weight two to the first eigenvector? Why can no subspace capture more than 17? What proves that 17 is attainable? How does SVD return the same choice? Finish with one limit of this guarantee.

## 47. Choose what an error costs.
`practice-metric` · Chapter 6

**Question:** Best reconstruction of which quantities?

[Return to the two position coordinates.] The proof gave us a strong result, but it fixed what counted as an error. A centimetre east and a centimetre north had equal cost. That was sensible for reconstructing positions. [Point to the three choices.] Now make the decision before fitting anything. For this stated task, keep the original distance measure. A different task could justify different weights. PCA will still optimize the chosen measure; it cannot decide whether that measure reflects our purpose. [Pause for a reason, then reveal feedback.] The next experiment changes only a unit label and its numbers. Watch how that can change the answer.

**Learner task:** Two position coordinates use centimetres, and equal position errors matter equally. Which starting metric fits this task?

[Primary reference](https://stat.cmu.edu/~cshalizi/dm/19/lectures/05/lecture-05.html)

## 48. A unit change can turn the ruler.
`practice-units` · Chapter 6

**Question:** Did the data change, or did our distance rule change?

[Start with both coordinates in the same unit.] These are the same observations we already understand. Predict the effect before moving the scale control. [Multiply the first coordinate by one hundred.] We have stretched one numerical axis. A gap of one on that axis now appears as one hundred, and its square appears as ten thousand. The optimizer responds to that new weighting. It has not learned a new physical fact. [Restore the scale.] Converting both coordinates consistently would preserve directions in the corresponding physical geometry. Mixing units requires an explicit correction or a chosen weighting. Centering alone cannot do that job.

**Learner task:** Convert east from metres to centimetres but leave north in metres. What should you expect from unadjusted covariance PCA?

[Primary reference](https://www.cs.cmu.edu/~11755/lectures/pca.pdf)

## 49. Standardization changes the question.
`practice-standardize` · Chapter 6

**Question:** Should one standard deviation count equally?

[Compare the original-scale and standardized views.] Standardization gives each feature the same training variance. A change of one now means one standard deviation of that feature. This can be useful when metres, seconds, and counts appear together. It is still a choice about distance. [Point to the noisy feature in the prompt.] A small scale does not tell us that a feature deserves more trust. Dividing by that scale can make its noise matter more. A constant feature needs separate handling because its standard deviation is zero. [Pause for the choice.] Keep the means and scales: future observations must use the same conversion.

**Learner task:** A tiny-variance sensor contains mostly measurement noise. Does scaling it to unit variance guarantee a better representation?

[Primary reference](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)

## 50. Translate the loss back into original units.
`practice-weighted-loss` · Chapter 6

**Question:** What did standardized PCA actually minimize?

[Point to one denominator at a time.] The scale is part of the loss. If a feature's scale is ten, a raw error of ten becomes an error of one in the standardized space. A raw error of one in a feature whose scale is one has the same cost. [Ask the learner to compare the two contributions.] Undoing the units after reconstruction does not undo the objective used to choose the subspace. This is why two correct PCA runs can produce different reconstructions. They may be optimizing different distances. [Return to the task statement.] Report the scaling choice beside any claim that the answer is best.

**Learner task:** A feature has scale 10 and another has scale 1. Under this loss, which raw error contributes equally to an error of 1 in the second feature?

[Primary reference](https://stat.cmu.edu/~cshalizi/dm/19/lectures/05/lecture-05.html)

## 51. Whitening changes score scale.
`practice-whiten` · Chapter 6

**Question:** What if a later method wants equal score variances?

[Compare the component variances before and after whitening.] Rotation removed cross-covariances. It did not make the spreads equal. Whitening adds a division by each retained standard deviation. [Trace one score through that division.] The direction with less variance receives a larger multiplier. That can suit a later method's assumptions, but it can also increase the influence of weak or noisy directions. A zero eigenvalue cannot be handled by this ordinary division. If you store the positive scale factors, you can reverse the rescaling before decoding. Dropped components remain lost. [Pause.] Name centering, rotation, truncation, and whitening as four different operations.

**Learner task:** Which operation is whitening?

[Primary reference](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)

## 52. Choose k from an error budget.
`practice-budget` · Chapter 6

**Question:** How much squared variation may we discard?

[Read the three eigenvalues as a budget.] We have ten units of total variance. Keeping the first component keeps eight and leaves two. Keeping the first two keeps nine and leaves one. [Pause for the smallest acceptable choice.] This is a precise use of explained variance: it controls reconstruction loss on these data in this metric. It does not tell us what a missed feature means. An elbow in a larger spectrum can suggest a useful cutoff, but it is a heuristic. The acceptable error still comes from the task. [Point ahead to validation.] We also need to learn whether the chosen representation works on new observations.

**Learner task:** Eigenvalues are 8, 1, 1. What is the smallest k that retains at least 90% of total variance?

[Primary reference](https://stat.cmu.edu/~cshalizi/dm/19/lectures/05/lecture-05.html)

## 53. Test the purpose, not just the spectrum.
`practice-validation` · Chapter 6

**Question:** Which validation score should choose k?

[Point to the task before reading either curve.] Suppose our goal is to predict a fault. The best reconstruction count may not give the best fault prediction. We must fit the full candidate pipeline on training data and compare its predictions on validation data. [Pause for the choice.] If the goal is compression instead, compare reconstruction with the cost of storing more scores. Keeping more directions cannot worsen projection error for a fixed nested basis, so error alone does not reward a shorter description. Choose an acceptable error or a storage tradeoff. Reserve separate test data for the final assessment after these choices are complete.

**Learner task:** You need accurate fault prediction from a short representation. Which evidence should guide k?

[Primary reference](https://scikit-learn.org/stable/auto_examples/cross_decomposition/plot_pcr_vs_pls.html)

## 54. Split before learning the representation.
`practice-pipeline` · Chapter 6

**Question:** Can an unsupervised step leak test information?

[Trace the arrows from training data to fitted transformations.] PCA learns from feature values even when it never reads a target. If test observations help determine the mean or direction, the representation has already seen part of the test distribution. [Point to the separate transform arrow.] A pipeline keeps the distinction clear: fit on training data, then apply the stored rule elsewhere. Repeat that fitting inside each training fold when comparing settings. Do not recompute the test mean just because the test table looks shifted. [Pause for the diagnostic choice.] That shift may be exactly the difficulty the final evaluation needs to reveal.

**Learner task:** PCA uses no target labels. May we fit it on all rows before a prediction benchmark?

[Primary reference](https://scikit-learn.org/stable/common_pitfalls.html)

## 55. Give tomorrow the same ruler.
`practice-frozen-transform` · Chapter 6

**Question:** How do we score one new observation?

[Follow one new row through the displayed formula.] The stored mean marks the origin of the training coordinate system. Subtract it, then project onto the stored directions. This formula shows the unscaled case; if the model used feature scaling, apply its stored scales before projection. [Pause at the self-centering choice.] A single observation centered on itself becomes zero. It has lost the very differences we meant to describe. Decode a score using the same directions, undo any scaling, and restore the training mean. Save the feature names and their order too. A correct matrix multiplied by shuffled columns answers a different question.

**Learner task:** For the unscaled formula shown, what happens if we center each new observation on itself?

[Primary reference](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)

## 56. Compute the same answer through SVD.
`practice-svd` · Chapter 6

**Question:** Must code build the covariance matrix?

[Point to the dimensions of X, then to V.] We have already proved the optimization result. SVD is another route to the same directions. With observations in rows, the right singular vectors live in feature space. Multiplying X by them produces the component scores. [Trace the variance formula.] Squaring each singular value and dividing by n minus one gives the sample variance in that direction. Forming covariance can be convenient when features are few, but direct SVD avoids its full feature-by-feature storage. Solver choice is a computational decision. Check numerical accuracy and resource use for the actual matrix, rather than treating one implementation path as the definition of PCA.

**Learner task:** Rows are observations and columns are features. Which SVD vectors are the feature-space principal directions?

[Primary reference](https://www.cs.cmu.edu/~11755/lectures/pca.pdf)

## 57. A sparse table needs a storage plan.
`practice-sparse` · Chapter 6

**Question:** What happens when we subtract a dense mean?

[Point to a stored zero in a sparse matrix.] A zero is cheap to store because we can omit it. Subtract a nonzero column mean and that entry is no longer zero. Explicit centering can therefore make a large sparse problem expensive. Some solvers handle centering without materializing every entry; another option is uncentered truncated SVD. [Pause at the comparison.] That second option preserves a different quantity: variation about the origin includes the mean structure. It can be useful, but we must name the change. Inspect memory, centering support, and the intended task before choosing an algorithm just because its name contains SVD.

**Learner task:** You replace centered PCA with uncentered truncated SVD. Which statement is safe?

[Primary reference](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html)

## 58. Check identities with a purpose.
`practice-checks` · Chapter 6

**Question:** What would reveal an implementation mistake?

[Read each check as a question about the objects.] Did we center the right axis? Are our retained directions unit length and perpendicular? Do score variances match the selected eigenvalues? Does the retained-plus-residual accounting still hold? These checks can expose a transpose, scaling, or indexing error. [Show the sign diagnostic.] A reversed direction is not automatically wrong: the score reverses too, and their product stays the same. Tied eigenvalues require comparing subspaces rather than demanding identical columns. Use tolerances for floating-point arithmetic. A successful numerical check supports this implementation on the tested cases; the general guarantee still comes from the argument we proved.

**Learner task:** Two solvers return opposite signs for one isolated principal direction. Their reconstructions agree. Is that a failure?

[Primary reference](https://www.cs.cmu.edu/~11755/lectures/pca.pdf)

## 59. The small direction may hold the answer.
`limits-small-signal` · Chapter 7

**Question:** Can excellent reconstruction lose a useful distinction?

[Show the elongated cloud before revealing its labels.] The long horizontal direction is an excellent description of where the points lie. Now reveal a fault label that changes only with the small vertical displacement. [Compare points that share a horizontal score.] The projection merges cases that the prediction task needs to separate. Nothing failed in the eigenvalue calculation. PCA solved the stated reconstruction problem. The problem was treating that guarantee as a prediction guarantee. [Pause for the choice.] Diagnose this by evaluating the later task on held-out data and by inspecting what changes in the discarded directions. The remedy may be a larger k or a different method.

**Learner task:** The fault label depends only on the small vertical coordinate. What can horizontal one-component PCA guarantee?

[Primary reference](https://scikit-learn.org/stable/auto_examples/cross_decomposition/plot_pcr_vs_pls.html)

## 60. Let the target influence the choice.
`limits-supervised` · Chapter 7

**Question:** Which alternative answers a prediction question?

[Return to the lost vertical distinction.] First try the simplest repair: retain enough components to keep it. The cost is a larger representation. A model on the original features is another important baseline. Supervised dimension reduction can use the target while forming its directions, which addresses a different objective from PCA. [Pause at the three proposed responses.] None of these names promises the winner on new data. Fit each full pipeline fairly, select settings using validation data, and assess the chosen process on untouched test data. The previous scene showed why a method can fail. This comparison supplies evidence for which remedy helps this task.

**Learner task:** What is a fair response to the small-signal failure?

[Primary reference](https://scikit-learn.org/stable/modules/generated/sklearn.cross_decomposition.PLSRegression.html)

## 61. One distant point can steer the line.
`limits-outlier` · Chapter 7

**Question:** Why does squared loss make this happen?

[Start with the clean cloud, then move one point outward.] Its squared distance grows faster than its distance. The covariance sums include those large squares and products, so this point can acquire great influence over the direction. [Compare the fit before and after the move.] That is a mechanism we can inspect. It does not tell us whether the point is wrong. A sensor error may need correction; a rare but real event may be the most important observation in the task. Check provenance and compare sensitivity. [Pause for the diagnostic choice.] A robust method changes how unusual observations affect the result, and that change also needs justification.

**Learner task:** A distant point rotates the first component. What should happen before removing it?

[Primary reference](https://arxiv.org/pdf/0912.3599)

## 62. A robust model adds assumptions.
`limits-robust` · Chapter 7

**Question:** What kind of corruption do we think occurred?

[Point to the two terms in the proposed split.] A low-rank-plus-sparse model says most structured variation is shared across dimensions while a limited set of entries is corrupted. That is one specific model, not a general definition of every robust PCA method. [Use the one-entry matrix in the prompt.] It is sparse and also rank one. Without more assumptions, the split cannot be unique. Recovery results impose conditions on structure and corruption. In practice, compare the repaired representation with known measurement behavior and the task. Suppressing a real rare event can be costly. A more resistant fit is useful only when its assumptions suit what went wrong.

**Learner task:** A matrix has one nonzero entry. Can its values alone uniquely tell us whether it belongs to L or S?

[Primary reference](https://arxiv.org/pdf/0912.3599)

## 63. A curved path is not a straight subspace.
`limits-curve` · Chapter 7

**Question:** Can one latent quantity still defeat one-component PCA?

[Trace a point around the curve.] One changing angle locates it on the circle, but that coordinate is nonlinear in the displayed axes. Project the circle onto a horizontal line and two different positions can share a score. Rotate the line and the same issue remains. [Ask the learner to identify a colliding pair.] This does not contradict our proof: the proof compared straight subspaces, not all possible descriptions. Structured reconstruction residuals can reveal that a line misses curvature. Keeping both original coordinates preserves the circle, but gives up the one-number compression. A nonlinear method may fit the structure better, provided we test the new objective and its assumptions.

**Learner task:** Two points on a circle have the same horizontal coordinate. Can that single score always recover which point we meant?

[Primary reference](https://www.cs.cmu.edu/~11755/lectures/pca.pdf)

## 64. A better picture may solve another problem.
`limits-nonlinear` · Chapter 7

**Question:** What does the nonlinear method preserve?

[Compare the intended linear and nonlinear representations.] Different methods preserve different relationships. A neighborhood method may emphasize nearby points; its settings can change how tightly the display packs them. Kernel PCA performs PCA in a chosen feature space, and returning to the original coordinates is a separate problem. An autoencoder learns an encoder and decoder with its own training choices. [Pause at the islands question.] Judge the result against the task: reconstruction, prediction, neighborhood preservation, or exploration. Vary important settings and test new data. A visually pleasing map is useful evidence for investigation, but it is not a substitute for validating the interpretation.

**Learner task:** Changing an embedding setting creates clearer islands. What should you conclude first?

[Primary reference](https://umap-learn.readthedocs.io/en/latest/parameters.html)

## 65. An axis can wobble while a plane stays useful.
`limits-stability` · Chapter 7

**Question:** What changes when eigenvalues nearly tie?

[Make the two displayed eigenvalues equal.] Moving weight between these directions no longer changes the variance. There is no unique best line in this plane. Now imagine the two values are merely close: small changes in observations can change which axis comes first. [Read the three-eigenvalue example.] The leading plane can still be well separated from the third direction. That distinction matters when people give individual components strong names. Compare subspaces, spectra, and resampled fits, not only vector signs. For time-dependent data, use resampling or validation that respects time. Stability supports an interpretation; it does not turn a descriptive axis into a cause.

**Learner task:** Eigenvalues are 5, 5, 1. Two runs choose different first axes inside the same leading plane. Is that necessarily an error?

[Primary reference](https://ocw.mit.edu/courses/18-642-topics-in-mathematics-with-applications-in-finance-fall-2024/1W7E-UsRG0zyYe1J1vHunh3QNejR5wd7v_transcript.pdf)

## 66. Counting a feature twice gives it more weight.
`limits-duplicate` · Chapter 7

**Question:** Does a larger table contain more evidence?

[Point to one column, then its copies.] These copies do not add a new fact. They do add new coordinates to the squared-distance sum. An error in this measurement now appears repeatedly, so fitting it becomes more valuable to the optimizer. [Pause for the choice.] This is a subtle reason why a dominant component may describe how we built the table rather than a fundamental factor in the world. Inspect groups of related features and choose whether equal weight per column is intended. Removing copies or using domain weights can help, but each changes the target. Record that decision before interpreting the resulting components.

**Learner task:** You duplicate one standardized feature ten times. What has changed?

[Primary reference](https://stat.cmu.edu/~cshalizi/dm/19/lectures/05/lecture-05.html)

## 67. A component is not automatically a hidden cause.
`limits-latent` · Chapter 7

**Question:** What extra claim does a latent-variable model make?

[Read the descriptive claim before the causal claims.] Positive weights tell us how the score combines the measured variables. They do not identify why those variables move together. Factor analysis adds a generative model with latent factors and feature-specific Gaussian noise variances. Probabilistic PCA uses a more restricted isotropic noise model. Those models can answer additional statistical questions when their assumptions are useful. [Pause for the choice.] Neither a component name nor a successful model fit proves a cause. Even zero covariance leaves room for nonlinear dependence. Use domain evidence and explicit assumptions when moving from a compact description to an explanation of the system.

**Learner task:** PC1 has positive weights on several measures. What does PCA alone establish?

[Primary reference](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.FactorAnalysis.html)

## 68. Cells: a small component can mark a rare group.
`application-seurat` · Chapter 7

**Question:** How does a real workflow choose what to retain?

[Identify the matrix axes: cells and measured gene features.] In the Seurat tutorial, preprocessing and feature selection come before PCA. The resulting scores support later analysis; loading inspection helps explain which features contribute. The current tutorial explicitly notes rare immune subsets associated with later components and asks users to vary the retained count. [Pause at the scenario.] A low-variance direction may still matter to a question about rare cells. Inspect relevant markers, measurement quality, and sensitivity rather than choosing from an elbow alone. This is a documented workflow example, not a guarantee that any later component is biological signal. Our lesson does not reproduce or validate that biological analysis.

**Learner task:** A rare cell group appears only after retaining more components. Which response is strongest?

[Primary reference](https://satijalab.org/seurat/articles/pbmc3k_tutorial.html)

## 69. Vision features: PCA can make a representation visible.
`application-dinov2` · Chapter 7

**Question:** What produced the features, and what produced the colors?

[Trace image patches to feature vectors, then to three color coordinates.] DINOv2 supplies learned feature vectors. PCA is applied afterward to inspect their variation. The paper's qualitative example filters patches using a first component and performs another PCA on retained patches across related images. Three scores become color channels. [Pause for the diagnostic choice.] The colors can reveal useful correspondences, but they are not intrinsic semantic labels. Eigenvector signs and the fitted patch set affect them. Compare related images using a shared fitted basis if you want comparable colors. This is a documented use of PCA in modern representation analysis; we are not claiming to run the model here.

**Learner task:** What can a coherent PCA color map establish by itself?

[Primary reference](https://arxiv.org/html/2304.07193v2#S7.SS5)

## 70. Tomorrow may have a different pattern.
`application-temporal` · Chapter 7

**Question:** How do we evaluate a representation learned from history?

[Point to maturities as features and dates as observations.] A yield-change example uses comparable units, so retaining relative volatility can be meaningful. The fitted directions can describe shared shifts and contrasts across maturities. They depend on which history we include and how we weight it. [Move the evaluation boundary forward in the timeline.] Assess a fit made from the past on later observations. Inspect reconstruction, the spectrum, and the task's actual loss as conditions change. A longer window supplies more observations but may mix different regimes; a shorter window can be noisier. This is a statistical workflow example, not a claim about current markets or a trading recommendation.

**Learner task:** You will fit on past observations and apply the model to future ones. Which evaluation best matches that use?

[Primary reference](https://ocw.mit.edu/courses/18-642-topics-in-mathematics-with-applications-in-finance-fall-2024/1W7E-UsRG0zyYe1J1vHunh3QNejR5wd7v_transcript.pdf)

## 71. Change one point. Explain both outcomes.
`practice-live-diagnosis` · Chapter 7

**Question:** Which identity survives, and which interpretation may fail?

[Use the native notebook angle control, then move the selected point.] First verify that the displayed quantities come from the same updated dataset. For a fixed dataset, rotating the ruler changes the retained and lost parts while preserving their sum. Moving a point changes the dataset, so the total itself may change. [Pause and ask which statement still holds.] The decomposition identity remains valid. The best direction can move, and its usefulness can change. Now explain whether the moved point represents corruption or an event the task needs. Do not let a successful arithmetic check answer that separate question. Record your diagnosis and the evidence you would request next.

**Learner task:** A moved point changes the preferred line, but kept plus lost variation still equals total. What follows?

[Primary reference](https://arxiv.org/pdf/0912.3599)

## 72. Make the choice reviewable.
`practice-decision-final` · Chapter 7

**Question:** Can someone else tell what your PCA result means?

[Read the report's claim aloud, then pause.] We now have enough understanding to be precise about both its strength and its gap. Ninety-five percent can be a clear accounting statement, once the data and metric are specified. It does not by itself establish prediction, causality, or scientific meaning. [Point to purpose, evidence, and boundary.] Make your own result reviewable: describe what was measured, what was transformed, what was kept, and what was checked. Include one plausible failure and a test that could change your conclusion. The next part asks you to rebuild the explanation for another audience. Keep the mathematical guarantee and its boundary together.

**Learner task:** A report says only: 'Two PCs explain 95%, so the system is understood.' Which response is best?

[Primary reference](https://stat.cmu.edu/~cshalizi/dm/19/lectures/05/lecture-05.html)

## 73. Explain the useful idea without its name.
`transfer-ruler-explanation` · Chapter 8

**Question:** How can one reading help us recover two?

[Leave the example hidden.] This is a translation task, not a test of whether you remember the term principal component. Imagine one listener who knows what a ruler and a dot are. Tell that listener what the shorter message lets us do. [Pause for an explanation.] Now ask the follow-up about two dots landing together. If the explanation cannot answer it, add the missing lost detail. Compare your answer with the rubric, not with the wording of the example. A different clear explanation can work. This lens assumes a particular starting knowledge; it does not set a limit based on anyone's age.

**Learner task:** Write or sketch your explanation. Include what we store once, what we store for each observation, and one detail that could disappear. Then answer: if two dots land at the same place on the line, were their original readings necessarily identical?

## 74. Turn that explanation into a calculation.
`transfer-signed-score` · Chapter 8

**Question:** Can a negative direction still give a useful score?

[Point to the stored mean before the direction.] These are temperatures, so the origin of our ruler matters. Subtracting twenty from each reading measures a deviation from the learned center. The second coefficient is negative because this direction represents a contrast between the sensors. It does not mean a negative temperature is required. [Pause before revealing the answer.] Once you have a score, reverse the process: multiply by the direction and put the center back. Now reverse the arrow. The coordinate changes sign, but the recovered point does not move. Explain that cancellation in ordinary language as well as symbols.

**Learner task:** Show the centered point, score, recovered pair, and squared gap. Explain each to the listener from the previous scene. Follow-up: replacing w by −w changes which results?

## 75. Explain why this matrix belongs here.
`transfer-covariance-warrant` · Chapter 8

**Question:** Can you derive covariance from the task?

[Keep the final matrix hidden while the learner expands the square.] The two separate variances are the same as in a rising cloud, so they cannot tell us which diagonal matters. We need the products that record how the two deviations occur together. Have the learner trace one matrix entry back to the four observations. Then ask why the same matrix works for every proposed direction. The coefficients change with the ruler; the stored sums do not. The final follow-up separates a negative relationship from a negative variance. A matrix can contain negative entries while every projected variance is nonnegative. That is the meaning of positive semidefinite here.

**Learner task:** Expand the square of z = w₁u + w₂v for centered coordinates u and v. Sum over the four observations, divide by n−1, and build C. Use the sign of its off-diagonal entry to explain the useful tilt. Follow-up: is negative covariance evidence that C has a negative eigenvalue?

## 76. Rebuild the argument without the slides.
`transfer-rebuild-proof` · Chapter 8

**Question:** Why is the leading direction globally best?

[Close notes and previous equations for the first attempt.] This is a reconstruction task, so allow time to write, draw, or speak the chain before opening the example. If a step is missing, identify its job: defining the allowed ruler, measuring loss, summarizing the data, finding candidates, or ruling out every better direction. Do not repair the whole proof for the learner. Offer the smallest missing connection, then ask for a fresh attempt. Pay special attention to the stationary condition. It cannot choose the maximum by itself. Finally, translate the proof back into the original geometry. Successful symbol manipulation should still explain what is recovered and what is lost.

**Learner task:** Reconstruct the proof in your own order, but justify every arrow. Include why the direction has unit length, why centering matters for variance, why Cw = λw alone is insufficient, and when equality holds in the final bound. Then explain the same argument using the ruler and its lost sideways detail.

[Primary reference](https://www.cs.cornell.edu/courses/cs6210/2025fa/lec/2025-11-03.html)

## 77. A different answer can be equally correct.
`transfer-tied-subspace` · Chapter 8

**Question:** What is unique when eigenvalues tie?

[Ask for a reason before selecting an option.] A numerical comparison can flag two different arrays even when both solve the same problem. Here the tie sits exactly at the two-component cutoff, so the ambiguity concerns the retained subspace itself. Now change the cutoff to three. We retain the whole tied plane, and the next eigenvalue is smaller. The leading subspace is then fixed, while a basis within it can still rotate. Use the follow-up to separate those two claims. This also explains why a near tie can make individual directions sensitive to small changes. Stability of a retained subspace depends on the gap at its own boundary.

**Learner task:** Choose a conclusion, then justify it with the top-k objective. Follow-up: what changes if k = 3? State the retained and discarded variance in both cases.

## 78. Zero covariance can hide a rule.
`transfer-independent-trap` · Chapter 8

**Question:** Do uncorrelated scores have to be independent?

[Have the learner predict B when A is zero.] This one conditional question is enough to challenge the claim of independence. We do not need a complicated dependence measure. The covariance vanishes because positive and negative contributions cancel, not because the variables have nothing to do with each other. Ask the learner to explain why both statements can be true. Then return to PCA. Perpendicular directions and zero cross-covariance of the fitted scores are precise achievements. They do not identify independent causes or eliminate nonlinear relations. Keep the distinction between the finite dataset used to fit PCA and a broader population that we hope the data represents.

**Learner task:** What follows? After selecting, explain how learning A = 0 changes what we know about B. Then say exactly which dependence claim PCA can justify for its training scores.

## 79. Audit the claim behind a clean plot.
`transfer-research-claim` · Chapter 8

**Question:** What evidence would turn a pattern into a useful finding?

[Separate the numerical statement from the scientific conclusion.] A correct calculation can support a much narrower claim than its headline. Ask which data, units, preprocessing, and objective the ninety-two percent belongs to. Then inspect the evaluation timeline. Even an unsupervised transformation learns from its input, so including future evaluation data can change the representation. Finally, ask what a stable direction means. A repeated nuisance, such as instrument setting, can be very stable. The learner should propose tests that could disconfirm their preferred interpretation and say what uncertainty survives. This scene practices research judgment; it does not claim that one course supplies a complete causal-inference method.

**Learner task:** Separate what the report may have demonstrated from its unsupported claims. Propose two discriminating checks and explain what each check can and cannot establish. Follow-up: can a stable PCA axis still reflect an irrelevant nuisance?

[Primary reference](https://scikit-learn.org/stable/common_pitfalls.html)

## 80. Design a fair comparison.
`transfer-compare-objectives` · Chapter 8

**Question:** Which smaller description serves this task?

[Ask the learner to name the two decisions before naming algorithms.] A single score cannot automatically settle both compression and fault detection. First define what the archive must recover and which prediction mistakes matter. Then plan how choices will be made without looking at the final evaluation outcomes. Keep a simple baseline in the comparison; an advanced method must earn its cost. Ask for the result that would change the recommendation, because a study designed only to confirm a favored method is weak evidence. Finish with the plain-language explanation. A research-level comparison should remain connected to the operational question that motivated it.

**Learner task:** Specify the hypotheses, data split, fitted preprocessing, candidate choices, and two outcome measures. State what result would change your recommendation. Explain the comparison to a colleague who knows the sensor task but has never heard of PCA.

[Primary reference](https://scikit-learn.org/stable/auto_examples/cross_decomposition/plot_pcr_vs_pls.html)

## 81. Translate the warning without losing the idea.
`transfer-explain-back` · Chapter 8

**Question:** Can you explain why a good compression can miss a fault?

[Keep the model explanation hidden until the learner answers the follow-up.] This is the return journey from technical reasoning to ordinary language. Removing hard words is not enough: the explanation must still connect the task, the chosen rule, and the missed detail. Ask the listener's question about keeping the tiny direction instead. A strong answer does not defend PCA at all costs. It explains that different questions can need different summaries. If the learner can only say that important information was lost, ask them to draw the two fault states and show exactly where that difference goes. Then try the explanation again in their own words.

**Learner task:** Give an explanation of no more than six sentences, with a sketch if helpful. Avoid “eigenvector,” “variance,” and “dimensionality.” Include the useful part of the method and its limit. Follow-up from the listener: “Then why not always keep the tiny direction instead?”

## 82. A cutoff must answer the analysis question.
`transfer-rare-population` · Chapter 8

**Question:** Would you discard a small but useful component?

[State that this is an interpretation exercise, not a complete single-cell protocol.] The documented Seurat workflow makes component count a decision and encourages checking how later choices affect results. That is the lesson to transfer. A small component can reflect a rare population, but it can also reflect an unwanted technical effect. Ask the learner what evidence distinguishes those possibilities. Then ask why retaining everything is not automatically better. The answer should connect back to the purpose of compression and noise reduction, while acknowledging their assumptions. Do not let a visually distinct group stand in for a validated biological finding.

**Learner task:** Choose the next action and explain the evidence you would seek. Follow-up: why is keeping every later PC also not an automatic solution?

[Primary reference](https://satijalab.org/seurat/articles/pbmc3k_tutorial)

## 83. Make a plan you could actually test.
`transfer-application-plan` · Chapter 8

**Question:** Where would PCA earn a place in your workflow?

[Ask for the purpose in one sentence first.] A plan becomes testable when another person can tell what success and failure would look like. Check the data axes before the method: a transposed matrix changes what observations and directions mean. Then examine the units, because they define the error we are minimizing. Ask where each learned quantity is fitted and how the retained dimension is chosen. Finally, request one failure and a concrete response. The plan does not need to use PCA to pass this task. A well-supported decision to keep the original features can be the best outcome.

**Learner task:** Specify: purpose; rows and features; units and preprocessing; fitting/evaluation split; component-count rule; baseline; success measure; one failure diagnostic; and the next action if that diagnostic fails. Finish by explaining your choice to a teammate in three plain sentences.

[Primary reference](https://scikit-learn.org/stable/common_pitfalls.html)

## 84. Come back and rebuild it.
`transfer-return-challenge` · Chapter 8

**Question:** What can you reconstruct after the explanation is no longer fresh?

[Do not reveal the example until the learner has saved their own return prompt.] This scene sets a future challenge; it does not claim that later recall has been measured, and it does not schedule a reminder. Choose a later opportunity when the learner can begin without rereading. Ask them to mark where their reasoning stopped, not to hide that gap with familiar terminology. Reopen the relevant bridge, repair it, and then change the case so the next attempt is more than copying. End with a question the learner can now investigate responsibly. The useful result is ownership of an argument and a decision process, not a claim of universal expertise.

**Learner task:** Save a short prompt for your later self: “Why covariance? Why an eigenvector? Why the largest? Best for what?” Answer it without this course, then reopen only the bridge you could not justify. After repair, try a different dataset or explanation recipient. What question would you now investigate beyond this course?
