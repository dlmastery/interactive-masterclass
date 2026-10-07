from pathlib import Path
p=Path('outputs/pca-studio/v/lesson/src/PcaScenes.tsx')
s=p.read_text(encoding='utf-8')
colors={'#26394c':'#dfe6dd','#52647b':'#87958e','#23374e':'#e1e8de','#102036':'#fbfaf6','#62e1cd15':'#177e6b12','#62e1cd':'#177e6b','#ff9f7a':'#c6642c','#dfeaf5':'#203b34','#8298b2':'#61756e'}
for a,b in colors.items():s=s.replace(a,b)
s=s.replace('const s = 187 / bound','const s = 200 / bound').replace('213 - (y - center[1]) * s','225 - (y - center[1]) * s')
start=s.index('className={"geometry "')
end=s.index('function VarianceCurve(')
b=s[start:end]
b=b.replace('viewBox="0 0 590 480"','viewBox="0 0 590 540"').replace('y2="363"','y2="430"').replace('y="238"','y="248"').replace('y="235"','y="248"')
for a,b2 in [('y1="416"','y1="476"'),('y2="416"','y2="476"'),('y1="408"','y1="468"'),('y2="424"','y2="484"'),('y="391"','y="449"'),('cy={416}','cy={476}'),('y={450}','y={510}')]:b=b.replace(a,b2)
b=b.replace('r="5"\n                fill={teal}','r="5"\n                fill={coral}')
b=b.replace('opacity={person === i ? 1 : .34}','opacity={person === i ? 1 : .65}')
b=b.replace('stroke={teal}\n            strokeWidth="2.5"','stroke={coral}\n            strokeWidth="2.5"')
s=s[:start]+b+s[end:]
p.write_text(s,encoding='utf-8')
p=Path('outputs/pca-studio/v/lesson/src/pca.css')
p.write_text(p.read_text(encoding='utf-8')+'''\n/* Concrete compression experiment. */\n.opening-purpose{font-size:20px;line-height:1.5;margin:0 0 14px;color:#203b34;max-width:650px}\n.compression-card{border:1px solid #d5ded7;border-radius:16px;background:#fff;padding:20px;margin:20px 0}\n.compression-card>div{display:flex;justify-content:space-between;gap:16px;align-items:center;padding:12px 0;border-bottom:1px solid #e7ebe4}\n.compression-card small{font-size:15px;max-width:200px;line-height:1.5;color:#61756e}\n.compression-card strong{font-size:22px;font-variant-numeric:tabular-nums;color:#176859;white-space:nowrap}\n.compression-card p{font-size:17px!important;margin:16px 0 0!important}\n.diagram-legend{display:flex;flex-wrap:wrap;justify-content:center;gap:12px;font-size:15px!important;color:#61756e;margin:8px 0 16px!important}\n.geometry svg{max-height:none}\n@media(max-width:1050px){.opening-purpose{font-size:19px}.compression-card{max-width:650px}}\n''',encoding='utf-8')
