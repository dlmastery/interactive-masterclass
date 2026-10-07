from pathlib import Path
from html import escape
import json,re

root=Path('outputs/pca-studio')
course=json.loads((root/'course-v2.json').read_text(encoding='utf-8'))

readme='''# PCA · from picture to proof

A 64-slide interactive course in native marimo-studio, with 79 equation steps. The 6 October 2026 repair restores the first version's light background, large geometric pictures, and readable two-column layout while retaining the full derivation.

## Open the course

- [Interactive slides](http://localhost:2719/lesson/)
- [Notebook and Studio](http://localhost:2718/studio/lesson/) — open this address in **Chrome or Edge** for authoring. Chrome was verified with the notebook, preview, and code-mode session running.
- [Teaching strategy and storyboard](PCA-TEACHING-PLAN.html)
- [Original 14-slide source recovery](original-first-version/README.md)

The in-app browser can show the slides, but native notebook authoring fails there. Its sandbox blocks access to `navigator.serviceWorker`; the browser reports a `SecurityError`. Open the Studio address in an external browser instead. No CSP or sandbox protection was weakened.

Inside Studio, enable **Show Notebook** when that checkbox is present. In a narrow layout, use **Visible surface** to choose **Notebook** or **Preview**. The notebook contains the Python model, live data controls, results, and the complete lesson text and derivation.

To restart after closing the servers, open two PowerShell terminals in this folder:

```powershell
# First terminal: notebook editor on port 2718
.\\Start-Lesson.ps1 -Edit
```

```powershell
# Second terminal: slides on port 2719
.\\Start-Lesson.ps1
```

Keep both processes running. The launchers require `uv` and use pinned packages. Keep the notebook, view source, and lockfile together. KaTeX styles and fonts load from jsDelivr on first use.

## The teaching route

| Slides | Question |
|---|---|
| 1–8 | What does PCA do? |
| 9–20 | How do we measure a view? |
| 21–30 | Why does covariance appear? |
| 31–45 | Why do eigenvectors solve it? |
| 46–56 | What can we keep and recover? |
| 57–64 | When does the result help? |

The opening gives the picture a concrete purpose: store one number for each marker, recover its position, and measure the gap. The shared example uses A(8,7), B(7,8), C(5,4), and D(4,5), in centimeters. Its mean is (6,6), covariance is [[10,8],[8,10]]/3, and eigenvalues are 6 and 2/3. Keeping PC1 preserves 90% of squared spread; this is not a measure of prediction accuracy.

The repair adds four linked teaching mechanisms:

- **Compression and recovery:** connect each marker, its one stored score, recovered position, and error. Move across an axis to see positions that share one score.
- **Covariance calculation:** follow a row of Xcᵀ and a column of Xc through paired products, an accumulating sum, division by three, and the destination matrix entry.
- **Stationary directions:** compare the gradient with the circle's tangent. Both the maximum and minimum have zero turning slope; a finite turn distinguishes their behavior.
- **Global maximum:** express a direction in the signed eigenvector basis. Its squared weights give a weighted eigenvalue average bounded by 6, reached at PC1.

The remaining route derives reconstruction, the minimum-error identity, multiple components, and SVD, then tests units, outliers, new observations, and limits. **Math at this step**, **Symbols**, and **Course route** provide local help and direct navigation.

Learner inputs and proof/scene state now survive navigation away from a slide and back during the same page session. **Reloading resets that state.** There is no persistent learner record, and written explanations still need human review.

## Source and recovery

`pca_lesson.py` owns the mathematics, data, lesson prose, and native controls. `course-v2.json` is its reviewable content snapshot. The view uses `PcaCourse.tsx`, `PcaScenes.tsx`, and `pca.css` under `v/lesson/src`. Six named projections carry Python results into the native view; slide 61 embeds actual marimo controls.

`serve_lesson.py` wraps Studio's native ASGI application to put notebook navigation in the outer page. The presentation keeps Studio's original sandbox.

`original-first-version/` preserves the recovered 14-slide source, original stylesheet and renderer, and 32 original notebook cells. Its manifest records source-map provenance and file hashes. That recovery package has not been separately built or run; it does not replace this 64-slide course.

## Checks and limits · 6 October 2026

- Production build passed.
- All 64 slides passed browser navigation, math-rendering, and input-pointer checks at the actual 870×668 viewport.
- Interaction checks passed for covariance 8÷3; zero slope at both extrema; finite 3° turns of approximately −0.0146 variance at the maximum and +0.0146 at the minimum; signed basis reversal; the upper bound 6; and state retained across slide navigation.
- Numerical checks passed for 1,629 projection frames and 2,880 additional direction cases. The combined projection payload is 946,805 bytes.
- Native Studio runtime validation passed with no issues: all 10 notebook cells parsed, the embedded native cell completed, and all six projected values resolved.

The prose uses short sentences and consistent mathematical terms. The copy pass checked all 64 claims/actions and 79 equation reasons; 394 slide-copy sentences met the simple 20/25-word limits. This does **not** establish 80% ASD-STE100 vocabulary or meaning compliance. No learner mastery or teaching-effectiveness claim follows from software checks.

Supported delivery is a local Python server. Static export, WASM, public hosting, and offline fonts have not been verified. Studio may report a temporary-directory cleanup warning on Windows after a successful build; build and runtime results are assessed separately.

The teaching sequence draws on the transcripts of [Luis Serrano](https://www.youtube.com/watch?v=g-Hb26agBFg), [StatQuest](https://www.youtube.com/watch?v=FgakZw6K1QQ), and [Shlens's PCA tutorial](https://arxiv.org/abs/1404.1100). Scenes and prose are original. The user's AI Learn Loop guidance informed prediction, calculation, explanation, and feedback.

Pinned environment: marimo-studio 0.2.3, marimo 0.25.0, NumPy 2.5.3, Deno 2.9.7.
'''
(root/'README.md').write_text(readme,encoding='utf-8')

