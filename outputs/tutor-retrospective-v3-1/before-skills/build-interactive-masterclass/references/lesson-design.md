# Design the inference, then its presentation

Read [content-contract.md](content-contract.md) alongside this reference. The inference route must support the complete promise, including when/where to use the idea, applications, limitations, mitigations, alternatives, and best practices. These are connected decisions, not an appendix added after the mathematical explanation.

## Purpose before the syllabus

Begin with a consequential question at the learner's level: a choice, prediction, explanation, construction, failure, or intellectual puzzle. State what the lesson enables. A named application or numerical example is insufficient if the learner cannot see why the task matters. Do not invent a commercial story when curiosity supplies the purpose.

Show the idea in action early. Expose an insufficiency in the current rule. The next concept should resolve it. Use a stable example until a deliberate contrast or new context teaches something it cannot. Return to the opening question after formal development. A motivating story alone does not justify an arbitrary later objective.

## Three graph views, one compact record

Maintain a compact route first. Add fields or generated views only where dependencies, revisions, or runtime branches justify them. Do not require three separate graph documents.

1. **Outcome and inference view:** changes in what the learner can reason about. Edge meanings include requires, motivates, represents, justifies, applies-in, fails-when, detected-by, mitigated-by, trades-off-with, alternative-to, and transfers. Prerequisite edges are acyclic within the chosen entry contract; revisits can loop. Break apparent prerequisite cycles with an entry example or provisional model, marking what is deferred.
2. **Per-problem state view:** attempt, uncertainty, feedback, help, detour, retry, transfer. The same answer may have different causes. Use adaptive-tutoring.md when these transitions must run in an application.
3. **Artifact dependency view:** contracts, content, code, reviews, and evidence depend on exact revisions. Changed inputs reopen affected claims. This view is distinct from concept dependencies.

The learner sees a short route of useful questions and their location. An internal dependency graph is not the learning map.

A full route connects purpose → method → validity → application → failure → diagnosis → mitigation with residual cost → alternative decision → transfer. Not every subject has the same kind of proof or mitigation. Add current-evidence links to modern application nodes. Link spoken script, figure state, and assessment to the same scene ID so a changed example cannot leave stale narration unnoticed.

## Critical bridge contract

Use a paragraph or row for each bottleneck, not a form per sentence. Include only fields needed to make the inference reviewable:

| Field | Decision |
|---|---|
| Need and entering model | Why the idea is needed; what the learner currently believes or can do |
| Target capability | New prediction, explanation, operation, justification, or distinction |
| Witness and representation | Example, contrast, trace, or diagram that exposes the relation |
| Bridge and validity | Familiar objects mapped to the new model; usefulness; assumptions, units, or evidence warrant |
| Learner work | What the learner supplies and what software/tutor supplies |
| Wrong rule and feedback | Plausible misconception, discriminating case, specific help |
| Exit and next use | Unassisted check, next question, deferred claims |

Example: in queueing, average demand below service capacity does not explain persistent waiting. Contrast evenly spaced arrivals with a burst at the same mean. Trace arrival, service, and leftover work. Ask which new schedule creates a queue and why. A time control helps only if it exposes the relation. State the toy model's assumptions before generalizing.

## Background at the point of need

Attach every refresher to a step: “We need this to do X,” one sufficient example, immediate use in X, and a return point. A small initial foundation may be necessary; do not prohibit it mechanically. Distinguish demonstrated, assumed, and unknown prerequisites.

Reserve the main mechanism, proof/argument, limits, and transfer before expanding preparation. A minimum slide count is a format constraint, not a sequence generator. Add screens to resolve inference or attention demands.

There is no generic slide ceiling. Use 100-plus slides when the explanatory depth warrants it, with chapters and progressive layers to protect learner attention. Audience routes may share a core without forcing every learner through every specialist branch. Do not remove a promised derivation or application to fit an arbitrary run time.

## Formal reasoning without hidden bridges

For an important mathematical step show the current question, operation, reason it is valid, assumptions, and meaning in the original problem. Map symbols, dimensions, indices, and units to the example. Distinguish definition, observation, identity, approximation, theorem invoked, necessary condition, and sufficient/global guarantee.

Numerical agreement illustrates an identity but does not prove it generally. State when a theorem is used without proof. In nonmathematical lessons, apply the same discipline to causal claims, interpretation, competing explanations, evidence quality, and inference limits. Do not force every subject into equations or a causal model.

## Attention and interaction

Choose a representation suited to the relation: geometry, flow, counts, timing, evidence, comparison, or system trace. Keep labels, units, scales, and semantic colors stable. Show the change and invariant together. Synchronize pointers, reveals, text, and voice with the exact operation.

Critical interactions need an explanatory job: prediction, counterfactual, construction, or diagnosis. Direct explanation and quiet reading remain useful. Avoid a compulsory seven-click ritual.

Keep the prompt, operation, and needed evidence within attention at intended viewport sizes. If scrolling is necessary, preserve the referenced diagram or clear return anchor. Provide keyboard paths, non-color cues, reset, reduced motion, and state recovery. Prototype dense and intermediate states, not just opening screenshots.

