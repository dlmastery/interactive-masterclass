# Teaching map · PCA first

Updated 6 October 2026 from `course-v2.json`: 64 slides and 79 equation steps. Start with one-number compression and recovery error; introduce each mathematical tool when the PCA argument needs it.

The current course uses the first version’s light visual style. The original 14-slide source is preserved separately in `original-first-version/`. Open `PCA-TEACHING-PLAN.html` for the design record and current repair checks.

## What does PCA do?

### 1. Can two coordinates become one?

**Try:** Select a marker. Turn the line and compare its original position with its recovered position.

**Main idea:** PCA chooses new axes through the center of the data. With fewer coordinates, we can recover approximate positions and measure the errors.

**Equation steps:** 0

### 2. A score is a position on a ruler

**Try:** Select A, then B. Follow each marker to its position on the score ruler.

**Main idea:** One score locates a point along the chosen axis. The shared axis and center let us turn that score into a recovered position.

**Equation steps:** 0

### 3. Which line recovers the points better?

**Try:** Compare 45° and 135°. Which direction gives smaller gaps between the original and recovered points?

**Main idea:** The choice of line changes the recovery error. We will choose the line with the smallest total squared error.

**Equation steps:** 0

### 4. Put each point at its closest place on the line

**Try:** Move the selected point to the line. Notice the right angle at the point where it arrives.

**Main idea:** A projection is the closest point on the line. The gap from the original point is perpendicular to the line.

**Equation steps:** 0

### 5. What did one score lose?

**Try:** Move the point across the axis. Check that its stored score stays fixed.

**Main idea:** Several original positions can have the same score. The missing coordinate tells them apart.

**Equation steps:** 0

### 6. Turning both axes loses nothing

**Try:** Keep both coordinates, then remove one. Compare the recovered position in each case.

**Main idea:** Two rotated coordinates still locate the point exactly. Removing one coordinate can create a recovery error.

**Equation steps:** 0

### 7. Choose an axis by a clear rule

**Try:** Turn the line. Compare the squared spread kept with the squared recovery error.

**Main idea:** With the same units, the axis that keeps the most squared spread also gives the least total squared recovery error.

**Equation steps:** 0

### 8. From a picture to a computation

**Try:** Subtract the center. Search for a direction. Store the scores. Recover a point from its score.

**Main idea:** We first move the mean to zero. Then we choose an axis, compute each score, and use the axis to recover positions.

**Equation steps:** 0

## How do we measure a view?

### 9. Measure change from a shared center

**Try:** Move the whole cloud toward the origin. Watch its center and the gaps between points.

**Main idea:** PCA measures how the observations differ from their shared center, the mean.

**Equation steps:** 0

### 10. Find the center of this cloud

**Try:** Add the four x values and divide by four. Repeat for y.

**Main idea:** The mean gives one shared center for the four observations.

**Equation steps:** 1

### 11. Move the center to zero

**Try:** Move the mean to zero. Follow the selected point as its coordinates change.

**Main idea:** Subtract each feature mean from that feature. The resulting coordinates measure differences from the shared center.

**Equation steps:** 1

### 12. The distances do not change

**Try:** Follow A and B as the cloud moves. Does the gap between them change?

**Main idea:** Subtracting the same center from every point preserves all pairwise distances.

**Equation steps:** 1

### 13. Describe the line with two numbers

**Try:** Turn the unit arrow. Compare its horizontal and vertical coordinates.

**Main idea:** The vector w specifies the axis direction. Its length is one, so every direction uses the same score scale.

**Equation steps:** 1

### 14. Calculate one score

**Try:** Select a point. Multiply its centered coordinates by the two direction weights, then add.

**Main idea:** The dot product gives a signed coordinate along a unit axis.

**Equation steps:** 1

### 15. Use one rule for every observation

**Try:** Select each row of Xc. Apply the same two weights to calculate its score.

**Main idea:** The 4×2 data table multiplies a 2×1 direction vector to produce four scores. Each row is one observation.

**Equation steps:** 1

### 16. Keep the ruler length fixed

**Try:** Double the direction length. Compare each score and the resulting variance.

