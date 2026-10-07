import { type ReactNode, useId, useRef, useState } from "react";
// @deno-types="npm:@types/katex@0.16.7"
import katex from "katex";

export type Point = [number, number];
export type Frame = {
  w: Point;
  sw: Point;
  z: number[];
  terms: Point[];
  projected: Point[];
  residual: Point[];
  kept: number[];
  lost: number[];
  lengths: number[];
  variance: number;
  loss: number;
  sumSquares: number;
  ratio: number;
  slope: number;
  turn: number;
  eigen: boolean;
};
export type Case = {
  raw: Point[];
  points: Point[];
  mean: Point;
  cov: number[][];
  sums: number[][];
  values: number[];
  axes: Point[];
  scores: Point[];
  std: Point;
  corr: number[][];
  scoreCov: number[][];
  scoreProducts: number[];
  total: number;
  ratio: number;
  n: number;
  angle: number;
  squared: Point[];
  signedSums: Point;
  squaresSums: Point;
  products: number[][][];
  singular: number[];
  frames: Frame[];
  recon: {
    points: Point[];
    raw: Point[];
    loss: number[];
    totalLoss: number;
    ratio: number;
  }[];
};
export type Lab = {
  base: Case;
  covCases: Case[];
  centers: { points: Point[]; mean: Point; fraction: number }[];
  scales: { raw: Case; standard: Case; factor: number }[];
  ruler: {
    length: number;
    w: Point;
    z: number[];
    norm2: number;
    variance: number;
  }[];
  mixtures: {
    p: number;
    a: number;
    b: number;
    variance: number;
    first: number;
    second: number;
  }[];
  challenge: Case;
  edgeCases: Case[];
  nuisance: Case;
  people: string[];
};
export type Problem = { prompt: string; answer: number; feedback: string };
export type ExamQ = {
  prompt: string;
  answer: number;
  tolerance: number;
  route: number;
  level: string;
  hint: string;
};
export type Course = {
  title: string;
  passTest: string;
  chapters: string[];
  slides: string[][];
  bridges: Record<string, string[]>;
  sequence: (number | string)[];
  equations: Record<string, string>;
  varianceSteps: string[][];
  svdSteps: string[][];
  calculusSteps: string[][];
  glossary: Record<string, string>;
  bridgeProblems: Record<string, Problem>;
  practices: Record<string, Problem & { options?: string[] }>;
  examVariants: ExamQ[][];
  map: {
    name: string;
    depends: string;
    unlocks: string;
    stuck: string;
    artifact: string;
  }[];
};
export type Attempt = {
  question: string;
  answer: string;
  reason: string;
  correct: boolean;
  guessed?: boolean;
  time: string;
};
export type RecordAttempt = (a: Omit<Attempt, "time">) => void;
export const f = (v: number, d = 2) =>
  Math.abs(v) < 1e-7 ? (0).toFixed(d) : v.toFixed(d);
