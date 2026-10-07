/// <reference path="./marimo-studio.d.ts" />
import { Deck, Slide } from "@revealjs/react";
import { useEffect, useRef, useState } from "react";
import type { RevealApi } from "reveal.js";
import "reveal.js/reveal.css";
import { useMarimoValue } from "./lib/use-marimo-value.ts";
import { chapters, scenes } from "./course.ts";
import { type Live, MathText, Visual } from "./Visuals.tsx";
import type { Point } from "./math.ts";
import { checkpoints } from "./checkpoints.ts";
import { ExplainBack } from "./LearningVisuals.tsx";
const config = {
  width: "100%",
  height: "100%",
  margin: 0,
  center: false,
  controls: false,
  progress: false,
  slideNumber: false,
  keyboard: false,
  touch: false,
  hash: false,
  scrollActivationWidth: 0,
  transition: "none",
} as const;
export function App() {
  const deck = useRef<RevealApi | null>(null);
  const [active, setActive] = useState(0),
    [panel, setPanel] = useState(""),
    [answer, setAnswer] = useState<number | null>(null);
  const s = scenes[active];
  const { hostRef, value: data, error } = useMarimoValue<
    { base: { raw: Point[] } }
  >("pca_data");
  const { hostRef: liveRef, value: live } = useMarimoValue<Live>("pca_live");
  const jump = (n: number) => {
    setActive(Math.max(0, Math.min(scenes.length - 1, n)));
    setAnswer(null);
    setPanel("");
  };
  useEffect(() => {
    let frame = 0, stop = false;
    function sync() {
      if (stop) return;
      if (deck.current?.isReady()) {
        deck.current.slide(active);
        deck.current.layout();
        deck.current.getCurrentSlide()?.querySelector<HTMLElement>(".scene")
          ?.scrollTo({ top: 0, left: 0 });
      } else frame = requestAnimationFrame(sync);
    }
    sync();
    return () => {
      stop = true;
      cancelAnimationFrame(frame);
    };
  }, [active, data]);
  useEffect(() => {
    function key(e: KeyboardEvent) {
      if (e.key === "Escape") {
        setPanel("");
        return;
      }
      if (
        panel || e.composedPath().some((t) =>
          t instanceof Element &&
          t.matches("input,button,textarea,select,a,marimo-cell")
        )
      ) return;
      if (e.key === "ArrowRight" || e.key === "PageDown") {
        e.preventDefault();
        jump(active + 1);
      }
      if (e.key === "ArrowLeft" || e.key === "PageUp") {
        e.preventDefault();
        jump(active - 1);
      }
    }
    window.addEventListener("keydown", key);
    const layout = () => deck.current?.layout();
    window.addEventListener("marimo-studio:idle", layout);
    return () => {
      window.removeEventListener("keydown", key);
      window.removeEventListener("marimo-studio:idle", layout);
    };
  }, [active, panel]);
  return (
    <div className="course">
      <span hidden mo-value="pca_data" ref={hostRef} />
      <span hidden mo-value="pca_live" ref={liveRef} />
      <header className="topbar">
        <div className="brand">
          <b>PCA</b>
          <span>A shorter description</span>
        </div>
        <nav>
          <button onClick={() => setPanel(panel === "route" ? "" : "route")}>
            Learning route
          </button>
          <button onClick={() => setPanel(panel === "notes" ? "" : "notes")}>
            Speaker notes
          </button>
          <button onClick={() => setPanel(panel === "help" ? "" : "help")}>
            Math help
          </button>
          <button onClick={() => setPanel(panel === "recall" ? "" : "recall")}>
            Pause & recall
          </button>
        </nav>
      </header>
      {error && (
        <div className="runtime-error">
          Notebook connection:{" "}
          {error.message}. The diagrams can still run, but live Python results
          are not available.
        </div>
      )}
      <div className="deck-space">
        <Deck config={config} deckRef={deck}>
          {scenes.map((scene, i) => (
            <Slide key={scene.id} notes={scene.notes}>
              <div className="scene">
                <div className="scene-copy">
                  <p className="eyebrow">
                    {String(scene.chapter + 1).padStart(2, "0")} /{" "}
                    {chapters[scene.chapter]}
                  </p>
                  <h1>{scene.title}</h1>
                  <p className="question">{scene.question}</p>
                  <p className="body">{scene.body}</p>
                  {scene.formula && <MathText tex={scene.formula} />}
                  <div className="takeaway">
                    <span>THE IDEA TO KEEP</span>
                    <p>{scene.takeaway}</p>
                  </div>
                  {scene.prompt && <p className="prompt">{scene.prompt}</p>}
                  {scene.choices && (
                    <div className="answers">
                      {scene.choices.map((c, j) => (
                        <button
                          key={j}
                          aria-pressed={answer === j}
                          onClick={() => setAnswer(j)}
                        >
                          {c}
                        </button>
                      ))}
                      {answer !== null && (
                        <p role="status" className="feedback">
                          {scene.feedback?.[answer]}
                        </p>
                      )}
                    </div>
                  )}
                </div>
                <div className="scene-visual">
                  {i === active && (
                    <Visual
                      key={scene.id}
                      s={scene}
                      live={live}
                      raw={data?.base.raw}
                    />
                  )}
                </div>
              </div>
            </Slide>
          ))}
        </Deck>
      </div>
      <footer>
        <button onClick={() => jump(active - 1)} disabled={active === 0}>
          ← Back
        </button>
        <label className="jump-label">
          <span>{active + 1} / {scenes.length}</span>
          <select
            aria-label="Choose a slide"
            value={active}
            onChange={(e) => jump(Number(e.target.value))}
          >
            {scenes.map((x, i) => (
              <option key={x.id} value={i}>{i + 1}. {x.title}</option>
            ))}
          </select>
        </label>
        <button
          className="primary"
          onClick={() => jump(active + 1)}
          disabled={active === scenes.length - 1}
        >
          Next →
        </button>
      </footer>
      <div className="progress">
        <i style={{ width: `${(active + 1) / scenes.length * 100}%` }} />
      </div>
      {panel && (
        <div className="panel-shade" onClick={() => setPanel("")}>
          <div
            className="panel"
            role="dialog"
            aria-modal="true"
            aria-label={panel === "route"
              ? "Learning route"
              : panel === "notes"
              ? "Speaker notes"
              : panel === "recall"
              ? "Pause and recall"
              : "Math at this step"}
            onClick={(e) => e.stopPropagation()}
          >
            <button className="close" autoFocus onClick={() => setPanel("")}>
              Close ×
            </button>
            {panel === "route"
              ? (
                <>
                  <p className="eyebrow">ONE QUESTION LEADS TO THE NEXT</p>
                  <h2>Your route through PCA</h2>
                  <p>
                    Start with the picture. Build the proof. Test the promise.
                  </p>
                  <ol className="route">
                    {chapters.map((c, k) => {
                      const start = scenes.findIndex((x) => x.chapter === k),
                        count = scenes.filter((x) => x.chapter === k).length;
                      return (
                        <li key={c}>
                          <button
                            disabled={start < 0}
                            onClick={() => jump(start)}
                          >
                            <b>{String(k + 1).padStart(2, "0")}</b>
                            <span>
                              {c}
                              <small>
                                {count}{" "}
                                scenes{s.chapter === k ? " · You are here" : ""}
                              </small>
                            </span>
                          </button>
                        </li>
                      );
                    })}
                  </ol>
                  <p className="caption">
                    Use the slide menu to jump to a specific question. Reload
                    starts at the opening; keep your slide number if you take a
                    break.
                  </p>
                </>
              )
              : panel === "notes"
              ? (
                <>
                  <p className="eyebrow">
                    SCENE {active + 1} · PRESENTER SCRIPT
                  </p>
                  <h2>{s.title}</h2>
                  <div className="script">
                    {s.notes.split(/(?=\[)/).map((p, i) => <p key={i}>{p}</p>)}
                  </div>
                  <p className="caption">
                    Brackets are visual cues. Text outside brackets is the
                    spoken script. These are authored notes, not a recorded
                    voice track.
                  </p>
                  {s.source && (
                    <a href={s.source} target="_blank" rel="noreferrer">
                      Primary source
                    </a>
                  )}
                </>
              )
              : panel === "recall"
              ? (
                <>
                  <p className="eyebrow">
                    CHAPTER CHECKPOINT · ATTEMPT BEFORE HELP
                  </p>
                  <h2>{checkpoints[s.chapter][0]}</h2>
                  <p>{checkpoints[s.chapter][1]}</p>
                  <ExplainBack
                    s={{
                      ...s,
                      id: "checkpoint-" + s.chapter,
                      rubric: [...checkpoints[s.chapter][2]],
                      example: undefined,
                    }}
                  />
                  <button className="primary" onClick={() => setPanel("")}>
                    Return to the exact scene
                  </button>
                </>
              )
              : (
                <>
                  <p className="eyebrow">ONLY THE MATH WE NEED NOW</p>
                  <h2>{s.refresh?.[0] ?? "A point, a ruler, and a gap"}</h2>
                  <p>
                    {s.refresh?.[1] ??
                      "A point has two coordinates. A direction is a pair of weights that locates a unit ruler. A score is one signed distance on that ruler. A reconstruction is the point recovered from the score. The residual is the gap from the reconstruction to the original point."}
                  </p>
                  <button className="primary" onClick={() => setPanel("")}>
                    Return to this step
                  </button>
                </>
              )}
          </div>
        </div>
      )}
    </div>
  );
}