**Main idea:** A longer direction vector enlarges every score without improving the axis. Unit length prevents this arbitrary increase.

**Equation steps:** 1

### 17. How spread out are the scores?

**Try:** Try two angles. Compare the positive and negative scores around zero.

**Main idea:** Centering the observations also centers their scores: the mean score is zero.

**Equation steps:** 1

### 18. Signs cancel; squares do not

**Try:** Compare each signed score with its square. Why do the signed scores add to zero?

**Main idea:** Positive and negative scores can cancel. Their squares measure spread on both sides of the center.

**Equation steps:** 1

### 19. Give spread a number

**Try:** Add the four squared scores and divide by three.

**Main idea:** Sample variance divides the squared score sum by n−1. Here n=4, so the divisor is three.

**Equation steps:** 1

### 20. Search with a variance curve

**Try:** Turn the line. Follow the matching point on the variance curve and find its highest position.

**Main idea:** The curve shows which direction gives the most score variance. We need a method that also works with many features.

**Equation steps:** 1

## Why does covariance appear?

### 21. Open one squared score

**Try:** Follow each product in (w1 a + w2 b)². Find the two equal cross-products.

**Main idea:** Multiplying the two brackets gives four products. The two equal cross-products combine into one term with a factor of two.

**Equation steps:** 3

### 22. Add the same terms across rows

**Try:** Expand each observation’s squared score. Group its terms with matching terms from the other observations.

**Main idea:** Every observation uses the same direction weights. We can place these fixed weights outside the sums.

**Equation steps:** 2

### 23. Two familiar sums and one new sum

**Try:** Compare the three sums. Which use squares, and which uses products of different features?

**Main idea:** The square sums give feature variances. The mixed product sum gives covariance, which measures how the centered features vary together.

**Equation steps:** 1

### 24. Build covariance from signed products

**Try:** Compare Together, Opposite, and Cancellation. Follow the signs in the product table.

**Main idea:** Same signs give positive products. Opposite signs give negative products. Covariance adds these contributions.

**Equation steps:** 1

### 25. Variance alone cannot tell the tilt

**Try:** Switch between the positive and negative tilts. Compare the variances and the covariance.

**Main idea:** These clouds have the same feature variances. Their opposite covariance signs describe opposite tilts.

**Equation steps:** 1

### 26. Store the three quantities in S

**Try:** Select an entry of S. Calculate its four products, their sum, and the division by three.

**Main idea:** The diagonal stores the two variances. The two off-diagonal entries store the same covariance.

**Equation steps:** 1

### 27. Compute S with one matrix product

**Try:** Select an entry of S. Match a row of Xcᵀ with a column of Xc, then add their paired products.

**Main idea:** Transposing turns feature columns into rows. Each row–column product calculates one sum needed by the covariance matrix.

**Equation steps:** 2

### 28. Read wᵀ S w from inside out

**Try:** Compute Sw first. Then multiply its coordinates by the matching entries of w and add.

**Main idea:** The compact expression wᵀSw is exactly the expanded score variance.

**Equation steps:** 2

### 29. Check both routes with real numbers

**Try:** Change the angle. Compare variance calculated from the scores with variance calculated from S.

**Main idea:** Both routes give the same number at every angle because they are two forms of the same expression.

**Equation steps:** 1

### 30. State the optimization problem

**Try:** Try several unit directions. Compare their variance and identify the largest value.

**Main idea:** We want the largest value of wᵀSw. The constraint wᵀw=1 keeps every direction vector at unit length.

**Equation steps:** 1

## Why do eigenvectors solve it?

### 31. What does S do to an arrow?

**Try:** Turn w. Compare its direction and length with the arrow Sw.

**Main idea:** Multiplying by S maps the input vector w to the output vector Sw.

**Equation steps:** 1

### 32. Find where the turning slope is zero

**Try:** Compare a direction with a small turn to either side. Check the variance curve at both candidate axes.

**Main idea:** At a stationary direction, the variance curve has zero slope. Both a maximum and a minimum can have this slope.

**Equation steps:** 1

### 33. Find the variance slope

**Try:** Differentiate with respect to w1 while holding w2 fixed. Then exchange their roles.

