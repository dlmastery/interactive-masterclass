# Human and AI tutoring: evidence and design rules

Read when choosing pedagogy, feedback, assessment, and adaptation. This is a practical synthesis, not proof that the combined protocol outperforms every teacher or generalizes to 1,000 topics. Verify updates before making current research claims.

## Evidence that changes decisions

| Source and type | Relevant observation | Design implication and limit |
|---|---|---|
| [IES practice guide, 2007](https://ies.ed.gov/ncee/wwc/Docs/PracticeGuide/20072004.pdf), official synthesis | Addresses spacing, worked examples with problems, concrete/abstract representations, and explanatory questions, with different evidence ratings. | Combine explanation and practice; ask deep questions once the learner has enough topic knowledge. It does not validate an AI prompt or a universal lesson rhythm. |
| [Collins, Brown, Newman, 1987](https://files.eric.ed.gov/fulltext/ED284181.pdf), cognitive apprenticeship framework | Makes expert activity visible through modeling, coaching, scaffolding, articulation, reflection, and exploration. | Show how a practitioner recognizes conditions, chooses, checks, and recovers; fade support. This is a design framework, not a causal estimate for this skill. |
| [Black and Wiliam, 2009](https://kclpure.kcl.ac.uk/ws/files/9119063/Black2009_Developing_the_theory_of_formative_assessment.pdf), formative-assessment theory | Evidence about current understanding informs the next instructional decision. | A quiz becomes formative when its result changes what happens next. Do not equate quiz presence with responsive teaching. Subject norms still matter. |
| [Chi and Wylie, 2014](https://education.asu.edu/sites/default/files/lcl/chiwylie2014icap_2.pdf), ICAP framework | Distinguishes manipulating material, generating inferences, and jointly developing ideas; discusses boundary conditions. | Inspect the learner's cognitive work. Sliders do not automatically make learning “interactive” in this sense; dialogue alone is not a guarantee. |
| [Kestin et al., 2025](https://doi.org/10.1038/s41598-025-97652-6), physics RCT | A structured AI tutoring package improved immediate performance in two introductory physics lessons against the tested active-class comparison. | Ground a tutor in verified content and reliable sequencing. This result does not isolate prompt quality, prove delayed retention, or establish superiority across subjects. |
| [Bastani et al., 2025](https://doi.org/10.1073/pnas.2422633122), classroom RCT | Assisted practice improved with both GPT conditions; the unrestricted condition harmed subsequent unassisted performance. The guarded tutor's unassisted estimate was statistically indistinguishable from control. | Evaluate after support is removed. Safeguards mitigating harm are not evidence of improved independent learning. Do not universalize this particular school/model/task result. |
| [Tutor CoPilot, 2025 version](https://scale.stanford.edu/sites/default/files/ai24_1054_v2.pdf), field experiment/working paper | Human tutors with access improved session exit-ticket results; the updated version reports over 700 tutors and 1,000 students and no significant end-of-year test improvement. | Human selection/override and session outcomes matter. Do not mix versions or equate a human+AI package with an autonomous tutor or long-term gains. |
| [Roediger and Karpicke, 2006](https://learninglab.psych.purdue.edu/downloads/2006/2006_Roediger_Karpicke_PsychSci.pdf), retrieval experiment | Testing schedules affected delayed recall of prose; immediate fluency and later recall diverged. | Reconstruct and use the taught model later. The study is not a universal retention rate, equal-time productivity estimate, or proof of mathematical transfer. |

The specific protocol below is a design inference informed by these sources. It still requires topic-specific tests. The sources disagree in setting and outcome; preserve those differences.

## Human tutoring practices to reproduce thoughtfully

Make expertise visible: verbalize what feature matters, how it changes the choice, what a good result should look like, how to check it, and what would trigger another method. Include uncertainty and legitimate alternatives. A polished final solution hides the recognition and monitoring that learners need.

Use a small readiness diagnostic, a worked case, or a labeled assumption. Do not infer readiness from age or one correct answer. Diagnose slips, prerequisite gaps, faulty relations, inappropriate strategy, misunderstood language, and defensible alternate interpretations differently.

Alternate modeling, coached completion, independent attempts, reflection, and transfer as useful. Fade help based on evidence. A beginner may need direct explanation; an experienced learner may need a difficult contrast. Do not force every learner through the same hint ladder.

Give specific, actionable feedback tied to the current attempt. Ask one diagnostic question if the cause is unclear. Let a learner state uncertainty. Use respectful encouragement without praising wrong reasoning or claiming understanding from “yes.”

Choose examples with variation: a clean case establishes the structure; contrasting/boundary cases distinguish where it applies; unfamiliar cases test transfer. Vary one important feature when isolating its effect, then deliberately vary multiple features for transfer. Do not mistake routine repetition for generalization.

## Additional requirements for AI tutoring

Use checked reference content, solutions, assumptions, common wrong rules, and known alternative methods. Generate feedback against the actual problem and learner state; do not infer it from a generic persona. Verify dynamic substitutions and tool results before teaching from them.

Separate learning from task completion. An answer can be useful when the user requests it, but completion with assistance cannot be scored as independent capability. Provide a worked answer when instruction requires it; do not adopt an absolute “never give answers” rule.

Keep explicit state and response branches; test contradictory explanations, partially correct work, right answer/wrong reason, guessing, requests for help, and nonstandard valid solutions. Allow uncertainty rather than invent a diagnosis. When relevant, route unresolved domain judgments to suitable human expertise.

A human+AI tutor should expose the reason for a suggested next move and allow the human to select, edit, or reject it. Do not represent assistant access as a replacement for the human's judgment.

## Two learner loops, distinct from authoring loops

The learner **outer loop** selects the next problem, concept, representation, level of support, or revisit based on evidence, prerequisites, purpose, and transfer needs. It considers what remains uncertain across several attempts. No arbitrary fixed mastery threshold should be invented.

The learner **inner loop** responds within the current problem: inspect the attempt → interpret the reason → choose a hint/model/contrast → retry with adjusted support → check and record evidence.

The authoring external/inner loops instead improve the course and explanation. Keep the terminology explicit in plans so a course revision is not confused with a learner's practice selection. A notebook with authored branches does not implement general practice selection by itself.

## Measurement and correction

Inspect learner-produced reasoning, not just correct outputs, completion, confidence, enjoyment, or clicks. Test interpretation, method choice, use/no-use decisions, failure diagnosis, mitigation choice, and new contexts. Separate assisted, immediately unassisted, delayed recall, and delayed transfer evidence.

For a history or writing lesson, valid reasoning may admit multiple conclusions. Use source warrants, coherent argument, constraints, and comparison rather than a rigid exact-answer grader. For practical skills, observe performance and recovery; verbal fluency alone is insufficient.

Record the evidence level and the strongest remaining uncertainty. Reuse validated teaching moves while allowing the subject and actual learner to change the route.

