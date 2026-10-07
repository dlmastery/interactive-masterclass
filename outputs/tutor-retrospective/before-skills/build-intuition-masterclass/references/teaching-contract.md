# Teaching record and regression scenarios

Use this reference to make a per-topic plan inspectable and testable. Keep the record in the current project's existing documentation where practical. One structured document can hold these sections; do not create a folder of empty process artifacts.

## Minimal record

### Audience and outcomes

State the learner's context, known prerequisites, unknowns, intended outcomes, and constraints. Define observable transfer, not "understand the topic." Label all assumptions. Distinguish requested depth from demonstrated readiness.

### Explainer comparison

For each inspected source record its URL, inspected material or time range, evidence type, opening, explanatory route, learner work, strengths, limits, and influence on the plan. Mark inaccessible evidence. State how the compared approaches differ.

### Route decision

For each candidate record the concept order, strongest justification, strongest objection, and audience fit. Record reviewer independence honestly. State what evidence caused selection or revision; do not invent a completed debate after building.

### Step contract

Use these fields for each conceptual bridge:

| Field | Required meaning |
|---|---|
| Step ID and question | The uncertainty this step resolves |
| Entry evidence | Prerequisites demonstrated, assumed, or still unknown |
| Change in understanding | What the learner should newly be able to explain |
| Example and boundary | Concrete case and where its analogy stops working |
| Learner action | Prediction, manipulation, construction, explanation, or practice |
| Response branches | Correct reasoning, common error, ambiguity, and request for help |
| Feedback | Specific response and next action for each branch |
| Check | Observable success and what does not count as success |
| Detour and return | Smaller subgoal, return state, and conditions for resuming |
| Visual contract | Objects, labels, units, invariants, transitions, pointers, and retained history |
| Exit | Next step or alternative route, with rationale |

The teaching contract precedes the visual contract. A diagram cannot rescue an undefined learning step.

### Review and evidence

Record each gate as pass, fail, or not tested, with evidence and remaining limits. Evidence from a previous revision must be labeled and rechecked for changed behavior. Keep user acceptance separate from automated checks.

## Cross-topic review scenarios

These are process tests, not mandatory examples in every tutorial. Substitute examples that match the subject and audience.

### PCA for a curious adult without recent linear algebra

- Ask why one coordinate could be useful before assuming compression is motivating.
- Trace one observation from data to projection, score, and reconstruction. Can the learner name what was lost?
- Compare two directions before introducing the optimization notation. Can the learner explain the criterion instead of repeating "largest spread"?
- Reach covariance through quantities the learner has already computed. Does the matrix summarize something they recognize?
- Test the distinction between rotation and discarding a coordinate, and between retained variance and usefulness for a downstream task.
- Supply a correct score with an incorrect reason. Numeric correctness must not be labeled conceptual mastery.
- Return from an eigenvector refresher to the same experiment. Verify saved answers and settings.
- Preserve requested mathematical depth. Mark any theorem invoked without proof; do not claim a stationary point alone proves a global maximum.

### Fractions for a younger learner

- Establish what one whole is and what the denominator counts. Do not infer this knowledge from grade.
- Subdivide the existing strip to compare equivalent fractions. Preserve the whole and selected area.
- Respond to "does six mean six shaded pieces?" with an appropriate diagnostic or explanation, not a prepared lecture.
- Ask for an equivalent fraction on a new example without giving the subdivision first. Distinguish independent reasoning from a copied pattern.

### Photosynthesis for a beginner

- Choose an entry question that creates a need to track matter and energy.
- Separate what enters, what changes, and what leaves. Arrows must mean a stated process, not vague motion.
- Use an authoritative reference for the mechanism. Mark where an analogy breaks.
- Diagnose the claim that a plant's mass comes mainly from soil with evidence and a suitable task.
- Provide a counterfactual prediction and explain the limits of a simplified simulation. Do not present a toy model as an experimentally validated system.

### General failure and interaction checks

- Learner changes an input after receiving feedback: feedback must be cleared or recomputed.
- Learner leaves and returns: preserve or explicitly restore attempt, experiment, and explanation state.
- Learner asks an unrelated question: clarify whether to detour or change the goal; do not silently replace it.
- Learner cannot answer an open question: offer a smaller task or direct explanation, not repeated interrogation.
- Learner skips a check: allow honest navigation without awarding understanding.
- Renderer or voice fails: preserve the teaching state and provide a truthful fallback.
- A beautiful scene has no learner task or clear explanatory role: simplify or replace it.
- Only transcripts were read: do not claim the original animations were evaluated.
- Only build tests passed: leave interaction and teaching gates unverified.