**Main idea:** Changing each coordinate gives one slope. Together, these slopes form the gradient 2Sw.

**Equation steps:** 4

### 34. Find the constraint direction

**Try:** Find the gradient of w1²+w2². Compare its outward direction with the circle’s tangent.

**Main idea:** The vector 2w points outward from the unit circle. A tangent to the circle is perpendicular to w.

**Equation steps:** 2

### 35. Match the two normal directions

**Try:** Compare both stationary directions. Check why each has zero change along the tangent.

**Main idea:** Zero slope along the tangent gives 2Sw=2λw, hence Sw=λw. This identifies candidates; we still need to find the maximum.

**Equation steps:** 3

### 36. This equation defines an eigenvector

**Try:** Compare w and Sw at 45° and 135°. How much does S scale each arrow?

**Main idea:** An eigenvector is a nonzero vector that S maps to a multiple of itself. Its eigenvalue is that multiplier.

**Equation steps:** 1

### 37. Find the possible scale factors

**Try:** Subtract λ from each diagonal entry. Calculate the determinant of the resulting 2×2 matrix.

**Main idea:** The matrix S−λI must send a nonzero vector to zero. Its determinant must therefore be zero.

**Equation steps:** 2

### 38. Solve our two eigenvalues

**Try:** Factor the difference of squares. Check each root in the original determinant equation.

**Main idea:** The two possible eigenvalues are 6 and 2/3.

**Equation steps:** 3

### 39. Find and normalize the directions

**Try:** Solve for the relation between the two coordinates. Divide each resulting vector by its length.

**Main idea:** The two unit directions are (1,1)/√2 and (1,−1)/√2.

**Equation steps:** 2

### 40. A candidate can be a minimum

**Try:** Select each eigenvector. Compare its variance with the nearby directions on the curve.

**Main idea:** The eigenvector equation finds both candidates. Their eigenvalues tell us that their variances differ.

**Equation steps:** 1

### 41. Why are these directions perpendicular?

**Try:** Calculate q1ᵀSq2 in two ways. What must its dot product be when the eigenvalues differ?

**Main idea:** Symmetry gives (λ1−λ2)q1ᵀq2=0. Different eigenvalues force the dot product to be zero, so these axes are perpendicular.

**Equation steps:** 3

### 42. Build any unit direction from them

**Try:** Turn w. Follow its coordinates a and b along the two eigenvector axes.

**Main idea:** These two perpendicular unit vectors span the plane. Every unit direction has coordinates a and b with a²+b²=1.

**Equation steps:** 1

### 43. Expand variance in the new basis

**Try:** Expand the four products. Use the perpendicular axes to remove the two cross-terms.

**Main idea:** The variance becomes λ1a²+λ2b²: each eigenvalue is weighted by a squared coordinate.

**Equation steps:** 3

### 44. Prove the largest value wins

**Try:** Change the squared weights. Can their weighted eigenvalue average exceed λ1?

**Main idea:** The squared weights are nonnegative and add to one. Their average cannot exceed λ1, and q1 reaches that bound.

**Equation steps:** 3

### 45. What if the eigenvalues tie?

**Try:** Turn the axis through the round cloud. Compare variance in different directions.

**Main idea:** Tied eigenvalues give the same variance in every direction of their shared space. The best axis can therefore be non-unique.

**Equation steps:** 1

## What can we keep and recover?

### 46. Find the next component

**Try:** Keep PC1 fixed. Find a unit direction perpendicular to it.

**Main idea:** PC2 maximizes variance among unit directions perpendicular to PC1. In two dimensions, only one perpendicular axis remains.

**Equation steps:** 1

### 47. Read the PCA coordinates

**Try:** Switch between the original axes and the PCA axes. Follow one observation’s two coordinates.

**Main idea:** Loadings describe the axes. Scores describe where each observation lies along those axes.

**Equation steps:** 1

### 48. Check the new covariance

**Try:** Compare the covariance before and after changing to PCA coordinates. Check the off-diagonal entries.

**Main idea:** The score columns have zero covariance. This does not generally make them independent.

**Equation steps:** 2

### 49. What does 90 percent measure?

