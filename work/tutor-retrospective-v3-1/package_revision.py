"""Package a focused teaching-skill revision; leave course files untouched."""
from pathlib import Path
from html.parser import HTMLParser
import difflib
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import zipfile

project=Path(__file__).resolve().parents[2]
work=project/'work/tutor-retrospective-v3-1'
out=project/'outputs/tutor-retrospective-v3-1'
root=Path('C:/Users/abhir/.codex/skills')
names=['build-interactive-masterclass','build-intuition-masterclass','build-research-codelabs']
def inventory(base):
    return {p.relative_to(base).as_posix():p for n in names for p in (base/n).rglob('*')
            if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p else None
before=inventory(out/'before-skills'); after=inventory(root)
changes=[]; patch=[]; sections=[]
for name in sorted(before.keys()|after.keys()):
    a,b=before.get(name),after.get(name)
    if sha(a)==sha(b):continue
    al=a.read_text(encoding='utf-8-sig').splitlines() if a else []
    bl=b.read_text(encoding='utf-8-sig').splitlines() if b else []
    delta=list(difflib.unified_diff(al,bl,fromfile='before/'+name,tofile='after/'+name,lineterm=''))
    patch.extend(delta)
    anchor='change-'+str(len(changes)+1)
    changes.append({'file':name,'before_sha256':sha(a),'after_sha256':sha(b),'anchor':anchor,
                    'added_lines':sum(s.startswith('+') and not s.startswith('+++') for s in delta),
                    'removed_lines':sum(s.startswith('-') and not s.startswith('---') for s in delta)})
    table=difflib.HtmlDiff(wrapcolumn=100).make_table(al,bl,fromdesc=html.escape('Before: '+name),todesc=html.escape('After: '+name),context=True,numlines=4)
    sections.append('<section id="'+anchor+'"><h2>'+html.escape(name)+'</h2><div class="wide">'+table+'</div></section>')
(out/'v3-to-v3-1.patch').write_text('\n'.join(patch)+'\n',encoding='utf-8')
diffpage='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Version 3.1 skill diffs</title><style>body{font:16px/1.5 system-ui;background:#f6f5f1;color:#20323c;margin:28px}a{color:#075f88}.wide{overflow:auto;background:white;border:1px solid #c9d4d9;margin-bottom:32px}table.diff{font:12px/1.5 Consolas,monospace;border-collapse:collapse;width:100%}td,th{padding:4px;vertical-align:top}.diff_header{background:#e5edf1}.diff_next{background:#e8edf2}.diff_add{background:#c9efcf}.diff_sub{background:#ffd4d4}.diff_chg{background:#ffeab1}li{margin:6px 0}</style></head><body><a href="REPORT.html">Return to report</a><h1>Version 3 to 3.1 — exact skill changes</h1>'''
diffpage+=f'<p>{len(changes)} changed files. Green: added; red: removed; amber: changed. Content comparison normalizes line endings; hashes identify exact file bytes.</p><p><a href="v3-to-v3-1.patch">Unified patch</a> · <a href="CHANGE-MANIFEST.json">File hashes</a> · <a href="updated-skills.zip">Complete updated bundle</a></p><ul>'
diffpage+=''.join('<li><a href="#'+c['anchor']+'">'+html.escape(c['file'])+'</a> · +'+str(c['added_lines'])+' / −'+str(c['removed_lines'])+'</li>' for c in changes)
diffpage+='</ul>'+''.join(sections)+'</body></html>'
(out/'DELTAS.html').write_text(diffpage,encoding='utf-8')

evidence=out/'evidence';evidence.mkdir(exist_ok=True)
for p in work.iterdir():
    if p.is_file() and p.suffix in {'.md','.txt','.json','.py'}:shutil.copy2(p,evidence/p.name)
receipt=work/'welch-source-inspection/access-manifest.json'
(evidence/'welch-source-inspection').mkdir(exist_ok=True)
shutil.copy2(receipt,evidence/'welch-source-inspection/access-manifest.json')

manifest=[];bad_skill_links=[]
for name,p in after.items():
    dest=out/'updated-skills'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    manifest.append({'file':name,'sha256':sha(p)})
    if p.suffix=='.md':
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8-sig')):
            if not link.startswith(('http:','https:','#')) and not (p.parent/link.split('#')[0]).exists():
                bad_skill_links.append(name+' -> '+link)
with zipfile.ZipFile(out/'updated-skills.zip','w',zipfile.ZIP_DEFLATED) as z:
    for entry in manifest:z.write(out/'updated-skills'/entry['file'],entry['file'])
(out/'CHANGE-MANIFEST.json').write_text(json.dumps({'revision':'3.1','deltas':changes,'installed_bundle':manifest},indent=2)+'\n',encoding='utf-8')

structure=[]
for name in names:
    r=subprocess.run([sys.executable,'-X','utf8',str(root/'.system/skill-creator/scripts/quick_validate.py'),str(root/name)],capture_output=True,text=True)
    structure.append({'skill':name,'exit_code':r.returncode,'stdout':r.stdout.strip(),'stderr':r.stderr.strip()})
script_changes=[c['file'] for c in changes if c['file'].endswith('.py')]
baseline=json.loads((project/'work/tutor-retrospective-v3/course-before.json').read_text(encoding='utf-8-sig'))
course_changes=[]
for entry in baseline:
    p=Path(entry['path'])
    if not p.exists() or sha(p)!=entry['sha256'].lower():course_changes.append(str(p))
bad_zip=[]
with zipfile.ZipFile(out/'updated-skills.zip') as z:
    for entry in manifest:
        if hashlib.sha256(z.read(entry['file'])).hexdigest()!=entry['sha256']:bad_zip.append(entry['file'])
validation={'revision':'3.1','changed_skill_files':len(changes),'packaged_files':len(manifest),
    'structure':structure,'broken_skill_links':bad_skill_links,'bundle_hash_mismatches':bad_zip,
    'executable_scripts_unchanged':not script_changes,'changed_scripts':script_changes,
    'course_baseline_files_compared':len(baseline),'course_baseline_changed_or_missing':course_changes,
    'review':'author-informed written integration review; three findings fixed and passed supervised recheck',
    'behavior_sample':'supervised hypothetical density teach-back: recipient adaptation versus subject misconception',
    'source_access':'creator text, research summaries, indexed official transcript, Welch notebook text/selected code, and two rendered workbook pages',
    'not_performed':['source-video playback/listening','Welch notebook execution','six-lens independent forward test','human learning observation','course rebuild','narration rehearsal','Astra model run'],
    'broken_report_links':[]}
# Make the receipt exist before validating links to it.
(out/'VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n',encoding='utf-8')
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])
broken=[]
for name in ['REPORT.html','DELTAS.html']:
    p=out/name;doc=Links();doc.feed(p.read_text(encoding='utf-8'))
    for link in doc.links:
        if link.startswith(('http:','https:')):continue
        if link.startswith('#'):
            if link[1:] not in doc.ids:broken.append(name+' -> '+link)
        elif not (p.parent/link.split('#')[0]).exists():broken.append(name+' -> '+link)
validation['broken_report_links']=broken
(out/'VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'changed_skill_files':len(changes),'bundle_files':len(manifest),'structure_pass':all(s['exit_code']==0 for s in structure),'bad_skill_links':bad_skill_links,'bad_report_links':broken,'bad_zip_hashes':bad_zip,'scripts_unchanged':not script_changes,'course_files_unchanged':not course_changes,'course_baseline_files':len(baseline)}))
if any(s['exit_code'] for s in structure) or bad_skill_links or broken or bad_zip or course_changes:raise SystemExit(1)
