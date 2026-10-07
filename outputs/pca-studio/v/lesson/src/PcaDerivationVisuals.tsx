import { useId, useState } from "react";
import { type Case, Eq, f, type Point } from "./LabComponents.tsx";
import "./derivation.css";

const GREEN = "#176a53", ORANGE = "#bc562c", INK = "#203d35", GREY = "#71817a";
const dot = (a: Point, b: Point) => a[0] * b[0] + a[1] * b[1];
const times = (v: Point, s: number): Point => [v[0] * s, v[1] * s];
const add = (a: Point, b: Point): Point => [a[0] + b[0], a[1] + b[1]];
const direction = (degrees: number): Point => {
  const r = degrees * Math.PI / 180;
  return [Math.cos(r), Math.sin(r)];
};
const multiply = (c: Case, w: Point): Point => [
  c.cov[0][0] * w[0] + c.cov[0][1] * w[1],
  c.cov[1][0] * w[0] + c.cov[1][1] * w[1],
];
const variance = (c: Case, w: Point) => dot(w, multiply(c, w));

function LabRange({ label, value, onChange, min, max, step = 1, suffix = "" }: {
  label: string;
  value: number;
  onChange: (v: number) => void;
  min: number;
  max: number;
  step?: number;
  suffix?: string;
}) {
  return (
    <label className="derivation-range">
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
        onChange={(e) => onChange(+e.target.value)}
      />
    </label>
  );
}

function Arrow({ from, to, color, marker, dashed = false, width = 3 }: {
  from: Point;
  to: Point;
  color: string;
  marker: string;
  dashed?: boolean;
  width?: number;
}) {
  if (Math.hypot(to[0] - from[0], to[1] - from[1]) < .6) return null;
  return (
    <line
      x1={from[0]}
      y1={from[1]}
      x2={to[0]}
      y2={to[1]}
      stroke={color}
      strokeWidth={width}
      strokeDasharray={dashed ? "5 4" : undefined}
      markerEnd={`url(#${marker})`}
    />
  );
}

function Markers({ id }: { id: string }) {
  return (
    <defs>
      {[["green", GREEN], ["orange", ORANGE], ["ink", INK]].map((
        [name, color],
      ) => (
        <marker
          key={name}
          id={`${id}-${name}`}
          viewBox="0 0 8 8"
          refX="7"
          refY="4"
          markerWidth="6"
          markerHeight="6"
          orient="auto-start-reverse"
        >
          <path d="M0,0 L8,4 L0,8 Z" fill={color} />
        </marker>
      ))}
    </defs>
  );
}