lines=['# Teaching map · PCA first','',
       'Updated 6 October 2026 from `course-v2.json`: 64 slides and 79 equation steps. Start with one-number compression and recovery error; introduce each mathematical tool when the PCA argument needs it.','',
       'The current course uses the first version’s light visual style. The original 14-slide source is preserved separately in `original-first-version/`. Open `PCA-TEACHING-PLAN.html` for the design record and current repair checks.','']
for i,ch in enumerate(course['chapters']):
    lines += ['## '+ch['question'],'']
    for slide in course['slides']:
        if slide['chapter']!=i: continue
        lines += [f"### {slide['id']}. {slide['title']}",'',
                  '**Try:** '+slide['action'],'',
                  '**Main idea:** '+slide['claim'],'',
                  f"**Equation steps:** {len(slide['steps'])}",'']
(root/'TEACHING-MAP.md').write_text('\n'.join(lines),encoding='utf-8')

plan_path=root/'PCA-TEACHING-PLAN.html'
plan=plan_path.read_text(encoding='utf-8')
plan=plan.replace('Teaching strategy · revision 2 · 4 October 2026','Teaching strategy · revision 3 · repaired 6 October 2026')
plan=plan.replace('This is the redesign specification. It replaces the rejected prerequisite-first sequence. The slide count is a structure for the argument, not evidence of learning.',
                  'Design record for the 64-slide course, with a repair update below. The slide count organizes the argument; it is not evidence of learning.')
plan=plan.replace('The notebook return action works. Refresh does not leave an invisible or mismatched slide.',
                  'Notebook authoring opens in a supported external browser. Refresh does not leave an invisible or mismatched slide.')
repair='''<section id="repair-2026-10-06"><h2>Repair strategy · 6 October 2026</h2>
<p>Restore the first version’s light background, large geometric illustration, and readable two-column layout. Preserve the 64-slide argument and its 79 equation steps. The original 14-slide source is now stored separately in <a href="original-first-version/README.md">original-first-version</a>, with provenance and hashes; that source recovery has not been separately built or run.</p>
<p>The opening now asks a concrete question: can one stored score recover a marker’s position with a small error? The covariance scene follows row–column products into an accumulating sum and matrix entry. The stationary-direction scene connects the gradient to the tangent. The global proof uses signed eigenvector coordinates and nonnegative squared weights to reach the variance bound. These are changes to the explanations and interactions, not only to the theme.</p>
<p>Learner inputs and scene/proof state remain available when navigating away and back in the same page session. Reload resets that state; this is not a persistent learner record. The storyboard below now uses the repaired learner-facing prose from the course JSON.</p>
<p><strong>Checked:</strong> production build; navigation, math rendering, and input-pointer behavior across all 64 slides at 870×668; covariance 8÷3; stationary slope at both extrema; finite 3° changes of approximately −0.0146 at the maximum and +0.0146 at the minimum; signed basis reversal; variance bound 6; and state preservation. Numerical checks cover 1,629 projection frames plus 2,880 additional direction cases. The projection payload is 946,805 bytes. Native Studio runtime validation passed with no issues: 10 notebook cells parsed, one native cell completed, and all six projected values resolved.</p>
<p><strong>Authoring:</strong> open <a href="http://localhost:2718/studio/lesson/">Studio</a> in Chrome or Edge. Chrome was verified with the actual notebook, preview, and code-mode session. Use Show Notebook or Visible surface according to the layout. The in-app browser blocks native authoring with a sandbox-related navigator.serviceWorker SecurityError; no CSP or sandbox permissions were weakened. The <a href="http://localhost:2719/lesson/">slideshow</a> remains available in the in-app browser.</p>
<p>The language pass reviewed all claims, learner actions, and equation reasons. Sentence-length checks do not establish 80% ASD-STE100 compliance, and browser/numerical checks do not establish learner mastery.</p></section>
'''
storyboard='<h2>64-slide storyboard</h2><p>Each item gives a learner action, its main idea, and the number of equation steps.</p>'
for s in course['slides']:
    storyboard+=f'<details><summary>{s["id"]:02d} · {escape(s["title"])}</summary><p><strong>Try:</strong> {escape(s["action"])}</p><p><strong>Main idea:</strong> {escape(s["claim"])}</p><p><small>Equation steps: {len(s["steps"])}</small></p></details>'
prefix=plan.split('<h2>64-slide storyboard</h2>')[0]
prefix=re.sub(r'<section id="repair-2026-10-06">.*?</section>', '', prefix, flags=re.S)
plan_path.write_text(prefix+repair+storyboard+'</main></html>\n',encoding='utf-8')

assert plan_path.read_text(encoding='utf-8').count('<details>')==64
assert (root/'TEACHING-MAP.md').read_text(encoding='utf-8').count('### ')==64
print('Updated README, teaching map, and teaching plan; both storyboards match all 64 current JSON slides. Runtime validation pass recorded from the native report.')
