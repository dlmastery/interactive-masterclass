/// <reference path="./marimo-studio.d.ts" />
import { Deck, Slide } from "@revealjs/react";
import { useEffect, useRef } from "react";
import type { RevealApi } from "reveal.js";
import { useMarimoValue } from "./lib/use-marimo-value.ts";
import "reveal.js/reveal.css";
import {LessonContent, LessonText, StepProof} from "./LessonText.tsx";

type Point = [number, number];
type Cloud = {
  points: Point[]; centered: Point[]; cov: number[][]; centerAmount: number;
  rho: number; w: Point; angle: number; projected: Point[]; variance: number;
  total: number; loss: number; curve: Point[]; eigenvalues: number[];
  axes: Point[]; scores: Point[]; pcAngle: number; reconstruction: Point[];
  k: number; reconstructionLoss: number; retained: number; degenerate: boolean;
};
type Units = {points:Point[];cov:number[][];axes:Point[];standardized:boolean;ratio:number;angle:number};
const fmt=(x:number|undefined,d=2)=>x===undefined?"…":x.toFixed(d);
const pct=(x:number|undefined)=>x===undefined?"…":`${(100*x).toFixed(1)}%`;
const source={"data-marimo-lens-inputs":"cloud-data","data-marimo-lens-render-source":'{"path":"src/Lesson.tsx"}'};
function Matrix({s}:{s?:number[][]}){return <div className="matrix" aria-label="Current covariance matrix"><span>S =</span><div>{(s??[[NaN,NaN],[NaN,NaN]]).flat().map((v,i)=><span key={i}>{Number.isNaN(v)?"…":fmt(v)}</span>)}</div></div>}
function Scatter({points=[],second,directions,direction,centroid,labels=["Feature 1 (a.u.)","Feature 2 (a.u.)"],title="Point cloud",quadrants=false}:{points?:Point[];second?:Point[];directions?:Point[];direction?:Point;centroid?:Point;labels?:string[];title?:string;quadrants?:boolean}){
  const all=[...points,...(second??[]),[0,0] as Point,...(centroid?[centroid]:[])];
  const minX=Math.min(...all.map(p=>p[0])),maxX=Math.max(...all.map(p=>p[0])),minY=Math.min(...all.map(p=>p[1])),maxY=Math.max(...all.map(p=>p[1]));
  const midX=(minX+maxX)/2,midY=(minY+maxY)/2;
  const scale=Math.min(486/Math.max(maxX-minX,1),342/Math.max(maxY-minY,1))*.87;
  const x=(v:number)=>330+(v-midX)*scale,y=(v:number)=>213-(v-midY)*scale;
  const loX=midX-258/scale,hiX=midX+258/scale,loY=midY-177/scale,hiY=midY+177/scale;
  const extent=Math.min(220/scale,155/scale),step=Math.max(1,Math.ceil(Math.max(hiX-loX,hiY-loY)/6));
  const ticks=Array.from({length:41},(_,i)=>(i-20)*step);
  return <svg className="scatter" viewBox="0 0 620 455" role="img" aria-label={title}><title>{title}</title>
    {quadrants&&<g opacity=".06"><rect x={x(0)} y={36} width={Math.max(0,588-x(0))} height={Math.max(0,y(0)-36)} fill="#127c78"/><rect x={72} y={y(0)} width={Math.max(0,x(0)-72)} height={Math.max(0,390-y(0))} fill="#127c78"/></g>}
    {ticks.filter(t=>t>loX&&t<hiX).map(t=><g key={`x${t}`}><line className={t===0?"zero":"grid"} x1={x(t)} x2={x(t)} y1="36" y2="390"/><text x={x(t)} y="415" textAnchor="middle">{t}</text></g>)}
    {ticks.filter(t=>t>loY&&t<hiY).map(t=><g key={`y${t}`}><line className={t===0?"zero":"grid"} x1="72" x2="588" y1={y(t)} y2={y(t)}/><text x="58" y={y(t)+6} textAnchor="end">{t}</text></g>)}
    <rect x="72" y="36" width="516" height="354" fill="none" className="frame"/>
    {directions?.map((v,i)=><g key={i}><line x1={x(-v[0]*extent)} y1={y(-v[1]*extent)} x2={x(v[0]*extent)} y2={y(v[1]*extent)} className={i===0?"pc1":"pc2"}/><text className="pc-label" x={x(v[0]*extent)+8} y={y(v[1]*extent)-10}>PC{i+1}</text></g>)}
    {direction&&<line x1={x(-direction[0]*extent)} y1={y(-direction[1]*extent)} x2={x(direction[0]*extent)} y2={y(direction[1]*extent)} className="pc2"/>}
    {second&&points.map((p,i)=><line key={i} x1={x(p[0])} y1={y(p[1])} x2={x(second[i][0])} y2={y(second[i][1])} className="residual"/>)}
    {points.map((p,i)=><circle key={i} cx={x(p[0])} cy={y(p[1])} r="4.3" className="point"><title>{`Observation ${i+1}: (${fmt(p[0])}, ${fmt(p[1])})`}</title></circle>)}
    {second?.map((p,i)=><circle key={i} cx={x(p[0])} cy={y(p[1])} r="3.6" className="projection"/>)}
    {centroid&&<g><path d={`M${x(centroid[0])-8},${y(centroid[1])}h16 M${x(centroid[0])},${y(centroid[1])-8}v16`} stroke="#a44516" strokeWidth="3"/><text x={x(centroid[0])+10} y={y(centroid[1])-14}>mean</text></g>}
    <text className="axis-title" x="330" y="448" textAnchor="middle">{labels[0]}</text><text className="axis-title" transform="translate(20 212) rotate(-90)" textAnchor="middle">{labels[1]}</text>
  </svg>;
}
function Curve({data}:{data?:Cloud}){
  const x=(v:number)=>75+v/180*480,y=(v:number)=>182-v/8*148;
  return <svg viewBox="0 0 620 240" className="curve" role="img" aria-label="Projected variance versus direction angle"><rect x="75" y="34" width="480" height="148" fill="none" className="frame"/>
    {[0,45,90,135,180].map(t=><g key={t}><line x1={x(t)} x2={x(t)} y1="34" y2="182" className="grid"/><text x={x(t)} y="205" textAnchor="middle">{t}°</text></g>)}
    {[0,2,4,6,8].map(t=><text key={t} x="63" y={y(t)+5} textAnchor="end">{t}</text>)}
    <path d={data?.curve.map(([a,v],i)=>`${i?"L":"M"}${x(a)},${y(v)}`).join(" ")??""} fill="none" className="pc1"/>
    {data&&<circle cx={x(data.angle)} cy={y(data.variance)} r="7" className="projection"/>}
    <text x="315" y="235" textAnchor="middle">Direction θ</text><text transform="translate(22 111) rotate(-90)" textAnchor="middle">Variance (a.u.²)</text></svg>;
}
const keyboardCondition=(event:KeyboardEvent)=>!event.composedPath().some(t=>t instanceof Element&&t.matches("marimo-cell,marimo-output,input,button,select,textarea"));
export const App=()=>{
 const deck=useRef<RevealApi|null>(null);
 const {hostRef,value:d,error}=useMarimoValue<Cloud>("cloud");
 const {hostRef:contentRef,value:content}=useMarimoValue<Record<string,string>>("lesson_content");
 const {hostRef:unitRef,value:u}=useMarimoValue<Units>("units");
 useEffect(()=>{const layout=()=>deck.current?.layout();document.addEventListener("marimo-studio:idle",layout);return()=>document.removeEventListener("marimo-studio:idle",layout);},[]);
 return <LessonContent.Provider value={content??{}}><span id="lesson-text-data" ref={contentRef} hidden mo-value="lesson_content" data-marimo-studio-site="site-3a3b56ed4191edc4d4a2a5a6699b92b03a101521cad91e9a1a9629d289faec4a"/><span id="cloud-data" ref={hostRef} hidden mo-value="cloud" data-marimo-studio-site="site-b3b9b11a2e93ffcbdbbf032ae5a3fd1586890c4db5dbf6bd2c97a8ce936c93be"/><span id="units-data" ref={unitRef} hidden mo-value="units" data-marimo-studio-site="site-75ca8811156d712963ccab0c730091f5c2fcea120ed1511f7f4bba1204ccd42d"/>
  <nav className="lesson-nav" aria-label="Lesson chapters"><span className="brand">PCA / an interactive lesson</span>{[['Geometry',1],['Covariance',2],['Derivation',4],['Example',6],['Reconstruction',9],['Units',11],['Quiz',13]].map(([name,index])=><button key={name} onClick={()=>deck.current?.slide(Number(index))}>{name}</button>)}</nav>
  {error&&<p role="alert">Notebook result unavailable: {error.message}</p>}
  <Deck className="studio-deck" deckRef={deck} config={{width:1280,height:800,margin:.03,controls:true,keyboardCondition,progress:true,slideNumber:'c/t',hash:true,center:false,scrollActivationWidth:0,transition:'fade'}}>
   <Slide><div className="split cover"><div><p className="kicker">01 / The question</p><h1>How much can<br/>one number<br/>tell us?</h1><p className="lead">Principal component analysis finds a new set of axes for your data.</p><p>Build the geometric intuition, then derive the answer from covariance.</p><button className="primary" onClick={()=>deck.current?.next()}>Explore the point cloud →</button></div><figure {...source}><Scatter points={d?.points} directions={d?.axes} title="Synthetic observations and principal axes"/><figcaption>One observation = two measurements.<br/>PC1 follows the direction of greatest spread.</figcaption></figure></div></Slide>
   <Slide><p className="kicker">02 / Centering</p><h2>The mean becomes our origin</h2><div className="split"><div><p className="question">Predict: does moving every point change the cloud's shape?</p><LessonText name="center_math"/><div className="control"><marimo-cell name="centering_control" data-marimo-studio-site="site-a443311b7a7bef05ebfc10b8dbf665b41c51cc9d6128c0f94bc2afbfe5803a1c"/></div><p className="small">Move the slider to 1. PCA describes deviations around the mean.</p></div><figure {...source}><Scatter points={d?.centered} centroid={d?[5*(1-d.centerAmount),3*(1-d.centerAmount)]:undefined} title="Point cloud translated toward zero mean"/><figcaption>Same observations, shifted origin. Both axes use equal scales.</figcaption></figure></div></Slide>
   <Slide><p className="kicker">03 / Covariance</p><h2>Do the features move together?</h2><div className="split"><div><LessonText name="covariance_math"/><div className="control"><marimo-cell name="correlation_control" data-marimo-studio-site="site-53491215ce5e11cbeaf43fea755a1bdf626b7311b32f5226c97d2d7033a46ffa"/></div><p className="small">Try positive, zero, and negative correlation. This updates the shared cloud throughout the lesson.</p></div><figure {...source}><Scatter points={d?.points} quadrants title="Covariance and centered deviations"/><Matrix s={d?.cov}/><figcaption>Shading: same-sign deviations. Variances stay fixed at 4.</figcaption></figure></div></Slide>
   <Slide><p className="kicker">04 / Projection experiment</p><h2>A direction turns each point into a score</h2><div className="split"><div><p className="question">Find the axis that preserves the most spread.</p><LessonText name="score_math"/><div className="control"><marimo-cell name="direction_control" data-marimo-studio-site="site-05103fbce4a5db6b518e13515b9e9b2c240d9a6c0f06c760d713c56e828a7c33"/></div><div className="metrics" {...source}><span>Retained variance<strong>{pct(d?d.variance/d.total:undefined)}</strong></span><span>Squared error / (n−1)<strong>{fmt(d?.loss)}</strong></span></div></div><figure {...source}><Scatter points={d?.points} second={d?.projected} direction={d?.w} title="Orthogonal projections onto the selected direction"/><figcaption><span className="teal">● Observations</span><span className="orange">● Projections</span><br/>Segments = discarded residuals</figcaption></figure></div></Slide>
   <Slide><p className="kicker">05 / Derivation, part I</p><h2>Projected variance is wᵀSw</h2><div className="split"><StepProof><LessonText name="variance_step1"/><LessonText name="variance_step2"/><LessonText name="variance_step3"/></StepProof><figure {...source}><Curve data={d}/><div className="result">Maximum at {d?.degenerate?"every angle":`${fmt(d?.pcAngle,0)}°`}<strong>{fmt(d?.eigenvalues[0])} a.u.²</strong></div><p className="small">The orange dot records your choice on the projection slide. The curve evaluates wᵀSw at every angle.</p><p className="hint">Use Next step to explore the derivation.</p></figure></div></Slide>
   <Slide><p className="kicker">06 / Derivation, part II</p><h2>The optimum is an eigenvector</h2><div className="full-proof"><StepProof><LessonText name="eigen_step1"/><LessonText name="eigen_step2"/><LessonText name="eigen_step3"/></StepProof></div><p className="hint">An eigenvector keeps its direction under S. Its eigenvalue measures variance along that direction.</p></Slide>
   <Slide><p className="kicker">07 / A calculation by hand</p><h2>Four points, one covariance matrix</h2><div className="split"><div><p className="question">A separate, tiny dataset makes every multiplication visible.</p><LessonText name="worked_data"/></div><div className="example-note"><p>Rows are observations.<br/>Columns are features.</p><p>Both column means are zero. These points are already centered.</p><p>The sample covariance divides by n−1 = 3.</p><p className="hint">Predict which diagonal direction should be PC1.</p></div></div></Slide>
   <Slide><p className="kicker">08 / The calculation completed</p><h2>The first axis retains 90% of variance</h2><div className="full-proof"><LessonText name="worked_solution"/></div><p className="hint">The remaining 10% is variation along the perpendicular direction.</p></Slide>
   <Slide><p className="kicker">09 / Remaining components</p><h2>The new coordinates are uncorrelated</h2><div className="split"><div><LessonText name="orthogonal_math"/><div className="metrics" {...source}><span>PC1 variance<strong>{fmt(d?.eigenvalues[0])}</strong></span><span>PC2 variance<strong>{fmt(d?.eigenvalues[1])}</strong></span></div><p className="small">Equal eigenvalues allow any orthonormal basis in that eigenspace.</p></div><figure {...source}><Scatter points={d?.scores} labels={["PC1 score (a.u.)","PC2 score (a.u.)"]} title="Principal component coordinates"/><figcaption>The shared cloud in its new coordinates.<br/>Cov(PC1, PC2) = 0 up to rounding.</figcaption></figure></div></Slide>
   <Slide><p className="kicker">10 / Compression</p><h2>Discarded variance becomes reconstruction error</h2><div className="split"><div><LessonText name="reconstruction_math"/><div className="control"><marimo-cell name="dimension_control" data-marimo-studio-site="site-2b31064f193ce2ac32532a8e473e4ba41f97fa343b2608ffca600c27f49eb383"/></div><div className="metrics" {...source}><span>Variance retained<strong>{pct(d?.retained)}</strong></span><span>Squared error / (n−1)<strong>{fmt(d?.reconstructionLoss)}</strong></span></div></div><figure {...source}><Scatter points={d?.points} second={d?.reconstruction} directions={d?.axes} title="Reconstruction from selected principal components"/><figcaption><span className="teal">● Original</span><span className="orange">● Reconstruction</span></figcaption></figure></div></Slide>
   <Slide><p className="kicker">11 / Why the objectives agree</p><h2>Pythagoras connects spread and error</h2><div className="full-proof"><LessonText name="loss_proof"/></div><div className="identity" {...source}><span>Total spread<strong>{fmt(d?.total)}</strong></span><b>=</b><span>Kept at your angle<strong>{fmt(d?.variance)}</strong></span><b>+</b><span>Lost at your angle<strong>{fmt(d?.loss)}</strong></span></div></Slide>
   <Slide><p className="kicker">12 / Choice of units</p><h2>Changing units can rotate PC1</h2><div className="split"><div><LessonText name="units_math"/><div className="control"><marimo-cell name="scale_control" data-marimo-studio-site="site-0720e10a6b9926f8edcd78865f12bc94b3fbaf9e7b921b3ec0f04585f6feec81"/></div><p className="question">Try ×8, then standardize. What changes back?</p></div><figure data-marimo-lens-inputs="units-data" data-marimo-lens-render-source='{"path":"src/Lesson.tsx"}'><Scatter points={u?.points} directions={u?.axes} labels={u?.standardized?["Standardized feature 1","Standardized feature 2"]:["Feature 1 (a.u.)","Feature 2 (rescaled units)"]} title="PCA after changing feature units"/><Matrix s={u?.cov}/><figcaption>PC1 angle {fmt(u?.angle,1)}°. Retains {pct(u?.ratio)} in the displayed metric.</figcaption></figure></div></Slide>
   <Slide><p className="kicker">13 / The implementation connection</p><h2>SVD gives the same principal directions</h2><div className="split"><div><LessonText name="svd_math"/></div><div className="code-panel"><LessonText name="implementation"/></div></div></Slide>
   <Slide><p className="kicker">14 / Check your understanding</p><h2>What has PCA actually learned?</h2><div className="split"><div><div className="control quiz"><marimo-cell name="quiz_control" data-marimo-studio-site="site-e8443cbb09d5280982f90de8ed90c1553a16a06096544a3ed8904a856d6f804b"/></div><div className="feedback"><marimo-cell name="quiz_feedback" data-marimo-studio-site="site-2e93aba62a507d69a72d35e22d2b31cb2644612f54eeb927bf5a2a27c18dc18a"/></div></div><div><LessonText name="cautions"/></div></div><p className="hint">Return to a chapter above and test your explanation against the live data.</p></Slide>
  </Deck><div className="runtime-note">Live notebook calculations · Arrow keys advance · Esc shows all slides</div>
 </LessonContent.Provider>;
};
