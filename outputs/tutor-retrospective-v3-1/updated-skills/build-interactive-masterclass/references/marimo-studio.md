# Native marimo-studio adapter

Inspect installed framework documentation, project instructions, and existing examples before promising features. Confirm versions, native slide support, notebook projection API, sandbox behavior, payload limits, and host navigation. Do not turn a bounded feasibility probe into a framework rewrite.

Keep computation, data, and native controls in the notebook where appropriate. Project named results into the native slide view. Browser controls may select precomputed Python frames; describe this honestly instead of claiming each drag executes Python. Demonstrate real notebook recomputation when it serves the lesson. Keep the mathematical explanation accessible in the notebook.

## Known failure patterns to check, not permanent API rules

These arose in one Windows Studio build and need verification against the current installation:

- Unstable Reveal configuration identity can reset navigation/reactive state.
- Nested `section` elements may become Reveal slide stacks and intercept intended controls; use neutral wrappers inside scenes.
- A large authored canvas scaled into a small viewport can make labels unreadable. Test actual host sizes and intermediate states.
- Sandbox restrictions can affect storage, service workers, and links. Use supported host navigation or a trusted outer-page link; do not weaken the sandbox.
- Projection scans may find declarations in unused source files. Keep archived views outside scanned roots.
- Duplicate precomputed frames can exceed transport limits. Measure the current aggregate payload and actual installed limit.
- Replaced notebook cells may leave stale editor state. Inspect live content; restart only the identified project server if needed.

## Feasibility and acceptance

Before mass authoring, prove one meaningful Python-backed interaction, native next/back navigation, one derivation reveal, and return to the editable notebook. Record how the user reaches each view in their actual browser. A standalone imitation is not native Studio support.

Test each scene family: prediction, manipulation, boundary, feedback, reset, and navigation. Exercise controls in the real rendered interface; a build cannot establish pointer behavior. Inspect formula/diagram/value agreement and dimensional accuracy. If a worked example is fixed while a diagram changes, label it clearly or connect their state.

At realistic viewport sizes, verify labels, controls, proof steps, keyboard access, and scrolling/attention continuity. Check state on revisit. Preserve user input and reset temporary test overrides.

Provide verified clean-start instructions for required processes, refresh behavior, return-to-notebook path, and offline/export limits. Keep implementation details outside learner prose unless needed to use the course. Teaching acceptance remains separate from framework acceptance.
