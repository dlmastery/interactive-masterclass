import json,re
from pathlib import Path
c=json.loads(Path('outputs/pca-studio/course-v2.json').read_text())
items=[]
for s in c['slides']:
    items.extend([(f"slide {s['id']} claim",s['claim'],25),(f"slide {s['id']} action",s['action'],20)])
    items.extend((f"slide {s['id']} reason {i+1}",step['why'],25) for i,step in enumerate(s['steps']))
for key,(_,body) in c['refreshers'].items():items.append(('refresher '+key,body,25))
rows=[]
for label,body,limit in items:
    for sentence in re.split(r'(?<=[.!?])\s+',body):
        count=len(re.findall(r"\S+",sentence))
        rows.append(dict(source=label,text=sentence,words=count,limit=limit,pass_length=count<=limit))
fail=[r for r in rows if not r['pass_length']]
report={'scope':'Notebook-owned claims, learner prompts, proof reasons, and refreshers. Frontend interface copy reviewed separately.','sentences':len(rows),'pass_length':len(rows)-len(fail),'percentage':round(100*(len(rows)-len(fail))/len(rows),1),'limits':'Instructions: 20 words. Descriptions: 25 words. Simple whitespace counts; not a formal STE word-count implementation.','not_certification':'This verifies sentence length only. It does not establish an 80% dictionary, approved-meaning, or part-of-speech compliance rate.','failures':fail}
Path('outputs/pca-studio/language-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
