import marimo._code_mode as cm
import re
import subprocess
import sys
import marimo_studio

names = []
async with cm.get_context() as ctx:
    for cell in ctx.cells:
        code = cell.code
        match = re.search(r'mo\.md\((r?"""[\s\S]*?""")\)', code)
        if not match or cell.name in ("welcome", "data_explanation"):
            continue
        name = cell.name
        variable = "text_" + name
        replacement = variable + " = " + match.group(1) + "\nmo.md(" + variable + ")"
        ctx.edit_cell(cell.id, code[:match.start()] + replacement + code[match.end():])
        ctx.run_cell(cell.id)
        names.append(name)
    cid = ctx.create_cell("lesson_content = {\n" + "\n".join(repr(n) + ": text_" + n + "," for n in names) + "\n}\nNone", name="slide_content")
    ctx.run_cell(cid)
print("Projected lesson text:", names)
view = marimo_studio.agent.current_workspace().view("lesson")
root = (await view.inspect()).root
subprocess.run([sys.executable, "-m", "deno", "add", "--frozen=false", "--save-exact", "npm:katex@0.16.22", "npm:marked@15.0.12"], cwd=root, check=True)
