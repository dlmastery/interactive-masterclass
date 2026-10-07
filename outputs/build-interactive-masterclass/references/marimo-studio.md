# Native marimo-studio implementation

Read installed Studio documentation and project instructions before editing. APIs and limits change. The PCA project used Studio 0.2.3, marimo 0.25.0, and the native Reveal.js React starter; those are observed versions, not permanent requirements.

Keep computations, data, and native controls in the notebook. Project named results into the slide view. Fast browser interactions can select precomputed Python frames; describe this accurately, rather than claiming every drag triggers Python. Include real notebook recomputation where it helps learning. Keep the mathematical explanation available in the notebook too.

Use the native slide view, not a static imitation called Studio. Verify notebook/slideshow navigation in the actual host browser. Framework correctness and teaching quality need separate reviews.

## Lessons from the Windows PCA build

- Keep Reveal configuration identity stable across reactive renders.
- The observed sandbox blocked session storage used by Reveal scroll mode. The course used `scrollActivationWidth: 0` with explicit responsive layouts.
- Projection scanning found declarations in unused TSX files. Archive old views outside the scanned root.
- Measure the actual aggregate projection budget. The observed transport limit was 1 MB; avoid repeated frame tables and verify the current limit.
- Sandboxed links may not navigate the parent or open a tab. Use supported parent UI or a trusted outer-page link; do not weaken the sandbox. The PCA standalone wrapper links to the editor; Studio's Visible surface dropdown switches Notebook/Preview.
- Replacing cells can leave stale editor state. Inspect real notebook content and live status. Restart only the identified task server if needed.
- Check the user's visible tab, preserve learner input, and reset temporary viewport overrides.
- On the observed Windows installation, some successful builds emitted temporary cleanup warnings. Check structured build results and runtime evidence separately.

## Browser verification

Test each distinct scene family: prediction, meaningful manipulation, boundary case, resulting explanation, reset, and navigation. Review screenshots for readability and faithful geometry; saving a screenshot alone is not a visual pass.

Inspect every derivation step and dynamic substitution. Selected observations, vector length, units, formulas, and plots must agree. Verify native data controls update Python results. Check difficult scenes on realistic screen sizes, not only a large authoring canvas.

Provide clean-start instructions for both local processes when notebook and presentation run separately. Verify the return link with both running. State offline/export limitations. Keep implementation details out of learner-facing scenes unless they help learners use the notebook.
