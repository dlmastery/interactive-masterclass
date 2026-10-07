# PCA teaching repair review

Reviewed 6 October 2026. Source review, not a learner study or rendered UI review.

Sources inspected: `outputs/pca-studio/course-v2.json`, `v/lesson/src/PcaScenes.tsx`, `v/lesson/src/PcaCourse.tsx`, and `outputs/PCA-TEACHING-ASSESSMENT.html`.

## Verdict

The 64-slide argument is mathematically much better than the earlier prerequisite-first route. Its dominant failure is that a small set of generic scenes substitutes for the actual operations the text promises. This produces a long course with remarkably little change in how the learner sees the problem. A color/theme replacement or another increase in slide count will not repair this.

The strongest existing elements are the continuous four-observation example, selected observation linking, covariance product table, explicit distinction between stationary and maximal directions, the global weighted-average bound, and the reconstruction triangle. Preserve these. The learner must be able to see one operation become the next operation.

The user's reference to a good first version is evidence to restore its concrete visual strengths after inspecting that version. It does not establish that the entire former sequence should be restored. Preserve a runnable copy before changes and compare the actual opening views side by side.

## Highest-impact failures and concrete repair

| Location | What fails | Smallest meaningful repair |
|---|---|---|
| Opening 1–8 | Four generic positions, an axis, and an unexplained “spread kept” percentage appear immediately. The learner is asked to optimize a named statistic before seeing a concrete consequence. | Give the cloud a job: “Store each marker with one number. How closely can we recover its position?” Select A, map to a score, reconstruct A, show the gap. Then compare two directions. Name variance only when quantifying the visible difference. |
| Opening 8 | The “Center” button selects a plot whose data are already centered; “Find the best direction” instantly selects 45°. Those captions suggest a process that the interaction skips. | Drive an actual four-phase animation/state sequence: raw coordinates and mean → subtract mean → candidate axis search → one score and reconstructed point. Keep raw and centered coordinates visibly distinct. |
| Slides 21–23 | Next equation reveals do not alter the visual operation. The three numeric variance terms are shown from the start; the learner never sees the two cross-products arise. | A 2×2 product tile expands one selected score square; click each pair to expose its contribution. Merge the two equal cross-terms, then aggregate each term across observations. Bind the equation step to the highlighted tile. |
| Slide 27 | It says “Animate a selected row of Xcᵀ meeting a column of Xc.” There is no Xc or Xcᵀ matrix picture, only an entry/product table and cloud. | Show Xc, its transpose, four paired products, an accumulator, and the destination entry in S. Entry selection chooses both feature columns; step through four observations. Retain the existing product table as the readable ledger. |
| Slides 32–35 | Slope, tangent, gradient, normal and multiplier arrive with the same w/Sw cloud. The viewer cannot see why zero turning gain implies parallel arrows. Slide 32 gives the derivative before slide 33 explains differentiation. | Use a dedicated large unit circle and local tangent at the tip of w. Show 2Sw decomposed into radial and tangential parts. Advance a small signed turn and show its predicted/actual variance change. At either stationary axis, the tangent part is zero; only the radial part remains. Then earn 2Sw=2λw and Sw=λw. |
| Slides 42–44 | The weight slider assumes a,b are positive; the figure is a generic cloud, not the q1/q2 decomposition. This visually under-supports “any unit direction.” | Show w=a q1+b q2 with perpendicular component segments, signed a/b, and a²+b²=1. Allow the whole direction circle. Squared weight bars then become an output of the geometric decomposition; optional weight control must also specify the signs. |
| Throughout | Proof steps mostly change text, not the diagram; many controls operate an unrelated background cloud. | Add a scene-owned proof step/onStep interface. At the covariance, stationarity, and global-bound bottlenecks, change the highlighted mathematical operation and picture together. Keep the angle control only where angle answers that slide's question. |
| Learner work | Scene is keyed by slide and unmounted on leaving it; local answer, reason, phase, and proof state reset. | Persist state by slide ID in the course root or a course store. A learner should be able to consult a refresher/earlier step and return to their work. |

## Two real teaching options

### Option A — repair the existing complete argument (recommended for this request)

Retain the 64-slide spine and the four observations. Replace the bottleneck representations in place. The core route remains:

1. One-number compression; recover a point; compare good and bad axes.
2. Score along a unit axis; squared spread; covariance appears when we expand the score variance.
3. Unit-circle search; local turning gain; no tangent gain means Sw is parallel to w.
4. Solve the two candidate directions; show one is a minimum.
5. Decompose any direction into the eigenvector axes; its variance is a weighted average; the largest eigenvalue is a global bound.
6. Reconstruct; derive the fixed total = kept + lost identity; generalize and test limits.

Benefits: minimal disruption, preserves the user's requested proof depth and 50+ slide course, keeps current numeric checks useful. Cost: the gradient path is still demanding and needs a real tangent/normal picture rather than a slogan. Do not add a general calculus chapter.

### Option B — covariance ellipse and a direct two-dimensional derivative first

After V=wᵀSw, use w=(cos θ,sin θ) and this example's V(θ)=10/3+(8/3)sin(2θ). The variance curve makes 45° and 135° concrete. Then show that their transformed arrows are parallel, name eigenvectors, and prove the general bound in the eigenbasis. Place the coordinate-gradient/Lagrange derivation immediately after as a second route.

