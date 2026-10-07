from pathlib import Path
import re

root=Path("outputs/pca-studio/v/lesson/src")
p=root/"Lesson.tsx"
s=p.read_text(encoding="utf-8")
s=s.replace('import "reveal.js/reveal.css";', 'import "reveal.js/reveal.css";\nimport {LessonContent, LessonText, StepProof} from "./LessonText.tsx";')
names=["center_math","covariance_math","score_math","variance_step1","variance_step2","variance_step3","eigen_step1","eigen_step2","eigen_step3","worked_data","worked_solution","orthogonal_math","reconstruction_math","loss_proof","units_math","svd_math","implementation","cautions"]
for name in names:
    s=s.replace(f'<marimo-cell name="{name}"/>',f'<LessonText name="{name}"/>')
s=s.replace(' const {hostRef:unitRef,value:u}', ' const {hostRef:contentRef,value:content}=useMarimoValue<Record<string,string>>("lesson_content");\n const {hostRef:unitRef,value:u}')
s=s.replace(' return <><span id="cloud-data"', ' return <LessonContent.Provider value={content??{}}><span id="lesson-text-data" ref={contentRef} hidden mo-value="lesson_content"/><span id="cloud-data"')
s=s.replace(' </>;\n};',' </LessonContent.Provider>;\n};')
s=s.replace('<div className="proof"><LessonText name="variance_step1"/><div className="fragment"><LessonText name="variance_step2"/></div><div className="fragment"><LessonText name="variance_step3"/></div></div>', '<StepProof><LessonText name="variance_step1"/><LessonText name="variance_step2"/><LessonText name="variance_step3"/></StepProof>')
s=s.replace('<div className="proof full-proof"><LessonText name="eigen_step1"/><div className="fragment"><LessonText name="eigen_step2"/></div><div className="fragment"><LessonText name="eigen_step3"/></div></div>', '<div className="full-proof"><StepProof><LessonText name="eigen_step1"/><LessonText name="eigen_step2"/><LessonText name="eigen_step3"/></StepProof></div>')
s=s.replace('The next arrow reveals each step.', 'Use Next step to explore the derivation.')
p.write_text(s,encoding="utf-8")
with (root/"lesson.css").open("a",encoding="utf-8") as f:
    f.write('''
.lesson-text{font-size:25px;line-height:1.5;color:#203333}.lesson-text p{margin:12px 0!important}.lesson-text .katex{font-size:1.12em}.lesson-text .katex-display{margin:16px 0;text-align:left}.math-display{display:block;margin:16px 0}.lesson-text ul{font-size:23px;margin:0;padding-left:24px;line-height:1.5}.lesson-text li{margin-bottom:14px}.lesson-text pre{margin:12px 0;padding:18px;background:#eef0e8;font:18px/1.6 Consolas,monospace;white-space:pre-wrap}.code-panel .lesson-text{font-size:22px}.code-panel .lesson-text h2{font-size:27px;margin-bottom:20px}.full-proof .lesson-text{font-size:29px}.step-nav{display:flex;align-items:center;gap:10px;border-bottom:1px solid #c8d5cb;padding-bottom:14px;margin-bottom:32px;font-size:18px}.step-nav span{margin-right:auto;color:#5f7871}.step-nav button{font:500 16px "Segoe UI",sans-serif;border:1px solid #a9beb4;border-radius:4px;background:transparent;color:#245f58;padding:9px 12px;cursor:pointer}.step-nav button:disabled{opacity:.3;cursor:default}.step-nav button:focus-visible{outline:3px solid #c76b25;outline-offset:2px}.step-body{min-height:420px}.full-proof .step-body{min-height:350px}.step-body [hidden]{display:none!important}
''')
print("Updated projected text and proof step controls")
