# Round 1: process and harness retrospective

**Review status: author-informed, not independent.** I reviewed the earlier visual regressions and authored the light-layout CSS and product-expansion component during the repair. I have not read the new educator retrospective. This report audits process evidence and proposes a design; it does not authorize or perform another course rebuild.

## Evidence and its limits

I read both installed skills, every linked reference, `build-interactive-masterclass/scripts/harness.py`, and `work/test_tutorial_harness.py`. I sampled the PCA assessment, README, original and repaired browser audits, runtime records, and my earlier visual review.

Both skills already prohibit prerequisite-first teaching, decorative controls, unsupported mastery claims, and treating correct mathematics as teaching evidence. Both require contrasting approaches, critique, a checked plan, and a difficult teaching sample before expansion. The intuition skill also requires state recovery, conditional feedback, and changing approach after two unsuccessful repair passes. These are substantial rules, not absent aspirations.

No `run.json` was found by a recursive filename search under this project's `work/` and `outputs/`. That establishes missing local execution records, **not proof that research, debate, or review never occurred**. The historical assessment positively records two transcript-based comparisons and missing independent competing-plan/cross-critique evidence. The later repair has actual agent reports and browser checks. Its audit records rendered slides, pointer availability, formula errors, and selected numerical interactions; these observations do not record unfamiliar learners' reasoning.

The assessment's broad phrase “three independent agent reviews” needs narrower provenance. Separate agents can inspect separately, but shared history, author involvement, and coordinator framing affect independence. My current review is explicitly author-informed.

## Why written rules did not control behavior

1. **The workflow was optional in execution.** `harness.py` accurately calls itself an evidence recorder. It does not dispatch or authorize work. Course editing, building, and a ready-sounding response remain possible without opening a run or passing a gate. More instructions alone will not close that gap.

2. **Passes are self-attestations attached to arbitrary files.** `record()` requires a nonempty note, an existing evidence file, and earlier fresh passes. It does not require a scene reference, observed failure, reviewer provenance, tested revision, or resolution of objections. Its tests deliberately pass the same short file through all stages to test sequencing. That is a valid structural test and also demonstrates that “all gates current” cannot mean “all work executed.”

3. **Freshness is about registered bytes, not the delivered system.** A review report can remain unchanged while the course changes. Unless every relevant artifact is listed, its pass remains fresh. Conversely, the single ordered chain invalidates every later stage for any recorded upstream change, even if unrelated. This encourages either excessive rework or loose registration. Runtime records include build hashes; the browser summary does not bind its observations to the exact code/content/environment manifest.

4. **The difficult inference had no enforceable owner.** “Explain covariance” could be satisfied by a formula, a product table, or an actual row/column accumulation. A scene-level promise and a global build pass were not joined by an acceptance observation. The historical assessment identifies precisely this mismatch on slide 27 and the gradient/constraint transition. Later repairs address it, but do not retroactively establish the earlier gate.

5. **Corrections triggered production, not hypothesis revision.** The course expanded, changed theme, and gained controls before a decisive sample established the teaching route. My own responsive repair initially made the opening controls fall below the fold. Root had to correct that after rendering. This is counterevidence to treating a plausible visual recommendation as a passed teaching sample.

6. **Duplicate skills create uncontrolled divergence.** Both names broadly trigger on the same request. One has a linear recorder and specific Studio notes; the other has richer runtime teaching-state contracts and a light-theme default. There is no canonical owner, shared version, or migration rule. The assistant can follow a convenient subset without noticing disagreement or omissions.

7. **Sunk effort was not bounded.** “Two repairs” exists only in prose; the recorder has no issue identity, attempt count, reserved core-work allocation, or stop transition. Countable outputs—slides, equations, control counts, builds—can accumulate while the same learner inference remains untested.

## Smallest maintainable harness

Keep **one canonical skill**, one schema, one runner, and one event log. Retain the other skill name only as a compatibility redirect. Keep framework-specific lessons in a short adapter reference. Do not build a general governance platform.

