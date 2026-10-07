from pathlib import Path
import json

root = Path('outputs/pca-studio')
course = json.loads((root/'course-v2.json').read_text(encoding='utf-8'))
(root/'README.md').write_text('''# PCA · from picture to proof

A 64-slide interactive course in a native marimo-studio Reveal.js view. The course starts with PCA. Statistics and linear algebra appear when they explain the next PCA operation.

## Open the course

- Slides: http://localhost:2719/lesson/
- Notebook and Studio: http://localhost:2718/studio/lesson/
- Full teaching strategy: `PCA-TEACHING-PLAN.html`

The **Back to notebook** link at the top right of the slideshow opens the native Studio editor. In Studio, use the **Notebook** and **Preview** toolbar controls to switch views. The notebook contains the model, live controls, results, and all 64 lesson claims and derivations.

To run later, open two PowerShell terminals in this folder. Start the editor in the first terminal:

```powershell
.\Start-Lesson.ps1 -Edit
```

Start the slides in the second terminal:

```powershell
.\Start-Lesson.ps1
```

Keep both processes running to use the return link. The launcher requires `uv`, builds the native Studio view, and uses pinned packages. Keep the notebook, view source, manifests, and lockfile together. A short extraction path helps on Windows. Pinned KaTeX styles and fonts load from jsDelivr on first use.

## Teaching route

| Slides | Question |
|---|---|
| 1–8 | What does PCA do? |
| 9–20 | How do we measure a view? |
| 21–30 | Why does covariance appear? |
| 31–45 | Why do eigenvectors solve it? |
| 46–56 | What can we keep and recover? |
| 57–64 | When does the result help? |

One example connects the pictures and equations: four measured positions in centimetres, A(8,7), B(7,8), C(5,4), and D(4,5). The mean is (6,6). The centered points are (2,1), (1,2), (−1,−2), and (−2,−1). Their sample covariance is [[10,8],[8,10]]/3. PC1 has variance 6 and retains 90% of total variance.

The main derivation expands a squared projection score, identifies the covariance terms, forms wᵀSw, derives Sw=λw, and proves a global maximum using the eigenbasis. Stationarity alone is not presented as a maximum proof. Later steps derive reconstruction and its minimum-error equivalence, the top-k extension, and the SVD connection. The symmetric-matrix basis theorem is stated, rather than silently assumed to have been proved.

There are 79 equation steps. Each step gives a reason. **Math at this step** provides a short refresher without leaving the current slide. **Symbols** fixes the notation, including rows as observations. **Course route** shows six questions and direct slide links.

## What learners can change

- Turn an axis; follow a selected observation to its score and perpendicular residual.
- Compare full rotation with dropping a coordinate.
- Move the cloud to its center and change the length of a candidate direction.
- Inspect individual products in a covariance entry, including cancellation.
- Change direction and eigenbasis weights while comparing variance with its upper bound.
- Change component count; reconstruct points and measure the error.
- Change units, enable standardization, and inspect outliers or a circular cloud.
- Change real notebook data with native marimo controls on slide 61.
- Attempt a fresh geometric task, numerical calculations, and a written teach-back.

Written reasons require human review. Numeric checks do not certify understanding. Inputs and local proof steps reset when their scene unmounts; this revision does not promise a persistent learner record.

## How Studio is used

`pca_lesson.py` owns the mathematics, data, lesson text, and native controls. Six explicit `mo-value` projections supply the view. A native `marimo-cell` embeds the notebook controls. Python prepares angle frames for immediate visual feedback; the browser selects those frames. Editing the native controls triggers new Python calculations.

`serve_lesson.py` wraps the native Studio ASGI application. Its outer page contains the working notebook navigation link. The authored presentation stays inside Studio's original sandbox. No sandbox permission is weakened.

Main files:

- `pca_lesson.py`: executable source of truth.
- `course-v2.json`: reviewable snapshot of the course content.
- `v/lesson/src/PcaCourse.tsx`: native slide shell, route, refreshers, and notation.
- `v/lesson/src/PcaScenes.tsx`: interactive scenes, proof controls, and exercises.
- `v/lesson/src/pca.css`: visual system and responsive layout.
- `verify_mathematics.py`: numerical verification.
- `language-review.json`: sentence-length audit with its limitations.

To reuse the pattern, replace the notebook model and course data, then design scenes around the new subject's causal questions. This is a reusable design, not an automatic course generator.

## Evidence and limits

Numerical checks cover 1,629 projection frames, covariance, scores, unit directions, the gradient, the global variance bound, reconstruction, SVD, and standardization. The combined projection payload is 940,547 bytes. All 64 slides and 79 equation steps were checked in the browser; live notebook data and return navigation were exercised. Full details are in `verification.json`.

The prose follows short-sentence, active-voice, consistent-term principles from ASD-STE100. All 358 audited content sentences meet the chosen length limits. This is not a formal dictionary, meaning, or part-of-speech audit, and does not establish the requested 80% full compliance rate. Teaching effectiveness still needs learner feedback.

The supported delivery is a local Python server. Static export, WASM, public hosting, and offline font loading have not been verified. Studio can emit temporary-directory cleanup warnings on Windows after a successful build; the build result and runtime result are checked separately.

## Sources and design guidance

The teaching strategy was informed by the transcripts of [Luis Serrano's PCA lesson](https://www.youtube.com/watch?v=g-Hb26agBFg), [StatQuest's PCA lesson](https://www.youtube.com/watch?v=FgakZw6K1QQ), and [Shlens' PCA tutorial](https://arxiv.org/abs/1404.1100). The scenes and prose here are original. The user's AI Learn Loop pack informed prediction, explanation, practice, and separate feedback.

Official references: [Studio overview](https://marimo-team.github.io/marimo-studio/), [Reveal.js view](https://marimo-team.github.io/marimo-studio/guide/frontend-options#reveal-js-slides), [projections](https://marimo-team.github.io/marimo-studio/reference/projections), and [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf).

Tested: marimo-studio 0.2.3, marimo 0.25.0, NumPy 2.5.3, Deno 2.9.7.
''', encoding='utf-8')

