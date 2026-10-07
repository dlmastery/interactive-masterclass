from pathlib import Path
import ast, base64, hashlib, json, re, shutil

workspace = Path.cwd().resolve()
project = workspace / 'outputs/pca-studio'
dest = project / 'original-first-version'
view = dest / 'v/lesson'
source_root = view / 'src'
source_root.mkdir(parents=True, exist_ok=True)

def sha(data):
    return hashlib.sha256(data).hexdigest()

records = []
def save(relative, data, origin, operation):
    target = dest / relative
    assert target.resolve().is_relative_to(dest.resolve())
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    records.append({'path':relative.replace('\\','/'), 'sha256':sha(data), 'bytes':len(data),
                    'origin':str(origin), 'operation':operation})

manifest = json.loads((workspace/'work/recovered-original/manifest.json').read_text(encoding='utf-8'))
entry = next(item for item in manifest if item['sha256'].startswith('cd4aee2df30c'))
candidate = next(item for item in entry['candidates'] if item['time'].startswith('2026-10-03T23:57:56'))
cache_dir = Path(candidate['path']).parent

def decode(path):
    text = path.read_text(encoding='utf-8')
    match = re.search(r'sourceMappingURL=data:application/json;base64,([^\r\n]+)', text)
    data = json.loads(base64.b64decode(match.group(1)))
    return data['sourcesContent'][0].encode('utf-8')

original = decode(cache_dir/'Lesson.tsx.js')
assert sha(original) == entry['sha256']
clean, stripped = re.subn(rb' data-marimo-studio-site="[^"]+"', b'', original)
assert clean.count(b'<Slide>') == 14
save('v/lesson/src/Lesson.tsx', clean, candidate['path'], f'Extract sourcesContent; remove only {stripped} injected data-marimo-studio-site attributes.')

for name in ['LessonText.tsx', 'main.tsx', 'lib/use-marimo-value.ts']:
    path = cache_dir/(name+'.js')
    save('v/lesson/src/'+name, decode(path), path, 'Extract exact sourcesContent from the same original build candidate.')

for name in ['lesson.css', 'marimo-studio.d.ts', 'index.html']:
    path = project/'v/lesson/src'/name
    save('v/lesson/src/'+name, path.read_bytes(), path, 'Copy surviving source unchanged.')

for name in ['view.toml', 'deno.json', 'deno.lock']:
    path = project/'v/lesson'/name
    save('v/lesson/'+name, path.read_bytes(), path, 'Copy existing pinned Studio scaffolding unchanged; not claimed to be a historical snapshot.')

notebook_source = project/'archive-v1/pca_lesson-before-cleanup.py'
notebook = notebook_source.read_bytes()
text = notebook.decode('utf-8')
tree = ast.parse(text)
first_later = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'masterclass_model')
cut_line = min(dec.lineno for dec in first_later.decorator_list)
prefix = ''.join(text.splitlines(keepends=True)[:cut_line-1]).rstrip()
recovered_notebook = (prefix+'\n\n\nif __name__ == "__main__":\n    app.run()\n').encode('utf-8')
recovered_tree = ast.parse(recovered_notebook.decode('utf-8'))
cell_names = [node.name for node in recovered_tree.body if isinstance(node, ast.FunctionDef)]
assert len(cell_names) == 32, cell_names
assert cell_names[-1] == 'slide_content'
assert set(re.findall(rb'<marimo-cell name="([^"]+)"', clean)).issubset({name.encode() for name in cell_names})
assert b'data-marimo-studio-site=' not in clean
save('pca_lesson.py', recovered_notebook, notebook_source, f'Keep original first {len(cell_names)} cells through slide_content; remove later cells; append app.run entry point.')
(workspace/'work/recovered-original/pca_lesson.py').write_bytes(recovered_notebook)

readme = '''# Original PCA lesson — recovered source

This folder preserves the original **14-slide lesson**, before the 54-slide and 64-slide expansions. It uses the light background, large point-cloud illustration, two-column composition, and native notebook controls shown in `../../pca-preview.png`.

**Status: recovered source only.** No native build, live execution, or browser comparison has been performed on this recovered package. It is not presented as a tested runnable release.

## What was recovered

- `v/lesson/src/Lesson.tsx`: the full original 14-slide component from native Studio's Deno cache. Only ten injected `data-marimo-studio-site` attributes were removed. Fresh Studio builds must generate their own mount IDs.
- `v/lesson/src/LessonText.tsx`, `main.tsx`, and `lib/use-marimo-value.ts`: exact source-map content from the same original build candidate.
- `v/lesson/src/lesson.css`: surviving original stylesheet, copied unchanged.
- `pca_lesson.py`: the original 32 notebook cells, through `slide_content`, extracted from the notebook backup. Later masterclass cells were removed. A standard `app.run()` entry point was retained.
- Studio declarations, HTML, view configuration, and pinned dependency files were copied from the existing project. These provide scaffolding; this is not a complete historical repository snapshot.

The recovered component was cached on 2026-10-03 at 23:57:56 and 23:58:05, before the saved original screenshot. The source uses a deterministic 48-point cloud, native correlation and projection controls, covariance calculations, a four-point worked example, reconstruction, units, SVD, and a quiz.

`recovery-manifest.json` records exact source locations, transformations, SHA-256 values, and verification status. The original build-stage component hash is `cd4aee2df30cc8863dd9b92f4af7e02f9dd2a3469b50252f55ce86f9d0ea071f`.

## Before presenting this version

1. Build this notebook's own `lesson` view with native marimo-studio, using the pinned dependencies.
2. Validate all notebook bindings and run it on separate ports from the active course.
3. Test correlation, centering, angle, component count, units, and quiz controls.
4. Compare slide 4 at angle 45 degrees and correlation 0.75 with the original screenshot. Expected retained variance: 87.5%. Expected displayed loss: 1.00.

Only Python syntax, the 32-cell extraction, the 14-slide count, and file hashes were checked during recovery. This package does not replace or change the active course. The original 14-slide sequence is an earlier baseline; it does not satisfy the later 50-plus-slide masterclass request on its own.
'''
save('README.md', readme.encode('utf-8'), 'Recovery investigation', 'New provenance and status notes; no runnable claim.')

record = {
    'schema':1, 'status':'source recovery only; not built or executed',
    'slide_count':14, 'notebook_cell_count':len(cell_names), 'cell_names':cell_names,
    'original_component_sha256':entry['sha256'], 'original_cache_candidates':entry['candidates'],
    'injected_attributes_removed':stripped, 'files':records,
    'verification':{'python_ast':'passed', 'slide_count':'14', 'browser_render':'not run', 'native_build':'not run'},
}
(dest/'recovery-manifest.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
assert all(sha((dest/item['path']).read_bytes()) == item['sha256'] for item in records)
print(json.dumps({'destination':str(dest), 'slides':14, 'cells':len(cell_names), 'files':len(records),
                  'clean_component_sha256':sha(clean), 'notebook_sha256':sha(recovered_notebook), 'removed_attributes':stripped},indent=2))
