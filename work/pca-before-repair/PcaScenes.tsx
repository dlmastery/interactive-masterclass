import { type ReactNode, useId, useState } from "react";
import { type Case, Eq, f, type Lab, type Point } from "./LabComponents.tsx";

export type Step = { tex: string; why: string };
export type Lesson = {
  id: number;
  title: string;
  action: string;
  claim: string;
  scene: string;
  chapter: number;
  steps: Step[];
};
const names = ["A", "B", "C", "D"];
const ink = "#dfeaf5", teal = "#62e1cd", coral = "#ff9f7a", muted = "#8298b2";
export function Slider(
  { label, value, min = 0, max = 180, step = 1, onChange }: {
    label: string;
    value: number;
    min?: number;
    max?: number;
    step?: number;
    onChange: (v: number) => void;
  },
) {
  return (
    <label className="pca-slider">
      <span>
        {label}
        <output>{f(value, step < 1 ? 1 : 0)}</output>
      </span>
      <input
        aria-label={label}
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(+e.target.value)}
      />
    </label>
  );
}
export function Angles(
  { angle, setAngle }: { angle: number; setAngle: (v: number) => void },
) {
  return (
    <div className="angle-controls">
      <Slider label="Axis angle in degrees" value={angle} onChange={setAngle} />
      <div className="preset-row">
        {[0, 45, 90, 135].map((a) => (
          <button
            key={a}
            aria-pressed={angle === a}
            onClick={() => setAngle(a)}
          >
            {a}°
          </button>
        ))}
      </div>
    </div>
  );
}
export function Metric(
  { label, value, note }: { label: string; value: string; note?: string },
) {
  return (
    <div className="metric">
      <small>{label}</small>
      <strong>{value}</strong>
      {note && <span>{note}</span>}
    </div>
  );
}
export function Proof({ steps }: { steps: Step[] }) {
  const [step, setStep] = useState(0);
  if (!steps.length) return null;
  return (
    <div className="proof">
      <div className="proof-label">
        FOLLOW THE DERIVATION <span>{step + 1} / {steps.length}</span>
      </div>
      {step > 0 && (
        <div className="previous-equation">
          <small>Previous expression</small>
          <Eq tex={steps[step - 1].tex} />
        </div>
      )}
      <div className="current-equation">
        <Eq tex={steps[step].tex} />
      </div>
      <p className="proof-reason">
        <span>Why this step</span>
        {steps[step].why}
      </p>
      {steps.length > 1 && (
        <div className="proof-nav">
          <button disabled={step === 0} onClick={() => setStep(step - 1)}>
            ← Previous step
          </button>
          <button
            className="accent"
            disabled={step === steps.length - 1}
            onClick={() => setStep(step + 1)}
          >
            Next step →
          </button>
        </div>
      )}
    </div>
  );
}
type GeometryProps = {
  c: Case;
  angle: number;
  person: number;
  setPerson: (v: number) => void;
  mode?: string;
  fraction?: number;
  keep?: number;
  sign?: number;
  compact?: boolean;
  newPoint?: Point;
  categories?: boolean;
  projectProgress?: number;
  rulerLength?: number;
};
export function Geometry(
  {
    c,
    angle,
    person,
    setPerson,
    mode = "shadow",
    fraction = 1,
    keep = 1,
    sign = 1,
    compact = false,
    newPoint,
    categories = false,
    projectProgress = 0,
    rulerLength = 1,
  }: GeometryProps,
) {
  const id = useId().replaceAll(":", "");
  const frame = c.frames[Math.round(angle)] ?? c.frames[0];
  const w = frame.w;
  const rotation = mode === "rotated" || mode === "rotateFree",
    raw = mode === "center";
  const source: Point[] = rotation
    ? mode === "rotateFree"
      ? c.points.map((p, i) => [frame.z[i], w[0] * p[1] - w[1] * p[0]])
      : c.scores.map((p) => [p[0] * sign, p[1]])
    : raw
    ? c.raw.map((
      p,
    ) => [p[0] - c.mean[0] * fraction, p[1] - c.mean[1] * fraction])
    : c.points;
  const center: Point = raw
    ? [c.mean[0] * (1 - fraction), c.mean[1] * (1 - fraction)]
    : [0, 0];
  const bound = Math.max(
    newPoint || mode === "eigen" || mode === "ruler" ? 6.5 : 2.8,
    ...c.points.flat().map(Math.abs),
  ) * 1.2;
  const s = 146 / bound,
    px = (x: number) => 285 + (x - center[0]) * s,
    py = (y: number) => 213 - (y - center[1]) * s;
  const dots = mode === "decode"
    ? c.recon[keep].points
    : projectProgress > 0
    ? source.map((pt, i): Point =>
      i === person
        ? [
          pt[0] + (frame.projected[i][0] - pt[0]) * projectProgress,
          pt[1] + (frame.projected[i][1] - pt[1]) * projectProgress,
        ]
        : pt
    )
    : source;
  const showProjection = [
    "shadow",
    "one",
    "loss",
    "triangle",
    "hidden",
    "eigen",
    "compare",
  ].includes(mode);
  const originalHidden = mode === "hidden";
  const scoreBound = Math.max(3.3, ...c.points.map((p) => Math.hypot(...p))) *
    1.2 * (mode === "ruler" ? 6 : 1);
  const sx = (z: number) => 285 + z * 215 / scoreBound;
  const scoreValues = mode === "ruler"
    ? frame.z.map((z) => z * rulerLength)
    : mode === "rotateFree"
    ? frame.z
    : rotation || mode === "decode"
    ? c.scores.map((p) => p[0])
    : frame.z;
  const scoreLabel = (mode === "rotated" || mode === "decode")
    ? "PC1 score"
    : "One score per observation";
  if (raw) {
    const X = (x: number) => 94 + x * 31, Y = (y: number) => 347 - y * 31;
    return (
      <div className="geometry">
        <svg
          viewBox="0 0 590 480"
          role="img"
          aria-label="Translate the data toward a zero mean"
        >
          {[0, 2, 4, 6, 8, 10].map((t) => (
            <g key={t}>
              <line x1={X(0)} y1={Y(t)} x2={X(11)} y2={Y(t)} stroke="#26394c" />
              <line x1={X(t)} y1={Y(0)} x2={X(t)} y2={Y(11)} stroke="#26394c" />
              <text x={X(t)} y={Y(0) + 24} textAnchor="middle" fill={muted}>
                {t}
              </text>
              <text x={X(0) - 15} y={Y(t) + 4} textAnchor="end" fill={muted}>
                {t}
              </text>
            </g>
          ))}
          <line x1="55" y1={Y(0)} x2="495" y2={Y(0)} stroke={muted} />
          <line x1={X(0)} y1="15" x2={X(0)} y2="430" stroke={muted} />
          {c.raw.map((pt, i) => (
            <g key={i}>
              <circle
                cx={X(pt[0])}
                cy={Y(pt[1])}
                r="6"
                fill="none"
                stroke="#52647b"
              />
              <line
                x1={X(pt[0])}
                y1={Y(pt[1])}
                x2={X(pt[0] - 6 * fraction)}
                y2={Y(pt[1] - 6 * fraction)}
                stroke="#52647b"
                strokeDasharray="4 5"
              />
              <circle
                cx={X(pt[0] - 6 * fraction)}
                cy={Y(pt[1] - 6 * fraction)}
                r={person === i ? 9 : 6}
                fill={person === i ? teal : ink}
              />
              <text
                x={X(pt[0] - 6 * fraction) + 12}
                y={Y(pt[1] - 6 * fraction) - 10}
                fill={ink}
              >
                {names[i]}
              </text>
            </g>
          ))}
          <circle
            cx={X(6 * (1 - fraction))}
            cy={Y(6 * (1 - fraction))}
            r="5"
            fill={coral}
          />
          <text
            x={X(6 * (1 - fraction)) + 12}
            y={Y(6 * (1 - fraction)) + 24}
            fill={coral}
          >
            mean ({f(6 * (1 - fraction), 1)}, {f(6 * (1 - fraction), 1)})
          </text>
          <text x="95" y="460" fill={muted}>
            The pale outlines mark the original positions.
          </text>
        </svg>
        <div className="observation-select">
          {names.map((name, i) => (
            <button
              key={name}
              aria-pressed={person === i}
              onClick={() => setPerson(i)}
            >
              {name}
            </button>
          ))}
        </div>
      </div>
    );
  }
  return (
    <div className={"geometry " + (compact ? "compact" : "")}>
      <svg
        viewBox="0 0 590 480"
        role="img"
        aria-label={mode === "eigen"
          ? "Direction w and the transformed direction S w"
          : `Centered data and projections at ${angle} degrees`}
      >
        <defs>
          <marker
            id={"arrow" + id}
            markerWidth="7"
            markerHeight="7"
            refX="5"
            refY="3.5"
            orient="auto"
          >
            <path d="M0,0 L6,3.5 L0,7" fill={teal} />
          </marker>
          <marker
            id={"warm" + id}
            markerWidth="7"
            markerHeight="7"
            refX="5"
            refY="3.5"
            orient="auto"
          >
            <path d="M0,0 L6,3.5 L0,7" fill={coral} />
          </marker>
        </defs>
        {[-3, -2, -1, 0, 1, 2, 3].map((t) => (
          <g key={t}>
            <line
              x1={px(-bound)}
              y1={py(t + center[1])}
              x2={px(bound)}
              y2={py(t + center[1])}
              stroke="#23374e"
            />
            <line
              x1={px(t + center[0])}
              y1={py(-bound)}
              x2={px(t + center[0])}
              y2={py(bound)}
              stroke="#23374e"
            />
          </g>
        ))}
        <line
          x1="68"
          y1={py(center[1])}
          x2="526"
          y2={py(center[1])}
          stroke={muted}
        />
        <line
          x1={px(center[0])}
          y1="38"
          x2={px(center[0])}
          y2="363"
          stroke={muted}
        />
        <text x="485" y="238" fill={muted}>
          {mode === "rotateFree" ? "along w" : rotation ? "PC1" : "x"}
        </text>
        <text x="304" y="42" fill={muted}>
          {mode === "rotateFree" ? "across w" : rotation ? "PC2" : "y"}
        </text>
        {[-2, 2].map((t) => (
          <g key={"tick" + t}>
            <text
              x={px(t + center[0])}
              y="235"
              textAnchor="middle"
              fill={muted}
            >
              {f(t + center[0], 0)}
            </text>
            <text
              x="268"
              y={py(t + center[1]) + 5}
              textAnchor="end"
              fill={muted}
            >
              {f(t + center[1], 0)}
            </text>
          </g>
        ))}
        {!raw && !rotation && mode !== "points" && (
          <line
            x1={px(-w[0] * bound)}
            y1={py(-w[1] * bound)}
            x2={px(w[0] * bound)}
            y2={py(w[1] * bound)}
            stroke={teal}
            strokeWidth="2.5"
          />
        )}
        {showProjection && c.points.map((p, i) => {
          const q = frame.projected[i];
          return (
            <g key={"projection" + i} opacity={person === i ? 1 : .34}>
              {!originalHidden && (
                <line
                  x1={px(p[0])}
                  y1={py(p[1])}
                  x2={px(q[0])}
                  y2={py(q[1])}
                  stroke={coral}
                  strokeWidth={person === i ? 2.5 : 1.5}
                  strokeDasharray="4 5"
                />
              )}
              <circle
                cx={px(q[0])}
                cy={py(q[1])}
                r="5"
                fill={teal}
                stroke="#102036"
                strokeWidth="2"
              />
            </g>
          );
        })}
        {mode === "hidden" && (
          <line
            x1={px(frame.projected[person][0] - w[1] * bound)}
            y1={py(frame.projected[person][1] + w[0] * bound)}
            x2={px(frame.projected[person][0] + w[1] * bound)}
            y2={py(frame.projected[person][1] - w[0] * bound)}
            stroke={coral}
            strokeWidth="3"
            strokeDasharray="5 6"
          />
        )}
        {mode === "triangle" && (
          <>
            <path
              d={`M${px(0)},${py(0)} L${px(c.points[person][0])},${
                py(c.points[person][1])
              } L${px(frame.projected[person][0])},${
                py(frame.projected[person][1])
              } Z`}
              fill="#62e1cd15"
              stroke={ink}
              strokeWidth="1.3"
            />
            <line
              x1={px(0)}
              y1={py(0)}
              x2={px(frame.projected[person][0])}
              y2={py(frame.projected[person][1])}
              stroke={teal}
              strokeWidth="5"
            />
          </>
        )}
        {mode === "ruler" && (
          <>
            <line
              x1={px(0)}
              y1={py(0)}
              x2={px(w[0] * rulerLength)}
              y2={py(w[1] * rulerLength)}
              stroke={teal}
              strokeWidth="5"
              markerEnd={`url(#arrow${id})`}
            />
            <text x="24" y="25" fill={teal}>
              Direction length: {f(rulerLength, 0)}
            </text>
            <text x="24" y="51" fill={muted}>
              The score ruler below keeps the same scale.
            </text>
          </>
        )}
        {mode === "eigen" && (
          <>
            <circle
              cx={px(0)}
              cy={py(0)}
              r={s}
              fill="none"
              stroke={muted}
              strokeDasharray="3 4"
            />
            <line
              x1={px(0)}
              y1={py(0)}
              x2={px(w[0])}
              y2={py(w[1])}
              stroke={teal}
              strokeWidth="5"
              markerEnd={`url(#arrow${id})`}
            />
            <line
              x1={px(0)}
              y1={py(0)}
              x2={px(frame.sw[0])}
              y2={py(frame.sw[1])}
              stroke={coral}
              strokeWidth="4"
              markerEnd={`url(#warm${id})`}
            />
            <text x="24" y="25" fill={teal}>w</text>
            <text x="85" y="25" fill={coral}>Sw</text>
            <text x="182" y="25" fill={muted}>
              Both arrows use the same scale
            </text>
          </>
        )}
        {mode === "decode" && c.points.map((pt, i) => (
          <g key={"original" + i}>
            <circle
              cx={px(pt[0])}
              cy={py(pt[1])}
              r="7"
              fill="none"
              stroke={muted}
            />
            <line
              x1={px(pt[0])}
              y1={py(pt[1])}
              x2={px(dots[i][0])}
              y2={py(dots[i][1])}
              stroke={coral}
              strokeDasharray="4 5"
            />
          </g>
        ))}
        {newPoint && (
          <g>
            <line
              x1={px(newPoint[0])}
              y1={py(newPoint[1])}
              x2={px((newPoint[0] + newPoint[1]) / 2)}
              y2={py((newPoint[0] + newPoint[1]) / 2)}
              stroke={coral}
              strokeWidth="2"
              strokeDasharray="5 5"
            />
            <circle
              cx={px(newPoint[0])}
              cy={py(newPoint[1])}
              r="9"
              fill={coral}
            />
            <text
              x={px(newPoint[0]) + 13}
              y={py(newPoint[1]) - 12}
              fill={coral}
            >
              NEW
            </text>
          </g>
        )}
        {!originalHidden &&
          dots.map((p, i) => (
            <g key={i} opacity={mode === "one" && i !== person ? .16 : 1}>
              <circle
                cx={px(p[0])}
                cy={py(p[1])}
                r={person === i ? 9 : 6}
                fill={categories
                  ? (p[1] > 0 ? coral : teal)
                  : person === i
                  ? "#fff"
                  : ink}
                stroke={person === i ? teal : "#102036"}
                strokeWidth="3"
              />
              <text
                x={px(p[0]) + 13}
                y={py(p[1]) - 12}
                fill={ink}
                fontWeight="700"
              >
                {categories ? (p[1] > 0 ? "+" : "−") : names[i] ?? i + 1}
              </text>
            </g>
          ))}
        <circle cx={px(center[0])} cy={py(center[1])} r="4" fill={teal} />
        <text x={px(center[0]) + 10} y={py(center[1]) + 26} fill={muted}>
          {raw ? `mean (${f(center[0], 1)}, ${f(center[1], 1)})` : "0 · center"}
        </text>
        {!raw && mode !== "points" && (
          <>
            <line
              x1="60"
              y1="416"
              x2="520"
              y2="416"
              stroke={teal}
              strokeWidth="2"
            />
            <line x1="285" y1="408" x2="285" y2="424" stroke={teal} />
            <text x="285" y="391" textAnchor="middle" fill={teal}>
              {scoreLabel}
            </text>
            {scoreValues.map((z, i) => {
              const overlaps = scoreValues.slice(0, i).filter((q) =>
                Math.abs(q - z) < .025
              ).length;
              return (
                <g key={"score" + i}>
                  <circle
                    cx={sx(z * sign)}
                    cy={416 + overlaps * 17}
                    r={person === i ? 7 : 5}
                    fill={person === i ? "#fff" : teal}
                  />
                  <text
                    x={sx(z * sign)}
                    y={450 + overlaps * 17}
                    textAnchor="middle"
                    fill={ink}
                  >
                    {names[i] ?? i + 1}
                    {person === i ? ` ${f(z * sign)}` : ""}
                  </text>
                </g>
              );
            })}
          </>
        )}
      </svg>
      <div className="observation-select" aria-label="Select an observation">
        {c.points.slice(0, 8).map((_, i) => (
          <button
            key={i}
            aria-pressed={person === i}
            onClick={() => setPerson(i)}
          >
            {names[i] ?? i + 1}
          </button>
        ))}
        <span>Select an observation</span>
      </div>
    </div>
  );
}
function VarianceCurve(
  { c, angle, setAngle }: {
    c: Case;
    angle: number;
    setAngle: (v: number) => void;
  },
) {
  const max = c.values[0] * 1.12;
  return (
    <div className="curve">
      <svg
        viewBox="0 0 590 160"
        role="img"
        aria-label="Variance against direction angle"
      >
        <line x1="45" y1="125" x2="552" y2="125" stroke={muted} />
        <path
          d={c.frames.map((p, i) =>
            `${i ? "L" : "M"}${45 + i * 507 / 180},${
              125 - p.variance / max * 98
            }`
          ).join(" ")}
          fill="none"
          stroke={teal}
          strokeWidth="3"
        />
        <circle
          cx={45 + angle * 507 / 180}
          cy={125 - c.frames[angle].variance / max * 98}
          r="6"
          fill={coral}
        />
        <text x="12" y="23" fill={muted}>variance</text>
        {[0, 45, 90, 135, 180].map((a) => (
          <text
            key={a}
            x={45 + a * 507 / 180}
            y="151"
            textAnchor="middle"
            fill={muted}
          >
            {a}°
          </text>
        ))}
      </svg>
      <div className="preset-row">
        <button onClick={() => setAngle(Math.round(c.angle))}>
          Show maximum
        </button>
        <button onClick={() => setAngle(Math.round((c.angle + 90) % 180))}>
          Show minimum
        </button>
      </div>
    </div>
  );
}
function Covariance(
  { c, entry, setEntry }: {
    c: Case;
    entry: number;
    setEntry: (n: number) => void;
  },
) {
  const row = Math.floor(entry / 2), col = entry % 2;
  return (
    <div className="covariance-board">
      <div className="matrix-buttons" aria-label="Covariance matrix">
        {c.cov.flat().map((v, i) => (
          <button
            key={i}
            aria-pressed={entry === i}
            onClick={() => setEntry(i)}
          >
            <small>S{Math.floor(i / 2) + 1}{i % 2 + 1}</small>
            {f(v, 3)}
          </button>
        ))}
      </div>
      <div className="product-table">
        <div className="table-row table-head">
          <span>Point</span>
          <span>{row ? "b" : "a"} × {col ? "b" : "a"}</span>
          <span>Product</span>
        </div>
        {c.points.map((p, i) => (
          <div className="table-row" key={i}>
            <span>{names[i] ?? i + 1}</span>
            <span>{f(p[row], 1)} × {f(p[col], 1)}</span>
            <strong className={p[row] * p[col] < 0 ? "warm" : "cool"}>
              {f(p[row] * p[col], 2)}
            </strong>
          </div>
        ))}
        <div className="table-row table-total">
          <span>Sum / {c.n - 1}</span>
          <span>{f(c.sums[row][col], 2)} / {c.n - 1}</span>
          <strong>{f(c.cov[row][col], 3)}</strong>
        </div>
      </div>
    </div>
  );
}
function Check(
  { prompt, answer, tolerance = .02, explain }: {
    prompt: string;
    answer: number;
    tolerance?: number;
    explain: string;
  },
) {
  const [value, setValue] = useState(""),
    [reason, setReason] = useState(""),
    [status, setStatus] = useState("");
  return (
    <div className="check">
      <p>{prompt}</p>
      <label>
        Your number<input
          type="number"
          value={value}
          onChange={(e) => {
            setValue(e.target.value);
            setStatus("");
          }}
        />
      </label>
      <label>
        Explain your method<textarea
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          placeholder="State the operation and why it applies."
        />
      </label>
      <button
        className="accent"
        disabled={!value || !reason.trim()}
        onClick={() =>
          setStatus(
            Math.abs(+value - answer) <= tolerance ? "correct" : "miss",
          )}
      >
        Check the number
      </button>
      {status && (
        <div role="status">
          <strong>
            {status === "correct"
              ? "The number is correct."
              : "The number does not match yet."}
          </strong>
          <p>{explain}</p>
          <small>
            Your written reason needs review. This check only grades the number.
          </small>
        </div>
      )}
    </div>
  );
}
type Props = {
  s: Lesson;
  lab: Lab;
  sandbox: Case | null;
  angle: number;
  setAngle: (v: number) => void;
  person: number;
  setPerson: (v: number) => void;
};
export function Scene(
  { s, lab, sandbox, angle, setAngle, person, setPerson }: Props,
) {
  const [phase, setPhase] = useState(0),
    [fraction, setFraction] = useState(0),
    [keep, setKeep] = useState(1),
    [variant, setVariant] = useState(0),
    [entry, setEntry] = useState(1),
    [weight, setWeight] = useState(50),
    [scale, setScale] = useState(0),
    [standard, setStandard] = useState(false),
    [answer, setAnswer] = useState(""),
    [note, setNote] = useState(""),
    [sent, setSent] = useState(false),
    [newX, setNewX] = useState(9),
    [newY, setNewY] = useState(7);
  const n = s.id;
  const c = n === 45 || n === 60
    ? lab.edgeCases[2]
    : n === 59
    ? (variant === 0
      ? lab.base
      : variant === 1
      ? lab.edgeCases[1]
      : lab.nuisance)
    : n === 58
    ? (standard ? lab.scales[scale].standard : lab.scales[scale].raw)
    : n === 61
    ? (sandbox ?? lab.base)
    : n === 62
    ? lab.challenge
    : n === 25
    ? lab.covCases[variant === 0 ? 0 : 1]
    : n === 24
    ? lab.covCases[variant]
    : lab.base;
  const p = Math.min(person, c.n - 1), frame = c.frames[angle] ?? c.frames[0];
  const angleControl = <Angles angle={angle} setAngle={setAngle} />;
  const geo = (mode = "shadow", compact = false, extra = {}) => (
    <Geometry
      c={c}
      angle={angle}
      person={p}
      setPerson={setPerson}
      mode={mode}
      compact={compact}
      {...extra}
    />
  );
  const metrics = (
    <div className="metrics">
      <Metric
        label="Kept variance"
        value={f(frame.variance)}
        note={`${f(frame.ratio * 100, 1)}% of total`}
      />
      <Metric
        label="Lost variance"
        value={f(frame.loss)}
        note="Squared residual sum / (n−1)"
      />
    </div>
  );
  let displayedSteps = s.steps;
  if (n === 24) {
    const r = Math.floor(entry / 2), k = entry % 2;
    displayedSteps = [{
      tex: `S_{${r + 1}${k + 1}}=\\frac{${
        c.points.map((pt) => `(${pt[r]})(${pt[k]})`).join("+")
      }}{${c.n - 1}}=${f(c.cov[r][k], 3)}`,
      why:
        "This is the selected entry. The table shows its product from each observation.",
    }];
  }
  if (n === 14) {
    displayedSteps = [{
      tex: `z_${names[p]}=w^\\top x_${names[p]}=${c.points[p][0]}w_1+(${
        c.points[p][1]
      })w_2`,
      why:
        "Multiply matching coordinates. Add the two products. A negative score is on the other side of the center.",
    }];
  }
  if (n === 11) {
    displayedSteps = [{
      tex: `x_${names[p]}=(${c.raw[p].join(",")})-(6,6)=(${
        c.points[p].join(",")
      })`,
      why:
        "Subtract the mean of each feature. The new coordinates measure position from the center.",
    }];
  }
  if (n === 50) {
    displayedSteps = [{
      tex: String.raw`\widehat r_i=\mu+\sum_{j=1}^k z_{ij}q_j`,
      why:
        "Use each retained score with its axis. Add these vectors to the stored mean.",
    }, {
      tex: `\\widehat r_${names[p]}=(${
        c.recon[keep].raw[p].map((v) => f(v, 2)).join(",")
      })`,
      why: `The original measurement is (${
        c.raw[p].join(", ")
      }). This reconstruction keeps ${keep} components.`,
    }];
  }
  const eq = (
    <Proof
      key={`${n}-${
        n === 24
          ? variant + "-" + entry
          : n === 11 || n === 14 || n === 50
          ? p + "-" + keep
          : ""
      }`}
      steps={displayedSteps}
    />
  );
  const split = (left: ReactNode, right: ReactNode, cls = "") => (
    <div className={"scene-split " + cls}>
      <div className="visual-side">{left}</div>
      <div className="reason-side">{right}</div>
    </div>
  );
  if (s.scene === "geometry") {
    const modes = [
      "shadow",
      "one",
      "compare",
      "one",
      "hidden",
      "rotated",
      "loss",
      "shadow",
    ];
    return split(
      <>
        <p className="diagram-caption">
          Four measured positions · coordinates from the center, in cm
        </p>
        {geo(
          n === 6
            ? (phase ? "shadow" : "rotateFree")
            : n === 8
            ? ["points", "shadow", "rotated", "decode"][phase]
            : modes[n - 1],
          false,
          n === 8 ? { keep: 1 } : n === 4 ? { projectProgress: fraction } : {},
        )}
        {angleControl}
        {n === 4 && (
          <Slider
            label="Move the point to its projection (%)"
            max={100}
            value={fraction * 100}
            onChange={(v) => setFraction(v / 100)}
          />
        )}
      </>,
      <>
        <p className="big-idea">
          {n === 1
            ? "PCA finds new axes through the center of the data. The first axis follows the largest spread. Keep fewer coordinates to store fewer numbers."
            : s.claim}
        </p>
        {n === 3
          ? (
            <>
              <div className="compare-bars">
                {[45, 135].map((a) => (
                  <button
                    key={a}
                    onClick={() => setAngle(a)}
                  >
                    <span>{a}° view</span>
                    <strong>{f(c.frames[a].ratio * 100, 0)}% kept</strong>
                    <i style={{ width: c.frames[a].ratio * 100 + "%" }} />
                  </button>
                ))}
              </div>
              <p>
                Both views use the same scale. The direction along the cloud
                keeps more spread.
              </p>
            </>
          )
          : (
            <div className="metrics">
              <Metric
                label="Spread kept"
                value={f(n === 6 && phase === 0 ? 100 : frame.ratio * 100, 1) +
                  "%"}
              />
              <Metric
                label="Spread lost"
                value={f(
                  n === 6 && phase === 0 ? 0 : (1 - frame.ratio) * 100,
                  1,
                ) + "%"}
              />
            </div>
          )}
        {n === 4 && (
          <p>
            The pale point is the measurement. Its teal point is the closest
            point on the line.
          </p>
        )}
        {n === 5 && (
          <p>
            Every point on the orange line has the same score. One coordinate
            cannot distinguish these points.
          </p>
        )}
        {n === 6 && (
          <div className="preset-row">
            <button onClick={() => setPhase(0)}>Keep both coordinates</button>
            <button onClick={() => setPhase(1)}>Keep one coordinate</button>
          </div>
        )}
        {n === 7 && (
          <p>
            We will prove this relation: kept squared distance + lost squared
            distance = a fixed total.
          </p>
        )}
        {n === 8 && (
          <div className="vertical-controls">
            {[
              "1 · Center the data",
              "2 · Find the best direction",
              "3 · Store the scores",
              "4 · Reconstruct a point",
            ].map((t, i) => (
              <button
                key={t}
                aria-pressed={phase === i}
                onClick={() => {
                  setPhase(i);
                  setAngle(45);
                }}
              >
                {t}
              </button>
            ))}
          </div>
        )}
        <div className="try">
          <small>TRY IT</small>
          <p>
            {n === 1
              ? "Compare the 45° and 135° views. Which view keeps the large differences in the cloud?"
              : s.action}
          </p>
        </div>
      </>,
    );
  }
  if (s.scene === "center") {
    return split(
      <>
        {geo("center", false, { fraction })}
        <Slider
          label="Move the mean to zero"
          max={100}
          value={fraction * 100}
          onChange={(v) => setFraction(v / 100)}
        />
      </>,
      <>
        {eq}
        <div className="metrics">
          <Metric label="Original mean" value="(6, 6)" />
          <Metric
            label="Selected point"
            value={`(${f(c.raw[p][0] - 6 * fraction, 1)}, ${
              f(c.raw[p][1] - 6 * fraction, 1)
            })`}
          />
        </div>
        <p>
          {n === 12
            ? "A and B stay √2 units apart during this move. Both points receive the same translation."
            : "The same four measurements remain in the cloud. Only the coordinate origin changes."}
        </p>
      </>,
    );
  }
  if (s.scene === "score") {
    return split(
      <>
        {n === 16 ? geo("ruler", false, { rulerLength: keep }) : geo("one")}
        {angleControl}
      </>,
      <>
        {eq}
        <div className="weighted-sum">
          <small>{names[p]} · follow the two products</small>
          <div>
            <span>
              {f(c.points[p][0])} × {f(frame.w[0] * (n === 16 ? keep : 1))}
            </span>
            <b>+</b>
            <span>
              {f(c.points[p][1])} × {f(frame.w[1] * (n === 16 ? keep : 1))}
            </span>
          </div>
          <strong>= {f(frame.z[p] * (n === 16 ? keep : 1))}</strong>
        </div>
        {n === 15 && (
          <div className="score-table">
            {frame.z.map((z, i) => (
              <button
                aria-pressed={p === i}
                onClick={() => setPerson(i)}
                key={i}
              >
                {names[i]}
                <span>{f(z)}</span>
              </button>
            ))}
          </div>
        )}
        {n === 16 && (
          <>
            <Slider
              label="Direction length"
              min={1}
              max={6}
              value={keep}
              onChange={setKeep}
            />
            <Metric
              label="Variance with this length"
              value={f(frame.variance * keep * keep)}
            />
            <p>
              The line stays the same. The scale changes. Use length one for a
              fair comparison.
            </p>
          </>
        )}
      </>,
    );
  }
  if (s.scene === "variance") {
    return split(
      <>{geo("shadow")}{angleControl}</>,
      <>
        {eq}
        {n === 20
          ? <VarianceCurve c={c} angle={angle} setAngle={setAngle} />
          : (
            <div className="square-ledger">
              {frame.z.map((z, i) => (
                <button
                  key={i}
                  aria-pressed={p === i}
                  onClick={() => setPerson(i)}
                >
                  <span>{names[i]}</span>
                  <span>{f(z)}²</span>
                  <strong>{f(z * z)}</strong>
                  <i style={{ width: Math.max(3, z * z / 10 * 100) + "%" }} />
                </button>
              ))}
              <div>
                Sum of squares <strong>{f(frame.sumSquares)}</strong>
              </div>
            </div>
          )}
        {metrics}
        {n === 19 && (
          <details>
            <summary>Why divide by n−1?</summary>
            <p>
              We estimated the mean from these observations. Their centered
              values must sum to zero. Only n−1 deviations are free.
            </p>
            <p>
              For independent samples, this divisor corrects the average
              underestimate of population variance. A divisor n gives the same
              PCA directions.
            </p>
          </details>
        )}
      </>,
    );
  }
  if (s.scene === "expansion") {
    const terms = [
      frame.w[0] ** 2 * c.cov[0][0],
      2 * frame.w[0] * frame.w[1] * c.cov[0][1],
      frame.w[1] ** 2 * c.cov[1][1],
    ];
    return split(
      <>
        {eq}
        <div className="term-strip">
          {["First square", "Cross-term", "Second square"].map((t, i) => (
            <div key={t}>
              <small>{t}</small>
              <strong>{f(terms[i], 3)}</strong>
            </div>
          ))}
        </div>
        <div className="term-total">Sum = {f(frame.variance, 3)}</div>
      </>,
      <>
        {geo("one", true)}
        {angleControl}
        <p>
          The terms change with the direction. Their sum always equals the
          variance of the four scores.
        </p>
      </>,
      "proof-layout",
    );
  }
  if (s.scene === "covariance") {
    return split(
      <>
        <Covariance c={c} entry={entry} setEntry={setEntry} />
        {n === 24 || n === 25
          ? (
            <div className="preset-row">
              {(n === 24
                ? ["Together", "Opposite", "Cancellation"]
                : ["Positive tilt", "Negative tilt"]).map((t, i) => (
                  <button
                    key={t}
                    aria-pressed={variant === i}
                    onClick={() => setVariant(i)}
                  >
                    {t}
                  </button>
                ))}
            </div>
          )
          : null}
        {eq}
      </>,
      <>
        {geo("points", true)}
        <p>
          {n === 27
            ? "Choose an entry of S. The product table shows one row-by-column calculation."
            : "Keep the individual products visible. Their sum explains the sign of the covariance."}
        </p>
      </>,
      "proof-layout",
    );
  }
  if (s.scene === "objective") {
    return split(
      <>
        {eq}
        <div className="calculation-compare">
          <Metric
            label="From all squared scores"
            value={f(frame.variance, 4)}
          />
          <span>=</span>
          <Metric
            label="From wᵀ S w"
            value={f(frame.w[0] * frame.sw[0] + frame.w[1] * frame.sw[1], 4)}
          />
        </div>
        <p>
          Here w = ({f(frame.w[0], 3)},{" "}
          {f(frame.w[1], 3)}). S w = ({f(frame.sw[0], 3)}, {f(frame.sw[1], 3)}).
        </p>
      </>,
      <>
        {geo("shadow", true)}
        {angleControl}
        {n === 30 && <VarianceCurve c={c} angle={angle} setAngle={setAngle} />}
      </>,
      "proof-layout",
    );
  }
  if (s.scene === "eigen") {
    return split(
      <>
        {eq}
        <div className="metrics">
          <Metric
            label="Variance at this direction"
            value={f(frame.variance, 3)}
          />
          <Metric
            label="Slope with a small turn"
            value={f(frame.slope, 3)}
            note="Derivative per radian"
          />
        </div>
        {n >= 35 && (
          <div className="candidate-controls">
            <button onClick={() => setAngle(45)}>Candidate 1 · 45°</button>
            <button onClick={() => setAngle(135)}>Candidate 2 · 135°</button>
            <button
              onClick={() => setAngle(20)}
            >
              A different direction
            </button>
          </div>
        )}
        <p className="numeric-witness">
          {Math.abs(frame.slope) < .001
            ? "The slope is zero here. Compare both stationary directions before choosing the maximum."
            : "A small turn can change variance. This is not a stationary direction."}
        </p>
      </>,
      <>
        {geo("eigen", true)}
        {angleControl}
        {n === 32 || n === 40
          ? <VarianceCurve c={c} angle={angle} setAngle={setAngle} />
          : (
            <p>
              The teal arrow is w. The orange arrow is Sw. Both arrows use the
              same scale. The small circle has radius one.
            </p>
          )}
      </>,
      "proof-layout",
    );
  }
  if (s.scene === "maximum") {
    const a = Math.sqrt(weight / 100),
      b = Math.sqrt(1 - weight / 100),
      v = c.values[0] * a * a + c.values[1] * b * b;
    const mixW = [
      a * c.axes[0][0] + b * c.axes[1][0],
      a * c.axes[0][1] + b * c.axes[1][1],
    ];
    const mixAngle = Math.round(
      (Math.atan2(mixW[1], mixW[0]) * 180 / Math.PI + 180) % 180,
    );
    return split(
      <>
        {eq}
        <div className="mixture">
          <div>
            <span>a² = {f(a * a)}</span>
            <i style={{ width: weight + "%" }} />
          </div>
          <div>
            <span>b² = {f(b * b)}</span>
            <i style={{ width: (100 - weight) + "%" }} />
          </div>
        </div>
        <Slider
          label="Squared weight on the first eigenvector (%)"
          max={100}
          value={weight}
          onChange={setWeight}
        />
        <div className="metrics">
          <Metric label="Weighted eigenvalue average" value={f(v, 3)} />
          <Metric label="Upper bound λ₁" value={f(c.values[0], 3)} />
        </div>
        <p>
          {n === 45
            ? "The bound is reached at every allocation. This cloud has no unique longest axis."
            : "Put more squared weight on the larger eigenvalue. The average reaches its maximum when all weight is there."}
        </p>
      </>,
      <>
        <Geometry
          c={c}
          angle={mixAngle}
          person={p}
          setPerson={setPerson}
          compact
        />
        <p>
          w = {f(a, 3)} q₁ + {f(b, 3)}{" "}
          q₂. The picture follows this direction, rounded to one degree.
        </p>
        <p>
          A real symmetric matrix has an orthonormal basis of eigenvectors. This
          theorem also applies when the number of features is larger.
        </p>
      </>,
      "proof-layout",
    );
  }
  if (s.scene === "coordinates") {
    return split(
      <>
        {geo(phase ? "rotated" : "shadow", false, { sign: variant ? -1 : 1 })}
        <div className="preset-row">
          <button
            onClick={() => {
              setPhase(0);
              setAngle(45);
            }}
          >
            Original axes
          </button>
          <button onClick={() => setPhase(1)}>PCA axes</button>
          <button onClick={() => setVariant(variant ? 0 : 1)}>
            Reverse PC1 sign
          </button>
        </div>
      </>,
      <>
        {eq}
        {n === 48
          ? (
            <>
              <div className="small-matrix">
                {c.scoreCov.flat().map((v, i) => (
                  <span key={i}>{f(v, 3)}</span>
                ))}
              </div>
              <p>
                Both off-diagonal entries are zero. The two score columns have
                zero sample covariance.
              </p>
            </>
          )
          : (
            <div className="spectrum-bars">
              {c.values.map((v, i) => (
                <div key={i}>
                  <span>PC{i + 1}</span>
                  <i style={{ width: v / c.total * 100 + "%" }} />
                  <strong>{f(v, 3)}</strong>
                </div>
              ))}
            </div>
          )}
        <div className="metrics">
          <Metric label="PC1 variance" value="6" />
          <Metric label="Total variance" value="6.667" />
        </div>
      </>,
    );
  }
  if (s.scene === "reconstruction") {
    return split(
      <>
        {geo(n === 51 || n === 52 ? "triangle" : "decode", false, { keep })}
        {n === 51 || n === 52 ? angleControl : (
          <div className="preset-row">
            {[0, 1, 2].map((k) => (
              <button
                key={k}
                aria-pressed={keep === k}
                onClick={() => {
                  setKeep(k);
                  setAngle(45);
                }}
              >
                Keep {k} {k === 1 ? "component" : "components"}
              </button>
            ))}
          </div>
        )}
      </>,
      <>
        {eq}
        {n === 51 || n === 52
          ? (
            <div className="triangle-ledger">
              <span>
                Original² <strong>{f(frame.lengths[p])}</strong>
              </span>
              <span>
                Kept² <strong>{f(frame.kept[p])}</strong>
              </span>
              <span>
                Lost² <strong>{f(frame.lost[p])}</strong>
              </span>
            </div>
          )
          : (
            <div className="metrics">
              <Metric
                label={`${names[p]} · original`}
                value={`(${c.raw[p].join(", ")})`}
              />
              <Metric
                label={`${names[p]} · reconstructed`}
                value={`(${
                  c.recon[keep].raw[p].map((v) => f(v, 1)).join(", ")
                })`}
              />
            </div>
          )}
        {n === 54 && (
          <>
            <Slider
              label="Required retained variance (%)"
              min={1}
              max={100}
              value={weight}
              onChange={setWeight}
            />
            <p>
              {keep === 0 ? 0 : keep === 1 ? 90 : 100}% retained.{" "}
              {((keep === 0 ? 0 : keep === 1 ? 90 : 100) >= weight)
                ? "This meets the target."
                : "This does not meet the target."}
            </p>
          </>
        )}
        <p>
          {n === 52
            ? "The total is fixed for this dataset. Increasing the kept sum reduces the lost sum by the same amount."
            : `With ${keep} retained components, the normalized squared error is ${
              f(c.recon[keep].totalLoss, 3)
            }.`}
        </p>
      </>,
    );
  }
  if (s.scene === "spectrum") {
    return split(
      <>{eq}</>,
      <>
        <p className="small-label">A SECOND EXAMPLE · FOUR-FEATURE SPECTRUM</p>
        <div className="spectrum-bars">
          {[6, 2, .9, .1].map((v, i) => (
            <button
              key={i}
              aria-pressed={i < keep}
              onClick={() => setKeep(i + 1)}
            >
              <span>PC{i + 1}</span>
              <i
                style={{ width: v / 6 * 70 + "%", opacity: i < keep ? 1 : .2 }}
              />
              <strong>{v}</strong>
            </button>
          ))}
        </div>
        <Slider
          label="Components to keep"
          min={1}
          max={4}
          value={keep}
          onChange={setKeep}
        />
        <Metric
          label="Variance retained in this spectrum"
          value={f(
            [6, 2, .9, .1].slice(0, keep).reduce((a, b) => a + b, 0) / 9 * 100,
            1,
          ) + "%"}
        />
        <p>
          Select a bar to keep that component and every component above it. The
          largest eigenvalues use the variance budget most efficiently.
        </p>
      </>,
      "proof-layout",
    );
  }
  if (s.scene === "newpoint") {
    const z = (newX - 6) * c.axes[0][0] + (newY - 6) * c.axes[0][1];
    return split(
      <>
        {geo("shadow", false, { newPoint: [newX - 6, newY - 6] })}
        <Slider
          label="New observation x"
          min={0}
          max={12}
          value={newX}
          onChange={setNewX}
        />
        <Slider
          label="New observation y"
          min={0}
          max={12}
          value={newY}
          onChange={setNewY}
        />
      </>,
      <>
        {eq}
        <Metric label="New PC1 score" value={f(z, 3)} />
        <p>
          The training center stays (6,6). The learned direction stays at 45°.
          Only the new score changes.
        </p>
        <Eq
          tex={`\\widehat r_{new}=(${f(6 + z * c.axes[0][0])},${
            f(6 + z * c.axes[0][1])
          })`}
        />
      </>,
    );
  }
  if (s.scene === "units") {
    return split(
      <>
        {geo("shadow")}
        <Slider
          label="Multiply the second feature by"
          min={1}
          max={10}
          value={scale + 1}
          onChange={(v) => {
            setScale(v - 1);
          }}
        />
        <button aria-pressed={standard} onClick={() => setStandard(!standard)}>
          {standard ? "Standardization on" : "Standardization off"}
        </button>
      </>,
      <>
        {eq}
        <Metric label="Computed PC1 angle" value={f(c.angle, 1) + "°"} />
        <Covariance c={c} entry={entry} setEntry={setEntry} />
        <p>
          Standardization removes the numerical unit difference. It also changes
          the relative importance of the features.
        </p>
      </>,
    );
  }
  if (s.scene === "outliers" || s.scene === "ring") {
    return split(
      <>
        {geo("shadow", false, { categories: n === 59 && variant === 2 })}
        {angleControl}
        {n === 59 && (
          <div className="preset-row">
            {["Original cloud", "Distant observation", "Label contrast"].map((
              v,
              i,
            ) => (
              <button
                key={v}
                aria-pressed={variant === i}
                onClick={() => {
                  setVariant(i);
                  setPerson(0);
                }}
              >
                {v}
              </button>
            ))}
          </div>
        )}
      </>,
      <>
        <p className="big-idea">{s.claim}</p>
        {metrics}
        <Metric label="Computed best direction" value={f(c.angle, 1) + "°"} />
        {variant === 2 && n === 59 && (
          <p>
            In this example, the labels depend on the vertical sign. The
            dominant horizontal variation hides that distinction after
            compression.
          </p>
        )}
        <p>
          {n === 60
            ? "Every direction of this ring has the same variance. A single line cannot preserve its circular layout."
            : "Inspect which observations create the squared spread. High variance alone does not establish a useful representation."}
        </p>
      </>,
    );
  }
  if (s.scene === "notebook") {
    return split(
      <>{geo("shadow")}{angleControl}</>,
      <>
        <p className="big-idea">Change an observation. Recompute the model.</p>
        <div className="native-controls">
          <marimo-cell name="masterclass_controls" />
        </div>
        <div className="metrics">
          <Metric
            label="Mean from Python"
            value={`(${c.mean.map((v) => f(v, 2)).join(", ")})`}
          />
          <Metric label="PC1 from Python" value={f(c.angle, 1) + "°"} />
        </div>
        <p>
          The notebook recalculates S and its eigenvectors after each change.
          The illustration receives those new results.
        </p>
        <button onClick={() => setAngle(Math.round(c.angle))}>
          Use the new PC1
        </button>
      </>,
    );
  }
  if (s.scene === "challenge") {
    return split(
      <>{geo("shadow")}{angleControl}</>,
      <>
        <p className="big-idea">Choose a direction for this new cloud.</p>
        <p>
          Find the largest spread. State why your direction is useful before
          checking it.
        </p>
        <label className="text-label">
          Your reason<textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
          />
        </label>
        <button
          className="accent"
          disabled={!note.trim()}
          onClick={() => setSent(true)}
        >
          Check this direction
        </button>
        {sent && (
          <div role="status">
            <Metric
              label="Your retained variance"
              value={f(frame.ratio * 100, 1) + "%"}
            />
            <Metric
              label="Maximum retained variance"
              value={f(c.ratio * 100, 1) + "%"}
            />
            <p>
              The computed PC1 is{" "}
              {f(c.angle, 1)}°. Your written reason needs a separate review.
            </p>
          </div>
        )}
      </>,
    );
  }
  if (s.scene === "exam") {
    return (
      <div className="exam-layout">
        <div>
          <p className="small-label">FRESH DATA · MEAN ALREADY REMOVED</p>
          <Eq
            tex={String
              .raw`X_c=\begin{bmatrix}3&1\\1&3\\-1&-3\\-3&-1\end{bmatrix}`}
          />
          <p>
            Complete the calculation before opening the explanation. The sample
            divisor is three.
          </p>
          <div className="vertical-controls">
            {["Covariance entry", "Projection score", "Reconstruction"].map((
              v,
              i,
            ) => (
              <button
                key={v}
                aria-pressed={phase === i}
                onClick={() => setPhase(i)}
              >
                {v}
              </button>
            ))}
          </div>
        </div>
        <Check
          key={phase}
          prompt={[
            "Calculate the covariance between the two columns.",
            "For the first point, calculate the score on (1,1)/√2.",
            "Keep that one score. What is the reconstructed first coordinate?",
          ][phase]}
          answer={[4, 4 / Math.sqrt(2), 2][phase]}
          explain={[
            "The products are 3, 3, 3, and 3. Their sum is 12. Divide by three to get 4.",
            "The weighted sum is 3/√2 + 1/√2 = 4/√2.",
            "Multiply the score 4/√2 by the first direction weight 1/√2. The result is 2.",
          ][phase]}
        />
      </div>
    );
  }
  return (
    <div className="teachback">
      <p className="big-idea">Explain the complete argument.</p>
      <ol>
        <li>What does PCA preserve, and what can it lose?</li>
        <li>Why does covariance appear in the variance of a score?</li>
        <li>Why does the largest eigenvalue give a global maximum?</li>
        <li>Why does the same choice minimize squared reconstruction error?</li>
        <li>When can this choice be unsuitable?</li>
      </ol>
      <label>
        Your explanation<textarea
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          rows={5}
        />
      </label>
      <button
        className="accent"
        disabled={!answer.trim()}
        onClick={() => setSent(true)}
      >
        Keep this explanation on the slide
      </button>
      {sent && (
        <p role="status">
          Your explanation is present below. Review the reasoning with a tutor
          or against the proof. No automatic mastery score is assigned.
        </p>
      )}
      {sent && <blockquote>{answer}</blockquote>}
    </div>
  );
}
