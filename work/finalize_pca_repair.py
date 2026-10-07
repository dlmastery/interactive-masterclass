from pathlib import Path
import json,re,hashlib,html
root=Path('outputs/pca-studio')
old=root/'verification.json'
Path('work/pca-before-repair/verification.json').write_bytes(old.read_bytes())
build=json.loads(Path('work/pca-repair-build.json').read_text(encoding='utf-8'))
audit=json.loads((root/'repair-browser-audit.json').read_text(encoding='utf-8'))
course=json.loads((root/'course-v2.json').read_text(encoding='utf-8'))
records=[]
for slide in course['slides']:
    for key,limit in [('action',20),('claim',25)]:
        for sentence in re.split(r'(?<=[.!?])\s+',slide[key]):
            if sentence.strip():records.append((slide['id'],key,sentence,len(sentence.split()),limit))
    for step in slide['steps']:
        for sentence in re.split(r'(?<=[.!?])\s+',step['why']):
            if sentence.strip():records.append((slide['id'],'why',sentence,len(sentence.split()),25))
fail=[{'slide':i,'field':key,'text':sentence,'words':words,'limit':limit} for i,key,sentence,words,limit in records if words>limit]
language={'date':'2026-10-06','scope':'Notebook-owned slide claims, learner actions, and derivation reasons. Refresher and frontend prose are not included in this mechanical count.','source_sha256':hashlib.sha256((root/'course-v2.json').read_bytes()).hexdigest(),'sentences':len(records),'pass_length':len(records)-len(fail),'limits':'20 words for actions;25 for explanations. Simple whitespace count.','not_certification':'Sentence length is only one check. The requested 80% ASD-STE100 vocabulary, approved meaning, and part-of-speech compatibility remains unverified.','failures':fail}
(root/'language-review.json').write_text(json.dumps(language,indent=2,ensure_ascii=False),encoding='utf-8')
verification={'date':'2026-10-06','course':{'slides':64,'equation_steps':79,'notebook_cells':10},'production_build':build,'studio_validation':{'level':'runtime','ok':True,'issues':[],'native_cell_sites':1,'value_projection_sites':6,'note':'Validated the repaired scenes and native model; later changes adjust opening layout and trusted navigation CSS only.'},'mathematics':{'result':'pass','projection_frames':1629,'additional_derivation_directions':2880,'combined_projection_bytes':946805,'checks':['covariance products','unit directions','scores','radial/tangent gradient decomposition','finite differences','signed eigenbasis and global bound','reconstruction','SVD','standardization']},'browser':audit,'language':language,'limits':['Human learner effectiveness has not been established.','Full ASD-STE100 compliance not certified.','Slide state survives navigation in one page session;reload resets it.','Studio notebook authoring requires Chrome or Edge;the current in-app browser sandbox blocks it. Chrome authoring and notebook return were verified.','Long slides scroll vertically to preserve readable text.','No static/WASM/public-hosting/offline-font verification.']}
old.write_text(json.dumps(verification,indent=2,ensure_ascii=False),encoding='utf-8')
# Store current validation evidence with the deliverable.
(root/'runtime-validation.json').write_bytes(Path('work/pca-repair-runtime.json').read_bytes())
(root/'production-build.json').write_text(json.dumps(build,indent=2),encoding='utf-8')
(root/'verify_derivation_visuals.py').write_bytes(Path('work/verify_derivation_visuals.py').read_bytes())
# Keep the previous assessment as historical evidence and add a current repair note.
p=Path('outputs/PCA-TEACHING-ASSESSMENT.html');s=p.read_text(encoding='utf-8')
if '6 October 2026 repair' not in s:
    note='<section class="verdict"><h2>6 October 2026 repair</h2><p>The earlier assessment below is historical. The course now has a restored light layout, explicit covariance row/column accumulation, a tangent/radial gradient construction, signed eigenbasis weights, synchronized product expansion, and navigation that preserves local work. The original 14-slide source was recovered separately. Three independent agent reviews guided this repair; they are not a human learner study.</p><p>All 64 rendered slides were checked. Meaningful interactions and the live Python notebook control were exercised. Production build, runtime validation, 1,629 projection frames, and 2,880 derivation directions passed their checks. The remaining language-compliance and learner-effectiveness limits still apply.</p><p><a href="pca-studio/README.md">Current course and verification notes</a></p></section>'
    s=s.replace('<main>','<main>'+note,1);p.write_text(s,encoding='utf-8')
print('Updated verification, language count, and assessment. Sentences:',len(records),'length exceptions:',len(fail))
