import marimo._code_mode as cm
import re

async with cm.get_context() as ctx:
    ctx.packages.add("numpy==2.5.3")
    for cell in ctx.cells:
        code = cell.code
        if "mo.md" not in code or "$$" not in code:
            continue
        if cell.name == "reconstruction_math":
            code = r'''mo.md(r"""
$$Z_k=X_cW_k,\qquad \widehat X_c=Z_kW_k^\top$$

$$\text{loss}=\frac{\lVert X_c-\widehat X_c\rVert_F^2}{n-1}$$

$$=\operatorname{tr}(S)-\sum_{j=1}^k\lambda_j=\sum_{j>k}\lambda_j$$

Add the mean back for original coordinates. Keeping all components preserves the data, up to rounding.
""")'''
        if cell.name == "variance_step2":
            code = r'''mo.md(r"""
Substitute $z=X_cw$.

$$\frac{(X_cw)^\top(X_cw)}{n-1}=\frac{w^\top X_c^\top X_cw}{n-1}$$

$$=w^\top\!\underbrace{\frac{X_c^\top X_c}{n-1}}_{S}\!w=w^\top Sw$$
""")'''
        code = re.sub(r"\$\$(.*?)\$\$", lambda m: "\n\n$$\n" + m.group(1).strip() + "\n$$\n\n", code, flags=re.S)
        ctx.edit_cell(cell.id, code)
        ctx.run_cell(cell.id)
print("Normalized display-math blocks")
