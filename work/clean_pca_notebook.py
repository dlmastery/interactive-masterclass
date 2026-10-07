from pathlib import Path
import marimo._code_mode as cm
_file=Path('C:/Users/abhir/Documents/Codex/2026-10-03/exp/outputs/pca-studio/pca_lesson.py')
_backup=_file.parent/'archive-v1'/'pca_lesson-before-cleanup.py'
if not _backup.exists():_backup.write_text(_file.read_text(encoding='utf-8'),encoding='utf-8')
_keep={'imports','welcome','masterclass_model','masterclass_data','masterclass_controls','masterclass_sandbox','pca_course_v2','pca_alternatives_v2','notebook_results','notebook_course'}
async with cm.get_context() as ctx:
    _snapshot=[(c.id,c.name,c.code) for c in ctx.cells]
    for _c in list(ctx.cells):
        if _c.name not in _keep:ctx.delete_cell(_c.id)
    _welcome=ctx.cells['welcome']
    ctx.edit_cell(_welcome.id,'''mo.md("""
# PCA: from picture to proof

This notebook supplies the calculations for the 64-slide course.

[Open the slides](http://localhost:2719/lesson/)

The example uses four invented position measurements in centimeters.
The first three observations stay fixed. Use the two controls below to change observation D.
The results update when you change either value.

Use **Course route** in the slides to move between six questions.
Use **Math at this step** for a short refresher without leaving the current scene.

The six expandable sections below contain the full argument and its equation steps.
""")''')
    ctx.run_cell(_welcome.id)
    _code='''_r=sandbox_lab
mo.vstack([
    mo.md("## The current model"),
    mo.ui.table([{"Observation":chr(65+i),"x (cm)":p[0],"y (cm)":p[1]} for i,p in enumerate(_r["raw"])],selection=None),
    mo.md(f"Mean: **{_r['mean']}**. PC1 angle: **{_r['angle']:.2f} degrees**. Retained variance: **{100*_r['ratio']:.2f}%**."),
    mo.md("### Covariance matrix"),
    mo.ui.table([{"Row":i+1,"Column 1":p[0],"Column 2":p[1]} for i,p in enumerate(_r["cov"])],selection=None),
    mo.md("### Eigenvalues and unit directions"),
    mo.ui.table([{"Component":i+1,"Eigenvalue":v,"x weight":_r["axes"][i][0],"y weight":_r["axes"][i][1]} for i,v in enumerate(_r["values"])],selection=None)
])'''
    _found=next((c for c in ctx.cells if c.name=='notebook_results'),None)
    if _found:ctx.edit_cell(_found.id,_code);_cid=_found.id
    else:_cid=ctx.create_cell(_code,name='notebook_results')
    ctx.run_cell(_cid)
    _course_code='''_sections={}
for _chapter in pca_course_v2['chapters']:
    _parts=[]
    for _slide in pca_course_v2['slides'][_chapter['start']:_chapter['end']]:
        _body='### '+str(_slide['id'])+'. '+_slide['title']+'\\n\\n'+_slide['claim']+'\\n\\n'
        for _step in _slide['steps']:
            _body+='$$'+_step['tex']+'$$\\n\\n'+_step['why']+'\\n\\n'
        _parts.append(mo.md(_body))
    _sections[_chapter['question']]=mo.vstack(_parts)
mo.accordion(_sections)'''
    _found=next((c for c in ctx.cells if c.name=='notebook_course'),None)
    if _found:ctx.edit_cell(_found.id,_course_code);_cid=_found.id
    else:_cid=ctx.create_cell(_course_code,name='notebook_course')
    ctx.run_cell(_cid)
print('Removed stale teaching cells after saving a backup. Added live results and six readable course sections.')
