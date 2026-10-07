import json
import marimo._code_mode as cm
async with cm.get_context() as ctx:
    for name in ['pca_course_v2','pca_alternatives_v2']:
        c=ctx.cells[name]
        print(name,c.status,c.errors)
    for key in ['pca_cov_v2','pca_edges_v2','pca_scales_v2','pca_course_v2']:
        print(key,len(json.dumps(ctx.globals[key]).encode()))
import marimo_studio
v=marimo_studio.agent.current_workspace().view('lesson')
print(await v.build())
print(await v.validate(level='runtime'))