**Try:** Divide the PC1 variance by total variance. Explain what the resulting percentage measures.

**Main idea:** PC1 keeps 6/(6+2/3)=90% of the total squared spread. This percentage does not measure prediction accuracy.

**Equation steps:** 1

### 50. Rebuild an observation from its score

**Try:** Select an observation. Multiply its score by q1, then add the mean.

**Main idea:** The recovered point lies on the line through the mean in direction q1.

**Equation steps:** 2

### 51. Draw the missing part

**Try:** Select a point. Compare its original vector, projection, and error vector as a right triangle.

**Main idea:** The original squared length equals the kept squared length plus the squared error. The right angle makes this identity possible.

**Equation steps:** 2

### 52. Prove the second objective

**Try:** Add the right-triangle identity for all observations. Find the term that stays fixed as the axis turns.

**Main idea:** Total squared distance from the center stays fixed. Maximizing score variance therefore minimizes total squared recovery error.

**Equation steps:** 3

### 53. Recover both coordinates

**Try:** Keep zero, one, and then two components. Compare the recovered positions.

**Main idea:** Both perpendicular coordinates together recover the original centered vector exactly.

**Equation steps:** 1

### 54. Choose how much to keep

**Try:** Set a retained-variance target. Compare the component count and the remaining recovery error.

**Main idea:** Choose an acceptable error for the task. A high retained-variance percentage alone does not establish usefulness.

**Equation steps:** 1

### 55. Extend from two features to p

**Try:** Choose k in the larger eigenvalue spectrum. Compare the sum kept with the sum discarded.

**Main idea:** Choose k perpendicular unit axes. The top k eigenvectors retain the most total variance; discarded eigenvalues give the remaining loss.

**Equation steps:** 3

### 56. Connect the result to SVD

**Try:** Substitute Xc=UΣVᵀ into the covariance formula. Follow the factors that cancel.

**Main idea:** The columns of V give PCA directions. Each eigenvalue is a squared singular value divided by n−1.

**Equation steps:** 3

## When does the result help?

### 57. Use the axes on a new observation

**Try:** Enter a new observation. Apply the existing mean and axes without changing them.

**Main idea:** Fit preprocessing and PCA on the training data. Reuse the same values to transform later observations.

**Equation steps:** 1

### 58. Decide what units mean

**Try:** Rescale the second feature. Turn standardization on and compare the resulting axis.

**Main idea:** Standardization gives each nonconstant feature unit variance. It changes the relative weight of the features in the PCA objective.

**Equation steps:** 1

### 59. Large variance is not always useful

**Try:** Compare the original cloud, a distant observation, and the labeled example. Is the largest spread useful each time?

**Main idea:** A distant observation can dominate squared spread. A direction with little variance can still separate useful categories.

**Equation steps:** 0

### 60. A line cannot follow every shape

**Try:** Turn a line through the ring. Check the gaps between the ring and the recovered points.

**Main idea:** One straight axis cannot preserve a circle’s shape. A curve may need two PCA coordinates even when one parameter describes it.

**Equation steps:** 0

### 61. Change the real notebook data

**Try:** Move observation D. Compare the new center, covariance, and PC1 with their earlier values.

**Main idea:** Changing a measurement changes the data that PCA describes. The notebook recalculates the center, covariance, axes, scores, and recovery errors.

**Equation steps:** 0

### 62. Solve a fresh geometric problem

**Try:** Choose an axis for the new cloud. Write your reason before checking the computed optimum.

**Main idea:** The same PCA rule applies to a new cloud. Its best axis can differ from the one in our worked example.

**Equation steps:** 0

### 63. Produce the calculation yourself

**Try:** Calculate the requested covariance, score, and recovered position. Explain why each operation is needed.

**Main idea:** Use the same three operations on new values: covariance, projection, and reconstruction.

**Equation steps:** 0

### 64. Teach PCA back in your own words

**Try:** Explain why covariance leads to eigenvectors and small recovery errors. Use a new example and name one limit.

**Main idea:** PCA’s axes keep the most squared spread. Their usefulness still depends on the task and the chosen units.

**Equation steps:** 0
