from pathlib import Path
import os
import zipfile
root=Path('outputs/pca-studio')
out=Path('outputs/pca-studio-source.zip')
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as archive:
    for folder, dirs, files in os.walk(root):
        dirs[:]=[d for d in dirs if d not in {'.artifacts','__pycache__','__marimo__','.venv','node_modules','archive-v1'}]
        for name in files:
            path=Path(folder)/name
            if path.suffix in {'.lock'} and name!='deno.lock':
                continue
            archive.write(path,Path('pca-studio')/path.relative_to(root))
print(f'{out}: {out.stat().st_size:,} bytes')
with zipfile.ZipFile(out) as archive:
    print(f'{len(archive.namelist())} files packaged')
