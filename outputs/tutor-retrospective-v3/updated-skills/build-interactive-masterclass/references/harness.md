# Coordinator workflow and executable guardrail

This is a coordinator-driven teaching process, not an autonomous model service. The CLI validates registered records and dependencies. It cannot verify truth, learning, independence, source inspection, or prevent direct tool edits.

## Use the smallest appropriate record

A small answer or correction does not need a run directory. For a substantial build or process audit, keep one compact contract in the project's work area: scope/mode, learner purpose, audience/readiness assumptions, promised capabilities, central inferences, source decisions, pilot obligations, constraints, work limits, and next action. Existing project formats can hold teaching detail; the JSON below only captures machine-checkable obligations.

Read research-debate.md before selecting a route; content-contract.md for full coverage; lesson-design.md for critical bridges; execution-quality.md and review.md for acceptance evidence. Give separate initial proposers the same brief without a favored answer, then cross-critique. Start with serious alternatives and expand when unresolved strategic questions warrant it. Do not treat a small source/pilot count as a quality ceiling.

Protect the core argument, full subject coverage, narration, and verification. Quality takes priority over an arbitrary production time or slide count. Record real user/tool/resource limits; do not invent a user token allowance or automatic global stop. Two failed local repairs trigger a different strategy and fresh pilot, not delivery of an unresolved explanation. Continue authorized work when new evidence supports a useful next iteration. Stop unchanged reviews; a genuine external limit requires a checkpoint with the remaining quality gap, not a false completion claim.

## Version 2 CLI

Requires standard-library Python. Paths in a contract are relative to its directory; paths in receipt/repair evidence are relative to that JSON file. Use absolute paths where ambiguity would matter.

```text
python <skill>/scripts/harness.py init work/tutorial-run --contract work/contract.json
python <skill>/scripts/harness.py check work/tutorial-run --node bridge --action review
python <skill>/scripts/harness.py record work/tutorial-run --file work/bridge-receipt.json
python <skill>/scripts/harness.py status work/tutorial-run
python <skill>/scripts/harness.py finding work/tutorial-run --file work/finding.json
python <skill>/scripts/harness.py repair work/tutorial-run --file work/repair.json
python <skill>/scripts/harness.py strategy work/tutorial-run --file work/strategy.json
```

`check` returns the current node revision and input hashes. It checks declared scope and accepted dependencies before the requested action. It allows work to repair an open finding, while `record` refuses affected acceptance until blocking findings are resolved. Neither command executes the action. `status` distinguishes accepted records, blocked nodes, stale receipts, and unverified claims. Acceptance means the required current attestations exist, not that teaching succeeds.

## Contract schema

For a flagship version-3 run, declare obligations for the research landscape and inspected technique ledger; the full content-contract map; critical conceptual bridges; applications/current evidence; limitations/mitigations/alternatives; storyboard and speaker notes when commissioned; real visual/oral/runtime review; and final route/transfer review. Link their actual inputs and dependencies. Use existing artifact/check/inference kinds and appropriate required claims. The CLI does not automatically infer these nodes from the topic or enforce the semantic completeness of the coverage map; the coordinator and reviewers must check that before recording acceptance.

Bind the script, storyboard, illustration sources, exported notes, audio/rendered sequence, and subject evidence to affected nodes. A changed example should reopen its narration and assessments as well as its equation checks. Counted source discovery and deeply inspected source evidence need different nodes/receipts if both are claimed. Thirty metadata entries cannot supply a deep-review receipt truthfully.

This is a small build example, not a prefilled real pass. Replace placeholders with actual work and include all relevant sources/components/environment files as declared inputs.

```json
{
  "schema": 2,
  "mode": "build",
  "topic": "Chosen topic",
  "audience": "Specific learner with stated preparation",
  "scope_roots": ["artifacts"],
  "nodes": [
    {"id":"bridge","kind":"inference","action":"review","critical":true,
     "depends_on":[],"inputs":["artifacts/bridge.html"],"outputs":[],
     "required_claims":["teaching-review","correctness"]},
    {"id":"alternative-pilot","kind":"pilot","action":"pilot",
     "depends_on":[],"inputs":["artifacts/alternative.html"],"outputs":["artifacts/alternative.html"],
     "required_claims":["teaching-review","interaction"]},
    {"id":"release","kind":"delivery","action":"deliver",
     "depends_on":["bridge"],"covers":["bridge"],
     "inputs":["artifacts/lesson.html"],"outputs":["artifacts/release.json"],
     "required_claims":["artifact","interaction"]}
  ]
}
```

