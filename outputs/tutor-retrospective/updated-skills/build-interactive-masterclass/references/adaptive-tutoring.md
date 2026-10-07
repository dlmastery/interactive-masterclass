# Per-problem tutoring runtime

Read only for authored branches, student questions, live tutoring, or stateful feedback. This skill and its CLI do not implement a runtime tutor.

Maintain goal, problem version, current question, representation state, learner attempt, reasoning evidence, assistance, pending action, detour stack, and return point. Separate observations from inferred mastery. Avoid unnecessary personal data. Explain storage lifetime; microphone or tab capture needs a user start action and consent.

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

Static courses must state which branches they support. Free-form model feedback needs the exact problem and visible state, uncertainty handling, and tests for right-answer/wrong-reason, ambiguity, contradiction, and off-topic input. A few multiple-choice branches are not general adaptation.

Verify interruption, restart, back/forward, detour return, feedback invalidation, and failure fallback in the actual interface. If implementation is out of scope, label this a runtime design and leave execution checks unperformed.

