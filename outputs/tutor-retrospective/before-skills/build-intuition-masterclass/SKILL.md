---
name: build-intuition-masterclass
description: Research, plan, build, and assess progressive interactive tutorials that form deep intuition about a topic. Use for tutorial, explainer, or masterclass creation and substantial teaching redesign across subjects. Compare diverse explainers, debate teaching routes, and check the teaching plan before visual implementation. Not for a short factual answer or an unrelated cosmetic edit.
---

# Build an intuition-first masterclass

The outcome is a learner who can predict, explain, apply, and question an idea. A long course, attractive diagrams, working sliders, or correct equations do not establish that outcome.

Start a fresh teaching plan for each topic and audience. Reuse the process, not a fixed sequence of slides. Do not silently replace an existing platform or rebuild work when the user only asked for an assessment.

## 1. Establish the teaching contract

Inspect the user's feedback and any existing tutorial, source, and test evidence. Separate what exists from what is promised. Preserve useful work, but reopen any teaching decision the user has rejected.

Record these facts in a compact teaching record in the project:

- Topic, intended learner, available time, and delivery format.
- What the learner wants to do and why the topic matters to them.
- Observable outcomes: what they will predict, explain, construct, calculate, or transfer without help.
- Known prior knowledge, unknown prior knowledge, and explicit assumptions. Grade or age is context, not evidence of mastery.
- Essential concepts and their dependencies. Identify the hardest conceptual bridges.
- Scope boundaries, required depth, and how learner feedback will be obtained.

Ask only questions that change the teaching route. Use a short diagnostic or a clearly labeled planning assumption when appropriate. Do not claim to remove all assumptions. Do not infer knowledge from silence or an ambiguous answer.

For a parent or funder demonstration, establish the need, the experience, and the value before starting a lesson. Distinguish the observer's tour from the student's actual journey. Do not make an ordinary learner read education jargon.

## 2. Research different ways to explain the topic

Research before committing to a teaching route. Seek genuinely different approaches, not several sources that repeat the same explanation. For a substantial masterclass, aim to compare at least three approaches where sources permit, including varied YouTube explainers and an authoritative technical or subject reference. Source count is not a quality score.

Inspect the explanation itself. Record whether the evidence is a transcript, viewed video segment, article, paper, or interactive activity. For videos, keep useful timestamps when available. A title or search snippet cannot support claims about pacing, animation, or teaching quality. A transcript supports claims about words and sequence, not unseen visuals. If access is blocked, disclose it and use accessible alternatives; do not fabricate a video review.

Compare:

- The opening question and motivation.
- What knowledge is assumed and when new terms appear.
- The analogy, concrete example, and route to a general model.
- How a visual becomes a calculation or an explanation.
- What the learner must do, rather than watch.
- Likely misconceptions, omitted steps, and limits of the analogy.

Keep a short source ledger with links, inspected sections, useful moves, risks, and the design decisions they informed. Check subject claims against authoritative sources. Popularity is not evidence of correctness or suitability. Synthesize original teaching; do not copy an explainer's script or reproduce protected material.

## 3. Debate the teaching route before designing screens

Develop at least two materially different routes. Examples include a concrete problem first, a visual experiment first, or a worked case followed by generalization. Do not make one route deliberately weak.

Review each route from three perspectives:

1. Subject reviewer: Are the statements true? Are prerequisites, units, conditions, and counterexamples handled?
2. Teaching reviewer: What mental model changes? Which bridge is too large? When should the tutor explain directly instead of asking another question?
3. Novice interaction reviewer: What does the learner see, try, and infer? Could they operate every control yet learn nothing?

Use separate reviewer agents when available and authorized. Give them the audience, raw sources, candidate routes, and criteria before the author's preferred decision. Otherwise perform explicit role-based critiques and label them as self-review, not independent judgment.

Keep the strongest objection to each route, the selected route, rejected alternatives, and unresolved risks. Agreement among models does not prove teaching effectiveness. Select by learner needs and evidence, not vote count.

## 4. Compile and check the teaching plan

Read [the teaching contract and review scenarios](references/teaching-contract.md) when preparing or reviewing a plan. Use its fields at conceptual bridges, not as paperwork for every sentence.

For each meaningful learning step specify:

- The question that creates a need for this idea.
- What the learner already needs to know, and the evidence for that belief.
- One intended change in understanding.
- The example, prompt, expected reasoning, and likely wrong or ambiguous responses.
- A useful learner action and the feedback it causes.
- A fallback explanation, smaller example, or prerequisite detour.
- Evidence needed before claiming the learner understands.
- How this step connects to the next idea and to the original purpose.

Build a broad map first, then deepen the ideas progressively. Introduce prerequisites at the point of need when that is clearer than a long preliminary course. Let rigor emerge from an example the learner understands. Do not remove the requested proof or advanced layer merely to make the course feel easy.

Use this learning cycle where it fits: encounter a need, predict, manipulate or attempt, observe, explain, then transfer. Do not force every small step through the entire cycle. Alternate concise direct explanation with genuine questions. Avoid guessing games, constant permission requests, and repeated demands to say "continue."

