# PCA course instructions

Build a native marimo-studio Reveal.js view. Follow the installed Studio skill for notebook ownership, projections, and lifecycle.

This is a 64-slide course for a 20-year-old. Start with PCA geometry. Introduce mathematical foundations only when a PCA operation needs them. Keep the full covariance-to-eigenvector derivation and global maximum proof in the main route. Do not use stationarity as proof of a maximum.

Use the same four measured positions in cm throughout the main example. Rows are observations. Raw r, centered x, candidate w, score z, covariance S, learned axis q, and eigenvalue lambda have fixed meanings. Preserve equal geometric scales and make each control change the quantity it claims to change.

Active files are PcaCourse.tsx, PcaScenes.tsx, and pca.css. Lesson.tsx is an export. LabComponents.tsx supplies shared types, numeric formatting, and KaTeX. Keep Reveal configuration identity stable. Keep scrollActivationWidth: 0 because the Studio sandbox blocks sessionStorage. Do not weaken the iframe sandbox.

The notebook owns the model, course data, and native data controls. React selects Python-computed frames. Keep explicit projection hosts and Lens metadata accurate. The aggregate projection payload must stay below 1,000,000 bytes; current default payload is 940,547. Do not project redundant full datasets.

Use concise active prose and explain every equation step. Sentence-length checks alone do not establish ASD-STE100 compliance. Numeric checking does not judge a written explanation. Do not claim mastery from navigation.

Build through Studio using the frozen Deno lockfile. Inspect runtime validation and test meaningful controls in the browser. The production server uses serve_lesson.py for trusted outer-page notebook navigation. Keep the editor running on 2718 and slides on 2719.

For future revisions update the teaching plan, source snapshot, README, verification evidence, and source ZIP. Preserve prior work outside the view root; Studio scans unused TSX files for projection declarations too.
