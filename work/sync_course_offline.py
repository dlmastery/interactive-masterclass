from pathlib import Path
import ast,json
p=Path('outputs/pca-studio/pca_lesson.py')
s=p.read_text(encoding='utf-8')
t=ast.parse(s)
f=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='pca_course_v2')
a=next(n for n in f.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='pca_course_v2' for x in n.targets))
lines=s.splitlines(keepends=True)
new=json.loads(Path('outputs/pca-studio/course-v2.json').read_text(encoding='utf-8'))
lines[a.lineno-1:a.end_lineno]=['    pca_course_v2 = '+repr(new)+'\n']
p.write_text(''.join(lines),encoding='utf-8')
ast.parse(p.read_text(encoding='utf-8'))
print('Synced native notebook course literal; preserved cell and return declaration.')
