# Welch Labs: transferable teaching patterns, with source checks

6 October 2026. Author-informed process research. No skill or course edits. These are observations of primary materials and proposed adaptations, not measured learning effects or a popularity ranking.

## Access and progression actually inspected

**Imaginary Numbers Are Real:** read Welch's official posts for Parts 2, 3, 5, 6, and 7, plus extracted text from the official [workbook preview](https://www.welchlabs.com/s/workbookPreview.pdf), especially printed pages 2–10. The text begins with a missing-root puzzle, motivates extending a number system, introduces a cubic-formula difficulty, and later asks the learner to connect complex arithmetic to geometry. I did not watch/listen to episodes or inspect animation timing. The coordinator separately owns static visual inspection. The 2015 announcement proposed ten parts; the 2016 preview contents and footnotes extend to Part 13. Do not report the early schedule as the final sequence.

**Neural Networks Demystified:** read the official [series index](https://www.welchlabs.com/blog/2015/1/16/neural-networks-demystified-part-1-data-and-architecture), creator repository README, complete markdown/movie text in notebooks 1, 3, 5, and 7, and selected code. The [README](https://github.com/stephencwelch/Neural-Networks-Demystified) explicitly identifies the notebooks as formulas, code, and movie text. This establishes textual progression, not observed performance. Copies and hashes are in `welch-source-inspection/`; they were retrieved from `master`, not pinned to a commit. Cell indices below are zero-based across all cells. No notebook was executed.

## Five patterns worth adapting

### 1. Let a specific failure earn the new idea

**Evidence:** [Imaginary Numbers Part 2](https://www.welchlabs.com/blog/2015/9/4/imaginary-numbers-are-real-part-2-a-little-history), introduction and cubic-root clarification, explains why a formula producing problematic quantities cannot simply be dismissed when the cubic has real roots. [Part 3](https://www.welchlabs.com/blog/2015/9/11/imaginary-numbers-area-real-part-3-cardans-problem) explicitly argues for understanding a tool's assumptions and limitations instead of merely obtaining homework answers. In [NN Part 3](https://github.com/stephencwelch/Neural-Networks-Demystified/blob/master/Part%203%20Gradient%20Descent.ipynb), cells 11–33, inaccurate predictions motivate a loss; brute-force search becomes impractical as the number of weights grows; a downhill direction then has a purpose.

**Adaptation and rationale:** Write the current model, its observable failure, and what the proposed extension must resolve before naming the method. The transition should answer a question the learner can state.

**Limit:** Do not invent a historical necessity, force every topic into a failure narrative, or use drama to replace proof. Timing claims from an old demonstration are not current benchmarks.

### 2. Give the learner a reconstructable bridge between representations

**Evidence:** [Imaginary Numbers Part 6](https://www.welchlabs.com/blog/2015/10/2/imaginary-numbers-are-real-part-6-the-complex-plane), “Your Assignment,” asks learners to plot operands and products for four examples, seek a pattern, and test assumptions. [Part 7](https://www.welchlabs.com/blog/2015/10/9/imaginary-numbers-are-real-part-7-complex-multiplication) then connects algebraic and geometric multiplication as two views of the same operation. This is a specific task-to-explanation handoff, not merely two pictures beside each other.

**Adaptation and rationale:** Supply prerequisite operations and a discriminating set of examples; ask the learner to translate between representations and justify the invariant relation. Follow their conjecture with a derivation and a new case.

**Limit:** Several examples suggest a rule; they do not prove it. Open discovery can overwhelm a novice. Offer a worked starting case, hints, or direct explanation when needed, and do not make guessing compulsory.

### 3. Keep a stable task while adding meaning and machinery

**Evidence:** [NN Part 1](https://github.com/stephencwelch/Neural-Networks-Demystified/blob/master/Part%201%20Data%20and%20Architecture.ipynb), cells 2–16, starts with inputs and a target, distinguishes regression from classification, and derives interface dimensions from the data. Its variable table links code, notation, meaning, and shape. Later notebooks retain the sleep/study prediction case as they add loss, gradients, checking, training, and generalization concerns.

**Adaptation and rationale:** Keep one running case through the difficult argument. Maintain a compact mapping of visible object, symbol, operation, and code identifier where code is relevant. New notation should expose something in the same case before requiring another domain story.

**Limit:** A small illustrative dataset is not evidence of a real predictive or causal relationship. Add transfer cases before claiming general understanding. Do not transplant this particular example or its old modeling claims into unrelated subjects.

### 4. Teach independent verification before trusting apparent success

**Evidence:** [NN Part 5](https://github.com/stephencwelch/Neural-Networks-Demystified/blob/master/Part%205%20Numerical%20Gradient%20Checking.ipynb), cells 2–9 and 17–25, warns that wrong gradients can produce apparently functioning code. It revisits the derivative through a simple function, then compares analytic and numerical gradients. Code cells 18 and 24 perturb parameters, restore them, and quantify disagreement. The official sequence puts this before training.

**Adaptation and rationale:** After a consequential derivation, create a check using a different route: numerical perturbation, a limiting case, dimensional reasoning, inverse operation, or independently constructed example. Make the reason for the check explicit. This also supplies just-in-time prerequisite grounding.

**Limit:** Agreement on sampled cases is not a universal proof; two implementations can share a bug. Numerical tolerances depend on scale and precision. Do not inherit a fixed epsilon or threshold as a general law.

### 5. Turn a successful demonstration into a diagnostic and decision

**Evidence:** [NN Part 7](https://github.com/stephencwelch/Neural-Networks-Demystified/blob/master/Part%207%20Overfitting%2C%20Testing%2C%20and%20Regularization.ipynb), cells 2–7, 19, and 24–29, challenges the preceding fit, distinguishes observations from an underlying process, introduces held-out behavior, and motivates regularization after diagnosing overfitting.

**Adaptation and rationale:** After showing the method work, test a condition in which that success is insufficient. Teach the failure mechanism, diagnostic, mitigation, residual tradeoff, and decision about another method. This keeps limitations inside the argument rather than in an appendix.

**Limit:** A surprising prediction is a prompt to investigate, not proof that a model is wrong. Validation used to select adjustments must not masquerade as untouched final testing. Demonstrate the mitigation's costs as well as its benefits.

## Do not inherit the source's defects

These findings strengthen the need to validate admired materials:

- **NN Part 3, cells 34–38:** the text implies its squared-error setup keeps the network objective convex. Squared error is convex in predictions, but composing it with a nonlinear network does not generally make it convex in weights. Reuse the motivation for optimization, not this guarantee.
- **NN Part 7, code cell 20:** training inputs are normalized in place before their maximum is reused for test scaling; that maximum is then one. This is a visible scaling defect, not a reported execution result. Preserve the original fitted scale when adapting the example.
- **NN Part 7, cells 19 and 24:** monitoring and adjusting against “testing” data requires a validation/final-test distinction; its examples-per-parameter heuristic is not a universal sample-complexity rule.
- **Imaginary Numbers Part 2:** the author adds a longer derivation and explicitly flags uncertainty in the compressed cubic argument. Treat explanatory compression as a review obligation: important assumptions belong at the point of inference, even when a supplement provides detail.

Use these patterns as testable choices within the existing teaching graph. Neither creator reputation nor our inspection establishes novice learning, correct execution, superior oration, or transferable effectiveness. No recommendation here authorizes copying scripts, signature visuals, or a fixed episode count.