/** Match a feature row to a feature column, accumulate, then divide. */
export function CovarianceProductLab({ c, entry, onEntryChange }: {
  c: Case;
  entry?: number;
  onEntryChange?: (entry: number) => void;
}) {
  const [localEntry, setLocalEntry] = useState(1);
  const [phase, setPhase] = useState(0);
  const chosen = entry ?? localEntry;
  const row = Math.floor(chosen / 2), col = chosen % 2;
  const products = c.points.map((p) => p[row] * p[col]);
  const count = Math.min(phase, c.n), divided = phase > c.n;
  const running = products.slice(0, count).reduce((a, b) => a + b, 0);
  const select = (i: number) => {
    setLocalEntry(i);
    onEntryChange?.(i);
    setPhase(0);
  };
  const names = c.points.map((_, i) => String.fromCharCode(65 + i));
  return (
    <div
      role="region"
      className="derivation-lab covariance-product-lab"
      aria-label="Build a covariance entry"
    >
      <div className="derivation-kicker">
        ONE ENTRY · ONE ROW MEETS ONE COLUMN
      </div>
      <div className="derivation-matrices">
        <div>
          <div className="derivation-matrix-title">
            Centered data X<sub>c</sub>
          </div>
          <div
            className="derivation-data-table"
            style={{ gridTemplateColumns: "25px repeat(2, 1fr)" }}
          >
            <small></small>
            <small>a</small>
            <small>b</small>
            {c.points.map((p, i) => (
              <div className="derivation-matrix-row" key={i}>
                <small>{names[i]}</small>
                {p.map((v, j) => (
                  <span
                    key={j}
                    className={`${j === col ? "column-selected" : ""} ${
                      i < count ? "product-counted" : ""
                    }`}
                  >
                    {f(v, 0)}
                  </span>
                ))}
              </div>
            ))}
          </div>
        </div>
        <div className="derivation-transpose-group">
          <div className="derivation-matrix-title">
            Transpose X<sub>c</sub>
            <sup>T</sup>
          </div>
          <div
            className="derivation-transpose-table"
            style={{ gridTemplateColumns: `repeat(${c.n}, 1fr)` }}
          >
            {[0, 1].map((j) =>
              c.points.map((p, i) => (
                <span
                  key={`${j}-${i}`}
                  className={`${j === row ? "row-selected" : ""} ${
                    i < count && j === row ? "product-counted" : ""
                  }`}
                >
                  {f(p[j], 0)}
                </span>
              ))
            )}
          </div>
          <p className="derivation-matrix-note">
            Feature {row ? "b" : "a"} becomes a row.<br />Pair it with feature
            {" "}
            {col ? "b" : "a"}.
          </p>
        </div>
        <div>
          <div className="derivation-matrix-title">Choose an entry of S</div>
          <div className="derivation-entry-grid">
            {c.cov.flat().map((v, i) => (
              <button
                key={i}
                aria-label={`Select covariance entry ${
                  Math.floor(i / 2) + 1
                }, ${i % 2 + 1}`}
                aria-pressed={chosen === i}
                onClick={() => select(i)}
              >
                <small>S{Math.floor(i / 2) + 1}{i % 2 + 1}</small>
                <strong>{chosen === i && !divided ? "?" : f(v, 2)}</strong>
              </button>
            ))}
          </div>
        </div>
      </div>
      <div
        className="derivation-products"
        style={{ gridTemplateColumns: `repeat(${c.n}, 1fr)` }}
      >
        {products.map((product, i) => (
          <button
            key={i}
            aria-label={`Accumulate through observation ${names[i]}`}
            aria-pressed={i < count}
            onClick={() => setPhase(i + 1)}
          >
            <small>{names[i]}</small>
            <span>
              <em>{f(c.points[i][row], 0)}</em> ×{" "}
              <b>{f(c.points[i][col], 0)}</b>
            </span>
            <strong>{i < count ? f(product, 0) : "·"}</strong>
          </button>
        ))}
      </div>
      <div className="derivation-accumulator" aria-live="polite">
        <div>
          <small>
            {divided
              ? "Divide the complete sum"
              : `${count} of ${c.n} products added`}
          </small>
          <strong>
            {divided
              ? `${f(running, 0)} ÷ ${c.n - 1} = ${f(running / (c.n - 1), 3)}`
              : f(running, 0)}
          </strong>
        </div>
        <p>
          {divided
            ? `This number goes in S${row + 1}${col + 1}. The divisor is ${
              c.n - 1
            } because there are ${c.n} observations.`
            : count === 0
            ? "Multiply matching entries for A. Then repeat for the other observations."
            : count === c.n
            ? "Every pair has contributed. Now divide the sum by n−1."
            : `The two highlighted feature values from ${
              names[count - 1]
            } contribute ${f(products[count - 1], 0)}.`}
        </p>
      </div>
      <div className="derivation-buttons">
        <button onClick={() => setPhase(0)} disabled={phase === 0}>
          Reset sum
        </button>
        <button
          className="derivation-primary"
          disabled={divided}
          onClick={() => setPhase(Math.min(phase + 1, c.n + 1))}
        >
          {count < c.n
            ? `Add ${names[count]}'s product →`
            : divided
            ? "Entry complete"
            : `Divide by ${c.n - 1} →`}
        </button>
      </div>
      <Eq
        tex={String.raw`S_{${row + 1}${col + 1}}=\frac{\sum_i x_{i,${
          row + 1
        }}x_{i,${col + 1}}}{n-1}`}
      />
    </div>
  );
}

