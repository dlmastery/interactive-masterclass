from pathlib import Path
import base64, hashlib, json, re, datetime

root = Path('\\\\?\\' + str(Path('outputs/pca-studio/v/lesson/.artifacts/.cache/deno/2.9.7/gen').resolve()))
groups = {}
for path in root.rglob('Lesson.tsx.js'):
    text = path.read_text(encoding='utf-8')
    match = re.search(r'sourceMappingURL=data:application/json;base64,([^\r\n]+)', text)
    if not match:
        continue
    data = json.loads(base64.b64decode(match.group(1)))
    source = data['sourcesContent'][0]
    digest = hashlib.sha256(source.encode()).hexdigest()
    entry = groups.setdefault(digest, {'sha256':digest, 'source':source, 'candidates':[]})
    entry['candidates'].append({'path':str(path.resolve()), 'time':datetime.datetime.fromtimestamp(path.stat().st_mtime).isoformat()})

out = Path('work/recovered-original')
out.mkdir(exist_ok=True)
manifest = []
for digest, entry in groups.items():
    source = entry.pop('source')
    entry['characters'] = len(source)
    entry['section_count'] = len(re.findall(r'<(?:section|Slide)\b', source))
    if len(source) > 100:
        target = out / f'Lesson-{digest[:12]}.tsx'
        target.write_bytes(source.encode('utf-8'))
        entry['extracted_source'] = str(target.resolve())
    manifest.append(entry)
    print(digest[:12],len(source),entry['section_count'], entry['candidates'][0]['time'], len(entry['candidates']))
(out/'manifest.json').write_text(json.dumps(manifest, indent=2),encoding='utf-8')
