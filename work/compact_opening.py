from pathlib import Path
p=Path('outputs/pca-studio/v/lesson/src/PcaScenes.tsx');s=p.read_text(encoding='utf-8')
a=s.index('  if (s.scene === "geometry") {');b=s.index('  if (s.scene === "center") {',a);part=s[a:b]
control='        {(n !== 8 || phase === 1) && angleControl}\n';part=part.replace(control,'')
part=part.replace('        {n === 3\n',control+'        {n === 3\n',1)
x=part.index('            A marker needs two coordinates.');y=part.index('          </p>',x)
part=part[:x]+'            Turn the axis. Keep <strong>one score</strong> for each marker. Watch the error change.\n'+part[y:]
part=part.replace('Principal component analysis (PCA) chooses new axes through the center of a dataset. We can then keep fewer coordinates. A good axis lets us recover the points with small squared errors.','Principal component analysis (PCA) finds new axes for the data. Here, we keep one coordinate and choose the axis with the smallest total squared error.')
s=s[:a]+part+s[b:];p.write_text(s,encoding='utf-8')
p=Path('outputs/pca-studio/v/lesson/src/pca.css');p.write_text(p.read_text(encoding='utf-8')+'''\n.opening-scene .pca-slider{padding:10px 14px}\n.opening-scene .preset-row{margin-top:6px}\n.opening-scene .preset-row button{padding:5px 13px;min-height:30px}\n.opening-scene .angle-controls{margin:10px 0}\n.opening-scene .geometry{max-width:460px}\n''',encoding='utf-8')
