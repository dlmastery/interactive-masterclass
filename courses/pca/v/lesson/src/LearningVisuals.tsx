import { useEffect, useState } from "react";
import type { Scene } from "./course.ts";
import { MathText, Plot } from "./Visuals.tsx";
import { fixed, model, type Point, RAW } from "./math.ts";
const drafts = new Map<string, string>();
export function Capacity() {
  const [p, set] = useState(.5);
  return (
    <div className="capacity">
      <p className="eyebrow">BUILD A LEGAL TWO-DIRECTION SUBSPACE</p>
      <p>Example: eigenvalues (12, 5, 2, 1), k = 2. Keep q₁. Mix q₂ and q₃.</p>
      <div className="capacity-columns">
        {[[12, 1], [5, 1 - p], [2, p], [1, 0]].map(([lambda, b], i) => (
          <div key={i}>
            <span>λ{i + 1} = {lambda}</span>
            <div className="capacity-slot">
              <i style={{ height: `${b * 100}%` }} />
            </div>
            <strong>b{i + 1} = {fixed(b)}</strong>
          </div>
        ))}
      </div>
      <label className="range">
        <span>
          Move squared weight from q₂ to q₃<strong>{fixed(p)}</strong>
        </span>
        <input
          aria-label="Weight moved to the smaller eigenvalue"
          type="range"
          min="0"
          max="1"
          step=".05"
          value={p}
          onChange={(e) => set(Number(e.target.value))}
        />
      </label>
      <p className="feedback">
        Total weight = 2. Kept variance = 12 + 5 × {fixed(1 - p)} + 2 ×{" "}
        {fixed(p)} = <b>{fixed(17 - 3 * p)}</b> ≤ 17.
      </p>
      <p className="caption">
        This is the subspace spanned by q₁ and √(1−p)q₂ + √p q₃. Each weight
        stays between 0 and 1. The proof below covers every legal subspace.
      </p>
    </div>
  );
}
export function ShapeFlow() {
  const [i, set] = useState(0), [k, setK] = useState(1);
  const m = model(RAW, 45), p = m.points[i];
  return (
    <div className="shape-flow">
      <p className="eyebrow">TRACE ONE OBSERVATION THROUGH THE PRODUCT</p>
      <div className="shape-row">
        <div>
          <b>X</b>
          <span>4 × 2</span>
          <small>
            centered row {String.fromCharCode(65 + i)}
            <br />({p.join(", ")})
          </small>
        </div>
        <span>×</span>
        <div>
          <b>W</b>
          <span>2 × {k}</span>
          <small>
            {k === 1 ? "one unit direction" : "two perpendicular directions"}
          </small>
        </div>
        <span>→</span>
        <div>
          <b>Z</b>
          <span>4 × {k}</span>
          <small>
            score row<br />
            {fixed(m.scores[i])}
            {k === 2 ? `, ${fixed((p[0] - p[1]) / Math.SQRT2)}` : ""}
          </small>
        </div>
      </div>
      <div className="presets">
        {["A", "B", "C", "D"].map((l, j) => (
          <button
            key={l}
            aria-pressed={i === j}
            onClick={() => set(j)}
          >
            {l}
          </button>
        ))}
        <button onClick={() => setK(k === 1 ? 2 : 1)}>
          Keep {k === 1 ? "two directions" : "one direction"}
        </button>
      </div>
      <p className="caption">
        For this fixture q₁=(1,1)/√2 and q₂=(1,−1)/√2. The sign of q₂ is a
        convention.
      </p>
    </div>
  );
}
export function ExplainBack(
  { s, compact = false }: { s: Scene; compact?: boolean },
) {
  const [draft, setDraft] = useState(drafts.get(s.id) ?? ""),
    [show, setShow] = useState(false),
    [example, showExample] = useState(false),
    [checks, setChecks] = useState<number[]>([]);
  useEffect(() => {
    drafts.set(s.id, draft);
  }, [draft, s.id]);
  const lens: Record<string, string> = {
    age10: "Ruler and dots · no vector knowledge assumed",
    age15: "Coordinates and Pythagoras",
    undergrad: "Objective, covariance, and proof",
    grad: "Assumptions, bounds, and edge cases",
    phd: "Evidence and research claims",
    postdoc: "Study design and judgment",
  };
  return (
    <div className={`experiment explain ${compact ? "compact" : ""}`}>
      <p className="eyebrow">{lens[s.mode ?? ""] ?? "REBUILD THE REASONING"}</p>
      <h3>Make your explanation first.</h3>
      <label className="draft-label">
        Your explanation<textarea
          aria-label="Your explanation"
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder="Write the reasoning, or use this space for notes after speaking it aloud."
          rows={compact ? 3 : 6}
        />
      </label>
      <p className="caption">
        Your text stays in this page while you move between scenes. Copy it
        before reloading. This course does not send it to an AI grader.
      </p>
      <div className="presets">
        <button onClick={() => setShow(!show)}>
          {show ? "Hide review prompts" : "Review my explanation"}
        </button>
        <button
          onClick={() => {
            setDraft("");
            setChecks([]);
            showExample(false);
            setShow(false);
          }}
        >
          Clear this response
        </button>
      </div>
      {show && (
        <div className="self-review">
          <p>Check only what your explanation actually supports.</p>
          {(s.rubric ??
            [
              "State the purpose.",
              "Connect the objects to the formula.",
              "Give a reason for the next step.",
              "Name an assumption or limit.",
            ]).map((r, i) => (
              <label key={i}>
                <input
                  type="checkbox"
                  checked={checks.includes(i)}
                  onChange={() =>
                    setChecks(
                      checks.includes(i)
                        ? checks.filter((x) => x !== i)
                        : [...checks, i],
                    )}
                />
                <span>{r}</span>
              </label>
            ))}
          <p className="caption">
            This is self-review, not a mastery score. For an unchecked item,
            identify the missing bridge, revisit it, then try again without the
            example.
          </p>
          {s.example && (
            <>
              <button onClick={() => showExample(!example)}>
                {example
                  ? "Hide example reasoning"
                  : "Compare one possible explanation"}
              </button>
              {example && <p className="feedback">{s.example}</p>}
            </>
          )}
        </div>
      )}
    </div>
  );
}
export function Proof({ s }: { s: Scene }) {
  const [step, setStep] = useState(0),
    [answer, setAnswer] = useState(""),
    [check, show] = useState(false);
  const steps = s.steps ?? [];
  return (
    <div className="experiment proof">
      {["more-capacity-weights", "more-global-k-bound"].includes(s.id) && (
        <Capacity />
      )}
      {["more-frame-shapes", "more-score-covariance"].includes(s.id) && (
        <ShapeFlow />
      )}
      <p className="eyebrow">ONE OPERATION · ONE REASON</p>
      <div className="proof-progress">
        {steps.map((_, i) => (
          <button
            key={i}
            aria-label={`Show reasoning through step ${i + 1}`}
            aria-pressed={i <= step}
            onClick={() => setStep(i)}
          >
            {i + 1}
          </button>
        ))}
        <span>{step + 1} / {steps.length}</span>
      </div>
      <div className="proof-steps">
        {steps.slice(0, step + 1).map(([tex, reason], i) => (
          <div className={`proof-step ${i === step ? "current" : ""}`} key={i}>
            <span className="step-number">{i + 1}</span>
            <div>
              <MathText tex={tex} />
              <p>{reason}</p>
            </div>
          </div>
        ))}
      </div>
      <div className="control-row">
        <button disabled={step === 0} onClick={() => setStep(step - 1)}>
          Previous step
        </button>
        <button
          className="primary"
          disabled={step === steps.length - 1}
          onClick={() => setStep(step + 1)}
        >
          Reveal next reason →
        </button>
        <button onClick={() => setStep(0)}>Reset</button>
      </div>
      <p className="caption">
        Before each reveal, name the operation you expect and why it is valid.
        Seeing a correct step is not the same as being able to supply it.
      </p>
      {s.id === "dot" && (
        <div className="numeric-check">
          <label>
            Reconstructed east offset for A<input
              aria-label="Reconstructed east offset for A"
              inputMode="decimal"
              value={answer}
              onChange={(e) => {
                setAnswer(e.target.value);
                show(false);
              }}
            />
          </label>
          <button onClick={() => show(true)}>Check my calculation</button>
          {check && (
            <p role="status" className="feedback">
              {answer.trim() !== "" && Math.abs(Number(answer) - 1.5) < .001
                ? "Yes. Multiply the score 3/√2 by the east direction weight 1/√2. The recovered offset is 1.5 cm."
                : "Use score × east direction weight: (3/√2)(1/√2). This gives an offset; the raw position also needs the mean."}
            </p>
          )}
        </div>
      )}
      {s.rubric && (
        <details>
          <summary>Test this reasoning without the derivation</summary>
          <ExplainBack s={s} compact />
        </details>
      )}
    </div>
  );
}
export function Center() {
  const [shift, set] = useState(0), [centered, show] = useState(false);
  const raw = RAW.map((p) => [p[0] + shift, p[1] + shift] as Point),
    m = model(raw);
  return (
    <div className="experiment">
      <div className="center-head">
        <p className="eyebrow">TRANSLATE THE DATA · KEEP THE SHAPE</p>
        <strong>Mean: ({fixed(m.mean[0], 0)}, {fixed(m.mean[1], 0)}) cm</strong>
      </div>
      <svg
        viewBox="0 0 460 260"
        role="img"
        aria-label="Translated positions and their fixed centered offsets"
      >
        <line x1="35" y1="222" x2="438" y2="222" stroke="#abc" />
        <line x1="35" y1="18" x2="35" y2="222" stroke="#abc" />
        {(centered ? m.points : raw).map((p, i) => {
          const x = centered ? 230 + p[0] * 23 : 35 + p[0] * 23,
            y = centered ? 130 - p[1] * 16 : 222 - p[1] * 16;
          return (
            <g key={i}>
              <circle cx={x} cy={y} r="7" fill="#167c80" />
              <text x={x + 10} y={y - 8}>
                {String.fromCharCode(65 + i)} ({fixed(p[0], 0)},{" "}
                {fixed(p[1], 0)})
              </text>
            </g>
          );
        })}
        <text x="40" y="252">
          {centered
            ? "Centered coordinates; one grid scale per coordinate"
            : "Raw positions; both coordinates shifted by the same amount"}
        </text>
      </svg>
      <label className="range">
        <span>
          Translate both coordinates <strong>{shift} cm</strong>
        </span>
        <input
          aria-label="Translate both coordinates"
          type="range"
          min="-3"
          max="3"
          step="1"
          value={shift}
          onChange={(e) => set(Number(e.target.value))}
        />
      </label>
      <button onClick={() => show(!centered)}>
        {centered ? "Show raw positions" : "Subtract the mean"}
      </button>
      <MathText
        tex={String.raw`x_A=(${8 + shift},${7 + shift})-(${6 + shift},${
          6 + shift
        })=(2,1)`}
      />
      <p className="feedback">
        {centered
          ? "The points no longer move when the common shift changes. Centering removes shared position."
          : "The cloud moves, but its internal gaps do not change. The mean moves with it."}
      </p>
      <p className="caption">
        This schematic uses fixed coordinate scales to make translation visible.
        Main projection plots use equal geometric scales.
      </p>
    </div>
  );
}
