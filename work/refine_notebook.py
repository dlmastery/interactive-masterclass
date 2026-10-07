import marimo._code_mode as cm
async with cm.get_context() as ctx:
    c = ctx.cells["score_math"]
    old = c.code
    code = old.replace("The **score** $z_i$ is a signed coordinate along the axis.\nThe **loading vector** $w$ tells us how to combine the original features.\nThe perpendicular segments show what a one-number representation loses.", "The **score** $z_i$ locates a point along the axis.\nThe **loading vector** $w$ combines the features.\nPerpendicular segments show the lost information.")
    ctx.edit_cell(c.id, code)
    ctx.run_cell(c.id)
print("Shortened projection slide copy")