/** Local turning gain, with coordinate and derivative scales kept explicit. */
export function StationarityLab({ c, angle, setAngle }: {
  c: Case;
  angle: number;
  setAngle: (angle: number) => void;
}) {
  const id = "station-" + useId().replaceAll(":", "");
  const [turn, setTurn] = useState(3);
  const w = direction(angle), tangent: Point = [-w[1], w[0]];
  const sw = multiply(c, w), gradient = times(sw, 2);
  const radialAmount = dot(gradient, w), tangentAmount = dot(gradient, tangent);
  const radial = times(w, radialAmount),
    tangential = times(tangent, tangentAmount);
  const turned = direction(angle + turn);
  const delta = variance(c, turned) - variance(c, w);
  const predicted = tangentAmount * turn * Math.PI / 180;
  const stationary = Math.abs(tangentAmount) < 1e-7;
  const maxMagnitude = Math.max(1, 2 * c.values[0]);
  const left = (p: Point): Point => [139 + p[0] * 87, 144 - p[1] * 87];
  const right = (
    p: Point,
  ): Point => [423 + p[0] * 84 / maxMagnitude, 144 - p[1] * 84 / maxMagnitude];
  const start = left(w), zero = right([0, 0]);
  const slopeText = stationary
    ? "No first-order gain from turning"
    : tangentAmount > 0
    ? "A small counterclockwise turn increases variance"
    : "A small clockwise turn increases variance";
  return (
    <div
      role="region"
      className="derivation-lab stationarity-lab"
      aria-label="Why stationary directions are eigenvectors"
    >
      <div className="derivation-kicker">ALLOWED MOTION IS A TURN</div>
      <div className="stationarity-body">
        <div className="stationarity-chart">
          <svg
            viewBox="0 0 568 270"
            role="img"
            aria-label="Unit direction on a circle and the radial and tangent parts of its variance gradient"
          >
            <Markers id={id} />
            <text
              x="139"
              y="20"
              textAnchor="middle"
              className="derivation-svg-heading"
            >
              Direction space
            </text>
            <text
              x="423"
              y="20"
              textAnchor="middle"
              className="derivation-svg-heading"
            >
              Gradient g = 2Sw
            </text>
            <line x1="280" y1="37" x2="280" y2="245" stroke="#d2ddd5" />
            <circle cx="139" cy="144" r="87" fill="#edf4ed" stroke="#a9bfb0" />
            <line x1="35" y1="144" x2="245" y2="144" stroke="#d2ddd5" />
            <line x1="139" y1="39" x2="139" y2="246" stroke="#d2ddd5" />
            <Arrow
              from={left([0, 0])}
              to={start}
              color={GREEN}
              marker={`${id}-green`}
              width={4}
            />
            <line
              x1={left(add(w, times(tangent, -.55)))[0]}
              y1={left(add(w, times(tangent, -.55)))[1]}
              x2={left(add(w, times(tangent, .55)))[0]}
              y2={left(add(w, times(tangent, .55)))[1]}
              stroke={ORANGE}
              strokeWidth="2"
              strokeDasharray="4 4"
            />
            <Arrow
              from={start}
              to={left(add(w, times(tangent, .45)))}
              color={ORANGE}
              marker={`${id}-orange`}
            />
            <circle
              cx={left(turned)[0]}
              cy={left(turned)[1]}
              r="5"
              fill={ORANGE}
            />
            <circle cx={start[0]} cy={start[1]} r="5" fill={GREEN} />
            <text x={left(times(w, .6))[0] + 8} y={left(times(w, .6))[1] - 6}>
              w
            </text>
            <text
              x={left(add(w, times(tangent, .45)))[0] + 9}
              y={left(add(w, times(tangent, .45)))[1] - 7}
            >
              t
            </text>
            <text x="139" y="259" textAnchor="middle">Circle radius = 1</text>
            <circle
              cx="423"
              cy="144"
              r="84"
              fill="none"
              stroke="#d2ddd5"
              strokeDasharray="3 4"
            />
            <line
              x1={right(times(w, -maxMagnitude))[0]}
              y1={right(times(w, -maxMagnitude))[1]}
              x2={right(times(w, maxMagnitude))[0]}
              y2={right(times(w, maxMagnitude))[1]}
              stroke="#afc7b7"
            />
            <Arrow
              from={zero}
              to={right(gradient)}
              color={INK}
              marker={`${id}-ink`}
              width={4}
            />
            <Arrow
              from={zero}
              to={right(radial)}
              color={GREEN}
              marker={`${id}-green`}
              width={3}
            />
            <Arrow
              from={right(radial)}
              to={right(add(radial, tangential))}
              color={ORANGE}
              marker={`${id}-orange`}
              width={3}
            />
            <circle cx={zero[0]} cy={zero[1]} r="3" fill={INK} />
            <text x={right(gradient)[0] + 9} y={right(gradient)[1] - 7}>g</text>
            <text x="423" y="259" textAnchor="middle">
              Dashed radius = {f(maxMagnitude, 1)} slope units
            </text>
          </svg>
          <div className="derivation-legend">
            <span>
              <i style={{ background: GREEN }} />radial: {f(radialAmount, 3)}
            </span>
            <span>
              <i style={{ background: ORANGE }} />tangent: {f(tangentAmount, 3)}
            </span>
          </div>
          <p className="derivation-scale-note">
            The gradient and both parts use the same scale in the right panel.
            The left panel shows unit directions.
          </p>
        </div>
        <div className="stationarity-controls">
          <LabRange
            label="Candidate direction"
            min={0}
            max={180}
            value={((angle % 180) + 180) % 180}
            onChange={setAngle}
            suffix="°"
          />
          <div className="derivation-buttons">
            <button onClick={() => setAngle(c.angle)}>
              Largest-variance direction
            </button>
            <button onClick={() => setAngle((c.angle + 90) % 180)}>
              Other stationary direction
            </button>
            <button onClick={() => setAngle(20)}>Try 20°</button>
          </div>
          <LabRange
            label="Small signed turn"
            min={-8}
            max={8}
            step={.5}
            value={turn}
            onChange={setTurn}
            suffix="°"
          />
          <div className="derivation-deltas">
            <div>
              <small>First-order prediction</small>
              <strong>{f(predicted, 4)}</strong>
            </div>
            <div>
              <small>Actual variance change</small>
              <strong>{f(delta, 4)}</strong>
            </div>
          </div>
          <p className="derivation-conclusion">
            {slopeText}. {stationary
              ? "A zero slope can be a maximum or a minimum. The finite-turn change still need not be zero."
              : "Make the turn smaller to compare the local prediction with the actual change."}
          </p>
          <Eq
            tex={String
              .raw`\Delta V\approx (2t^\top Sw)\,\Delta\theta\quad\text{(angle in radians)}`}
          />
        </div>
      </div>
    </div>
  );
}

