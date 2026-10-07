from pathlib import Path
p=Path('outputs/pca-studio/v/lesson/src/pca.css')
s=p.read_text()
colors={
'#0a1626':'#fbfbf7','#e7edf5':'#243d39','#ffb496':'#b86a28','#dce8f3':'#28443f','#162b41':'#f5f6ee','#36506a':'#b8c9bf','#234158':'#eaf0e7','#062b29':'#ffffff','#62e1cd':'#237b70','#8af0dc':'#226f66','#91a6bd':'#61736d','#263c52':'#d9e0d5','#3a516b':'#d2ddd2','#d4dfeb':'#34534b','#94a8bc':'#69796f','#f5f4eb':'#173f36','#edf3f5':'#253e38','#93a6b8':'#63756a','#acc0d1':'#4c685d','#859bb4':'#69796f','#ff9f7a':'#c57d35','#ffb092':'#a85f23','#132b3e':'#f1f4ec','#89a5ba':'#61736d','#16353277':'#e8f1e5','#324960':'#d0dcd0','#122b3e':'#f1f4ec','#385068':'#d0dcd0','#e9f0f4':'#243d39','#355067':'#d0dcd0','#748aa1':'#829889','#253b52':'#dce3d8','#8ba4bc':'#61736d','#182c40':'#f0f3ea','#8496a8':'#829889','#112f3c':'#e5eee1','#324b64':'#d0dcd0','#f5f7f3':'#f2f5ee','#18243a':'#243d39','#adc0d1':'#4c685d','#13283c':'#ffffff','#e7f0f4':'#243d39','#425f79':'#afc1b3','#020912bd':'#233d3266','#102238':'#fffffc','#3a556e':'#ccd8c9','#0007':'#19362a26','#f1f1e8':'#173f36','#314a63':'#d9e3d4','#193e47':'#e5eee1','#98adc1':'#61736d','#9db3c7':'#61736d','#a8bacb':'#61736d','#b9cbdc':'#405c50'
}
for a,b in colors.items(): s=s.replace(a,b)
s=s.replace('color-scheme: dark','color-scheme: light')
s += '''

/* Recovered paper layout. These dimensions are viewport pixels, never a
   scaled 1440-pixel artboard. Reveal retains slide selection and navigation. */
:root {
  --course-ink: #243d39;
  --course-muted: #61736d;
  --course-paper: #fbfbf7;
  --course-green: #237b70;
  --course-orange: #c57d35;
  --course-line: #d9e0d5;
  --course-header-height: 56px;
  --course-chapters-height: 36px;
  --course-footer-height: 50px;
  font-family: 'Segoe UI', Arial, sans-serif;
  font-size: 18px;
  color-scheme: light;
}
html, body, #app-shell {
  width: 100%;
  height: 100%;
  min-height: 0;
  overflow: hidden;
}
body { color: var(--course-ink); background: var(--course-paper); }
button, select, textarea, input { font-size: 15px; }
button { min-height: 36px; padding: 8px 12px; border-radius: 5px; }
button:disabled { opacity: .5; }
button[aria-pressed=true], button.accent {
  background: var(--course-green);
  color: #fff;
  border-color: var(--course-green);
}
.course-nav {
  position: fixed;
  inset: 0 0 auto;
  height: var(--course-header-height);
  min-height: 0;
  padding: 0 22px;
  flex-wrap: nowrap;
  align-items: center;
  gap: 16px;
  background: #f7f8f1;
  color: var(--course-ink);
  z-index: 40;
}
.course-nav > div { flex-wrap: nowrap; gap: 6px; }
.course-nav button { font-size: 15px; padding: 7px 10px; white-space: nowrap; }
.course-nav .wordmark, .course-nav .course-wordmark, .course-wordmark {
  font: 28px/1.1 Georgia, 'Times New Roman', serif;
  font-weight: 400;
  color: #173f36;
  letter-spacing: -.03em;
  border: 0;
  background: transparent;
  padding: 0;
  white-space: nowrap;
}
.wordmark span, .course-wordmark span {
  font: 14px/1.3 'Segoe UI', Arial, sans-serif;
  margin-left: 13px;
  color: var(--course-muted);
  letter-spacing: 0;
}
.notebook-link {
  display: inline-flex;
  align-items: center;
  min-height: 36px;
  font-size: 15px;
  color: #226f66;
  padding: 7px 10px;
  white-space: nowrap;
  margin-left: 3px;
}
.chapter-strip {
  position: fixed;
  z-index: 35;
  top: var(--course-header-height);
  left: 0;
  right: 0;
  height: var(--course-chapters-height);
  display: flex;
  justify-content: center;
  align-items: stretch;
  gap: 4px;
  padding: 0 20px;
  overflow-x: auto;
  overflow-y: hidden;
  scrollbar-width: thin;
  background: #f7f8f1;
  border-bottom: 1px solid var(--course-line);
}
.chapter-link {
  flex: 0 0 auto;
  min-height: 0;
  padding: 6px 14px;
  color: #52695e;
  background: transparent;
  border: 0;
  border-bottom: 3px solid transparent;
  border-radius: 0;
  font-size: 15px;
  line-height: 20px;
  white-space: nowrap;
}
.chapter-link:hover { background: #eaf0e7; }
.chapter-link.active {
  color: #173f36;
  border-bottom-color: var(--course-green);
  background: #e8efe2;
  font-weight: 600;
}
.pca-deck.reveal {
  position: fixed !important;
  top: calc(var(--course-header-height) + var(--course-chapters-height)) !important;
  bottom: var(--course-footer-height) !important;
  left: 0 !important;
  right: 0 !important;
  width: 100% !important;
  height: calc(100% - var(--course-header-height) - var(--course-chapters-height) - var(--course-footer-height)) !important;
  min-height: 0 !important;
  margin: 0 !important;
  overflow: hidden;
  font-size: 18px;
  background: var(--course-paper);
}
.pca-deck.reveal .slides {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  min-height: 0 !important;
  margin: 0 !important;
  transform: none !important;
  zoom: 1 !important;
  text-align: left;
}
.pca-deck.reveal .slides > section {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  min-height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  transform: none !important;
  overflow: hidden;
}
.pca-deck.reveal .slides > section:not(.present) { display: none !important; }
.pca-deck.reveal .slides > section.present { display: block !important; }
.pca-slide {
  height: 100%;
  min-height: 0;
  max-height: 100%;
  padding: 24px clamp(24px, 4.2vw, 66px) 36px;
  display: block;
  overflow-x: hidden;
  overflow-y: auto;
  overscroll-behavior: contain;
  scrollbar-gutter: stable;
  scroll-padding: 20px;
  background: var(--course-paper);
}
.pca-slide header { padding-bottom: 18px; }
.chapter-label { font-size: 13px; line-height: 1.4; letter-spacing: .075em; margin: 0 0 10px; }
.pca-slide h1 { font-size: clamp(32px, 3.2vw, 42px); line-height: 1.14; color: #173f36; max-width: 1150px; }
.scene-split, .scene-split.proof-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.12fr) minmax(0, 1fr);
  gap: 36px;
  align-items: start;
}
.visual-side, .reason-side { min-width: 0; }
.reason-side { padding-top: 7px; }
.reason-side p, .proof-layout .reason-side > p { font-size: 18px; line-height: 1.5; margin: 12px 0; }
.big-idea { font-size: 22px !important; line-height: 1.45 !important; margin: 4px 0 20px !important; }
.diagram-caption { font-size: 15px; margin: 0 0 5px; color: var(--course-muted); }
.geometry { max-width: 560px; margin: 0 auto; }
.geometry.compact { max-width: 440px; }
.geometry svg { overflow: visible; }
.geometry svg text { font-size: 18px; }
.observation-select { font-size: 15px; gap: 7px; flex-wrap: wrap; margin: 4px 0; }
.observation-select button { font-size: 15px; min-width: 38px; padding: 6px 12px; }
.observation-select span { margin-left: 5px; }
.angle-controls { max-width: 530px; margin: 12px auto 0; padding: 9px 14px 3px; background: #eef2e8; border-radius: 6px; }
.pca-slider { margin: 8px 0; }
.pca-slider > span { font-size: 15px; line-height: 1.35; margin-bottom: 5px; }
.pca-slider input { min-height: 20px; }
.preset-row { margin: 9px 0; }
.preset-row button { font-size: 15px; min-width: 60px; }
.metrics { gap: 22px; margin: 20px 0 14px; }
.metric { min-width: 130px; }
.metric small { font-size: 15px; }
.metric strong { font-family: Georgia, 'Times New Roman', serif; font-size: 34px; }
.metric span { font-size: 14px; line-height: 1.35; }
.try { margin-top: 22px; padding: 12px 16px; background: #f1f3e9; border-left-color: var(--course-orange); }
.try small, .small-label { font-size: 13px !important; }
.try p { font-size: 18px; line-height: 1.5; }
.proof { padding-top: 6px; }
.proof-label { font-size: 13px; line-height: 1.4; }
.proof .equation, .exam-layout .equation { font-size: 21px; line-height: 1.5; overflow-x: auto; }
.proof .katex-display { margin: .5em 0; }
.previous-equation, .proof-layout .previous-equation { opacity: 1; margin-top: 15px; padding: 8px 12px; color: #536a5f; background: #f0f3eb; border-left: 3px solid #b5c5b4; }
.previous-equation small { font-size: 13px; color: #536a5f; }
.previous-equation .equation, .proof-layout .previous-equation .equation { font-size: 18px; color: #536a5f; }
.current-equation { border-left-color: var(--course-green); margin-top: 12px; padding: 10px 16px; background: #eaf3e7; }
.proof-reason, .pca-slide:has(.small-matrix) .proof-reason { font-size: 18px !important; line-height: 1.5; margin: 14px 0 !important; }
.proof-reason > span { font-size: 14px; }
.proof-nav { margin: 14px 0; gap: 12px; }
.proof-nav button { font-size: 15px; }
.weighted-sum { margin: 20px 0; padding-top: 16px; }
.weighted-sum > div { font-size: 22px; gap: 15px; flex-wrap: wrap; }
.weighted-sum small { font-size: 15px; }
.weighted-sum strong { font-size: 30px; }
.square-ledger button { font-size: 17px; }
.term-strip { gap: 12px; margin-top: 20px; }
.term-strip small { font-size: 14px; line-height: 1.4; }
.term-strip strong { font-size: 28px; }
.covariance-board { grid-template-columns: 165px minmax(0, 1fr); gap: 20px; }
.matrix-buttons button { min-width: 0; font-size: 20px; }
.matrix-buttons small { font-size: 13px; }
.table-row { font-size: 16px; }
.table-head { font-size: 13px; }
.candidate-controls button { font-size: 15px; }
.calculation-compare { flex-wrap: wrap; margin: 22px 0; }
.calculation-compare .metric strong { font-size: 29px; }
.mixture { margin-top: 20px; }
.mixture span { font-size: 17px; }
.small-matrix { font-size: 26px; }
.spectrum-bars > div, .spectrum-bars > button { font-size: 17px; }
.triangle-ledger { flex-wrap: wrap; gap: 16px; }
.triangle-ledger span { font-size: 15px; min-width: 110px; }
.triangle-ledger strong { font-size: 28px; }
.curve svg { max-height: none; }
.curve text { font-size: 16px; }
.exam-layout { gap: 36px; padding-top: 10px; }
.exam-layout p, .check p, .teachback li { font-size: 18px; line-height: 1.5; }
.check [role=status] { font-size: 17px; }
.check [role=status] small { font-size: 14px; }
.text-label, .check label, .teachback label { font-size: 16px; }
textarea, input[type=number] { font-size: 18px; }
.native-controls { border: 1px solid var(--course-line); }
.course-footer {
  position: fixed;
  inset: auto 0 0;
  height: var(--course-footer-height);
  padding: 0 22px;
  gap: 14px;
  background: #f7f8f1;
  color: var(--course-ink);
  z-index: 40;
}
.course-footer button { font-size: 15px; padding: 7px 12px; }
.course-footer button:last-child { background: var(--course-green); color: white; border-color: var(--course-green); }
.slide-picker { min-width: 0; font-size: 17px; gap: 14px; }
.slide-picker > span { color: var(--course-ink) !important; white-space: nowrap; }
.slide-picker small { font-size: 14px; }
.slide-picker select { max-width: min(430px, 37vw); min-width: 0; font-size: 15px; padding: 6px; }
.course-progress { position: fixed; height: 3px; z-index: 45; }
.drawer-backdrop { z-index: 60; padding: 20px; }
.course-drawer { background: #fffffc; color: var(--course-ink); border-color: var(--course-line); }
.course-drawer p, .course-drawer dd { color: #405c50; }
.course-drawer h2 { font-size: 34px; color: #173f36; }
.route-list strong { font-size: 18px; }
.route-list small { font-size: 14px; }
.route-list button { min-height: 60px; }
.close-drawer { min-width: 38px; }
.notation dd { font-size: 17px; line-height: 1.5; }
.status-page { padding-top: 130px; font-size: 19px; }
.status-page h1 { font-size: 38px; }
details, details p { font-size: 16px !important; }
@media (max-width: 1050px) {
  .course-nav { padding: 0 16px; gap: 10px; }
  .course-nav .wordmark span, .course-wordmark span { display: none; }
  .course-nav > div { gap: 4px; }
  .course-nav button { padding-inline: 8px; }
  .chapter-strip { justify-content: flex-start; padding-inline: 16px; }
  .chapter-link { padding-inline: 12px; }
  .pca-slide { padding: 23px 30px 32px; }
  .pca-slide h1 { font-size: 35px; }
  .scene-split, .scene-split.proof-layout, .exam-layout { grid-template-columns: minmax(0, 1fr); gap: 22px; }
  .scene-split.proof-layout .visual-side { order: 0; }
  .geometry { max-width: 510px; }
  .geometry.compact { max-width: 420px; }
  .reason-side { padding-top: 0; }
  .big-idea { font-size: 22px !important; }
  .course-footer { padding-inline: 16px; }
  .slide-picker select { max-width: 36vw; }
  .teachback { max-width: 760px; }
}
@media (max-width: 600px) {
  :root { --course-header-height: 88px; }
  .course-nav { align-content: center; flex-wrap: wrap; gap: 4px 10px; padding: 6px 12px; }
  .course-nav .wordmark, .course-nav .course-wordmark { font-size: 24px; }
  .course-nav > div { flex: 1 1 auto; justify-content: flex-end; flex-wrap: wrap; gap: 2px; }
  .course-nav button, .notebook-link { font-size: 15px; padding: 6px; min-height: 32px; }
  .notebook-link { border-left: 0; margin: 0; }
  .chapter-strip { padding-inline: 8px; }
  .chapter-link { padding-inline: 11px; font-size: 15px; }
  .pca-slide { padding: 20px 18px 30px; }
  .pca-slide h1 { font-size: 32px; }
  .chapter-label { font-size: 12px; }
  .reason-side p, .proof-layout .reason-side > p, .try p { font-size: 18px; }
  .big-idea { font-size: 21px !important; }
  .geometry { max-width: 510px; }
  .observation-select span { flex-basis: 100%; text-align: center; margin: 0; }
  .metrics { gap: 14px; }
  .metric { min-width: 115px; }
  .metric strong { font-size: 30px; }
  .proof .equation { font-size: 19px; }
  .previous-equation .equation, .proof-layout .previous-equation .equation { font-size: 18px; }
  .proof-nav button { font-size: 15px; }
  .covariance-board { grid-template-columns: 140px minmax(0, 1fr); gap: 12px; }
  .matrix-buttons button { font-size: 18px; padding-inline: 3px; }
  .table-row { font-size: 15px; gap: 5px; }
  .table-head { font-size: 13px; }
  .term-strip { flex-wrap: wrap; }
  .term-strip > div { min-width: 95px; }
  .course-footer { padding-inline: 8px; gap: 7px; }
  .course-footer button { font-size: 15px; padding: 7px 9px; }
  .slide-picker { gap: 5px; font-size: 16px; }
  .slide-picker select { max-width: 24vw; font-size: 15px; }
  .course-drawer { padding: 45px 22px 24px; }
  .course-drawer h2 { font-size: 30px; }
  .route-list strong { font-size: 17px; }
  .route-list button { gap: 12px; }
}
'''
p.write_text(s)
