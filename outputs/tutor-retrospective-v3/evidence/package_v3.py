"""Create reviewable exact skill deltas and a bundle. Does not edit the course."""
from pathlib import Path
import difflib
import hashlib
import html
import json
import re
import shutil
import zipfile

project = Path(__file__).resolve().parents[2]
work = project / 'work/tutor-retrospective-v3'
out = project / 'outputs/tutor-retrospective-v3'
installed = Path('C:/Users/abhir/.codex/skills')
names = ('build-interactive-masterclass', 'build-intuition-masterclass', 'build-research-codelabs')

def files(root, selected):
    return {str(p.relative_to(root)).replace('\\','/'):p for name in selected
            for p in (root/name).rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path else None

def diff_bundle(before_root, after_root, selected, patch_name, html_name, title):
    before, after = files(before_root, selected), files(after_root, selected)
    records, patches, sections, links = [], [], [], []
    hd = difflib.HtmlDiff(wrapcolumn=100)
    for name in sorted(before.keys() | after.keys()):
        a, b = before.get(name), after.get(name)
        if digest(a) == digest(b):
            continue
        left = a.read_text(encoding='utf-8-sig').splitlines() if a else []
        right = b.read_text(encoding='utf-8-sig').splitlines() if b else []
        patch = list(difflib.unified_diff(left,right,fromfile='before/'+name,tofile='after/'+name,lineterm=''))
        patches.extend(patch)
        count_add = sum(x.startswith('+') and not x.startswith('+++') for x in patch)
        count_del = sum(x.startswith('-') and not x.startswith('---') for x in patch)
        anchor = 'file-' + str(len(records)+1)
        records.append({'file':name,'before_sha256':digest(a),'after_sha256':digest(b),'added_lines':count_add,'removed_lines':count_del,'diff_anchor':anchor})
        links.append(f'<li><a href="#{anchor}">{html.escape(name)}</a> · +{count_add} / −{count_del}</li>')
        table = hd.make_table(left,right,fromdesc=html.escape('Before: '+name),todesc=html.escape('After: '+name),context=True,numlines=4)
        sections.append(f'<section id="{anchor}"><h2>{html.escape(name)}</h2><p>+{count_add} / −{count_del} lines. Content diff normalizes line endings; hashes identify exact saved bytes.</p><div class="wide">{table}</div></section>')
    (out/patch_name).write_text('\n'.join(patches)+'\n',encoding='utf-8')
    page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Skill diffs</title><style>body{font:16px/1.5 system-ui;background:#f6f5f1;color:#202d35;margin:0;padding:28px}h1{font-size:2rem}a{color:#075b80}.wide{overflow:auto;background:white;border:1px solid #ccd5da;margin-bottom:35px}table.diff{font:12px/1.5 Consolas,monospace;border-collapse:collapse;width:100%}td,th{padding:4px;vertical-align:top}.diff_header{background:#e6edf0}.diff_next{background:#e8edf2}.diff_add{background:#c9efcf}.diff_sub{background:#ffd4d4}.diff_chg{background:#ffeab1}section{scroll-margin-top:15px}li{margin:5px 0}.meta{color:#53636d}</style></head><body>'''
    page+=f'<p><a href="REPORT.html">Return to report</a> · <a href="{patch_name}">Download unified patch</a></p><h1>{html.escape(title)}</h1><p class="meta">{len(records)} changed files. Green: added; red: removed; amber: changed. Four surrounding lines are shown; new files are shown in full. Use horizontal scroll for wide comparisons.</p><ul>'+''.join(links)+'</ul>'+''.join(sections)+'</body></html>'
    (out/html_name).write_text(page,encoding='utf-8')
    return records

current=diff_bundle(out/'before-skills',installed,names,'v2-to-v3.patch','DELTAS.html','Current revision: version 2 to version 3')
previous=project/'outputs/tutor-retrospective'
historical=diff_bundle(previous/'before-skills',previous/'updated-skills',names[:2],'earlier-v1-to-v2.patch','EARLIER-DIFFS.html','Previously missing deltas: version 1 to version 2')

evidence=out/'evidence'; evidence.mkdir(exist_ok=True)
for p in work.iterdir():
    if p.is_file() and p.suffix in {'.md','.txt','.json','.py'}:
        shutil.copy2(p,evidence/p.name)
manifest=[]; broken=[]
for name,p in files(installed,names).items():
    dest=out/'updated-skills'/name; dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(p,dest); manifest.append({'file':name,'sha256':digest(p)})
    if p.suffix=='.md':
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8-sig')):
            if not link.startswith(('http:','https:','#')) and not (p.parent/link.split('#')[0]).exists():
                broken.append(str(p)+' -> '+link)
with zipfile.ZipFile(out/'updated-skills.zip','w',zipfile.ZIP_DEFLATED) as z:
    for item in manifest:z.write(out/'updated-skills'/item['file'],item['file'])

ledger=json.loads((work/'pca-video-candidates.json').read_text(encoding='utf-8-sig'))
videos=ledger['candidates']
assert len({v['youtube_id'] for v in videos})==len(videos)>=30
rows=[]
for v in videos:
    metrics=v['observed_metrics']
    esc=lambda x:html.escape(str(x))
    count=lambda x:'unknown' if x is None else f'{x:,}'
    rows.append(f'<tr><td>{esc(v["candidate_id"])}</td><td><a href="{esc(v["url"])}">{esc(v["title"])}</a><br>{esc(v.get("creator") or "unknown creator")}</td><td>{count(metrics.get("views"))}<br>{count(metrics.get("likes"))} likes</td><td>{esc(", ".join(v["topic_angle"]))}</td><td>{esc(v["access"]["current_pass"])}<br>{esc(v["access"].get("prior_access",""))}</td><td>{esc(v["candidate_value_inference"])}<br><strong>Limit:</strong> {esc(v["inspection_limit"])}</td><td>{"Shortlist" if v["initial_shortlist"] else "Candidate"}<br>{esc(v["next_inspection_question"])}</td></tr>')
landscape='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PCA video candidate landscape</title><style>body{font:15px/1.5 system-ui;margin:25px;color:#202d35;background:#f6f5f1}table{border-collapse:collapse;background:white}th,td{border:1px solid #ccd3d8;padding:10px;text-align:left;vertical-align:top}th{background:#e5edf0}a{color:#075b80}.wide{overflow:auto}</style></head><body><a href="REPORT.html">Return to report</a><h1>31 PCA video candidates</h1><p>This is broad discovery, not a global ranking or completed review. Every current-pass entry is metadata-level. View/like counts are observed indexed snapshots with unknown underlying counter dates. No videos were watched in this pass. Candidate strengths are selection hypotheses. Ten entries are shortlisted for future inspection.</p><p><a href="evidence/pca-video-candidates.json">Full JSON ledger and provenance</a></p><div class="wide"><table><tr><th>ID</th><th>Video / creator</th><th>Indexed views / likes</th><th>Advertised scope</th><th>Access</th><th>Proposed value and limit</th><th>Next action</th></tr>'''+''.join(rows)+'</table></div></body></html>'
(out/'VIDEO-LANDSCAPE.html').write_text(landscape,encoding='utf-8')

(out/'CHANGE-MANIFEST.json').write_text(json.dumps({'current_deltas':current,'previous_deltas':historical,'installed_bundle':manifest,'broken_skill_links':broken},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'current_changed_files':len(current),'previous_changed_files':len(historical),'packaged_files':len(manifest),'video_candidates':len(videos),'broken_skill_links':broken}))
if broken:raise SystemExit(1)
