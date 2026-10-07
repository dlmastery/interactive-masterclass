# Round 1 — comparator evidence and a teaching process

6 October 2026. **Author-informed review:** I reviewed this course and authored some repair components. This is not independent review or evidence of student learning. No course or skill changes were made for this report.

## Access and scope

I inspected selected, timestamped passages in two existing YouTube transcript exports under `C:/Users/abhir/AppData/Local/Temp/browser-use/exports/`: `youtube-g-Hb26agBFg-5064ddee-d61f-4fd1-b89c-4693a808e3fa.txt` and `youtube-FgakZw6K1QQ-806fb977-aba6-431e-8b04-545daca5753d.txt`. The former marks captions as auto-generated; the latter says authored or unspecified. They were not found by the workspace filename search, but were present in the earlier export directory.

For 3Blue1Brown I read the creator's illustrated article, including prompts and descriptions of its figures. Image URLs resolved, but pixels/animation timing were not visually inspected. I did not watch these videos in this round. The research papers below were read through extracted PDF text, including relevant methods, results, and limitations. Creator popularity is not an accuracy or learning measure.

## What these explanations actually do

**Serrano — purpose, then a missing measurement.** [PCA video](https://www.youtube.com/watch?v=g-Hb26agBFg).

*Observed in transcript:* At 0:45–1:58, the task is choosing a camera position for a group of friends; competing projections make the loss visible. At 2:03–2:48, housing features explain why fewer columns could be useful. At 8:29–10:40, two clouds have the same separate feature variances but different tilt. Covariance answers a question the current measurements cannot answer. At 14:53–17:37, specific vectors and then a circle are transformed before eigenvectors/eigenvalues are named.

*Inference for us:* New mathematics should solve a visible insufficiency, not appear because the syllabus says it is next. Across subjects, first show two cases the learner's current rule cannot distinguish. Preserve the useful analogy, but state its limits: retained variance is not all task-relevant information; the viewing direction and retained projection axis are perpendicular. The transcript also announces a prerequisite route early, so copying its chapter order would not itself satisfy this user's requested approach.

**StatQuest — one example, one isolated reason, then terminology.** [PCA step by step](https://www.youtube.com/watch?v=FgakZw6K1QQ).

*Observed:* At 0:30–3:25, the same samples progress through one, two, and three measured variables, creating the need for a lower-dimensional display. At 5:53–7:32, the explanation isolates one point and its fixed distance from the origin. A right triangle explains the trade between projection length and residual length. At 9:55–12:23, a mixing recipe becomes a linear combination, then a unit vector, then named loadings/eigenvector. Naming follows an operation the learner has already encountered.

*Inference:* We presented complete formulas beside broadly relevant diagrams while leaving the difficult connection for the learner. A better scene isolates the single changing quantity and keeps the invariant visible. However, this video is not a complete covariance-to-global-optimality proof. We must supply that requested depth rather than claiming imitation of its pace provides it. Its illustrative wording and numbers still require our own mathematical checks.

**3Blue1Brown — let the representation carry the argument.** [Bayes' theorem, creator article](https://www.3blue1brown.com/lessons/bayes-theorem/).

*Observed in article:* “Steve” starts with a prediction about occupation. Concrete population counts lead to counts compatible with the description. The formula is assembled from those counts. In “Thinking with area,” the sample becomes a unit square, and evidence restricts the relevant region. Equal likelihoods supply a case where belief should not change. “Steve's controversy” distinguishes the mathematical update from debatable assumptions about the population and description.

*Inference:* A lasting model should be something the learner can redraw and use, not merely recognize on our slide. This applies beyond geometry: a causal chain, flow, dependency diagram, or state transition can expose the mechanism. The Bayes article is also interactive, so the contrast is not simply good video versus bad software. Its represented quantities do intellectual work. We should test whether ours do.

## Research: useful constraints, not a universal recipe

**Multimedia explanation — primary experiment.** [Mayer & Anderson (1992)](https://doi.org/10.1037/0022-0663.84.4.444), inspected through [the author's hosted paper copy](https://www.researchgate.net/profile/Richard-Mayer-4/publication/232585988_The_Instructive_Animation_Helping_Students_Build_Connections_Between_Words_and_Pictures_in_Multimedia_Learning/links/57799b8208aeb9427e2c00b2/The-Instructive-Animation-Helping-Students-Build-Connections-Between-Words-and-Pictures-in-Multimedia-Learning.pdf?origin=publication_detail).

*Finding:* Concurrent narration and animation improved problem-solving transfer for pump/brake explanations compared with several separated or single-channel conditions. The authors restrict their conclusions by learner experience, explanatory material, and outcome measure; overall retention did not reveal the same differences.

*Implication/inference:* Synchronize the explanation with the exact depicted operation. A formula reveal should change its corresponding representation. This does not establish that animation, narration, or more visual detail always helps, or that the same effect size applies to our mathematical interface.

**Guidance — original meta-analysis, not a single experiment.** [Alfieri et al. (2011), paper](https://app.nova.edu/toolbox/instructionalproducts/edd8124/articles/2011-Alfieri_et_al.pdf).

*Finding:* Across 164 studies, explicit instruction generally outperformed unassisted discovery; enhanced discovery had favorable results against a mixed set of comparison methods. Feedback, scaffolds, examples, and elicited explanations matter. The paper includes varied tasks and operational definitions, and acknowledges dependence among comparisons.

*Implication/inference:* A novice should not face an empty sandbox and be expected to rediscover the theory. Demonstrate a worked case, guide a discriminating experiment, then fade support. This is not evidence that every slider helps or that guided discovery universally beats good explicit explanation. Retrieval also cannot recover knowledge the learner never understood or encoded.

**Delayed retrieval — primary experiment; the cited percentages verified.** [Roediger & Karpicke (2006), author-lab PDF](https://learninglab.psych.purdue.edu/downloads/2006/2006_Roediger_Karpicke_PsychSci.pdf), Experiment 2, pp. 251–253.

*Finding:* Four study periods (SSSS) yielded 83% recall after five minutes and 40% after one week. One study plus three recall periods (STTT) yielded 71% and 61%. These are separate retention-interval groups, not the same people measured twice. Participants were undergraduates learning prose; tests assessed recalled idea units. Study periods lasted five minutes and recall periods ten, so this is not an equal-time productivity comparison.

*Implication/inference:* Test delayed reconstruction of the explanation as well as immediate fluency. The percentages do not establish an AI-tutor effect, universal forgetting rates, mastery of derivations, or superiority of any 12-role workflow. Explanation, guided practice, and later retrieval have different jobs.

## Why our result could feel worse

The earlier course source supports a narrower diagnosis than “AI cannot teach”: we optimized countable outputs—slides, equation steps, controls, numerical checks—without showing that each scene supported its intended inference. Author instructions leaked into learner prose. A repeated cloud accompanied different algebraic operations. The opening statistic lacked an earned interpretation. Software success was reported too broadly.

The root reviewer later reported a Reveal integration failure: nested `section` wrappers were treated as slide stacks and controls stopped receiving clicks. I did not independently reproduce that UI failure. It is a concrete reminder that my numeric checks were not evidence of working interaction, let alone learning.

## Reusable outer and inner loops

**Outer loop: choose and revise the teaching hypothesis.** Define the learner's purpose, initial model, hardest inference, and fresh transfer task. Compare contrasting explanatory routes with source-access records. Build the opening, bottleneck, and transfer scene before expanding. Review purpose, causal/mechanistic continuity, proof, and practical limits separately. A failure changes the representation or sequence, not merely the amount of text. For nonmathematical subjects, the central argument may be causal or evidential rather than geometric.

**Inner loop: earn one inference.** Pose a concrete question; obtain a prediction; demonstrate or manipulate the discriminating case; explain the change and invariant; connect it to formal language; ask for an explanation without the display. Supply a hint or worked step when prior knowledge is insufficient. Fade support when the learner succeeds. Preserve their state. Later, ask them to reconstruct and transfer the idea. This is a design hypothesis to test, not a mandatory seven-click ritual.

## Fair comparison protocol

Compare matched learning goals and learner prerequisites, not our 64-slide coverage against a short video's opening. Give both formats comparable time and access to replay. Predefine fresh prediction, causal explanation, calculation/proof, boundary-case, and delayed-retrieval tasks. Score with an explicit rubric and record assistance, navigation failures, time, and confidence separately. Counterbalance order where feasible; do not treat rereading after a video as a clean comparison. Let the interactive version exploit controlled counterfactuals and reversible experiments, while retaining expert pacing through a guided path. Creator-informed inspection can expose missing mechanisms; only actual learner evidence can support comparative learning claims.
