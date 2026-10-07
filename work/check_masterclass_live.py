import marimo._code_mode as cm
import marimo_studio
async with cm.get_context() as ctx:
    for name in ['masterclass_model','masterclass_controls','masterclass_sandbox','masterclass_data','masterclass_guide']:
        c=ctx.cells[name]
        print(name,c.status,c.errors)
    print('context readers', [n for n in dir(ctx) if any(s in n for s in ['value','variable','globals'])])
v=marimo_studio.agent.current_workspace().view('lesson')
print(await v.build())
