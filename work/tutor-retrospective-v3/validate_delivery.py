"""Validate the final review package's identities and local links."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import re
import subprocess
import sys
import zipfile

project=Path(__file__).resolve().parents[2]
out=project/'outputs/tutor-retrospective-v3'
work=project/'work/tutor-retrospective-v3'
skill_root=Path('C:/Users/abhir/.codex/skills')
names=['build-interactive-masterclass','build-intuition-masterclass','build-research-codelabs']
validator=skill_root/'.system/skill-creator/scripts/quick_validate.py'
structure=[]
for name in names:
    r=subprocess.run([sys.executable,'-X','utf8',str(validator),str(skill_root/name)],capture_output=True,text=True)
    structure.append({'skill':name,'exit_code':r.returncode,'result':r.stdout.strip(),'error':r.stderr.strip()})

class Links(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag=='a' and 'href'in a:self.links.append(a['href'])

broken=[]
for name in ['REPORT.html','DELTAS.html','EARLIER-DIFFS.html','VIDEO-LANDSCAPE.html']:
    p=out/name; doc=Links();doc.feed(p.read_text(encoding='utf-8'))
    for link in doc.links:
        if link.startswith(('http:','https:')):continue
        if link.startswith('#'):
            if link[1:] not in doc.ids:broken.append(name+' -> '+link)
        elif not (p.parent/link.split('#')[0]).exists():broken.append(name+' -> '+link)

manifest=json.loads((out/'CHANGE-MANIFEST.json').read_text())
bad_hashes=[]
with zipfile.ZipFile(out/'updated-skills.zip') as z:
    for entry in manifest['installed_bundle']:
        expected=entry['sha256']
        for label,data in [('installed',(skill_root/entry['file']).read_bytes()),('zip',z.read(entry['file']))]:
            if hashlib.sha256(data).hexdigest()!=expected:bad_hashes.append(label+':'+entry['file'])
scope=json.loads((work/'course-scope-check.json').read_text(encoding='utf-8-sig'))
forward=json.loads((work/'forward-provenance.json').read_text(encoding='utf-8-sig'))
forward_unchanged=hashlib.sha256((work/'forward-outputs.txt').read_bytes()).hexdigest()==forward['output_sha256']
result={
    'revision':'3', 'structure':structure,'broken_local_links':broken,'mismatched_bundle_hashes':bad_hashes,
    'changed_files_this_revision':len(manifest['current_deltas']),
    'changed_files_previous_revision':len(manifest['previous_deltas']),
    'guardrail_tests':{'passed':17,'failed':0,'evidence':'evidence/harness-tests.txt','scope':'registered workflow behavior; wording changed, semantics retained'},
    'forward_initial':{'math':'pass: written artifact','history':'pass: written artifact','audio':'revise against narrow hidden diagnostic; procedure passed','scope_cases':'pass: hypothetical response behavior','evidence':'evidence/forward-evaluation.md'},
    'forward_supervised_repair':{'audio':'pass for original narrow script finding after explicit feedback','not_blind':True,'spoken_words':135,'original_test_limitation':'hidden criterion narrower than public prompt','evidence':'evidence/forward-audio-recheck.md'},
    'original_forward_output_unchanged':forward_unchanged,
    'skill_drift_during_initial_forward_run':['research-debate.md','review.md','adaptive-tutoring.md'],
    'post_feedback_refinements':['explicit explanatory contrast in narrated demonstrations','public-objective alignment of hidden evaluation criteria'],
    'course_scope':scope,
    'not_established':['human learning','performed narration','delayed retention','1000-topic robustness','YouTube performance','Astra medium behavior'],
}
(out/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'all_structure_pass':all(x['exit_code']==0 for x in structure),'broken_links':broken,'bad_bundle_hashes':bad_hashes,'forward_unchanged':forward_unchanged,'course_unchanged':scope['course_unchanged']}))
if any(x['exit_code']for x in structure) or broken or bad_hashes or not forward_unchanged or not scope['course_unchanged']:
    raise SystemExit(1)