export const percent = (v: number) => `${f(v * 100, 1)}%`;
export const point = (v: Point) => `(${f(v[0])}, ${f(v[1])})`;
export const colors = ["#0e817d", "#cb653a", "#6954a3", "#a58018"];
export function Eq({ tex }: { tex: string }) {
  return (
    <div
      className="equation"
      dangerouslySetInnerHTML={{
        __html: katex.renderToString(tex, {
          displayMode: true,
          throwOnError: false,
          trust: false,
        }),
      }}
    />
  );
}
export function Tabs(
  { labels, value, onChange, label = "Choose an option" }: {
    labels: string[];
    value: number;
    onChange: (i: number) => void;
    label?: string;
  },
) {
  return (
    <div className="choice-row" role="group" aria-label={label}>
      {labels.map((s, i) => (
        <button
          key={s}
          className={value === i ? "chosen" : ""}
          aria-pressed={value === i}
          onClick={() => onChange(i)}
        >
          {s}
        </button>
      ))}
    </div>
  );
}
export function Range(
  { label, value, onChange, min = 0, max = 180, step = 1, suffix = "°" }: {
    label: string;
    value: number;
    onChange: (v: number) => void;
    min?: number;
    max?: number;
    step?: number;
    suffix?: string;
  },
) {
  return (
    <label className="range">
      <span>
        {label}
        <output>{f(value, step < 1 ? 1 : 0)}{suffix}</output>
      </span>
      <input
        type="range"
        aria-label={label}
        min={min}
        max={max}
        step={step}
        value={value}
        onInput={(e) => onChange(Number(e.currentTarget.value))}
      />
    </label>
  );
}
export function Metric(
  { name, value, small }: { name: string; value: string; small?: boolean },
) {
  return (
    <div className={"metric" + (small ? " compact" : "")}>
      <span>{name}</span>
      <strong>{value}</strong>
    </div>
  );
}
export function People(
  { selected, setSelected }: {
    selected: number;
    setSelected: (i: number) => void;
  },
) {
  return (
    <Tabs
      labels={["Person A", "Person B", "Person C", "Person D"]}
      value={selected}
      onChange={setSelected}
      label="Select a person"
    />
  );
}
export function DataTable(
  { rows, headers = ["Test A", "Test B"], selected, onSelect }: {
    rows: number[][];
    headers?: string[];
    selected?: number;
    onSelect?: (i: number) => void;
  },
) {
  return (
    <table className="data-table">
      <thead>
        <tr>
          <th>Person</th>
          {headers.map((h) => <th key={h}>{h}</th>)}
        </tr>
      </thead>
      <tbody>
        {rows.map((r, i) => (
          <tr
            key={i}
            className={selected === i ? "selected" : ""}
            onClick={() => onSelect?.(i)}
          >
            <th>
              <button
                aria-label={`Select person ${String.fromCharCode(65 + i)}`}
                onClick={() => onSelect?.(i)}
                style={{ color: colors[i % 4] }}
              >
                {String.fromCharCode(65 + i)}
              </button>
            </th>
            {r.map((v, j) => <td key={j}>{f(v)}</td>)}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
export function Matrix(
  { data, active, onSelect, prefix = "S" }: {
    data: number[][];
    active?: number;
    onSelect?: (i: number) => void;
    prefix?: string;
  },
) {
  return (
    <div className="matrix">
      <b>{prefix} =</b>
      <div className="matrix-grid">
        {data.flat().map((v, i) => (
          <button
            key={i}
            className={active === i ? "selected" : ""}
            aria-label={`${prefix} row ${Math.floor(i / 2) + 1} column ${
              i % 2 + 1
            }`}
            onClick={() => onSelect?.(i)}
          >
            {f(v)}
          </button>
        ))}
      </div>
    </div>
  );
}
export function Plot({
  points,
  second,
  w,
  axes,
  selected = -1,
  onSelect,
  onAngle,
  mean,
  guides = false,
  triangle = false,
  labels = ["Test A · centered points", "Test B · centered points"],
  bound,
  category = false,
  vectors,
  vectorLabels,
}: {
  points: Point[];
  second?: Point[];
  w?: Point;
  axes?: Point[];
  selected?: number;
  onSelect?: (i: number) => void;
  onAngle?: (a: number) => void;
  mean?: Point;
  guides?: boolean;
  triangle?: boolean;
  labels?: string[];
  bound?: number;
  category?: boolean;
  vectors?: Point[];
  vectorLabels?: string[];
}) {
  const drag = useRef(false);
  const svgRef = useRef<SVGSVGElement>(null);
  const uid = useId().replace(/:/g, "");
  const all = [
    ...points,
    ...second ?? [],
    ...vectors ?? [],
    ...mean ? [mean] : [],
  ];
  const R = bound ??
    Math.max(3, Math.ceil(Math.max(...all.flat().map(Math.abs), 1) * 1.15));
  const s = 160 / R,
    x = (n: number) => 300 + n * s,
    y = (n: number) => 194 - n * s;
  const ext = R * .92;
  const tick = R > 5 ? Math.ceil(R / 4) : 1;
  const ticks = Array.from(
    { length: Math.floor(R / tick) * 2 + 1 },
    (_, i) => (i - Math.floor(R / tick)) * tick,
  );
  const change = (e: { clientX: number; clientY: number }) => {
    const mat = svgRef.current?.getScreenCTM();
    if (!mat || !onAngle) return;
    const p = new DOMPoint(e.clientX, e.clientY).matrixTransform(mat.inverse());
    let a = Math.atan2(194 - p.y, p.x - 300) * 180 / Math.PI;
    a = (a + 180) % 180;
    onAngle(Math.round(a));
  };
  return (
    <div
      className="plot-wrap"
      onDragOver={(e) => {
        if (onAngle) e.preventDefault();
      }}
      onDrop={(e) => {
        if (onAngle) {
          e.preventDefault();
          change(e);
        }
      }}
    >
      <svg
        ref={svgRef}
        className={"plot" + (onAngle ? " draggable" : "")}
        viewBox="0 0 600 424"
        role="img"
        aria-label={onAngle
          ? "Interactive projection diagram. Drag the orange handle or use the angle slider."
          : "Linked scatterplot"}
        onPointerMove={(e) => {
          if (drag.current) change(e);
        }}
        onPointerUp={() => drag.current = false}
        onPointerCancel={() => drag.current = false}
      >
        <defs>
          <marker
            id={"arrow" + uid}
            viewBox="0 0 10 10"
            refX="9"
            refY="5"
            markerWidth="6"
            markerHeight="6"
            orient="auto-start-reverse"
          >
            <path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke" />
          </marker>
        </defs>
        {ticks.map((t) => (
          <g key={t}>
            <line
              className={t === 0 ? "origin" : "gridline"}
              x1={x(t)}
              x2={x(t)}
              y1="24"
              y2="364"
            />
            <line
              className={t === 0 ? "origin" : "gridline"}
              y1={y(t)}
              y2={y(t)}
              x1="115"
              x2="485"
            />
            <text x={x(t)} y="387" textAnchor="middle">{t}</text>
            <text x="101" y={y(t) + 5} textAnchor="end">{t}</text>
          </g>
        ))}
        <text x="300" y="418" textAnchor="middle" className="axislabel">
          {labels[0]}
        </text>
        <text
          transform="translate(33 194) rotate(-90)"
          textAnchor="middle"
          className="axislabel"
        >
          {labels[1]}
        </text>
        {triangle && second && selected >= 0 && (
          <path
            d={`M${x(0)},${y(0)} L${x(second[selected][0])},${
              y(second[selected][1])
            } L${x(points[selected][0])},${y(points[selected][1])} Z`}
            fill="#f6d9b599"
            stroke="#b97b33"
            strokeWidth="2"
          />
        )}
        {axes?.map((v, i) => (
          <line
            key={i}
            x1={x(-v[0] * ext)}
            y1={y(-v[1] * ext)}
            x2={x(v[0] * ext)}
            y2={y(v[1] * ext)}
            stroke={i ? "#aa87c4" : "#16938a"}
            strokeWidth="3"
            strokeDasharray={i ? "6 4" : undefined}
          />
        ))}
        {w && (
          <line
            x1={x(-w[0] * ext)}
            y1={y(-w[1] * ext)}
            x2={x(w[0] * ext)}
            y2={y(w[1] * ext)}
            stroke="#d37737"
            strokeWidth="3"
          />
        )}
        {second &&
          points.map((p, i) => (
            <line
              key={i}
              x1={x(p[0])}
              y1={y(p[1])}
              x2={x(second[i][0])}
              y2={y(second[i][1])}
              stroke={selected === i ? "#9c5230" : "#bcb6aa"}
              strokeWidth={selected === i ? 3 : 1.4}
              strokeDasharray="5 4"
            />
          ))}
        {guides && points[selected] && (
          <path
            d={`M${x(points[selected][0])},${y(0)} V${
              y(points[selected][1])
            } H${x(0)}`}
            fill="none"
            stroke={colors[selected % 4]}
            strokeDasharray="5 5"
            strokeWidth="2"
          />
        )}
        {points.map((p, i) => (
          <g key={i} className="dot">
            <circle
              cx={x(p[0])}
              cy={y(p[1])}
              r={selected === i
                ? 11
                : category
                ? (i < points.length / 2 ? 10 : 5)
                : 7}
              stroke={selected === i ? "#182d2b" : "white"}
              strokeWidth="2"
              fill={category
                ? (i < points.length / 2 ? "#d16b40" : "#317abc")
                : colors[i % 4]}
            />
            {points.length <= 5 && (
              <text x={x(p[0]) + 14} y={y(p[1]) - 9} fill={colors[i % 4]}>
                {String.fromCharCode(65 + i)}
              </text>
            )}
          </g>
        ))}
        {second?.map((p, i) => (
          <circle
            key={i}
            cx={x(p[0])}
            cy={y(p[1])}
            r="5"
            fill="#f5ab59"
            stroke="#a26628"
          />
        ))}
        {mean && (
          <g>
            <path
              d={`M${x(mean[0]) - 9},${y(mean[1])}h18 M${x(mean[0])},${
                y(mean[1]) - 9
              }v18`}
              stroke="#112f30"
              strokeWidth="3"
            />
            <text x={x(mean[0]) + 13} y={y(mean[1]) + 22}>mean</text>
          </g>
        )}
        {vectors?.map((v, i) => (
          <g key={i}>
            <line
              x1={x(0)}
              y1={y(0)}
              x2={x(v[0])}
              y2={y(v[1])}
              stroke={i ? "#6e52a1" : "#d37737"}
              strokeWidth="4"
              markerEnd={`url(#arrow${uid})`}
            />
            <text x={x(v[0]) + 12} y={y(v[1]) - 12}>
              {vectorLabels?.[i] ?? ""}
            </text>
          </g>
        ))}
      </svg>
      {onSelect &&
        points.map((p, i) => (
          <button
            key={i}
            className="point-hit"
            aria-label={`Select plotted person ${String.fromCharCode(65 + i)}`}
            style={{ left: `${x(p[0]) / 6}%`, top: `${y(p[1]) / 4.24}%` }}
            onClick={() => onSelect(i)}
          />
        ))}
      {w && onAngle && (
        <button
          className="drag-handle"
          draggable
          onDrag={(e) => {
            if (e.clientX || e.clientY) change(e);
          }}
          onDragEnd={(e) => {
            drag.current = false;
            if (e.clientX || e.clientY) change(e);
          }}
          aria-label="Drag projection axis; arrow keys rotate it"
          style={{
            left: `${x(w[0] * ext) / 6}%`,
            top: `${y(w[1] * ext) / 4.24}%`,
          }}
          onPointerDown={(e) => {
            e.currentTarget.setPointerCapture(e.pointerId);
            drag.current = true;
          }}
          onPointerMove={(e) => {
            if (drag.current) change(e);
          }}
          onPointerUp={() => drag.current = false}
          onPointerCancel={() => drag.current = false}
          onKeyDown={(e) => {
            if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
              e.preventDefault();
              const a = Math.round(
                (Math.atan2(w[1], w[0]) * 180 / Math.PI + 180) % 180,
              );
              onAngle((a + (e.key === "ArrowRight" ? 1 : 179)) % 180);
            }
          }}
        />
      )}
    </div>
  );
}
export function Bars(
  { values, labels, highlight = -1 }: {
    values: number[];
    labels: string[];
    highlight?: number;
  },
) {
  const max = Math.max(...values.map(Math.abs), 1);
  return (
    <div className="bars">
      {values.map((v, i) => (
        <div key={i} className={highlight === i ? "highlight" : ""}>
          <span>{labels[i]}</span>
          <div className="bar-track">
            <i
              style={{
                width: `${Math.abs(v) / max * 100}%`,
                background: v < 0 ? "#b35950" : colors[i % 4],
              }}
            />
          </div>
          <b>{f(v)}</b>
        </div>
      ))}
    </div>
  );
}
export function Budget({ ratio }: { ratio: number }) {
  return (
    <div className="budget">
      <div className="budget-track">
        <i style={{ width: `${ratio * 100}%` }} />
        <span style={{ width: `${100 - ratio * 100}%` }} />
      </div>
      <div>
        <span>Kept {percent(ratio)}</span>
        <span>Lost {percent(1 - ratio)}</span>
      </div>
    </div>
  );
}
export function Steps({ steps }: { steps: string[][] }) {
  const [i, setI] = useState(0);
  return (
    <div className="proof">
      <div className="step-tabs" role="group" aria-label="Derivation steps">
        {steps.map((_, j) => (
          <button
            className={i === j ? "chosen" : ""}
            key={j}
            onClick={() => setI(j)}
          >
            Step {j + 1}
          </button>
        ))}
      </div>
      <Eq tex={steps[i][0]} />
      <p>{steps[i][1]}</p>
      <div className="step-buttons">
        <button disabled={i === 0} onClick={() => setI(i - 1)}>
          ← Previous equality
        </button>
        <button disabled={i === steps.length - 1} onClick={() => setI(i + 1)}>
          Next equality →
        </button>
      </div>
    </div>
  );
}
export function Practice(
  { problem, record }: { problem: Problem; record: RecordAttempt },
) {
  const [value, setValue] = useState(""),
    [reason, setReason] = useState(""),
    [checked, setChecked] = useState(false),
    [explain, setExplain] = useState(false);
  const good = value.trim() !== "" &&
    Math.abs(Number(value) - problem.answer) < .015;
  return (
    <div className="practice">
      <span className="phase">
        {!checked
          ? "YOUR ATTEMPT"
          : explain
          ? "FOCUSED EXPLANATION"
          : "CHECK RESULT"}
      </span>
      <h3>{problem.prompt}</h3>
      <label>
        Your answer<input
          aria-label="Your numeric answer"
          type="number"
          value={value}
          disabled={checked}
          onChange={(e) => setValue(e.target.value)}
        />
      </label>
      <label>
        Your reasoning<textarea
          aria-label="Your reasoning"
          placeholder="Write the operation you used, not just the result."
          value={reason}
          disabled={checked}
          onChange={(e) => setReason(e.target.value)}
        />
      </label>
      {!checked
        ? (
          <button
            className="primary"
            disabled={!value.trim() || !reason.trim()}
            onClick={() => {
              setChecked(true);
              record({
                question: problem.prompt,
                answer: value,
                reason,
                correct: good,
              });
            }}
          >
            Submit attempt
          </button>
        )
        : (
          <div className="result-box">
            <strong>
              {good
                ? "Numeric answer passes."
                : "Not yet. Return to the operation that caused the miss."}
            </strong>
            <p>Your reasoning is recorded for review.</p>
            <button onClick={() => setExplain(!explain)}>
              {explain ? "Hide explanation" : "Explain this step"}
            </button>
            {explain && <p>{problem.feedback}</p>}
          </div>
        )}
    </div>
  );
}
export function Prediction(
  { problem, record }: {
    problem: Problem & { options?: string[] };
    record: RecordAttempt;
  },
) {
  const [answer, setAnswer] = useState<number | null>(null),
    [checked, setChecked] = useState(false),
    [show, setShow] = useState(false);
  return (
    <div className="practice">
      <span className="phase">PREDICT → COMMIT → COMPARE</span>
      <h3>{problem.prompt}</h3>
      <Tabs
        labels={problem.options ?? []}
        value={answer ?? -1}
        onChange={(i) => {
          if (!checked) setAnswer(i);
        }}
      />
      {!checked
        ? (
          <button
            className="primary"
            disabled={answer === null}
            onClick={() => {
              setChecked(true);
              record({
                question: problem.prompt,
                answer: problem.options?.[answer!] ?? "",
                reason: "Prediction",
                correct: answer === problem.answer,
              });
            }}
          >
            Commit prediction
          </button>
        )
        : (
          <>
            <p className="result-box">
              {answer === problem.answer
                ? "Prediction matches."
                : "The experiment gives a different result."}
            </p>
            <button onClick={() => setShow(!show)}>
              Compare the two people
            </button>
            {show && <p>{problem.feedback}</p>}
          </>
        )}
    </div>
  );
}
export function Card({ children }: { children: ReactNode }) {
  return <div className="calculation-card">{children}</div>;
}
