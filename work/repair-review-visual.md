# PCA visual recovery review

Reviewed the active AGENTS.md, PcaCourse.tsx, PcaScenes.tsx and pca.css, plus the saved previews of the 14-, 54-, and 64-slide versions. This review uses those files and screenshots, not a live browser audit.

## Verdict

The first version is the right visual baseline. Restore its bright paper background, green/orange diagram encoding, legible claim-and-equation composition, and directly visible topic navigation. Keep the 64-slide PCA-first sequence and its derivation; reverting all content to 14 slides would discard the user's requirements.

## Observed regressions and precise repairs

1. **The current course shrinks in the actual in-app viewport.** The saved 64-slide preview is 812 px wide. Its fixed 1440×850 Reveal canvas (`PcaCourse.tsx:18–19`) is squeezed below two unscaled 68/62 px bars (`pca.css:76,123`). Its plot/control labels are visibly tiny. The responsive layout only starts below 760 px (`pca.css:895`), so the 812–1000 px app panel falls into the scaled desktop layout. Make slides use actual viewport dimensions/CSS layout instead of shrinking a 1440 px artboard. At typical IAB widths, use a legible 18–20 px body floor, 15 px control floor, 32–40 px title, and scroll the slide when necessary. Use one column below roughly 980 px. Keep next/previous accessible without eating 130 px of vertical space.

2. **The useful plot is much smaller than its SVG container.** `PcaScenes.tsx:166` uses `s=146/bound`, so the plot grid spans only 292 units inside a 590-unit viewBox. At the saved preview size, the useful grid is about 160 px wide, with generous empty margins on both sides. The first version showed a roughly 390 px plot at 1280 px width. Increase the useful plot region to 420–450 of the 590 units, or use a tighter plot viewBox and a separate score-strip SVG. Preserve equal x/y scales. Do not enlarge only the surrounding card.

3. **The dark redesign removed the first version's readable hierarchy.** Current navy background plus muted small labels suppresses axes and residual lines. Return to warm white/paper, dark green headings, teal observations and orange projection marks/axis. Replace hardcoded SVG dark grid/stroke colors in `Geometry`; CSS theme changes alone will leave those wrong. Give diagrams a clear legend: measured point, projected point, discarded distance. Use readable axis labels such as 'Feature x (cm)' and 'Feature y (cm)' in the introduction; introduce compact x/y after their meanings are clear.

4. **The current score strip collides at the exact example PCA axis.** At 45°, A/B and C/D share scores. The screenshot shows tightly stacked letters and 'A 2.12'. Current collision logic adds 17 SVG units vertically (`PcaScenes.tsx:604`), leaving little room at the bottom of the viewBox. Use explicit grouped score labels ('A, B: 2.12' and 'C, D: −2.12') or separate named rows. Preserve and explain the shared score: it is the evidence of information loss, not an overlap to hide.

5. **The visual repeats too much unrelated material.** `Geometry` draws the score strip for every mode except points, including eigenvector scenes. For `mode='eigen'`, hide the score strip and data markers unless they support that step. Show the unit circle, w, Sw, and their difference clearly. For covariance scenes, give the chosen matrix entry and product table more area. Keep the same underlying dataset, but make the illustration specific to the question instead of repeating the same tiny cloud on nearly every slide.

6. **Navigation is harder to scan than the first version.** The first preview displayed Geometry / Covariance / Derivation / Example / Reconstruction / Units / Quiz directly. The new view hides all six major questions in a modal and exposes a long 64-item dropdown. Restore a compact visible topic strip on wide layouts, with the current topic and slide number visible. On narrow layouts use one clearly labelled chapter menu. Keep notebook return permanently visible. The route drawer should offer the six questions plus progress within the current one; it must not be the only clue to course structure.

7. **Experiments and proof positions reset when learners return.** Only the active `Scene` is mounted and it is keyed by slide id (`PcaCourse.tsx:177`), so local phase/variant/proof step resets. The visual result contradicts a learner's expectation of returning to an experiment. Store state per slide in the root or an explicit scene state map. Preserve state on chapter navigation; offer 'Reset this experiment' separately. Do not silently change shared angle on return unless the scene is intentionally a fixed worked example.

8. **The proof is readable algebra, but not yet a visual derivation.** `Proof` swaps complete expressions, while the previous expression fades to 46% opacity. Tie each equation step to the adjacent scene: mark the two dot-product factors, highlight the cross-term in orange, illuminate the selected covariance entry, then carry its color into wᵀSw. Keep prior/current expressions both legible. This needs scene-specific highlighting, not a universal animation. Root should prioritize the covariance-to-objective and global-maximum scenes after restoring the main layout.

## Smallest useful repair sequence

1. Restore the first-version light palette and typographic hierarchy; remove desktop artboard scaling at IAB widths.
2. Reclaim plot area, fix score collisions, and give each visual mode only the elements it needs.
3. Restore visible topic navigation; preserve per-slide experiment and proof state.
4. Review opening, projection, covariance construction, eigenvector maximum proof, and reconstruction at 850×700 and 1280×720. Verify meaningful controls change both the picture and numbers consistently.
5. Keep 64 slides and the full mathematical path. Treat teaching quality as a separate review from the slide count or numeric checks.

Do not claim this repair is complete from screenshots of one opening slide. The saved first-version image is a useful aesthetic reference; it does not establish that the original shallow course satisfied the mathematical teaching request.
