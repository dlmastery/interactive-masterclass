from pathlib import Path
import json,re

before=json.loads(Path('work/course-before-learner-copy.json').read_text(encoding='utf-8'))
after=json.loads(Path('outputs/pca-studio/course-v2.json').read_text(encoding='utf-8'))
changes={key:sum(a[key]!=b[key] for a,b in zip(before['slides'],after['slides'])) for key in ['title','action','claim']}
changes['why']=sum(x['why']!=y['why'] for a,b in zip(before['slides'],after['slides']) for x,y in zip(a['steps'],b['steps']))
sentences=[]
for s in after['slides']:
    values=[('action',s['action'],20),('claim',s['claim'],25)]+[('reason '+str(i+1),step['why'],25) for i,step in enumerate(s['steps'])]
    for label, text, limit in values:
        for sentence in re.split(r'(?<=[.!?])\s+',text):
            count=len(sentence.split())
            sentences.append((s['id'],label,sentence,count,limit))
failures=[item for item in sentences if item[3]>item[4]]
print(json.dumps({'changes':changes,'slide_sentences':len(sentences),'length_failures':failures},ensure_ascii=False,indent=2))