Benefits: a learner can solve the running example before meeting gradients; connects directly to the angle control. Costs: can look like a special trick for an equal-diagonal 2×2 matrix; trig differentiation introduces its own prerequisite; risks delaying why the general method is eigenvectors. This is a useful alternate explanation, not the best repair spine here.

Reject “start with eigenvectors/matrix stretching and later say this is PCA.” That repeats the user's central complaint. Also reject “derive only from reconstruction error”: it moves the requested covariance argument later, although the reconstruction triangle is useful motivation.

## Concrete opening, retaining eight slides

1. **Can two coordinates become one?** Original four marker locations; one selected marker. A two-value coordinate card becomes one stored score. Reconstruction remains visible. Caption: “PCA chooses new axes. We can keep fewer coordinates and accept some error.” No percentage yet.
2. **A score is a position on the ruler.** Drag/rotate the axis; link A in the cloud, its nearest point on the axis, and A on a one-dimensional ruler. The same color and letter connect all three.
3. **Try a poor view and a useful view.** Two views use identical scales. Learner predicts which one recovers the markers better; toggles original/reconstructed overlays. Explain collisions of A and B rather than hiding them.
4. **How do we put a point on the line?** Animate A to its closest point. Mark the right angle. Name projection now.
5. **What did we lose?** Move A along a perpendicular family while its score stays fixed. This must be a genuine movement control, not only an orange line reveal.
6. **Turning axes alone loses nothing.** Two new coordinates remain visible; remove the second, then restore it. Recover A exactly with both.
7. **Choose an axis by a clear rule.** Show total squared distance, kept squared distance, and lost squared distance as additive lengths/areas. Preview the rule visually; say the later proof explains why it works. If percentages are introduced, label “fraction of squared spread,” not general information kept.
8. **Our route from picture to computation.** Replay the four computational stages with actual state changes. A small breadcrumb maps each stage to the upcoming proof. It should summarize actions the learner has just seen.

Keep the basic four-point case for the derivation. A denser introductory cloud can be attractive, but a mid-course unannounced dataset replacement breaks the argument. If the earlier version uses a dense cloud worth preserving, label the transition explicitly: “We will use four points to calculate every step by hand.”

## The three representative repairs to build before restyling all 64 slides

### 1. Projection and reconstruction scene

Input: axis angle and selected observation. Picture: original point, perpendicular projection, one-dimensional score, recovered point. Consequence: error segment changes with angle. Prediction: “Can A and B have the same stored number?” Transfer: choose a direction for a rotated cloud. No “information retained” claim from variance alone.

### 2. Covariance matrix multiplication scene

Input: destination S entry, observation step 1–4, sign-flipped second column. Picture: highlighted feature columns become a row/column pair; each product is deposited into the sum; divide by 3 and insert it into S. Consequence: diagonal unchanged by sign flip; off-diagonal sign reverses. Prediction: “Which entries change when we reverse the second feature?” This is stronger evidence of understanding than clicking an entry that already displays its answer.

### 3. Stationarity then global maximum scene

Input: candidate angle, small turn direction, and later eigenbasis angle. Picture A: unit circle at large scale, tangent at w, gradient 2Sw and its radial/tangential decomposition. Show the small angular displacement and its variance change on a synchronized curve. At 45° and 135°, label “zero first-order turning gain,” never just “no improvement” because a minimum is also stationary. Picture B: a q1+b q2 component construction and squared weights. A stacked bar shows 6a²+(2/3)b² against a fixed upper bound 6. At q1 the bound is reached. Keep “stationary candidate” and “global maximum proof” separate in both text and picture.

Mathematical detail: using the gradient arrow 2Sw alongside w can create a 12:1 length ratio for this example. Do not shrink one arrow silently. Use a dedicated coordinate view with an explicit common scale, or draw vectors at a marked display scale and show the numeric magnitudes separately. The tiny unit circle inside the current large cloud is inadequate.

## Wording repairs

Remove writer instructions from course content and notebook output. Examples in current JSON:

- Slide 10: “Introduce the mean only because we need this center.” → “The mean gives one shared center for the four observations.”
- Slide 15: “Show the matrix shapes here.” → “The 4×2 data table maps one 2×1 direction to four scores.”
- Slide 21: “Show the two identical cross-products…” → “The two cross-products are equal. Together, they give the factor two.”
- Slide 37: “Explain determinant only here.” → “A nonzero direction exists only when this matrix flattens at least one direction to zero.” Then support that singularity statement with a visual or a narrowly scoped refresher.
- Slide 42: “State the symmetric-matrix basis theorem…” → move the theorem to an explicit assumption card beside its application.
- Slide 62/63: replace “Require a prediction” and “Record numeric correctness” with the actual learner tasks.

Write exact observable claims, not claims about the tutor's process. Sentence length checks do not establish the user's 80% STE target.

## Repair acceptance evidence

Before claiming the course is repaired, the rendered opening must let a reviewer explain what one stored number means and point to what was lost. The covariance scene must actually show the row/column operation its title promises. The proof scene must visibly show why turning gain vanishes at both candidates and separately why the larger eigenvalue wins globally. Changing any control must update its labels, plot, and numeric result together. Navigating away and back must preserve learner work. These are specific scene checks, not a learner-efficacy claim.

Do not spend this repair rebuilding everything, adding another methodology artifact, or certifying beauty from screenshots. Prioritize these three scenes, preserve the usable original presentation style after inspecting it, and then remove redundant controls/text around them.
