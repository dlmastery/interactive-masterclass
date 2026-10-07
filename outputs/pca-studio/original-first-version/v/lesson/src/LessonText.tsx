// @deno-types="npm:@types/katex@0.16.7"
import katex from "katex";
import { marked } from "marked";
import { createContext, useContext, useState, type ReactNode } from "react";

export const LessonContent = createContext<Record<string,string>>({});
export function LessonText({name}:{name:string}) {
  const text=useContext(LessonContent)[name];
  if(!text)return <div className="lesson-text" aria-busy="true">Loading lesson…</div>;
  const equations:string[]=[];
  const markdown=text.replace(/\$\$([\s\S]*?)\$\$|\$([^$\n]+?)\$/g,(_match,block,inline)=>{
    const display=block!==undefined;
    const html=katex.renderToString((block??inline).trim(),{displayMode:display,throwOnError:true,trust:false});
    const index=equations.push(display?`<div class="math-display">${html}</div>`:html)-1;
    return `MATHSLOT${index}END`;
  });
  const html=(marked.parse(markdown,{async:false}) as string).replace(/MATHSLOT(\d+)END/g,(_m,i)=>equations[Number(i)]);
  return <div className="lesson-text" data-marimo-lens-inputs="lesson-text-data" data-marimo-lens-label={name} data-marimo-lens-render-source='{"path":"src/LessonText.tsx"}' dangerouslySetInnerHTML={{__html:html}}/>;
}
export function StepProof({children}:{children:ReactNode[]}){
  const [step,setStep]=useState(0);
  return <div className="step-proof">
    <div className="step-nav"><span>Step {step+1} of {children.length}</span><button disabled={step===0} onClick={()=>setStep(step-1)}>Previous step</button><button disabled={step===children.length-1} onClick={()=>setStep(step+1)}>Next step</button></div>
    <div className="step-body">{children.map((child,i)=><div key={i} hidden={i!==step}>{child}</div>)}</div>
  </div>;
}