Modes: `audit` permits inspect/research/review/report; `plan` also permits plan; `build` also permits implement/pilot/deliver. Mode and permitted output roots are pinned at initialization. Input inspection can be outside output roots. The tool scopes declared outputs only; actual filesystem writes are not sandboxed by it. For an audit that edits skills, record that authorized work in the audit report; this CLI's action vocabulary is not a filesystem permission system.

Each node declares `id`, `kind`, `action`, `depends_on`, `inputs`, `outputs`, and `required_claims`. Critical inference nodes require a teaching-review claim and a real input artifact. Delivery must cover and depend on every declared critical inference. The script cannot discover an omitted critical inference. Extra fields can contain the compact teaching contract; their presence does not mean the script semantically validates them.

Dependencies must form a DAG. Learner detours and retries belong in teaching/runtime records, not this DAG. A changed node or declared upstream input invalidates dependent receipts; unrelated branches remain current. Shared component changes should invalidate conservatively through declared edges. Missing or unregistered files limit the guarantee.

## Receipt schema

Save the actual report first, compute its SHA-256, obtain the current node revision/input hashes from `check` or `status`, and create the receipt only after the review occurs.

```json
{
  "node":"bridge","claim_type":"teaching-review","outcome":"pass",
  "revision":"COPY_CURRENT_NODE_REVISION",
  "input_hashes":{"ABSOLUTE_INPUT_PATH":"COPY_CURRENT_INPUT_SHA256"},
  "scenario":"The reviewer attempts the new-case task using only the visible explanation.",
  "observed_result":"Describe the actual reasoning, cited warrant, difficulty, and disposition.",
  "reviewer":{"id":"actual reviewer","relationship":"fresh-context",
              "context":"State what was shared, withheld, and previously known."},
  "evidence_type":"simulated-review",
  "limitations":["AI artifact review; human learning unverified."],
  "evidence":[{"path":"actual-review.txt","sha256":"ACTUAL_REPORT_SHA256"}]
}
```

Claims: artifact, correctness, interaction, visual, teaching-review, simulated-learner, human-learning, retention, learner-tested. Relationships: author, author-informed, fresh-context, human. Evidence types: tool-observation, author-review, simulated-review, human-study, source-inspection. A simulated-learner claim needs simulated-review evidence. Human-learning/learner-tested/retention claims need human-study evidence with positive `human_evidence.participants` and `tasks`; retention also needs positive `delay_days`. These fields remain assertions, not authenticated study evidence. A reviewed artifact release need not claim human efficacy.

## Findings, repair, and strategy change

A finding file contains stable `id`, affected `nodes`, `severity` (blocking/nonblocking), and concrete `observation`. Record the learner consequence and test in the observation or linked report. A rejection opens the relevant finding; do not erase valid unrelated evidence.

A repair file contains `issue`, `outcome` (failed/resolved), causal `change`, and hashed `evidence`. To resolve, also give `resolution_receipts`: paths to current receipts covering all affected nodes. Each receipt names the finding in `resolves`. A resolved finding can reopen when its resolution evidence becomes stale. Clearing a finding does not automatically supply every missing acceptance claim.

After two failed repairs in the current strategy, another repair requires a strategy record: `issue`, a new `hypothesis`, a declared `pilot_node`, and changed hashed `evidence` for the strategy decision. The alternative pilot must be evaluable independently of the failed branch. After recording the strategy, change the pilot's actual input artifact and obtain fresh required pilot receipts. Reusing an old accepted pilot or merely changing a label cannot satisfy this strategy-review requirement. The finding remains open until its specific recheck resolves it. This checkpoint permits continued quality work after a new strategy; it is not a total attempt limit.

Keep stable issue IDs; renaming a problem does not resolve the old finding. The tool preserves event history in an atomically replaced state file, but it is not tamper-proof or an authenticated audit service. Overall effort limits, completeness of the inference graph, and user-review requirements remain coordinator obligations.

An explicit user review-before-build instruction is a real pending dependency. Preserve that instruction and the eventual user response in the project record. Do not represent an AI review as user approval. The CLI does not authenticate user authorization.

## Legacy and handoff

Schema-1 journals are status-only. Start a new schema-2 run instead of promoting old passes. Never overwrite an existing run to erase history. At handoff include the next permitted action, exact blockers, unresolved claims, relevant file revisions, and scope boundary. Do not call a plan, schema pass, or journal a deployed tutor.

Run `python <skill>/scripts/test_harness.py` after changing the guardrail. Its disposable synthetic fixtures check workflow behavior, not lesson quality or real learner evidence.
