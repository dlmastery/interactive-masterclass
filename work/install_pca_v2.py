from pathlib import Path
import marimo._code_mode as cm
root=Path('C:/Users/abhir/Documents/Codex/2026-10-03/exp/work')
async with cm.get_context() as ctx:
    for name in ['pca_course_v2','pca_alternatives_v2','masterclass_controls']:
        filename='masterclass_sandbox_control.py' if name=='masterclass_controls' else name+'.py'
        code=(root/filename).read_text(encoding='utf-8')
        found=next((c for c in ctx.cells if c.name==name),None)
        if found:
            cid=found.id
            ctx.edit_cell(cid,code)
        else: cid=ctx.create_cell(code,name=name)
        ctx.run_cell(cid)
print('Installed PCA-first course and additional notebook-owned visual calculations.')