The runner controls supported execution actions, rather than merely accepting `pass` afterward. Manual tool use remains possible; therefore disclose the enforcement boundary and refuse a harness-certified delivery when required action receipts are missing. This is workflow integrity, not a claim that software can automatically judge pedagogy.

### Outer loop: author and revise the teaching system

Contract → inspected evidence → competing routes → adjudicated teaching graph → representative pilot → construction → separate reviews → delivery. The graph permits returning to the actual failed decision. It is not an eight-document waterfall.

Each consequential decision stores alternatives, strongest objections, why one route was chosen, the observation that could falsify it, and the pilot that tests it. Research records modality honestly: transcript evidence supports wording and order; a claim about an animation needs viewed visual evidence. The opening, hardest representation-to-reasoning bridge, and transfer scene are tested before repeating their design across the course.

### Inner loop: execute one problem or conceptual bridge

Each topic supplies a **teaching graph**, not a fixed slide template. A node records the learner's question, intended inference, prerequisite evidence or assumption, example, representation, action, expected reasoning, likely error, ambiguity handling, feedback, and next step. Dependencies distinguish “must already know,” “can learn here,” and “optional detour.” A node can be direct explanation; not every node needs a quiz.

At runtime: present the problem → obtain or explicitly assume entry evidence → explain/act → capture the attempt and reasoning → interpret with uncertainty → give targeted feedback → transfer or bounded detour → restore the original state. Preserve the current question, learner work, pending action, scene state, and return point. Correct numbers with wrong reasoning must follow a different branch from demonstrated understanding.

For a static course, author these branches and disclose that arbitrary reasoning is not diagnosed. For an adaptive application, these transitions require actual application wiring and replayable events. Neither a Markdown graph nor a CLI recorder is a deployed tutor.

## Gates that can actually block

Represent each review as `{node, claim, artifact_revision, scenario, observed_trace, inference, severity, reviewer_provenance, disposition}`. Attach tool/build receipts and relevant source hashes. A finding must describe a learner-visible failure or supported inference, not “8/10 clarity.”

The runner blocks dependent construction when a required pilot has an unresolved critical finding. Delivery requires current artifact-bound runtime evidence and separate correctness, visual-interaction, and teaching reviews. Author review, unfamiliar simulated review, and actual learner evidence remain distinct states. Missing evidence is **unverified**, not failure and not pass.

Changing a node, example, notation, content source, component, or environment invalidates dependent claims through recorded edges. Unaffected checks remain usable. A user's rejection records an event against the affected claim and reopens its decision; it cannot be cleared merely by generating more slides. Explicit review-before-rebuild requests place an approval dependency before implementation. That dependency is pending for this retrospective's proposed rebuild.

Track an issue fingerprint and repair attempts. Two failed attempts at the same inference trigger route/representation reconsideration and stop expansion of that pattern. Allocate remaining effort to the core argument and verification first; if unavailable, reduce scope with an honest draft status. Do not invent a user token budget. A declared local work allocation is a planning limit, not user authorization or evidence of quality.

Test the runner against stale code with unchanged reports, unrelated changes, copied generic evidence, rejected feedback, wrong-method/right-answer cases, detour restoration, and missing runtime wiring. Test the process on one mathematical and one nonmathematical topic, plus a small request that must avoid the full harness.

## Rival explanation and counterevidence

Framework instability and rapid scope growth plausibly caused some failures. Real sandbox, state, viewport, and nested-section problems consumed effort; the original 14-slide version also could not satisfy the later depth requirement. However, technical instability does not explain accepting an untested teaching route, changing the visual baseline without preserving its advantages, or substituting frame counts for learner reasoning. Conversely, actual numerical/runtime work and concrete repair observations refute “nothing was tested.” The failure is misaligned acceptance and execution control, not a total absence of effort or useful evidence.
