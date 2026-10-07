import { useState } from "react";
// @deno-types="npm:@types/katex@0.16.7"
import katex from "katex";
import { dot, fixed, model, type Point, RAW } from "./math.ts";
import type { Scene } from "./course.ts";
import { Center, ExplainBack, Proof } from "./LearningVisuals.tsx";
import { PracticalVisual } from "./PracticalVisuals.tsx";
export function MathText({ tex }: { tex: string }) {
  return (
    <span
      className="math"
      dangerouslySetInnerHTML={{
        __html: katex.renderToString(tex, {
          throwOnError: false,
          displayMode: true,
        }),
      }}
    />
  );
}
const colors = ["#167c80", "#8a53b2", "#bd661c", "#3754bd"];
export function Plot({
  raw = RAW,
  angle = 45,
  selected = 0,
  onSelect,
  showRaw = false,
  triangle = false,
}: {
  raw?: Point[];
  angle?: number;
  selected?: number;
  onSelect?: (i: number) => void;
  showRaw?: boolean;
  triangle?: boolean;
}) {
  const m = model(raw, angle),
    ps = showRaw ? raw : m.points,
    origin = showRaw ? m.mean : [0, 0] as Point;
  const extent = Math.max(3, ...m.points.flat().map(Math.abs)) * 1.35,
    scale = 165 / extent;
  const xy = (
    p: Point,
  ): Point => [
    225 + (p[0] - origin[0]) * scale,
    205 - (p[1] - origin[1]) * scale,
  ];
  const at = (p: Point) =>
    xy(showRaw ? [p[0] + m.mean[0], p[1] + m.mean[1]] : p);
  const [cx, cy] = xy(origin),
    end1 = at([-m.w[0] * extent * 1.18, -m.w[1] * extent * 1.18]),
    end2 = at([m.w[0] * extent * 1.18, m.w[1] * extent * 1.18]);
  return (
    <svg
      viewBox="0 0 450 435"
      className="plot"
      role="img"
      aria-label={`Point cloud and projection onto a ruler at ${angle} degrees. Filled dots are observations. Hollow dots are reconstructions.`}
    >
      <defs>
        <pattern
          id="grid"
          width={scale}
          height={scale}
          patternUnits="userSpaceOnUse"
          x={cx}
          y={cy}
        >
          <path
            d={`M ${scale} 0 L 0 0 0 ${scale}`}
            fill="none"
            stroke="#dfe7e7"
            strokeWidth=".7"
          />
        </pattern>
      </defs>
      <rect x="20" y="15" width="410" height="380" fill="url(#grid)" />
      <line x1="22" y1={cy} x2="425" y2={cy} stroke="#a7b6ba" />
      <line x1={cx} y1="15" x2={cx} y2="395" stroke="#a7b6ba" />
      <text x="420" y={cy + 18} textAnchor="end" className="axis-label">
        {showRaw ? "east (cm)" : "centered east (cm)"}
      </text>
      <text x={cx + 9} y="26" className="axis-label">
        {showRaw ? "north (cm)" : "north − mean (cm)"}
      </text>
      <line
        x1={end1[0]}
        y1={end1[1]}
        x2={end2[0]}
        y2={end2[1]}
        stroke="#167c80"
        strokeWidth="3"
      />
      <circle cx={cx} cy={cy} r="4" fill="#162c36" />
      <text x={cx + 8} y={cy - 9} className="axis-label">
        {showRaw ? "mean (6, 6)" : "0"}
      </text>
      {ps.map((p, i) => {
        const a = xy(p), b = at(m.reconstructed[i]);
        return (
          <g key={i} opacity={triangle && i !== selected ? .2 : 1}>
            <line
              x1={a[0]}
              y1={a[1]}
              x2={b[0]}
              y2={b[1]}
              stroke="#ce7650"
              strokeWidth={i === selected ? 3 : 1.5}
              strokeDasharray="5 4"
            />
            {triangle && i === selected && (
              <>
                <line
                  x1={cx}
                  y1={cy}
                  x2={a[0]}
                  y2={a[1]}
                  stroke="#344853"
                  strokeWidth="2"
                />
                <line
                  x1={cx}
                  y1={cy}
                  x2={b[0]}
                  y2={b[1]}
                  stroke="#167c80"
                  strokeWidth="5"
                />
              </>
            )}
            <circle
              cx={b[0]}
              cy={b[1]}
              r="6"
              fill="#fbfcf7"
              stroke="#167c80"
              strokeWidth="2"
            />
            <circle
              cx={a[0]}
              cy={a[1]}
              r={i === selected ? 8 : 6}
              fill={colors[i % 4]}
              stroke="#fff"
              strokeWidth="2"
              onClick={() => onSelect?.(i)}
            />
            <text
              x={a[0] + 11}
              y={a[1] - 8}
              fill={colors[i % 4]}
              fontWeight="700"
            >
              {String.fromCharCode(65 + i)}
            </text>
          </g>
        );
      })}
      <text x="24" y="420" className="axis-label">● original point</text>
      <text x="175" y="420" className="axis-label">○ recovered point</text>
      <text x="335" y="420" className="axis-label">┄ lost detail</text>
    </svg>
  );
}
function Range(
  { label, value, set, min = 0, max = 180, step = 1 }: {
    label: string;
    value: number;
    set: (n: number) => void;
    min?: number;
    max?: number;
    step?: number;
  },
) {
  return (
    <label className="range">
      <span>
        {label}
        <strong>{value}{max === 180 ? "°" : ""}</strong>
      </span>
      <input
        aria-label={label}
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => set(Number(e.target.value))}
      />
    </label>
  );
}
export function Geometry({ s, raw = RAW }: { s: Scene; raw?: Point[] }) {
  const [angle, set] = useState(s.angle ?? 45),
    [selected, select] = useState(0),
    [reveal, see] = useState(false);
  const m = model(raw, angle), p = m.points[selected], z = m.scores[selected];
  return (
    <div className="experiment">
      <div className="plot-row">
        <Plot
          raw={raw}
          angle={angle}
          selected={selected}
          onSelect={select}
          showRaw={s.mode === "raw"}
          triangle={s.kind === "triangle"}
        />
        <div className="instrument">
          <p className="eyebrow">ONE SHARED RULER</p>
          <div className="metric">
            <span>
              {s.chapter === 0 ? "Kept squared detail" : "Kept variance"}
            </span>
            <strong>{fixed(m.variance)}</strong>
            <small>cm² along the line</small>
          </div>
          <div className="metric lost">
            <span>
              {s.chapter === 0 ? "Lost squared detail" : "Lost variance"}
            </span>
            <strong>{fixed(m.loss)}</strong>
            <small>cm² sideways</small>
          </div>
          <div className="sum">
            Total <b>{fixed(m.total)} cm²</b>
          </div>
          <div className="energy">
            <i style={{ width: `${m.variance / m.total * 100}%` }} />
          </div>
          <p className="caption">
            {s.chapter === 0
              ? "Squared distances, divided by 3. We will earn this measure in chapter 2."
              : "Same points. Same total. Only the split changes."}
          </p>
        </div>
      </div>
      <div className="control-row">
        <Range label="Ruler angle" value={angle} set={set} />
        <button
          onClick={() => {
            set(s.angle ?? 45);
            select(0);
            see(false);
          }}
        >
          Reset
        </button>
      </div>
      <div className="presets">
        {[0, 45, 90, 135].map((a) => (
          <button
            key={a}
            aria-pressed={angle === a}
            onClick={() => set(a)}
          >
            {a}°
          </button>
        ))}
        <span>Inspect a point</span>
        {raw.slice(0, 4).map((_, i) => (
          <button
            key={i}
            aria-pressed={i === selected}
            onClick={() => select(i)}
          >
            {String.fromCharCode(65 + i)}
          </button>
        ))}
      </div>
      {s.mode !== "raw" && (
        <div className="calculation">
          <span>
            Point {String.fromCharCode(65 + selected)}: ({fixed(p[0])},{" "}
            {fixed(p[1])})
          </span>
          <span>Score: {fixed(z)} cm</span>
          <span>Squared gap: {fixed(m.losses[selected])} cm²</span>
        </div>
      )}
      {s.mode === "predict" && (
        <>
          <button className="primary" onClick={() => see(!reveal)}>
            {reveal ? "Hide explanation" : "Compare with the optimum"}
          </button>
          {reveal && (
            <p className="feedback">
              The best direction is {fixed(m.bestAngle, 1)}°. Its variance is
              {" "}
              {fixed(m.eigenvalues[0])}. Your choice keeps{" "}
              {fixed(m.variance)}. The missing part is reconstruction loss, not
              automatically useless information.
            </p>
          )}
        </>
      )}
    </div>
  );
}
export function Covariance() {
  const [selected, select] = useState(0),
    [angle, set] = useState(45),
    [reveal, see] = useState(false),
    [negative, flip] = useState(false);
  const raw = negative ? RAW.map((p) => [p[0], 12 - p[1]] as Point) : RAW;
  const m = model(raw, angle), p = m.points[selected], a = m.w[0], b = m.w[1];
  return (
    <div className="experiment">
      <div className="cov-top">
        <Plot raw={raw} angle={angle} selected={selected} onSelect={select} />
        <div>
          <p className="eyebrow">BUILD THE SUMMARY</p>
          <table>
            <thead>
              <tr>
                <th>Dot</th>
                <th>x²</th>
                <th>xy</th>
                <th>y²</th>
              </tr>
            </thead>
            <tbody>
              {m.points.map((v, i) => (
                <tr
                  key={i}
                  className={i === selected ? "chosen" : ""}
                  onClick={() => {
                    select(i);
                    see(false);
                  }}
                >
                  <th>
                    <button
                      onClick={() => {
                        select(i);
                        see(false);
                      }}
                    >
                      {String.fromCharCode(65 + i)}
                    </button>
                  </th>
                  <td>{fixed(v[0] ** 2, 0)}</td>
                  <td>
                    {i === selected && !reveal ? "?" : fixed(v[0] * v[1], 0)}
                  </td>
                  <td>{fixed(v[1] ** 2, 0)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <button onClick={() => see(true)}>Reveal selected product</button>
          <p className="caption">
            For {String.fromCharCode(65 + selected)}: x = {p[0]}, y ={" "}
            {p[1]}. Multiply their signed offsets.
          </p>
          <MathText
            tex={String.raw`S=\frac{1}{3}\begin{bmatrix}10&${
              negative ? -8 : 8
            }\\${negative ? -8 : 8}&10\end{bmatrix}`}
          />
        </div>
      </div>
      <Range label="Ruler angle" value={angle} set={set} />
      <div className="term-bars">
        <div>
          <span>East term</span>
          <strong>{fixed(a * a * m.cov[0][0])}</strong>
        </div>
        <div>
          <span>Cross term</span>
          <strong>{fixed(2 * a * b * m.cov[0][1])}</strong>
        </div>
        <div>
          <span>North term</span>
          <strong>{fixed(b * b * m.cov[1][1])}</strong>
        </div>
        <div>
          <span>Score variance</span>
          <strong>{fixed(m.variance)}</strong>
        </div>
      </div>
      <button
        onClick={() => {
          flip(!negative);
          see(false);
        }}
      >
        Flip the tilt; keep both separate variances
      </button>
      <p className="caption">
        The diagonal entries stay 10/3. The covariance changes sign. The best
        ruler changes with it.
      </p>
    </div>
  );
}
export function Mixture() {
  const [weight, set] = useState(100), [tie, toggle] = useState(false);
  const l2 = tie ? 6 : 2 / 3, v = 6 * weight / 100 + l2 * (1 - weight / 100);
  return (
    <div className="experiment mixture">
      <p className="eyebrow">ALL UNIT DIRECTIONS · ONE BOUND</p>
      <div className="mixture-axes">
        <div>
          <span>q₁</span>
          <strong>6</strong>
          <small>first eigenvalue</small>
        </div>
        <div>
          <span>q₂</span>
          <strong>{fixed(l2)}</strong>
          <small>second eigenvalue</small>
        </div>
      </div>
      <Range
        label="Squared weight on q₁ (%)"
        value={weight}
        set={set}
        max={100}
      />
      <div className="weight-track">
        <i style={{ width: `${weight}%` }} />
        <b style={{ width: `${100 - weight}%` }} />
      </div>
      <p>{weight}% on q₁ + {100 - weight}% on q₂ = 100%</p>
      <MathText
        tex={String.raw`V=6\times${fixed(weight / 100)}+${
          tie ? "6" : String.raw`\tfrac23`
        }\times${fixed(1 - weight / 100)}=${fixed(v)}`}
      />
      <div className="bound">
        <span>Variance</span>
        <div>
          <i style={{ width: `${v / 6 * 100}%` }} />
        </div>
        <strong>{fixed(v)} ≤ 6</strong>
      </div>
      <p className="feedback">
        {tie
          ? "Both eigenvalues are 6. Every mixture is optimal. A best line exists, but it is not unique."
          : weight === 100
          ? "The upper bound is reached. All squared weight is on the top eigenvector."
          : "Moving weight to the smaller eigenvalue lowers the weighted average. This holds for every unit direction."}
      </p>
      <button onClick={() => toggle(!tie)}>
        {tie ? "Restore unequal eigenvalues" : "Make the eigenvalues equal"}
      </button>
      <p className="caption">
        The positive-coefficient direction is at{" "}
        {fixed(45 + Math.acos(Math.sqrt(weight / 100)) * 180 / Math.PI, 1)}° in
        the original plot: w = √p q₁ + √(1−p) q₂, with q₂ pointing at 135°.
        Weights are squared coefficients. The direction uses their square roots;
        changing a coefficient sign does not change its variance.
      </p>
    </div>
  );
}
export function Eigen() {
  const [angle, set] = useState(20);
  const m = model(RAW, angle),
    sw: Point = [dot(m.cov[0] as Point, m.w), dot(m.cov[1] as Point, m.w)],
    tangent: Point = [-m.w[1], m.w[0]],
    side = dot(sw, tangent);
  const scale = 28;
  return (
    <div className="experiment">
      <svg
        viewBox="0 0 460 320"
        role="img"
        aria-label="Direction w and transformed vector S w"
      >
        <line x1="230" y1="15" x2="230" y2="305" stroke="#ddd" />
        <line x1="15" y1="160" x2="445" y2="160" stroke="#ddd" />
        <circle
          cx="230"
          cy="160"
          r="85"
          fill="none"
          stroke="#bac9ca"
          strokeDasharray="4 5"
        />
        <line
          x1={230 + m.w[0] * 85 - tangent[0] * 55}
          y1={160 - m.w[1] * 85 + tangent[1] * 55}
          x2={230 + m.w[0] * 85 + tangent[0] * 55}
          y2={160 - m.w[1] * 85 - tangent[1] * 55}
          stroke="#8a53b2"
          strokeWidth="2"
          strokeDasharray="5 4"
        />
        <text
          x={230 + m.w[0] * 85 + tangent[0] * 58}
          y={160 - m.w[1] * 85 - tangent[1] * 58}
        >
          tangent
        </text>
        <line
          x1="230"
          y1="160"
          x2={230 + tangent[0] * side * scale}
          y2={160 - tangent[1] * side * scale}
          stroke="#8a53b2"
          strokeWidth="4"
        />
        <text x="20" y="310">Purple: sideways part of Sw</text>
        <line
          x1="230"
          y1="160"
          x2={230 + m.w[0] * 85}
          y2={160 - m.w[1] * 85}
          stroke="#167c80"
          strokeWidth="5"
        />
        <text x={240 + m.w[0] * 85} y={160 - m.w[1] * 85}>w (unit)</text>
        <line
          x1="230"
          y1="160"
          x2={230 + sw[0] * scale}
          y2={160 - sw[1] * scale}
          stroke="#b57921"
          strokeWidth="4"
        />
        <text x={240 + sw[0] * scale} y={160 - sw[1] * scale}>Sw</text>
      </svg>
      <Range label="Ruler angle" value={angle} set={set} />
      <div className="presets">
        {[20, 45, 90, 135].map((a) => (
          <button
            key={a}
            onClick={() => set(a)}
          >
            {a}°
          </button>
        ))}
      </div>
      <MathText
        tex={String.raw`\frac{dV}{d\theta}=2t^TSw=${fixed(2 * side)}`}
      />
      <p className="feedback">
        {Math.abs(side) < .001
          ? angle === 45
            ? "No sideways push at 45°. This eigenvector gives the maximum."
            : "No sideways push at 135°. This eigenvector gives the minimum! Stationarity alone cannot choose the winner."
          : side > 0
          ? "The sideways part is positive. A small increase in angle raises the variance."
          : "The sideways part is negative. A small decrease in angle raises the variance."}
      </p>
      <p className="caption">
        Derivative is per radian. The vectors share a direction at eigenvectors;
        their drawn lengths use separate labeled scales.
      </p>
    </div>
  );
}
export type Live = {
  angleDeg: number;
  raw: Point[];
  variance: number;
  loss: number;
  totalVariance: number;
  cov: number[][];
  w: Point[] | Point;
};
export function LiveLab({ live }: { live?: Live }) {
  return (
    <div className="experiment">
      <div className="native-controls">
        <marimo-cell name="sandbox_controls" />
      </div>
      {live
        ? (
          <>
            <Plot raw={live.raw} angle={live.angleDeg} />
            <div className="term-bars">
              <div>
                <span>Python kept</span>
                <strong>{fixed(live.variance)}</strong>
              </div>
              <div>
                <span>Python lost</span>
                <strong>{fixed(live.loss)}</strong>
              </div>
              <div>
                <span>Python total</span>
                <strong>{fixed(live.totalVariance)}</strong>
              </div>
            </div>
          </>
        )
        : (
          <p>
            Waiting for the notebook. Open the editable notebook if this message
            remains.
          </p>
        )}
    </div>
  );
}
export function Visual(
  { s, live, raw }: { s: Scene; live?: Live; raw?: Point[] },
) {
  switch (s.kind) {
    case "rank":
      return s.steps ? <Proof s={s} /> : <PracticalVisual s={s} />;
    case "proof":
    case "matrix":
      return <Proof s={s} />;
    case "center":
      return <Center />;
    case "lens":
      return <ExplainBack s={s} />;
    case "covariance":
      return <Covariance />;
    case "mixture":
      return <Mixture />;
    case "eigen":
      return <Eigen />;
    case "live":
      return <LiveLab live={live} />;
    case "geometry":
    case "triangle":
      return <Geometry s={s} raw={raw} />;
    default:
      return <PracticalVisual s={s} />;
  }
}