Teaching-plan gate: check accuracy, prerequisite coverage, mental-model changes, misconception responses, transfer, scope, and assumptions. Fail the gate for an unexplained conceptual leap, false claim, missing critical information, or activity with no learning purpose. Repair the plan before polishing screens. A reviewer must cite the failing step and a concrete failure scenario; vague praise or a numerical score is insufficient.

For a build request, show a concise plan and proceed through the checks within the authorized scope. Do not make every internal gate a new user approval request. For a plan-only request, stop before implementation.

## 5. Design the visual explanation from the checked plan

Each scene must answer a teaching question. Write its visual states, learner actions, feedback, and exit condition before implementation.

- Begin with the problem's meaning, not a wall of terminology or a finished formula.
- Use stable objects, labels, units, and scales. Connect symbols to the exact visual objects they name.
- Show what changes and what stays fixed. Link a changed input to its effect and its reason.
- Transform the current diagram when possible. If a new representation helps, explain the mapping and preserve a comparison. Do not replace a strip with a pie chart without a teaching reason.
- Draw, highlight, and point at the relevant object as it is explained. Reveal only the necessary part. A moving cursor without a linked explanation is decoration.
- Remove temporary marks selectively. Preserve student work and important previous states. Do not erase the whole board to avoid managing it.
- Use code-native diagrams for geometry, data, processes, and exact labels. Do not add generated imagery when a precise diagram does the job.
- Use a light, clean background by default for this user's tutorials. Keep labels legible, controls close to their effects, and visual emphasis restrained. Preserve a different theme only when the user chooses it for that work.
- Provide keyboard operation, non-color cues, reduced motion, and readable narrow layouts. Voice, when in scope, must agree with the visible step and have a text alternative.

A slider alone is not a lesson. Add a meaningful prediction, contrast, explanation, or task. Do not reveal the answer before a prediction task unless the learner chooses a worked example. Do not equate animation count, slide count, or interaction density with quality.

Presentation-plan gate: mentally trace the visual states against the teaching plan. Check bounds, labels, overlap, dimensions, and whether each transition preserves the argument. Prototype the hardest conceptual bridge before building the full course. If the bridge still needs outside narration to make sense, revise it.

## 6. Make the journey responsive and recoverable

For an adaptive tutor, keep explicit state: original goal, current step, learner evidence, open question, detour stack, return point, and saved board states.

When the learner asks a question:

1. Stop stale speech, animations, and queued actions when applicable.
2. Identify whether they need clarification, a prerequisite, another representation, or a different goal.
3. Preserve the board and pending task. Create a bounded subplan if a detour is useful.
4. Explain and check the detour without asserting understanding from an acknowledgment alone.
5. Offer a clear return to the original step, or revise the route if the learner changed the goal.

Questions are not interruptions to ignore. Nor should every question restart the entire course. Unknown reasoning is not wrong reasoning. A correct number can result from a wrong method. Distinguish hints, assisted success, and independent transfer.

Keep revisitable multimodal notes: meaningful board snapshots, learner attempts, explanations, and conclusions. Back/forward navigation must not silently discard answers or experiment state. Explain storage lifetime and privacy; do not record microphone or tab content without the user's start action and consent.

A static tutorial can provide authored branches and explicit review limits. Do not claim it diagnoses arbitrary reasoning. If free-form feedback uses a model, ground it in the exact task and board state, allow uncertainty, and test wrong, ambiguous, and contradictory explanations.

This authoring skill is not a runtime tutoring engine. If the user asks for per-problem runtime planning, implement versioned planning, review, presentation, and execution stages in the application. Document which stages are actually wired into the UI. Do not call a Markdown file a deployed harness.

## 7. Verify separately, then report honestly

Maintain separate evidence for:

1. Subject correctness: equations, computations, invariants, edge cases, claims, and analogy limits.
2. Interaction correctness: exercise real controls, input paths, state restoration, detours, and accessibility in the delivered interface. A build is not a browser test.
3. Teaching usability: have an unfamiliar reviewer attempt the learner tasks with only learner-visible help. Record their predictions, confusion, reasoning, recovery, and transfer attempts. Do not coach the test to the expected answer. A simulated novice is not evidence from real students.
4. Visual quality: inspect representative rendered states at intended sizes, including failures, intermediate states, dense labels, and saved history. A screenshot is not proof of a working interaction.

Use the regression scenarios in the reference. Correct numbers with faulty reasoning, navigation loss, failed detours, and persistent user confusion block teaching acceptance even if all builds pass.

Repair failed gates within the task's scope. After two failed repair passes for the same teaching issue, report the evidence and revise the approach rather than repeating cosmetic edits. If more authority, learner evidence, or domain review is needed, state what is missing.

Report precise states: plan reviewed; prototype; interactions verified; simulated novice reviewed; learner acceptance pending. Never promote these into "mastery proven" without appropriate evidence. A user rejection reopens the relevant gate.

Write in clear, short, active sentences. Define technical terms when first needed and use them consistently. Follow ASD-STE100-inspired principles when requested, but do not claim formal compliance from a sentence-length script.

Keep the teaching record, implementation, and verification evidence aligned. At handoff identify the strongest remaining gap and the next concrete test. Do not use "beautiful," "intuitive," or "masterclass" as substitutes for evidence.
