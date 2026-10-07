from pathlib import Path
import marimo._code_mode as cm
root=Path('C:/Users/abhir/Documents/Codex/2026-10-03/exp/work')
async with cm.get_context() as ctx:
    for name,filename in [('masterclass_model','masterclass_model.py'),('masterclass_data','masterclass_data.py'),('masterclass_controls','masterclass_sandbox_control.py'),('masterclass_sandbox','masterclass_sandbox.py'),('masterclass_guide','masterclass_content.py')]:
        code=(root/filename).read_text(encoding='utf-8')
        if name=='masterclass_guide':
            code+='\n'+(root/'masterclass_bridges.py').read_text(encoding='utf-8')
        found=next((c for c in ctx.cells if c.name==name),None)
        if found:
            cid=found.id
            ctx.edit_cell(cid,code)
        else:
            cid=ctx.create_cell(code,name=name)
        ctx.run_cell(cid)
print('Created masterclass model, teaching content, prepared interaction frames, and live sandbox controls.')
