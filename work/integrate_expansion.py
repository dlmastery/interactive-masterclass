from pathlib import Path
import json
p=Path('outputs/pca-studio/v/lesson/src/PcaScenes.tsx')
s=p.read_text(encoding='utf-8')
a=s.index('  if (s.scene === "expansion") {')
b=s.index('  if (s.scene === "covariance") {',a)
s=s[:a]+'''  if (s.scene === "expansion") {
    return split(
      <><ProductExpansion c={c} angle={angle} person={p} setPerson={setPerson} step={n === 21 ? proofStep : n === 22 ? 3 + proofStep : 5} />{angleControl}</>,
      <>{eq}<p>The same direction weights apply to all four observations. Each score is squared first. Then we add those squares and divide by n−1.</p></>,
      "derivation-layout",
    );
  }
'''+s[b:]
p.write_text(s,encoding='utf-8')
p=Path('work/pca_course_v2.py')
course=json.loads(Path('outputs/pca-studio/course-v2.json').read_text(encoding='utf-8'))
p.write_text('pca_course_v2 = '+repr(course)+'\nNone\n',encoding='utf-8')
