from pathlib import Path
import marimo._code_mode as cm
root = Path('C:/Users/abhir/Documents/Codex/2026-10-03/exp')
async with cm.get_context() as ctx:
    cell = ctx.cells['pca_course_v2']
    prior = cell.code
    ctx.edit_cell(cell.id, (root / 'work/pca_course_v2.py').read_text(encoding='utf-8'))
    ctx.run_cell(cell.id)
    print(cell.status)
print('Synced the repaired learner copy to its native notebook cell.')
