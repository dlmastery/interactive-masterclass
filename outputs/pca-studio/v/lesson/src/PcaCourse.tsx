/// <reference path="./marimo-studio.d.ts" />
import { Deck, Slide } from "@revealjs/react";
import { useEffect, useRef, useState } from "react";
import type { RevealApi } from "reveal.js";
import "reveal.js/reveal.css";
import { useMarimoValue } from "./lib/use-marimo-value.ts";
import { type Case, type Lab } from "./LabComponents.tsx";
import { type Lesson, Scene } from "./PcaScenes.tsx";

type Course = {
  title: string;
  chapters: { start: number; end: number; question: string }[];
  slides: Lesson[];
  refreshers: Record<string, string[]>;
  notation: string[][];
};
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
function LessonExperiment(
  { s, model, sandbox }: { s: Lesson; model: Lab; sandbox: Case | null },
) {
  const [angle, setAngle] = useState(
    s.id >= 46 && s.id <= 58 ? 45 : s.id === 62 || s.id === 1 ? 0 : 15,
  );
  const [person, setPerson] = useState(0);
  return (
    <Scene
      s={s}
      lab={model}
      sandbox={sandbox}
      angle={angle}
      setAngle={setAngle}
      person={person}
      setPerson={setPerson}
    />
  );
}
export function App() {
  const deck = useRef<RevealApi | null>(null);
  const { hostRef, value: lab, error } = useMarimoValue<Lab>("pca_model_v2");
  const { hostRef: courseHost, value: course, error: courseError } =
    useMarimoValue<Course>("pca_course_v2");
  const { hostRef: sandboxHost, value: sandbox } = useMarimoValue<Case>(
    "sandbox_lab",
  );
  const { hostRef: covHost, value: covCases } = useMarimoValue<Case[]>(
    "pca_cov_v2",
  );
  const { hostRef: edgeHost, value: edges } = useMarimoValue<Case[]>(
    "pca_edges_v2",
  );
  const { hostRef: scaleHost, value: scales } = useMarimoValue<Lab["scales"]>(
    "pca_scales_v2",
  );
  const model = lab && covCases && edges && scales
    ? {
      ...lab,
      base: covCases[0],
      covCases,
      edgeCases: [covCases[0], edges[0], edges[1]],
      nuisance: edges[2],
      scales,
    }
    : null;
  const [active, setActive] = useState(0),
    [visited, setVisited] = useState<Set<number>>(() => new Set([0])),
    [drawer, setDrawer] = useState("");
  const lesson = course?.slides[active];
  const jump = (n: number) => {
    const next = Math.min(Math.max(0, n), (course?.slides.length ?? 1) - 1);
    setActive(next);
    setVisited((previous) => new Set([...previous, next]));
    deck.current?.slide(next);
    setDrawer("");
  };
  useEffect(() => {
    let frame = 0, cancel = false;
    const sync = () => {
      if (cancel) return;
      if (deck.current?.isReady()) deck.current.slide(active);
      else frame = requestAnimationFrame(sync);
    };
    sync();
    return () => {
      cancel = true;
      cancelAnimationFrame(frame);
    };
  }, [active, course]);
  useEffect(() => {
    const key = (e: KeyboardEvent) => {
      if (
        drawer || e.composedPath().some((t) =>
          t instanceof Element &&
          t.matches("input,button,a,textarea,select,summary,marimo-cell")
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
    };
    window.addEventListener("keydown", key);
    return () => window.removeEventListener("keydown", key);
  }, [active, course, drawer]);
  return (
    <>
      <span ref={hostRef} hidden id="pca-model-v2" mo-value="pca_model_v2" />
      <span
        ref={courseHost}
        hidden
        id="pca-course-v2"
        mo-value="pca_course_v2"
      />
      <span ref={sandboxHost} hidden id="pca-live-v2" mo-value="sandbox_lab" />
      <span ref={covHost} hidden id="pca-cov-v2" mo-value="pca_cov_v2" />
      <span ref={edgeHost} hidden id="pca-edges-v2" mo-value="pca_edges_v2" />
      <span
        ref={scaleHost}
        hidden
        id="pca-scales-v2"
        mo-value="pca_scales_v2"
      />
      <nav className="course-nav" aria-label="Course navigation">
        <button className="wordmark" onClick={() => jump(0)}>
          PCA<span>picture → proof</span>
        </button>
        <div>
          <button onClick={() => setDrawer("route")}>Course route</button>
          <button onClick={() => setDrawer("refresh")}>
            Math at this step
          </button>
          <button onClick={() => setDrawer("notation")}>Symbols</button>
          <a
            className="notebook-link"
            href="http://localhost:2718/studio/lesson/"
            target="_blank"
            rel="noopener noreferrer"
          >
            Back to notebook ↗
          </a>
        </div>
      </nav>
      {error || courseError
        ? (
          <main className="status-page">
            <h1>The notebook could not load.</h1>
            <p>{error?.message ?? courseError?.message}</p>
          </main>
        )
        : !model || !course
        ? (
          <main className="status-page">
            <h1>Preparing the PCA model…</h1>
            <p>The notebook supplies the data and the calculations.</p>
          </main>
        )
        : (
          <>
            <nav className="chapter-strip" aria-label="Course chapters">
              {course.chapters.map((chapter, i) => (
                <button
                  key={chapter.start}
                  className={"chapter-link" +
                    (lesson?.chapter === i ? " active" : "")}
                  aria-current={lesson?.chapter === i ? "step" : undefined}
                  onClick={() => jump(chapter.start)}
                >
                  <span>{i + 1}</span> {[
                    "The picture",
                    "Measure a view",
                    "Covariance",
                    "Find & prove",
                    "Keep & recover",
                    "Test its limits",
                  ][i]}
                </button>
              ))}
            </nav>
            <Deck deckRef={deck} className="pca-deck" config={config}>
              {course.slides.map((s, i) => (
                <Slide key={s.id}>
                  <article
                    className="pca-slide"
                    data-marimo-lens-inputs="pca-model-v2 pca-course-v2 pca-live-v2 pca-cov-v2 pca-edges-v2 pca-scales-v2"
                    data-marimo-lens-label={`PCA ${s.id}: ${s.title}`}
                    data-marimo-lens-render-source='{"path":"src/PcaScenes.tsx"}'
                  >
                    <header>
                      <p className="chapter-label">
                        <span>{String(s.chapter + 1).padStart(2, "0")}</span>
                        {course.chapters[s.chapter].question}
                      </p>
                      <h1>{s.title}</h1>
                    </header>
                    {visited.has(i) && (
                      <LessonExperiment
                        key={s.id}
                        s={s}
                        model={model}
                        sandbox={sandbox ?? null}
                      />
                    )}
                  </article>
                </Slide>
              ))}
            </Deck>
            <footer className="course-footer">
              <button
                aria-label="Previous slide"
                disabled={active === 0}
                onClick={() => jump(active - 1)}
              >
                ← Previous
              </button>
              <label className="slide-picker">
                <span>
                  {String(active + 1).padStart(2, "0")}{" "}
                  <small>/ {course.slides.length}</small>
                </span>
                <select
                  aria-label="Jump to slide"
                  value={active}
                  onChange={(e) => jump(+e.target.value)}
                >
                  {course.slides.map((s, i) => (
                    <option value={i} key={s.id}>{s.id}. {s.title}</option>
                  ))}
                </select>
              </label>
              <button
                aria-label="Next slide"
                disabled={active === course.slides.length - 1}
                onClick={() => jump(active + 1)}
              >
                Next →
              </button>
            </footer>
            <div
              className="course-progress"
              style={{ width: (active + 1) / course.slides.length * 100 + "%" }}
            />
            {drawer && (
              <div
                className="drawer-backdrop"
                onClick={() => setDrawer("")}
              >
                <section
                  className="course-drawer"
                  role="dialog"
                  aria-modal="true"
                  aria-label={drawer === "route"
                    ? "Course route"
                    : drawer === "refresh"
                    ? "Math at this step"
                    : "Symbols"}
                  onClick={(e) => e.stopPropagation()}
                >
                  <button
                    className="close-drawer"
                    onClick={() => setDrawer("")}
                    aria-label="Close panel"
                  >
                    ×
                  </button>
                  {drawer === "route"
                    ? (
                      <>
                        <p className="chapter-label">
                          ONE ARGUMENT · SIX QUESTIONS
                        </p>
                        <h2>From the picture to the proof.</h2>
                        <p>
                          Choose a question to return to that part of the
                          course.
                        </p>
                        <ol className="route-list">
                          {course.chapters.map((c, i) => (
                            <li key={c.start}>
                              <button
                                className={lesson?.chapter === i
                                  ? "current"
                                  : ""}
                                onClick={() => jump(c.start)}
                              >
                                <span>{String(i + 1).padStart(2, "0")}</span>
                                <div>
                                  <strong>{c.question}</strong>
                                  <small>
                                    Slides {c.start + 1}–{c.end}
                                    {lesson?.chapter === i
                                      ? " · You are here"
                                      : ""}
                                  </small>
                                </div>
                                <span>→</span>
                              </button>
                            </li>
                          ))}
                        </ol>
                        <p className="drawer-note">
                          Math refreshers stay beside the current step. They do
                          not move you to a separate course.
                        </p>
                      </>
                    )
                    : drawer === "refresh"
                    ? (
                      <>
                        <p className="chapter-label">A SHORT REFRESHER</p>
                        <h2>
                          {course.refreshers[lesson?.scene ?? "geometry"]
                            ?.[0] ?? "Use the model you derived"}
                        </h2>
                        <p>
                          {course.refreshers[lesson?.scene ?? "geometry"]
                            ?.[1] ??
                            "Center the observation with the training mean. Project it onto the learned direction. Use the score and direction to reconstruct it."}
                        </p>
                        <button
                          className="accent"
                          onClick={() => setDrawer("")}
                        >
                          Return to this experiment
                        </button>
                      </>
                    )
                    : (
                      <>
                        <p className="chapter-label">
                          ONE SYMBOL · ONE MEANING
                        </p>
                        <h2>Read the notation.</h2>
                        <dl className="notation">
                          {course.notation.map(([term, meaning]) => (
                            <div key={term}>
                              <dt>{term}</dt>
                              <dd>{meaning}</dd>
                            </div>
                          ))}
                        </dl>
                      </>
                    )}
                </section>
              </div>
            )}
          </>
        )}
    </>
  );
}
