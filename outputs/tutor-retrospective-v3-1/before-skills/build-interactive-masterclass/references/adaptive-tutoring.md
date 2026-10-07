# Per-problem tutoring runtime

Read only for authored branches, student questions, live tutoring, or stateful feedback. This skill and its CLI do not implement a runtime tutor.

Use [tutoring-evidence.md](tutoring-evidence.md) for evidence-informed practices and their limits. Distinguish authoring revision from two learner loops: the learner outer loop selects the next problem/concept/representation/support level; the learner inner loop responds to a step within the current problem. Both should change behavior based on evidence, not merely follow a script.

Maintain goal, problem version, current question, representation state, learner attempt, reasoning evidence, assistance, pending action, detour stack, and return point. Separate observations from inferred mastery. Avoid unnecessary personal data. Explain storage lifetime; microphone or tab capture needs a user start action and consent.

Across problems maintain demonstrated capabilities, uncertain prerequisites, recurring wrong rules, assistance needed, contexts tried, use/no-use judgments, mitigation/alternative choices, and later-revisit evidence. Record observable evidence and uncertainty rather than an invented precise mastery score. Select a new task that resolves the important uncertainty while preserving the learner's purpose.

The practice-selection outer loop chooses among prerequisite support, another guided case, a varied independent problem, a boundary/alternative decision, more distant transfer, or consolidation/revisit. Use several observations where feasible; one lucky answer does not establish readiness. Do not keep serving easy repeats to inflate apparent success. Progression should reduce assistance and vary context when evidence supports it, or reopen the relevant prerequisite when it does not. Preserve meaningful learner choice and permit an honest skipped/unverified state.

| Observed state | Tutor response | Evidence to continue |
|---|---|---|
| Entry knowledge missing | Short direct model/worked example, then a smaller task | Uses the required operation |
| Right answer and supported reasoning | Fade a scaffold; change the case | Unaided application |
| Right answer, faulty rule | Discriminating case | Corrected reasoning applied |
| Wrong answer, identifiable rule | Address that specific relation | Retry with less help |
| Ambiguous/contradictory reasoning | One diagnostic question; allow “not sure” | Unknown is not labeled wrong |
| Stuck | Hint, smaller case, worked step | No repeated interrogation |
| Skipped check | Permit honest navigation | Status stays unverified |
| Side question | Save state; answer or bounded detour | Return or explicit goal change |

On interruption, stop stale speech/animation where supported. Save the scene, open question, work, and pending action before a detour. Restore them afterward. Changed inputs invalidate old feedback. Separate assisted and independent attempts.

Use worked example → completion task → unaided problem → transfer when suitable. Retrieval should reconstruct and use a model, not only labels. Later retrieval checks retention; schedule it only when requested. Immediate correctness is not delayed retention.

Distinguish a calculation slip, missing prerequisite, wrong relation, inappropriate strategy, confusing wording, and a defensible alternative solution. Verify model-generated hints against checked reference content and the current state. Make practitioner thinking visible: recognize conditions, select a method, check the result, detect a limitation, choose a mitigation or alternative. Assess those decisions in addition to answers. For interpretive subjects, permit multiple well-supported conclusions rather than exact-string grading.

Support human tutors with reasons for suggested next moves and preserve their ability to edit or reject them. Respond respectfully to uncertainty and frustration without inferring an emotional diagnosis. Direct explanation or a worked answer is appropriate when needed; “never give answers” and endless Socratic questioning are not universal rules.

Static courses must state which branches they support. Free-form model feedback needs the exact problem and visible state, uncertainty handling, and tests for right-answer/wrong-reason, ambiguity, contradiction, and off-topic input. A few multiple-choice branches are not general adaptation.

Verify interruption, restart, back/forward, detour return, feedback invalidation, and failure fallback in the actual interface. If implementation is out of scope, label this a runtime design and leave execution checks unperformed.