/** Full-circle signed coordinates, followed by their nonnegative squared weights. */
export function EigenbasisLab({ c, angle, setAngle }: {
  c: Case;
  angle: number;
  setAngle: (angle: number) => void;
}) {
  const id = "basis-" + useId().replaceAll(":", "");
  const w = direction(angle), q1 = c.axes[0], q2 = c.axes[1];
  const a = dot(w, q1), b = dot(w, q2);
  const aq = times(q1, a), bq = times(q2, b);
  const first = c.values[0] * a * a, second = c.values[1] * b * b;
  const v = first + second, bound = c.values[0], denom = Math.max(bound, 1e-12);
  const xy = (p: Point): Point => [148 + p[0] * 91, 145 - p[1] * 91];
  const label = (q: Point, name: string, color: string) => (
    <text
      x={xy(times(q, 1.23))[0]}
      y={xy(times(q, 1.23))[1]}
      fill={color}
      textAnchor="middle"
    >
      {name}
    </text>
  );
  const circleAngle = ((angle % 360) + 360) % 360;
  return (
    <div
      role="region"
      className="derivation-lab eigenbasis-lab"
      aria-label="Prove the global variance bound"
    >
      <div className="derivation-kicker">
        ANY DIRECTION · TWO SIGNED COORDINATES
      </div>
      <div className="derivation-basis-top">
        <svg
          viewBox="0 0 296 280"
          role="img"
          aria-label="A unit vector decomposed along both eigenvector axes"
        >
          <Markers id={id} />
          <circle cx="148" cy="145" r="91" fill="#edf4ed" stroke="#a9bfb0" />
          {[q1, q2].map((q, i) => (
            <line
              key={i}
              x1={xy(times(q, -1.18))[0]}
              y1={xy(times(q, -1.18))[1]}
              x2={xy(times(q, 1.18))[0]}
              y2={xy(times(q, 1.18))[1]}
              stroke={i ? ORANGE : GREEN}
              strokeWidth="1.4"
            />
          ))}
          {label(q1, "q₁", GREEN)}
          {label(q2, "q₂", ORANGE)}
          <Arrow
            from={xy([0, 0])}
            to={xy(aq)}
            color={GREEN}
            marker={`${id}-green`}
            width={5}
          />
          <Arrow
            from={xy(aq)}
            to={xy(add(aq, bq))}
            color={ORANGE}
            marker={`${id}-orange`}
            width={4}
          />
          <Arrow
            from={xy([0, 0])}
            to={xy(w)}
            color={INK}
            marker={`${id}-ink`}
            width={2}
          />
          <line
            x1={xy(bq)[0]}
            y1={xy(bq)[1]}
            x2={xy(w)[0]}
            y2={xy(w)[1]}
            stroke={GREEN}
            strokeDasharray="4 4"
          />
          <circle cx={xy(w)[0]} cy={xy(w)[1]} r="5" fill={INK} />
          <text x={xy(w)[0] + 10} y={xy(w)[1] - 7}>w</text>
          <text x="148" y="269" textAnchor="middle">
            w has length 1 at every angle
          </text>
        </svg>
        <div className="derivation-coefficients">
          <div>
            <small>Along q₁</small>
            <strong className="derivation-green">a = {f(a, 3)}</strong>
          </div>
          <div>
            <small>Along q₂</small>
            <strong className="derivation-orange">b = {f(b, 3)}</strong>
          </div>
          <p>
            The signs select the sides of the axes. Squaring removes those
            signs.
          </p>
          <Eq tex={String.raw`w=aq_1+bq_2`} />
        </div>
      </div>
      <LabRange
        label="Direction around the full circle"
        min={0}
        max={359}
        value={circleAngle}
        onChange={setAngle}
        suffix="°"
      />
      <div className="derivation-buttons">
        <button onClick={() => setAngle(c.angle)}>Use q₁</button>
        <button onClick={() => setAngle((c.angle + 90) % 360)}>
          Use the other axis
        </button>
        <button onClick={() => setAngle((circleAngle + 180) % 360)}>
          Reverse w
        </button>
      </div>
      <div
        className="derivation-weight-bar"
        aria-label="Squared weights sum to one"
      >
        <span style={{ width: a * a * 100 + "%" }} />
        <b style={{ width: b * b * 100 + "%" }} />
      </div>
      <div className="derivation-weight-labels">
        <span>a² = {f(a * a, 3)}</span>
        <strong>Total = 1</strong>
        <span>b² = {f(b * b, 3)}</span>
      </div>
      <div className="derivation-bound-plot">
        <div className="derivation-bound-track">
          <span style={{ width: first / denom * 100 + "%" }} />
          <b style={{ width: second / denom * 100 + "%" }} />
        </div>
        <div className="derivation-bound-labels">
          <span>Variance = {f(v, 3)}</span>
          <strong>Upper bound λ₁ = {f(bound, 3)}</strong>
        </div>
      </div>
      <Eq
        tex={String.raw`V=${f(c.values[0], 3)}a^2+${f(c.values[1], 3)}b^2\leq${
          f(bound, 3)
        }(a^2+b^2)=${f(bound, 3)}`}
      />
      <p className="derivation-conclusion">
        {Math.abs(c.values[0] - c.values[1]) < 1e-7
          ? "The eigenvalues tie. Every allocation reaches the same bound."
          : "The squared weights are nonnegative and sum to one. Put all the weight on the larger eigenvalue to reach the bound."}
      </p>
    </div>
  );
}
