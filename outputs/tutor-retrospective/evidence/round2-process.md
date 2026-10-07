# Round 2 — practicality and enforcement critique

**Author-informed review.** I read the proposed process and both other round-one reports. I agree with their distinction between exposing operations and earning an inference. I challenge the proposed mechanism's size and several enforcement implications.

## Keep the evidence claim narrower than the process

The educator's concrete observations strengthen the need for purpose, the projection-to-score bridge, and an early explanation of variance versus reconstruction error. They do not establish that every topic needs the same opening, or that a live narrator would fail. The comparator report correctly marks transcripts, author articles, and unviewed animations separately. Preserve these distinctions in the synthesis; do not turn three reports into a consensus certificate.

Equal-time comparative learning and delayed retrieval are useful tests, but cannot be mandatory completion gates for every authored tutorial. They require learners, recruitment, timing, and consent beyond routine course creation. Require them only for corresponding effectiveness claims. A delivery may be an expert-reviewed candidate with human learning and retention unverified.

## Reduce three graphs to one small record with two edge types

Three separately maintained graph representations risk becoming the new sunk-cost activity. Use one `plan.json`: critical inference nodes, artifact/check nodes, typed dependency edges, and optional learner branch references. Render different views when useful; do not maintain duplicate graph files. Validate acyclicity only for prerequisite/production dependencies. Detour and retry transitions can loop and need explicit return targets.

Do not require an identical field set for every sentence or slide. Require the richer teaching contract only at consequential bridges. The runner should establish that the claimed obligations are linked and reviewed, not infer whether the example really explains anything.

## Minimum executable schema-2 contract

Keep the existing CLI and add only:

1. **Run scope:** mode (`audit`, `plan`, `build`), permitted artifact roots, intended delivery label, and an explicit review-before-build dependency when requested. In audit mode, build/delivery-as-course passes are invalid. The current retrospective must not receive a course-build permit.
2. **Named obligations:** stable node ID, kind, critical flag, dependency IDs, input artifact paths, and required review types. A few content fields hold purpose, intended inference, misconception, and learner task. Validate IDs, missing dependencies, and production cycles.
3. **Evidence receipts:** node, reviewed revision digest, report file digest, review type, reviewer relationship (`author`, `author-informed`, `fresh-context`, `human`), scenario, observed result, and limitations. Merely supplying a generic file is insufficient structure; the runner cannot determine whether its contents are truthful.
4. **Findings and attempts:** stable finding ID, affected nodes, severity, causal repair description, attempt events, and resolution evidence. Critical unresolved findings block a current pass. Two unsuccessful attempts block another local repair permit until a recorded strategy-revision event supplies a new hypothesis and test. Renaming an issue must not silently clear its history.
5. **`status`/`next`:** calculate current, stale, blocked, and unverified obligations; explain the exact blockers and next permitted action. Preserve schema-1 records read-only. Do not silently migrate old passes into stronger claims.

An append-only event log and an atomically replaced state snapshot are enough. Avoid databases, agent orchestration, browser integration, automatic rubric scoring, or a universal teaching engine in this change.

## What this can and cannot enforce

The CLI can reject invalid transitions, missing typed receipts, mismatched hashes, unresolved blocking findings, and exceeded local attempt limits. It can withhold a release record. It **cannot prevent direct file edits or tool calls**, prove reviewer independence, confirm video inspection, judge an inference, or establish learning. The skill/coordinator must obey the permits; review remains fallible judgment. Describe this as a guardrail, not end-to-end autonomous enforcement.

Hash the declared input manifest plus node contract and prerequisite revisions. Invalidate downstream reviews, not unrelated upstream research. Report manifest coverage explicitly: unregistered files are outside the freshness guarantee. Default to conservative invalidation for a shared component change; do not attempt automatic semantic change detection.

## Cost and decisive tests

Default limits should bound work, not manufacture evidence. Reuse sources and receipts still valid for the same audience and claim. Stop repeated unchanged reviews. Reserve effort for the hardest bridge before creating more scenes. Record actual limit changes with reasons; never imply a local action cap is a user token budget.

Test skipped critical dependencies, stale source with unchanged review, unresolved findings, two failed repairs, bounded strategy revision, unrelated-node preservation, audit-mode build rejection, legacy status, and human review remaining unverified. Then execute a small mathematical and nonmathematical planning scenario. Passing these tests establishes workflow integrity only. The next course rebuild still waits for the user's review of this proposal.
