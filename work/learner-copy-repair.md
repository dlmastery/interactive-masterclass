# Learner copy repair

Changed only the active `outputs/pca-studio/course-v2.json`. The notebook still needs the parent's synchronization step. No active TSX, CSS, server, skill, or harness was changed.

- Reviewed all 64 claims, 64 learner actions, and 79 equation reasons for meaning. Rewrote them as explanations or tasks addressed to the learner. Changed 11 titles and aligned three local refresher paragraphs.
- The first eight slides now start with storing one number, recovering a position, and inspecting the gap. They progress through a score ruler, competing axes, closest-point projection, missing coordinates, rotation, squared error, and the computation route.
- Slide 8 now asks for the actual sequence: subtract the center → search for a direction → store scores → recover a point. It no longer talks about a tutor's plan.
- Removed author instructions such as “Show the matrix shapes,” “Explain determinant only here,” and “Record numeric correctness.” Replaced them with matrix dimensions, a singularity explanation, and learner calculations.
- Named squared spread and squared recovery error precisely. The 90% result remains a variance fraction, with no claim that it measures general information or prediction accuracy.
- Clarified the shared center and axis needed to recover a position from one score; the covariance divisor; transpose and paired products; the tangent slope; stationary points versus maxima; the eigenvalue bound; and recovery error units.
- Equation reasons now explain intermediate operations. Examples: factoring fixed weights out of a sum, why the two cross-terms match, how symmetry moves S between vectors, and why unit length makes projection squared length equal z².
- Avoided fixed-point explanations where controls can select another observation. The centering, score, covariance-entry, and reconstruction reasons remain valid for the selected data.

Preserved exactly: all 64 IDs and their order, 79 TeX expressions and their order, scene names, chapter assignments and ranges, and notation entries. No derivation was removed.

Checks: parsed JSON; exact structural/TeX comparisons against `work/course-before-learner-copy.json`; 394 slide-copy sentences checked with simple whitespace counts, all within 20 words for actions or 25 for descriptions. This is a length check, not certification of the requested ASD-STE100 vocabulary/meaning compliance.

Final JSON SHA-256: `9aa844eb648949438f697e3bdefaa2549116bf6740c9145f96bd32bcbcaad4a4`.

The renderer contains additional hardcoded prose, including overrides on slide 1. That copy was outside this task's file scope and needs the parent's scene review. No learner-effectiveness or rendered-layout claim is made from this copy pass.
