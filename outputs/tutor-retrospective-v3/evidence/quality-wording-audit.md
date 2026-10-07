# Narrow wording change and quality-first consistency audit

6 October 2026. Author-informed review: I contributed the schema-2 guardrail and earlier course work. No PCA file was changed.

Changed only the two requested error messages in canonical `scripts/harness.py`, from “Repair cap reached” to “Strategy review required; changed hypothesis and fresh pilot needed before another local repair.” Updated four existing test assertions to match the new message prefix. The conditions, threshold, state changes, required fresh pilot, and preserved history are unchanged.

Executed the installed `scripts/test_harness.py`: **17 tests passed**, including the test that blocks repeated local repairs until a changed strategy and fresh pilot exist, then allows continued work. Output is saved in `harness-tests.txt`. These are guardrail behavior tests, not teaching or learner evidence.

The revised canonical SKILL.md, execution-quality.md, harness.md, lesson-design.md, content-contract.md, and research-debate.md consistently prioritize quality, permit 100-plus slides, avoid invented duration/source ceilings, and distinguish authoring effort from learner time. The codelab entrypoint and course-standard.md now carry the same standard; the old generic three-image ceiling is explicitly superseded. I found no remaining substantive fixed slide/time/authoring-attempt ceiling in the inspected material.

Two minor terminology remnants remain for the coordinator's documentation pass:

- `references/review.md` still names a forward-test scenario “capped repeated failure.” Prefer “repeated failure requiring strategy revision.”
- `references/harness.md` still says relabelling cannot “reset the cap.” Prefer “satisfy the strategy-review requirement.” These are wording ambiguities, not current instructions to stop all work.

Retain real experimental budgets, protected evaluation limits, laptop paths, and matched-time comparison controls in the codelab references. They constrain scientific validity or declared resources, not overall teaching quality. Likewise, a bounded learner detour or framework feasibility probe protects scope and need not become an authoring ceiling.

The narration/tutoring references were still being written by the coordinator during this snapshot; this audit does not claim to have inspected their final versions. No other installed files were edited.
