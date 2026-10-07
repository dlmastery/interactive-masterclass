import marimo._code_mode as cm
import marimo_studio

async with cm.get_context() as ctx:
    empty = next((c for c in ctx.cells if not c.code.strip()), None)
    if empty:
        ctx.edit_cell(empty.id, "import marimo as mo\nimport numpy as np", name="imports")
        ctx.run_cell(empty.id)
    else:
        cid = ctx.create_cell("import marimo as mo\nimport numpy as np", name="imports")
        ctx.run_cell(cid)
    cid = ctx.create_cell('mo.md("# Principal component analysis\\nA geometric intuition, followed by the covariance derivation.")', name="welcome")
    ctx.run_cell(cid)

workspace = marimo_studio.agent.current_workspace()
print([(s.id, str(s.availability)) for s in await workspace.starters()])
view = await workspace.create_view("lesson", starter="marimo-studio/react:reveal")
print(await view.build())
