from pathlib import Path
root=Path('outputs/pca-studio/v/lesson/src')
for name in ['PcaDerivationVisuals.tsx','PcaProductExpansion.tsx']:
 p=root/name;s=p.read_text(encoding='utf-8').replace('<section\n','<div\n      role="region"\n').replace('</section>','</div>');p.write_text(s,encoding='utf-8')
p=root/'PcaScenes.tsx';s=p.read_text(encoding='utf-8')
a=s.index('  if (s.scene === "geometry") {');b=s.index('  if (s.scene === "center") {',a)
part=s[a:b]
start=part.index('        {n === 1 && (')
end=part.index('        <p className="diagram-caption">',start)
purpose=part[start:end]
part=part[:start]+part[end:]
control='        {(n !== 8 || phase === 1) && angleControl}\n'
part=part.replace(control,'')
part=part.replace('        {geo(\n',control+'        {geo(\n',1)
part=part.replace('        <p className="big-idea">',purpose+'        <p className="big-idea">',1)
part=part.replace('PCA chooses new axes through the center of a dataset.','Principal component analysis (PCA) chooses new axes through the center of a dataset.')
# The opening gets a compact experiment beside the explanation at IAB width.
last=part.rfind('      </>,\n    );')
assert last>=0
part=part[:last]+part[last:].replace('      </>,\n    );','      </>,\n      "opening-scene",\n    );',1)
s=s[:a]+part+s[b:];p.write_text(s,encoding='utf-8')
p=root/'pca.css';s=p.read_text(encoding='utf-8')+'''\n/* Keep the opening experiment within reach in an app side panel. */\n@media(min-width:800px){\n.scene-split.opening-scene{grid-template-columns:minmax(0,1.08fr) minmax(0,1fr);gap:26px}\n.opening-scene .geometry{max-width:460px}\n.opening-scene .geometry svg text{font-size:22px}\n.opening-scene .opening-purpose{font-size:19px;line-height:1.4}\n.opening-scene .big-idea{font-size:18px!important;line-height:1.5}\n.opening-scene .compression-card{padding:12px;margin:14px 0}\n.opening-scene .compression-card>div{padding:9px 0;gap:8px}\n.opening-scene .compression-card strong{font-size:19px}\n.opening-scene .compression-card small{font-size:14px}\n.opening-scene .angle-controls{margin:6px 0 0}\n.opening-scene .diagram-caption{font-size:15px;margin:0 0 8px}\n}\n.pca-deck.reveal .slides>section.present{pointer-events:auto}\n.derivation-layout{grid-template-columns:minmax(0,1.35fr) minmax(0,1fr)}\n@media(max-width:1050px){.scene-split.derivation-layout{grid-template-columns:minmax(0,1fr)}}\n''';p.write_text(s,encoding='utf-8')
