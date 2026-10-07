/// <reference path="./marimo-studio.d.ts" />
import { Deck, Slide } from "@revealjs/react";
import { useEffect, useRef, useState } from "react";
import type { RevealApi } from "reveal.js";
import "reveal.js/reveal.css";
import { useMarimoValue } from "./lib/use-marimo-value.ts";
import {
  type Attempt,
  type Case,
  type Course,
  type Lab,
  type RecordAttempt,
} from "./LabComponents.tsx";
import { CoreLab } from "./CoreLabs.tsx";
import { BridgeLab } from "./BridgeLabs.tsx";

const chapterEntries: (number | string)[] = [0, 6, "blend", 15, 20, 23, 27];
const chapterOf = (i: number, starts: number[]) =>
  starts.filter((n) => n <= i).length - 1;
const deckConfig = {
  width: 1440,
  height: 780,
  margin: .02,
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
  const { hostRef, value: lab, error } = useMarimoValue<Lab>("pca_lab");
  const { hostRef: courseRef, value: course, error: courseError } =
    useMarimoValue<Course>("masterclass");
  const { hostRef: sandboxRef, value: sandbox } = useMarimoValue<Case>(
    "sandbox_lab",
  );
  const [active, setActive] = useState(0),
    [person, setPerson] = useState(0),
    [angle, setAngle] = useState(0),
    [drawer, setDrawer] = useState(""),
    [term, setTerm] = useState("Observation"),
    [attempts, setAttempts] = useState<Attempt[]>([]);
  const chapterStarts = course
    ? chapterEntries.map((e) => course.sequence.indexOf(e))
    : [0];
  const jump = (i: number) => {
    const next = Math.max(0, Math.min(i, (course?.sequence.length ?? 1) - 1));
    setActive(next);
    deck.current?.slide(next);
    setDrawer("");
    requestAnimationFrame(() => window.scrollTo(0, 0));
  };
  const jumpCore = (n: number) => jump(course?.sequence.indexOf(n) ?? 0);
  useEffect(() => {
    let cancelled = false;
    let timer = 0;
    const sync = () => {
      if (cancelled) return;
      if (deck.current?.isReady()) deck.current.slide(active);
      else timer = requestAnimationFrame(sync);
    };
    sync();
    return () => {
      cancelled = true;
      cancelAnimationFrame(timer);
    };
  }, [active, course]);
  const record: RecordAttempt = (a) =>
    setAttempts((prev) => [...prev, { ...a, time: new Date().toISOString() }]);
  useEffect(() => {
    const handle = (e: KeyboardEvent) => {
      if (
        drawer || e.composedPath().some((t) =>
          t instanceof Element &&
          t.matches(
            "input,textarea,select,button,summary,marimo-cell,marimo-output",
          )
        )
      ) return;
      if (e.key === "ArrowRight" || e.key === "PageDown") {
        e.preventDefault();
        jump(active + 1);
      } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
        e.preventDefault();
        jump(active - 1);
      }
    };
    window.addEventListener("keydown", handle);
    return () => window.removeEventListener("keydown", handle);
  }, [active, course, drawer]);
  const download = () => {
    const payload = {
      course: "PCA masterclass",
      goal: course?.passTest,
      currentSlide: active + 1,
      level: "Undergraduate foundations, taught as needed",
      attempts,
      notes:
        "Numeric checks are automatic. Written reasoning has not been graded by AI. Review misses before claiming mastery.",
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "pca-learning-record.json";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };
  return (
    <>
      <span ref={hostRef} id="pca-lab-data" hidden mo-value="pca_lab" />
      <span ref={courseRef} id="course-data" hidden mo-value="masterclass" />
      <span ref={sandboxRef} id="sandbox-data" hidden mo-value="sandbox_lab" />
      <nav className="topbar" aria-label="Masterclass navigation">
        <a
          className="brand"
          href="#"
          onClick={(e) => {
            e.preventDefault();
            jump(0);
          }}
        >
          PCA <span>from the ground up</span>
        </a>
        <div className="nav-actions">
          <button onClick={() => setDrawer(drawer === "map" ? "" : "map")}>
            Learning map
          </button>
          <button
            onClick={() => setDrawer(drawer === "glossary" ? "" : "glossary")}
          >
            Explain a term
          </button>
          <button
            onClick={() => setDrawer(drawer === "record" ? "" : "record")}
          >
            My attempts ({attempts.length})
          </button>
        </div>
      </nav>
      {error || courseError
        ? (
          <div role="alert" className="loading">
            The notebook data did not load:{" "}
            {error?.message ?? courseError?.message}
          </div>
        )
        : !lab || !course
        ? (
          <div className="loading">
            <h1>Preparing your experiments…</h1>
            <p>
              The notebook is calculating the covariance, projections, and
              examples.
            </p>
          </div>
        )
        : (
          <>
            <Deck deckRef={deck} className="master-deck" config={deckConfig}>
              {course.sequence.map((entry, i) => {
                const bridge = typeof entry === "string";
                const text = bridge
                  ? course.bridges[entry]
                  : course.slides[entry];
                const chapter = chapterOf(i, chapterStarts);
                return (
                  <Slide key={String(entry)}>
                    <div
                      className="slide-shell"
                      data-marimo-lens-inputs={entry === 28
                        ? "pca-lab-data course-data sandbox-data"
                        : "pca-lab-data course-data"}
                      data-marimo-lens-label={`Slide ${i + 1}: ${text[0]}`}
                      data-marimo-lens-render-source='{"path":"src/Masterclass.tsx"}'
                    >
                      <header className="slide-heading">
                        <p className="eyebrow">
                          {course.chapters[chapter]}{" "}
                          <span>
                            {bridge
                              ? "JUST-IN-TIME FOUNDATION"
                              : entry === 31
                              ? "INDEPENDENT CHECK"
                              : entry === 29 || entry === 30
                              ? "OPTIONAL DEEPER CONNECTION"
                              : "PCA EXPERIMENT"}
                          </span>
                        </p>
                        <h1>{text[0]}</h1>
                      </header>
                      <div className="lesson-grid">
                        <aside className="explanation">
                          <p className="explain-copy">{text[1]}</p>
                          <div className="mission">
                            <span>YOUR MOVE</span>
                            <p>{text[2]}</p>
                          </div>
                          <details className="takeaway">
                            <summary>Why this matters</summary>
                            <p>{text[3]}</p>
                          </details>
                          {bridge && (
                            <p className="bridge-note">
                              This foundation appears here because you need it
                              for the next PCA step.
                            </p>
                          )}
                          <button
                            className="subtle"
                            onClick={() => setDrawer("glossary")}
                          >
                            A symbol or word is unfamiliar →
                          </button>
                        </aside>
                        <div
                          className="experiment"
                          aria-label={`Experiment ${i + 1}`}
                          data-slide={i + 1}
                        >
                          {bridge
                            ? (
                              <BridgeLab
                                id={entry}
                                lab={lab}
                                course={course}
                                person={person}
                                setPerson={setPerson}
                                angle={angle}
                                setAngle={setAngle}
                                record={record}
                              />
                            )
                            : (
                              <CoreLab
                                id={entry}
                                lab={lab}
                                course={course}
                                sandbox={sandbox}
                                person={person}
                                setPerson={setPerson}
                                angle={angle}
                                setAngle={setAngle}
                                record={record}
                                jumpCore={jumpCore}
                              />
                            )}
                        </div>
                      </div>
                    </div>
                  </Slide>
                );
              })}
            </Deck>
            <footer className="bottom-bar">
              <button onClick={() => jump(active - 1)} disabled={active === 0}>
                ← Previous slide
              </button>
              <label>
                Jump to slide<select
                  aria-label="Jump to slide"
                  value={active}
                  onChange={(e) => jump(Number(e.target.value))}
                >
                  {course.sequence.map((v, i) => (
                    <option key={i} value={i}>
                      {i + 1}. {(typeof v === "string"
                        ? course.bridges[v]
                        : course.slides[v])[0]}
                    </option>
                  ))}
                </select>
              </label>
              <span className="slide-count">
                {active + 1} / {course.sequence.length}
              </span>
              <button
                className="next"
                onClick={() => jump(active + 1)}
                disabled={active === course.sequence.length - 1}
              >
                Next slide →
              </button>
            </footer>
            <div className="course-progress">
              <i
                style={{
                  width: `${(active + 1) / course.sequence.length * 100}%`,
                }}
              />
            </div>
            {drawer && (
              <div className="drawer-backdrop">
                <section
                  className="drawer"
                  role="dialog"
                  aria-modal="true"
                  aria-label={drawer === "map"
                    ? "Learning map"
                    : drawer === "record"
                    ? "Learning record"
                    : "Term explanations"}
                >
                  <button className="close" onClick={() => setDrawer("")}>
                    Close ×
                  </button>
                  {drawer === "map"
                    ? (
                      <>
                        <p className="eyebrow">
                          SEVEN CONNECTED NODES · {course.sequence.length}{" "}
                          INTERACTIVE SLIDES
                        </p>
                        <h2>Your path through PCA</h2>
                        <p>{course.passTest}</p>
                        <div className="map-nodes">
                          {course.map.map((node, i) => (
                            <button
                              key={node.name}
                              onClick={() => jump(chapterStarts[i])}
                            >
                              <span>{i + 1}</span>
                              <div>
                                <h3>{node.name}</h3>
                                <p>
                                  <b>Needs:</b> {node.depends} → <b>Unlocks:</b>
                                  {" "}
                                  {node.unlocks}
                                </p>
                                <p>
                                  <b>Common snag:</b> {node.stuck}
                                </p>
                                <p>
                                  <b>You produce:</b> {node.artifact}
                                </p>
                              </div>
                            </button>
                          ))}
                        </div>
                      </>
                    )
                    : drawer === "glossary"
                    ? (
                      <>
                        <p className="eyebrow">EXPLAIN ONLY THE STUCK PART</p>
                        <h2>Translate the vocabulary</h2>
                        <label>
                          Choose a term<select
                            aria-label="Choose a term"
                            value={term}
                            onChange={(e) => setTerm(e.target.value)}
                          >
                            {Object.keys(course.glossary).map((s) => (
                              <option key={s}>{s}</option>
                            ))}
                          </select>
                        </label>
                        <div className="definition">
                          <h3>{term}</h3>
                          <p>{course.glossary[term]}</p>
                        </div>
                        <p>
                          Close this panel and redo the operation in your own
                          words.
                        </p>
                      </>
                    )
                    : (
                      <>
                        <p className="eyebrow">LEARNER RECORD · THIS VISIT</p>
                        <h2>Attempts, not slides viewed</h2>
                        <p>
                          {attempts.length} submitted attempts ·{" "}
                          {attempts.filter((a) => !a.correct).length}{" "}
                          misses or guesses.
                        </p>
                        <p>
                          Written reasons are preserved exactly as you entered
                          them. They need tutor or self-review; this deck does
                          not silently grade them with an AI.
                        </p>
                        <button className="primary" onClick={download}>
                          Save learning record
                        </button>
                        <p className="quiet">
                          Save before reloading. The record is held in this
                          browser session, with no external account or upload.
                        </p>
                        {attempts.map((a, i) => (
                          <article className="attempt" key={i}>
                            <h3>{i + 1}. {a.question}</h3>
                            <p>
                              <b>Your answer:</b> {a.answer}
                            </p>
                            <p>
                              <b>Your reason:</b> {a.reason}
                            </p>
                            <span>
                              {a.correct
                                ? "Numeric/choice check passed"
                                : "Needs review"}
                              {a.guessed ? " · admitted guess" : ""}
                            </span>
                          </article>
                        ))}
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
