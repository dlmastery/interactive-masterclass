---
name: build-interactive-masterclass
description: Research, debate, plan, build, and review an intuitive interactive tutorial or masterclass on a requested topic. Use for this user's substantial tutorial requests, including progressive mathematical explanations and notebook-backed slide courses. Start with the topic's purpose and mechanism; introduce prerequisites as needed. Do not turn a quick factual answer or small lesson edit into a full course project.
---

# Build an interactive masterclass

Produce a course that builds a usable mental model, then earns its formal explanation. A learner should be able to predict, explain, calculate when relevant, recognize limits, and transfer the idea. Correct code, slide count, attractive styling, and many controls do not prove good teaching.

This skill captures the user's corrections from the PCA course. For full tutorial requests, first configure and execute a topic-specific teaching harness: research, competing proposals, critique, synthesis, a representative working lesson, construction, and separate reviews. Do not merely write a plan saying these happened.

## Scope and defaults

- Recover the topic, audience, output, sources, existing work, and constraints. Infer routine choices; ask only about material unknowns while continuing independent work.
- Default audience: an interested 20-year-old. Assume normal intelligence, not prior graduate mathematics. Preserve depth while explaining new operations.
- Prefer native marimo-studio for this user's interactive notebook/slide courses. Preserve a different requested format. Verify the framework before promising features.
- Start with the target concept in action: its problem, mechanism, what changes, what remains, and why it matters. Use geometry for geometric topics and a grounded case or causal model for others.
- Introduce background at its first point of use. Do not front-load a separate algebra, statistics, terminology, or history course.
- Honor requested length. A minimum slide count is a floor, not a design method. Do not impose PCA's 64-slide count on every subject.
- Use clear ASD-STE100-inspired prose. Assess the user's target of at least 80% compatibility honestly using the language rules in the review reference.
- A quality gate is an internal check, not a new permission request. Continue reversible work already authorized. Wait for plan approval only when the user asks for that workflow.

## Execute the teaching harness

Read [the harness protocol](references/harness.md) for topic configuration, roles, state, and evidence. The coordinator uses available research, agent, implementation, and browser tools. `scripts/harness.py` records gates and detects stale evidence; it does not call agents or judge pedagogy by itself.

1. **Define observable outcomes.** Specify a fresh prediction, causal explanation, worked derivation or argument, counterexample, and transfer task. Record assumptions, scope, and the user's corrections.
2. **Research contrasting explanations.** Follow [research and debate](references/research-debate.md). Inspect substantive YouTube explanations and authoritative written sources. Compare teaching strategies, not just presenters. Record whether you inspected metadata, transcripts, representative video frames, or full videos. Popularity is a discovery signal, not an accuracy score.
3. **Debate before settling the sequence.** Request separate proposer/reviewer subagents when available and permitted. Use the three roles in the harness reference. Obtain proposals before cross-critique. If separate agents cannot run, use explicitly labeled sequential perspectives; never call them independent review. Record objections and reasons for the chosen route.
4. **Create the teaching plan.** Follow [lesson design](references/lesson-design.md). Specify narrative, misconceptions, notation, example lifecycle, prerequisite insertion points, conceptual transitions, proof route, interactions, assessments, and visual brief. Budget the central argument before refreshers. Share the concrete plan, then continue authorized work.
5. **Build a representative teaching sample.** Implement the opening intuition, the hardest intuition-to-formalism transition, and a failure or transfer scene in the actual framework. Repair their teaching and interaction before multiplying the pattern. A polished title slide is not a representative sample.
6. **Complete the course.** Keep one connected example until a deliberate counterexample or new task needs another. Every control must explain a relationship. Keep the central proof and limits in the main route. For Studio, read [the framework notes](references/marimo-studio.md).
7. **Review separately, then repair.** Use [review standards](references/review.md): correctness, progression, visual explanation, interaction fidelity, language, runtime, and transfer. Execute checks and log findings, repairs, and rechecks. Do not average away a broken proof or unreadable scene with successful build tests.
8. **Deliver with calibrated claims.** Provide the tutorial, source, notebook where relevant, plan, and evidence. Distinguish expert review, simulated learner review, and actual learner evidence. State the strongest unresolved teaching gap. Do not certify beauty or mastery from automated tests.

## Prevent the failures that caused this skill

- Every prerequisite bridge must name the target step it unlocks and immediately return to that step.
- Use additional slides to resolve actual transitions, not to inflate a count.
- Previous/Next and answer reveals are not substitutes for experimental interaction.
- A formula plus a short “why” can still hide the hard step. Show the operation, assumptions, and concrete meaning.
- A theme or screenshot is not evidence of visual teaching quality. Judge whether the picture reveals the mechanism.
- Never exhaust effort polishing setup while compressing or omitting the promised central derivation.
- Keep broad orientation and deep explanation: show where the topic fits, and trace how one complete example actually works.
- Preserve useful learner state across explanations, refreshers, and student interruptions where supported.

## Maintain the skill

Record which learner inference failed, why the scene failed to support it, and what changed. Add only specific lessons supported by feedback. Do not add unrelated governance or publication requirements.

For substantial changes, test a mathematical topic, a nonmathematical topic, and a small request that should not start a full harness. Label the creator's self-review as such. Record whether independent forward-testing actually ran.