mapping = ['# Teaching map · PCA first', '', 'The executable course has 64 slides and 79 equation steps. Open PCA-TEACHING-PLAN.html for the complete strategy.', '']
for ch in course['chapters']:
    mapping += [f"## {ch['question']}", '']
    for s in course['slides'][ch['start']:ch['end']]:
        mapping += [f"### {s['id']}. {s['title']}", '', f"**Do:** {s['action']}", '', f"**Learn:** {s['claim']}", '', f"**Equation steps:** {len(s['steps'])}", '']
(root/'TEACHING-MAP.md').write_text('\n'.join(mapping),encoding='utf-8')

view=root/'v/lesson'
(view/'AGENTS.md').write_text('''# PCA course instructions

Build a native marimo-studio Reveal.js view. Follow the installed Studio skill for notebook ownership, projections, and lifecycle.

This is a 64-slide course for a 20-year-old. Start with PCA geometry. Introduce mathematical foundations only when a PCA operation needs them. Keep the full covariance-to-eigenvector derivation and global maximum proof in the main route. Do not use stationarity as proof of a maximum.

Use the same four measured positions in cm throughout the main example. Rows are observations. Raw r, centered x, candidate w, score z, covariance S, learned axis q, and eigenvalue lambda have fixed meanings. Preserve equal geometric scales and make each control change the quantity it claims to change.

Active files are PcaCourse.tsx, PcaScenes.tsx, and pca.css. Lesson.tsx is an export. LabComponents.tsx supplies shared types, numeric formatting, and KaTeX. Keep Reveal configuration identity stable. Keep scrollActivationWidth: 0 because the Studio sandbox blocks sessionStorage. Do not weaken the iframe sandbox.

The notebook owns the model, course data, and native data controls. React selects Python-computed frames. Keep explicit projection hosts and Lens metadata accurate. The aggregate projection payload must stay below 1,000,000 bytes; current default payload is 940,547. Do not project redundant full datasets.

Use concise active prose and explain every equation step. Sentence-length checks alone do not establish ASD-STE100 compliance. Numeric checking does not judge a written explanation. Do not claim mastery from navigation.

Build through Studio using the frozen Deno lockfile. Inspect runtime validation and test meaningful controls in the browser. The production server uses serve_lesson.py for trusted outer-page notebook navigation. Keep the editor running on 2718 and slides on 2719.

For future revisions update the teaching plan, source snapshot, README, verification evidence, and source ZIP. Preserve prior work outside the view root; Studio scans unused TSX files for projection declarations too.
''',encoding='utf-8')
(view/'DESIGN.md').write_text('''# PCA design

PCA first. Six questions connect geometry, measured spread, covariance, optimal axes, reconstruction, and use. Sixty-four slides support a paced course; 79 equation steps explain the proof.

The geometry is the largest region. Use a navy background, teal for retained directions, coral for residuals, pale text, and readable serif headings. Keep axes equally scaled. Use a separate score line and label selected observations A–D. Both coordinates are position measurements in cm.

The baseline covariance is [[10,8],[8,10]]/3, with eigenvalues 6 and 2/3. Retaining PC1 keeps 90% of variance. Both axes keep 100%. Changing a candidate length must change its arrow, scores, and variance consistently.

Use one claim and one learner action per slide. Keep current and previous equation steps together, with a reason. A six-question route replaces the prerequisite tree. Refreshers and notation open in place. Native controls on slide 61 recalculate the Python model.

Narrow screens stack the scene and explanation. Long proof content scrolls. All pointer controls have keyboard equivalents. Distinguish prediction, numerical feedback, and written explanation review. No timed locks or false mastery labels.
''',encoding='utf-8')
print('Updated course documentation and view instructions.')
