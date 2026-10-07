# Topic-specific teaching harness

This is a coordinator-driven workflow with durable evidence, not an unattended model service. Configure the run, execute research and debate with available tools, build the artifact, and record actual reviews. Configuration alone is a scaffold.

## Run contract

Create a run directory in the task's working area or reuse a suitable project record. Record the topic, audience, prior knowledge, format, user corrections, observable learner capabilities, scope boundaries, sources, tool limits, roles, review criteria, requirements-to-scene coverage, and next action.

Allocate effort across research, the representative sample, core explanation/proof, expansion, and review. Do not invent a user token budget. Save concise artifacts when real: contract, source inventory, proposals, debate, plan, pilot review, final review, and delivery record. Existing formats are acceptable; avoid ceremonial paperwork for minor edits.

## Durable state

Ordered gates: `intake`, `research`, `debate`, `plan`, `pilot`, `build`, `review`, `delivery`. Later passes require earlier passes and unchanged evidence. Revision preserves history and invalidates dependent passes.

```text
python <skill>/scripts/harness.py init work/tutorial-run --topic "PCA" --audience "Interested 20-year-old"
python <skill>/scripts/harness.py record work/tutorial-run --stage intake --status pass --evidence work/tutorial-run/contract.json --note "Outcomes and constraints recorded."
python <skill>/scripts/harness.py status work/tutorial-run
```

The script hashes evidence files and refuses skipped gates or stale prerequisites. A later edit requires re-review and a new record. Record a gate only after the action occurs. The script cannot verify that an agent report is truthful, a source was read, or a lesson teaches well; the coordinator must inspect those claims. Records are not tamper-proof attestations.

## Debate roles

For full courses, request three separate subagents when tools and higher-priority instructions permit:

1. **Intuition and audience designer:** phenomenon, example, analogy limits, predictions, and minimum prerequisite bridges.
2. **Subject and derivation reviewer:** formal route, assumptions, proof obligations, counterexamples, and technical evidence.
3. **Visual and interaction designer:** representations, manipulations, feedback, transitions, and a visual teaching sample.

Give each the same learner brief and inspected-source inventory without the coordinator's preferred answer. Request a coherent proposal, tradeoffs, and a design for the hardest transition. Then share competing proposals for cross-critique. Ask what disagreement matters most and which sample would resolve it. Synthesize explicit decisions, not a collage of all suggestions.

Do not create user-owned chats for subtasks. Do not invent reviews, tool calls, or consensus. With one agent, save labeled sequential perspectives and the independence limitation. Similar models agreeing is not learner evidence.

## Gates

| Gate | Evidence before passing |
|---|---|
| Intake | Outcomes and prior corrections are traceable |
| Research | Contrasting substantive explanations and technical sources inspected |
| Debate | Competing proposals, specific objections, reasoned synthesis |
| Plan | Every major transition has an example, explanation, interaction, and check |
| Pilot | Opening and hardest transition work in the requested framework |
| Build | Complete scope; central proof and transfer included |
| Review | Separate dimensions reviewed; no unresolved critical failure |
| Delivery | Working links, launch steps, source, navigation, and honest limits |

A repair loop is observed failure -> specific change -> affected check rerun -> evidence and decision. Repeated inspection without change is not improvement. Stop expanding a failed pattern. After two unsuccessful repairs of the same issue, reconsider the representation or sequence. Do not ask the user to solve routine implementation choices.

For plan-only work, stop after the plan and label later gates unexecuted. For audit-only work, report observations without inventing earlier history. For a small correction, rerun affected checks without forcing full-course research.
