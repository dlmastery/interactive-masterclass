/// <reference path="./marimo-studio.d.ts" />
import { useState } from "react";
import type { Scene } from "./course.ts";
import { fixed, model, type Point, RAW } from "./math.ts";
// @deno-types="npm:@types/katex@0.16.7"
import katex from "katex";
import "./practical.css";

const teal = "#167c80", amber = "#b66630";

function MathText({ tex }: { tex: string }) {
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

function Slider({ label, value, set, min = 0, max, step = 1, unit = "" }: {
  label: string;
  value: number;
  set: (v: number) => void;
  min?: number;
  max: number;
  step?: number;
  unit?: string;
}) {
  return (
    <label className="pv-slider">
      <span>
        {label}
        <strong>{fixed(value, step < 1 ? 1 : 0)}{unit}</strong>
      </span>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        aria-label={label}
        onChange={(e) => set(Number(e.target.value))}
      />
    </label>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="pv-stat">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function Matrix({ values, label }: { values: number[][]; label: string }) {
  return (
    <table className="pv-matrix">
      <caption>{label}</caption>
      <tbody>
        {values.map((row, i) => (
          <tr key={i}>{row.map((v, j) => <td key={j}>{fixed(v)}</td>)}</tr>
        ))}
      </tbody>
    </table>
  );
}

/** Equal pixel scales on x and y; data is already in the stated coordinates. */
function Cloud(
  {
    points,
    angle = 0,
    caption,
    xLabel = "x",
    yLabel = "y",
    labels = false,
    highlight = -1,
    project = false,
  }: {
    points: Point[];
    angle?: number;
    caption: string;
    xLabel?: string;
    yLabel?: string;
    labels?: boolean;
    highlight?: number;
    project?: boolean;
  },
) {
  const extent = Math.max(1, ...points.flat().map(Math.abs)) * 1.22;
  const scale = 115 / extent, cx = 170, cy = 145;
  const w: Point = [
    Math.cos(angle * Math.PI / 180),
    Math.sin(angle * Math.PI / 180),
  ];
  const xy = (p: Point): Point => [cx + p[0] * scale, cy - p[1] * scale];
  return (
    <figure className="pv-cloud">
      <svg viewBox="0 0 340 295" role="img" aria-label={caption}>
        <line x1="24" y1={cy} x2="316" y2={cy} stroke="#becdca" />
        <line x1={cx} y1="20" x2={cx} y2="264" stroke="#becdca" />
        <line
          x1={cx - w[0] * 130}
          y1={cy + w[1] * 130}
          x2={cx + w[0] * 130}
          y2={cy - w[1] * 130}
          stroke={teal}
          strokeWidth="2"
        />
        {points.map((p, i) => {
          const a = xy(p),
            z = p[0] * w[0] + p[1] * w[1],
            b = xy([z * w[0], z * w[1]]);
          const color = labels
            ? p[1] > 0 ? amber : teal
            : i === highlight
            ? amber
            : "#516b80";
          return (
            <g key={i}>
              {project && (
                <>
                  <line
                    x1={a[0]}
                    y1={a[1]}
                    x2={b[0]}
                    y2={b[1]}
                    stroke="#b6c6c4"
                    strokeDasharray="3 3"
                  />
                  <circle
                    cx={b[0]}
                    cy={b[1]}
                    r="3"
                    fill="white"
                    stroke={teal}
                  />
                </>
              )}
              {labels && p[1] > 0
                ? (
                  <rect
                    x={a[0] - 4}
                    y={a[1] - 4}
                    width="8"
                    height="8"
                    fill={color}
                  />
                )
                : (
                  <circle
                    cx={a[0]}
                    cy={a[1]}
                    r={i === highlight ? 7 : 4.5}
                    fill={color}
                  />
                )}
              {i === highlight && <text x={a[0] + 10} y={a[1] - 8}>D</text>}
            </g>
          );
        })}
        <text x="312" y={cy + 18} textAnchor="end">{xLabel}</text>
        <text x={cx + 8} y="21">{yLabel}</text>
        <text x="22" y="282" className="pv-small">
          Equal axis scale · ±{fixed(extent, 1)} shown
        </text>
      </svg>
      <figcaption>{caption}</figcaption>
    </figure>
  );
}

function VarianceBars(
  { values, labels }: { values: number[]; labels: string[] },
) {
  const max = Math.max(1, ...values);
  return (
    <div className="pv-bars">
      {values.map((v, i) => (
        <div className="pv-bar-row" key={i}>
          <span>{labels[i]}</span>
          <div>
            <i style={{ width: `${v / max * 100}%` }} />
          </div>
          <b>{fixed(v)}</b>
        </div>
      ))}
    </div>
  );
}

function ScaleVisual({ mode }: { mode?: string }) {
  const [factor, setFactor] = useState(1),
    [standardized, setStandardized] = useState(false);
  const [error, setError] = useState(10), [white, setWhite] = useState(false);
  if (mode === "weighted-loss") {
    return (
      <div className="experiment pv">
        <p className="eyebrow">TWO RAW ERRORS · ONE CHOSEN METRIC</p>
        <Slider
          label="Error in feature 1"
          value={error}
          set={setError}
          max={20}
        />
        <table className="pv-table">
          <thead>
            <tr>
              <th>Feature</th>
              <th>Raw error</th>
              <th>Scale</th>
              <th>Squared cost</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th>1</th>
              <td>{error}</td>
              <td>10</td>
              <td>({error}/10)² = {fixed((error / 10) ** 2)}</td>
            </tr>
            <tr>
              <th>2</th>
              <td>1</td>
              <td>1</td>
              <td>(1/1)² = 1</td>
            </tr>
          </tbody>
        </table>
        <VarianceBars
          labels={["Feature 1 cost", "Feature 2 cost"]}
          values={[(error / 10) ** 2, 1]}
        />
        <p className="feedback">
          {error === 10
            ? "Equal scaled cost: 10 raw units in feature 1 count like 1 in feature 2."
            : `Feature 1 contributes ${
              fixed((error / 10) ** 2)
            } times the cost of feature 2.`}
        </p>
        <button onClick={() => setError(10)}>Restore equal cost</button>
      </div>
    );
  }
  if (mode === "whiten") {
    const base = model(RAW), q: Point = [Math.SQRT1_2, Math.SQRT1_2];
    const scores = base.points.map((p) =>
      [(p[0] + p[1]) * q[0], (p[0] - p[1]) * q[0]] as Point
    );
    const shown = scores.map((p) =>
      [
        p[0] / (white ? Math.sqrt(6) : 1),
        p[1] / (white ? Math.sqrt(2 / 3) : 1),
      ] as Point
    );
    return (
      <div className="experiment pv">
        <p className="eyebrow">ROTATED SCORES → RESCALED SCORES</p>
        <Cloud
          points={shown}
          caption={white
            ? "Both component scores now have unit sample variance."
            : "Uncorrelated scores still have unequal spreads."}
          xLabel="score 1"
          yLabel="score 2"
        />
        <VarianceBars
          labels={["Variance 1", "Variance 2"]}
          values={white ? [1, 1] : [6, 2 / 3]}
        />
        <button aria-pressed={white} onClick={() => setWhite(!white)}>
          {white ? "Undo whitening" : "Whiten positive-variance scores"}
        </button>
        <p className="caption">
          Divide by √6 and √(2/3), respectively. This changes component-score
          scale, not the original feature means. Zero eigenvalues cannot use
          this division.
        </p>
      </div>
    );
  }
  const multiplier = mode === "standardize" ? 10 : factor;
  const stretched = RAW.map((p) => [p[0] * multiplier, p[1]] as Point),
    rawModel = model(stretched);
  const stds = [Math.sqrt(rawModel.cov[0][0]), Math.sqrt(rawModel.cov[1][1])];
  const z = rawModel.points.map((p) =>
    [p[0] / stds[0], p[1] / stds[1]] as Point
  );
  const useStandard = mode === "standardize" && standardized;
  const shown = useStandard ? z : rawModel.points, fit = model(shown);
  return (
    <div className="experiment pv">
      <p className="eyebrow">
        {useStandard
          ? "DISTANCE IN STANDARD DEVIATIONS"
          : "DISTANCE IN THE DISPLAYED NUMBERS"}
      </p>
      <Cloud
        points={shown}
        angle={fit.bestAngle}
        xLabel={useStandard ? "standardized x" : `x × ${multiplier}`}
        yLabel={useStandard ? "standardized y" : "y"}
        caption={`Leading direction: ${
          fixed(fit.bestAngle, 1)
        }° in these coordinates.`}
      />
      <div className="pv-stats">
        <Stat label="x variance" value={fixed(fit.cov[0][0])} />
        <Stat label="y variance" value={fixed(fit.cov[1][1])} />
        <Stat label="Top direction" value={`${fixed(fit.bestAngle, 1)}°`} />
      </div>
      {mode === "standardize"
        ? (
          <>
            <button
              aria-pressed={standardized}
              onClick={() => setStandardized(!standardized)}
            >
              {standardized
                ? "Restore original scale"
                : "Center and divide by training scales"}
            </button>
            <p className="caption">
              Fixture: x was multiplied by 10. Training sample scales are{" "}
              {fixed(stds[0])} and{" "}
              {fixed(stds[1])}. Both axes use the same pixel scale.
            </p>
          </>
        )
        : (
          <>
            <Slider
              label="Multiply the x coordinate"
              value={factor}
              set={setFactor}
              min={1}
              max={100}
              unit="×"
            />
            <div className="pv-actions">
              {[1, 10, 100].map((n) => (
                <button
                  key={n}
                  aria-pressed={factor === n}
                  onClick={() => setFactor(n)}
                >
                  {n === 1 ? "Restore 1×" : `${n}×`}
                </button>
              ))}
            </div>
            <p className="caption">
              x-error weight is multiplied by{" "}
              {factor ** 2}. The physical observations have not changed. The
              displayed numerical geometry has.
            </p>
          </>
        )}
    </div>
  );
}

function SpectrumVisual({ s }: { s: Scene }) {
  const tail = s.id === "more-discarded-tail";
  const validation = s.mode === "validation";
  const [k, setK] = useState(tail ? 2 : 1),
    spectrum = tail ? [12, 5, 2, 1] : [8, 1, 1],
    total = spectrum.reduce((a, b) => a + b, 0),
    kept = spectrum.slice(0, k).reduce((a, b) => a + b, 0),
    loss = total - kept;
  return (
    <div className="experiment pv">
      <p className="eyebrow">
        {validation
          ? "DIFFERENT TASKS · DIFFERENT EVIDENCE"
          : `${total} UNITS OF TOTAL SAMPLE VARIANCE`}
      </p>
      <div
        className="pv-spectrum"
        role="img"
        aria-label={`Eigenvalues ${
          spectrum.join(", ")
        }. ${k} retained components keep ${kept / total * 100} percent.`}
      >
        {spectrum.map((v, i) => (
          <div key={i}>
            <b>{v}</b>
            <div className="pv-column">
              <i
                className={i < k ? "kept" : ""}
                style={{ height: `${v / spectrum[0] * 100}%` }}
              />
            </div>
            <span>PC {i + 1}</span>
          </div>
        ))}
      </div>
      <Slider
        label="Retained components k"
        value={k}
        set={setK}
        min={0}
        max={spectrum.length}
      />
      <div className="pv-stats">
        <Stat label="Kept" value={`${kept / total * 100}%`} />
        <Stat label="Normalized loss" value={`${loss}`} />
        {tail
          ? <Stat label="Raw squared-error sum" value={`${4 * loss}`} />
          : <Stat label="Scores per observation" value={`${k}`} />}
      </div>
      {tail
        ? (
          <>
            <MathText
              tex={String
                .raw`n=5,\quad L_{\rm normalized}=${loss},\quad {\rm SSE}=(n-1)L=4\times${loss}=${
                4 * loss
              }`}
            />
            <p className="feedback">
              Keeping {k} directions retains {kept}/{total}{" "}
              of the variance. The omitted tail is{" "}
              {loss}; multiply by n−1=4 for the raw squared-error sum. None of
              these quantities alone measures fault-prediction accuracy.
            </p>
            {s.steps?.map(([tex, why]) => (
              <div className="pv-code-detail" key={tex}>
                <MathText tex={tex} />
                <p>{why}</p>
              </div>
            ))}
          </>
        )
        : validation
        ? (
          <table className="pv-table">
            <thead>
              <tr>
                <th>Purpose</th>
                <th>Choose using</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <th>Compression</th>
                <td>Reconstruction error AND storage budget</td>
              </tr>
              <tr>
                <th>Fault prediction</th>
                <td>Held-out fault error AND size constraint</td>
              </tr>
            </tbody>
          </table>
        )
        : (
          <p className="feedback">
            {k < 2
              ? "The 90% target is not met."
              : k === 2
              ? "Two components are the smallest choice that reaches 90%."
              : "All variation is retained, but the 90% target needed only two components."}
          </p>
        )}
      <p className="caption">
        {tail
          ? "Scene fixture: eigenvalues 12,5,2,1 and five observations. All reported losses use this same fixture."
          : validation
          ? "Illustrative spectrum, not a prediction benchmark. This accounting cannot reveal the validation fault error."
          : "The spectrum 8,1,1 is a separate three-dimensional fixture. Loss uses the sample-variance normalization."}
      </p>
    </div>
  );
}

function OutlierVisual({ robust = false }: { robust?: boolean }) {
  const [distance, setDistance] = useState(0),
    [ambiguity, setAmbiguity] = useState(false);
  if (robust) {
    return (
      <div className="experiment pv">
        <p className="eyebrow">
          A MODEL OF CORRUPTION · NOT AN EXECUTED ESTIMATOR
        </p>
        <div className="pv-matrix-equation">
          <Matrix label="M" values={[[4, 0], [0, 0]]} />
          <span>=</span>
          <Matrix
            label="L: low rank"
            values={ambiguity ? [[4, 0], [0, 0]] : [[0, 0], [0, 0]]}
          />
          <span>+</span>
          <Matrix
            label="S: sparse"
            values={ambiguity ? [[0, 0], [0, 0]] : [[4, 0], [0, 0]]}
          />
        </div>
        <button
          aria-pressed={ambiguity}
          onClick={() => setAmbiguity(!ambiguity)}
        >
          Assign the same entry to{" "}
          {ambiguity ? "sparse corruption" : "low-rank structure"}
        </button>
        <p className="feedback">
          The one-entry matrix has rank 1 AND only one nonzero entry. Both
          decompositions fit. Low rank plus sparsity alone does not identify the
          intended explanation.
        </p>
        <p className="caption">
          Illustration of an ambiguity. Robust covariance estimation and
          low-rank-plus-sparse decomposition impose different assumptions.
        </p>
      </div>
    );
  }
  const raw = RAW.map((p, i) =>
      [p[0] + (i === 3 ? distance : 0), p[1]] as Point
    ),
    m = model(raw),
    base = model(RAW);
  return (
    <div className="experiment pv">
      <p className="eyebrow">ONE OBSERVATION CAN CHANGE THE FIT</p>
      <Cloud
        points={m.points}
        angle={m.bestAngle}
        highlight={3}
        caption="D moves; the mean and best-fitting line are recomputed."
        xLabel="centered x (cm)"
        yLabel="centered y (cm)"
        project
      />
      <Slider
        label="Move D to the right"
        value={distance}
        set={setDistance}
        max={8}
        step={0.5}
        unit=" cm"
      />
      <table className="pv-table">
        <thead>
          <tr>
            <th>Quantity</th>
            <th>Original</th>
            <th>Now</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th>Best angle</th>
            <td>{fixed(base.bestAngle, 1)}°</td>
            <td>{fixed(m.bestAngle, 1)}°</td>
          </tr>
          <tr>
            <th>Top variance (cm²)</th>
            <td>{fixed(base.eigenvalues[0])}</td>
            <td>{fixed(m.eigenvalues[0])}</td>
          </tr>
          <tr>
            <th>D's centered squared length</th>
            <td>5</td>
            <td>{fixed(m.points[3][0] ** 2 + m.points[3][1] ** 2)}</td>
          </tr>
        </tbody>
      </table>
      <button onClick={() => setDistance(0)}>Restore D</button>
    </div>
  );
}

function NuisanceVisual({ duplicate = false }: { duplicate?: boolean }) {
  const [reveal, setReveal] = useState(false),
    [copies, setCopies] = useState(1);
  if (duplicate) {
    return (
      <div className="experiment pv">
        <p className="eyebrow">DUPLICATE A FEATURE · REPEAT ITS COST</p>
        <Slider
          label="Copies of feature x"
          value={copies}
          set={setCopies}
          min={1}
          max={6}
        />
        <div className="pv-feature-strip">
          {Array.from(
            { length: copies },
            (_, i) => <span key={i}>x{i + 1}</span>,
          )}
          <span className="other">y</span>
        </div>
        <MathText tex={String.raw`L=${copies}\,e_x^2+e_y^2`} />
        <VarianceBars
          labels={["x error: 1 per copy", "y error: 1"]}
          values={[copies, 1]}
        />
        <p className="feedback">
          The same x error is counted {copies}{" "}
          {copies === 1 ? "time" : "times"}. Copying a column changes feature
          weighting; it does not add an independent observation.
        </p>
        <button onClick={() => setCopies(1)}>Keep one copy</button>
      </div>
    );
  }
  const points: Point[] = [-4, -2, 2, 4].flatMap(
    (x) => [[x, -0.3] as Point, [x, 0.3] as Point],
  );
  const m = model(points);
  return (
    <div className="experiment pv">
      <p className="eyebrow">AN INVENTED FAULT-DETECTION TASK</p>
      <Cloud
        points={points}
        labels={reveal}
        project
        caption="Paired observations have identical horizontal scores and opposite vertical labels."
        xLabel="nuisance variation"
        yLabel="small signal"
      />
      <button aria-expanded={reveal} onClick={() => setReveal(!reveal)}>
        {reveal ? "Hide fault labels" : "Reveal fault labels"}
      </button>
      {reveal && (
        <div className="pv-label-key">
          <span>■ fault: y = +0.3</span>
          <span>● normal: y = −0.3</span>
        </div>
      )}
      <div className="pv-stats">
        <Stat label="Horizontal variance" value={fixed(m.cov[0][0])} />
        <Stat label="Vertical variance" value={fixed(m.cov[1][1], 3)} />
      </div>
      <p className="feedback">
        {reveal
          ? "Each horizontal score occurs in both classes. Keeping only PC1 loses this label distinction; the sign of y separates it exactly in this fixture."
          : "PCA chooses the long horizontal direction. Predict whether that direction is useful for the hidden fault label."}
      </p>
      <p className="caption">
        The fixture demonstrates a possibility. It does not estimate performance
        on real faults.
      </p>
    </div>
  );
}

function CurveVisual({ nonlinear = false }: { nonlinear?: boolean }) {
  const [angle, setAngle] = useState(30);
  if (nonlinear) {
    return (
      <div className="experiment pv">
        <p className="eyebrow">COMPARE THE PURPOSE BEFORE THE PICTURE</p>
        <table className="pv-table">
          <thead>
            <tr>
              <th>Family</th>
              <th>What it tries to preserve</th>
              <th>Inspect</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th>Linear PCA</th>
              <td>Squared linear reconstruction</td>
              <td>Residuals and spectrum</td>
            </tr>
            <tr>
              <th>Kernel PCA</th>
              <td>Variance in a kernel feature space</td>
              <td>Kernel choice; decoding</td>
            </tr>
            <tr>
              <th>Neighborhood embedding</th>
              <td>Chosen local relationships</td>
              <td>Parameters; stability; new data</td>
            </tr>
            <tr>
              <th>Autoencoder</th>
              <td>Trained encoding/decoding loss</td>
              <td>Held-out reconstruction; capacity</td>
            </tr>
          </tbody>
        </table>
        <p className="feedback">
          A separated display is evidence about an embedding. It is not, by
          itself, evidence of separate source populations.
        </p>
        <p className="caption">
          Objective comparison only. No nonlinear method or dataset is executed
          here.
        </p>
      </div>
    );
  }
  const radians = angle * Math.PI / 180,
    a: Point = [Math.cos(radians), Math.sin(radians)],
    b: Point = [a[0], -a[1]];
  return (
    <div className="experiment pv">
      <p className="eyebrow">ONE SCORE · TWO POSITIONS</p>
      <svg
        viewBox="0 0 400 310"
        role="img"
        aria-label={`Two circle points at plus and minus ${angle} degrees both project to x=${
          fixed(a[0])
        }.`}
      >
        <circle
          cx="200"
          cy="150"
          r="105"
          fill="none"
          stroke="#9bb9b5"
          strokeWidth="3"
        />
        <line
          x1="45"
          y1="150"
          x2="355"
          y2="150"
          stroke={teal}
          strokeWidth="2"
        />
        {[a, b].map((p, i) => (
          <g key={i}>
            <line
              x1={200 + p[0] * 105}
              y1={150 - p[1] * 105}
              x2={200 + p[0] * 105}
              y2="150"
              stroke={amber}
              strokeDasharray="4 4"
            />
            <circle
              cx={200 + p[0] * 105}
              cy={150 - p[1] * 105}
              r="7"
              fill={i ? amber : teal}
            />
            <text x={212 + p[0] * 105} y={150 - p[1] * 105}>
              {i ? "B" : "A"}
            </text>
          </g>
        ))}
        <circle
          cx={200 + a[0] * 105}
          cy="150"
          r="7"
          fill="white"
          stroke={teal}
          strokeWidth="3"
        />
        <text x="35" y="287">
          Horizontal score of A = score of B = {fixed(a[0])}
        </text>
      </svg>
      <Slider
        label="Position above and below the line"
        value={angle}
        set={setAngle}
        min={10}
        max={90}
        unit="°"
      />
      <p className="feedback">
        The line cannot tell these points apart. An angle can parameterize the
        circle (with a wraparound), but a single linear coordinate merges
        positions.
      </p>
    </div>
  );
}

function RankVisual({ sparse = false }: { sparse?: boolean }) {
  const [center, setCenter] = useState(false), [k, setK] = useState(1);
  if (!sparse) {
    return (
      <div className="experiment pv">
        <p className="eyebrow">ADD RETAINED DIRECTIONS</p>
        <Slider label="Retained rank k" value={k} set={setK} min={0} max={3} />
        <VarianceBars
          labels={[
            "First contribution: 8",
            "Second contribution: 1",
            "Third contribution: 1",
          ]}
          values={[k >= 1 ? 8 : 0, k >= 2 ? 1 : 0, k >= 3 ? 1 : 0]}
        />
        <MathText
          tex={String.raw`\hat X_k=\sum_{j=1}^{${k}}\sigma_j u_jv_j^T`}
        />
        <p className="caption">
          Separate spectrum fixture: 8,1,1. Each retained outer product adds one
          rank-one contribution.
        </p>
      </div>
    );
  }
  const raw = [[2, 0, 0], [0, 3, 0], [0, 0, 1]], mean = [2 / 3, 1, 1 / 3];
  const shown = center ? raw.map((row) => row.map((v, j) => v - mean[j])) : raw;
  return (
    <div className="experiment pv">
      <p className="eyebrow">ZERO ENTRIES CAN BECOME NONZERO</p>
      <Matrix
        label={center ? "Centered matrix" : "Sparse observations"}
        values={shown}
      />
      <div className="pv-stats">
        <Stat
          label="Nonzero entries"
          value={`${
            shown.flat().filter((v) => Math.abs(v) > 1e-12).length
          } of 9`}
        />
        <Stat label="Stored training mean" value="(2/3, 1, 1/3)" />
      </div>
      <button aria-pressed={center} onClick={() => setCenter(!center)}>
        {center ? "Restore sparse observations" : "Subtract every column mean"}
      </button>
      <p className="feedback">
        {center
          ? "Every former zero now contains minus its column mean. This explicit matrix is dense."
          : "Only three entries are nonzero. Predict what happens to the six zeros after centering."}
      </p>
      <p className="caption">
        Uncentered truncated SVD approximates the original matrix about the
        origin. Centered PCA approximates deviations about the mean; these
        objectives differ.
      </p>
    </div>
  );
}

type CodeLine = { code: string; shape: string; explanation: string };
const SVD_LINES: CodeLine[] = [
  {
    code: "import numpy as np",
    shape: "NumPy",
    explanation: "Rows are observations; columns are features.",
  },
  {
    code: "mu = train.mean(axis=0)",
    shape: "mu: (p,)",
    explanation: "Fit the training mean once.",
  },
  {
    code: "X = train - mu",
    shape: "X: (n, p)",
    explanation: "Center each training observation using that mean.",
  },
  {
    code: "U, s, Vt = np.linalg.svd(X, full_matrices=False)",
    shape: "r=min(n,p); Vt: (r,p)",
    explanation: "Rows of Vt are the right singular directions.",
  },
  {
    code: "W = Vt[:k].T",
    shape: "W: (p, k)",
    explanation:
      "Transpose selected rows to put retained directions in columns.",
  },
  {
    code: "Z = X @ W",
    shape: "Z: (n, k)",
    explanation: "One retained score per component per observation.",
  },
  {
    code: "X_hat = Z @ W.T + mu",
    shape: "X_hat: (n, p)",
    explanation: "Decode scores, then restore the training mean.",
  },
  {
    code: "eigenvalues = s**2 / (len(train) - 1)",
    shape: "eigenvalues: (r,)",
    explanation: "Squared singular values become sample variances.",
  },
];

function CodeVisual({ s }: { s: Scene }) {
  const mode = s.mode;
  const authored = s.id === "more-numpy-meaning" && Boolean(s.example);
  const [step, setStep] = useState(0),
    [newX, setNewX] = useState(9),
    [sign, setSign] = useState(1),
    [showCode, setShowCode] = useState(!authored);
  let lines = SVD_LINES;
  if (mode === "pipeline") {
    lines = [
      {
        code: "train, validation, test = split_before_fitting(data)",
        shape: "separate observation sets",
        explanation:
          "Conceptual split step: choose a split appropriate to the task. This helper is pseudocode.",
      },
      {
        code: "mu = train.mean(axis=0)",
        shape: "(p,)",
        explanation: "Only training observations determine the mean.",
      },
      {
        code: "_, s, Vt = np.linalg.svd(train - mu, full_matrices=False)",
        shape: "directions fitted on training",
        explanation:
          "Inside cross-validation, repeat this fit inside each training fold.",
      },
      {
        code: "W = Vt[:k].T",
        shape: "(p, k)",
        explanation:
          "Choose candidate k using validation and the task constraint.",
      },
      {
        code: "Z_validation = (validation - mu) @ W",
        shape: "(n_validation, k)",
        explanation:
          "Apply stored mean and directions; do not refit on validation.",
      },
      {
        code: "Z_test = (test - mu) @ W",
        shape: "(n_test, k)",
        explanation: "Use the reserved test data after the choices are fixed.",
      },
    ];
  }
  if (mode === "frozen-transform") {
    lines = [
      {
        code: "mu_train = np.array([6., 6.])",
        shape: "(2,)",
        explanation:
          "This is the stored mean of the fixed four training points.",
      },
      {
        code: "W = np.array([[1.], [1.]]) / np.sqrt(2)",
        shape: "(2, 1)",
        explanation:
          "The stored leading direction stays fixed as the new point moves.",
      },
      {
        code: `new = np.array([[${newX}., 7.]])`,
        shape: "(1, 2)",
        explanation:
          "One held-out observation; do not include it in a new fit.",
      },
      {
        code: "z_new = (new - mu_train) @ W",
        shape: "(1, 1)",
        explanation: "Subtract the stored mean, then project.",
      },
      {
        code: "recovered = z_new @ W.T + mu_train",
        shape: "(1, 2)",
        explanation: "Decode the score and restore the stored mean.",
      },
    ];
  }
  if (mode === "checks") {
    lines = [
      {
        code: "assert np.allclose(X.mean(axis=0), 0)",
        shape: "centering",
        explanation: "Means are near zero up to floating-point tolerance.",
      },
      {
        code: "assert np.allclose(W.T @ W, np.eye(k))",
        shape: "(k, k)",
        explanation: "Retained directions are orthonormal.",
      },
      {
        code: "assert np.allclose(np.var(Z, axis=0, ddof=1), eigenvalues[:k])",
        shape: "(k,)",
        explanation: "Use the same n−1 normalization on both sides.",
      },
      {
        code: "loss = np.sum((X - Z @ W.T)**2) / (len(X)-1)",
        shape: "normalized squared error",
        explanation: "Compare this loss to the sum of discarded eigenvalues.",
      },
      {
        code: "assert np.allclose((-Z) @ (-W).T, Z @ W.T)",
        shape: "(n, p)",
        explanation:
          "Matching direction and score signs cancel in reconstruction.",
      },
    ];
  }
  if (authored) {
    const annotations = [
      [
        "mu: (8,)",
        "The fitted mean stores one value for each of the eight features.",
      ],
      [
        "X: (100, 8)",
        "Subtract that training mean from all 100 observation rows.",
      ],
      [
        "U: (100,8); sigma: (8,); Vt: (8,8)",
        "Reduced SVD returns right singular directions as rows of Vt.",
      ],
      [
        "W: (8, 3)",
        "Select three rows of Vt, then transpose: feature directions become columns.",
      ],
      ["Z: (100, 3)", "Encode each observation as three retained scores."],
      [
        "A_hat: (100, 8)",
        "Decode into eight features, then restore the fitted mean.",
      ],
      [
        "lam: (8,)",
        "Divide squared singular values by n−1=99 to obtain sample variances.",
      ],
      [
        "W.T @ W: (3,3)",
        "Compare with the identity using a floating-point tolerance; this checks orthonormality.",
      ],
      [
        "Both sides: (100,3)",
        "This independent score identity can catch a slicing or transpose error.",
      ],
      [
        "Both sides: scalar",
        "Use np.sum for the total over both array axes. Compare normalized residual error with the eigenvalue tail.",
      ],
    ];
    lines = s.example!.split("\n").map((code, i) => ({
      code,
      shape: annotations[i]?.[0] ?? "Authored example",
      explanation: annotations[i]?.[1] ??
        "Read this operation in the context of the fitted training model.",
    }));
  }
  const current = Math.min(step, lines.length - 1),
    score = (newX - 5) / Math.sqrt(2);
  return (
    <div className="experiment pv">
      <p className="eyebrow">
        {mode === "pipeline"
          ? "FIT ON TRAINING → APPLY TO HELD-OUT DATA"
          : "READ THE OPERATIONS AND THEIR SHAPES"}
      </p>
      {authored && (
        <>
          <p className="caption">
            Shape fixture: n=100 observations, d=8 features, k=3 retained
            directions. NumPy is imported as np.
          </p>
          <button
            aria-expanded={showCode}
            onClick={() => setShowCode(!showCode)}
          >
            {showCode
              ? "Hide authored example"
              : "Reveal authored NumPy example"}
          </button>
        </>
      )}
      {showCode && (
        <>
          <ol className="pv-code">
            {lines.map((line, i) => (
              <li key={i} className={current === i ? "active" : ""}>
                <button
                  onClick={() =>
                    setStep(i)}
                  aria-current={current === i ? "step" : undefined}
                  aria-label={`Inspect line ${i + 1}: ${line.code}`}
                >
                  <code>{line.code}</code>
                </button>
              </li>
            ))}
          </ol>
          <div className="pv-code-detail">
            <b>{lines[current].shape}</b>
            <p>{lines[current].explanation}</p>
          </div>
          <div className="pv-actions">
            <button
              disabled={current === 0}
              onClick={() => setStep(current - 1)}
            >
              Previous line
            </button>
            <button
              disabled={current === lines.length - 1}
              onClick={() => setStep(current + 1)}
            >
              Next line
            </button>
          </div>
        </>
      )}
      {mode === "frozen-transform" && (
        <>
          <Slider
            label="New observation x; y stays 7"
            value={newX}
            set={setNewX}
            max={12}
          />
          <div className="pv-stats">
            <Stat label="Stored mean" value="(6, 6)" />
            <Stat label="New score" value={fixed(score)} />
            <Stat
              label="Reconstruction"
              value={`(${fixed(6 + score / Math.sqrt(2))}, ${
                fixed(6 + score / Math.sqrt(2))
              })`}
            />
          </div>
        </>
      )}
      {mode === "checks" && (
        <>
          <button onClick={() => setSign(-sign)}>
            Flip direction and score signs
          </button>
          <p className="feedback">
            For centered point A=(2,1): q₁={sign > 0 ? "+" : "−"}(1,1)/√2;
            z={fixed(sign * 3 / Math.sqrt(2))}. Reconstruction remains
            (1.5,1.5).
          </p>
        </>
      )}
      <p className="caption">
        {mode === "frozen-transform"
          ? "The displayed arithmetic is computed in the browser using the fixed training model."
          : "Readable NumPy recipe, not a code execution console. k must fit the available directions. Validate real code in the editable notebook."}
      </p>
    </div>
  );
}

function Flow({ nodes }: { nodes: string[] }) {
  return (
    <ol className="pv-flow">
      {nodes.map((node, i) => (
        <li key={i}>
          <span>{i + 1}</span>
          {node}
        </li>
      ))}
    </ol>
  );
}

function DecisionVisual({ mode }: { mode?: string }) {
  const [window, setWindow] = useState(3);
  if (mode === "seurat" || mode === "dinov2") {
    return (
      <div className="experiment pv">
        <p className="eyebrow">DOCUMENTED APPLICATION · SCHEMATIC ONLY</p>
        <Flow
          nodes={mode === "seurat"
            ? [
              "Cells × selected gene features",
              "Center/scale selected features",
              "PCA scores and loadings",
              "Inspect components; compare downstream choices",
            ]
            : [
              "Image patches",
              "Pretrained encoder features",
              "PCA inspection of patch features",
              "Filter with a component; map three components to colors",
            ]}
        />
        <p className="feedback">
          {mode === "seurat"
            ? "A later component can carry information about a rare subset. Check how the result changes with the retained component count."
            : "The neural encoder learned the features. PCA supplies coordinates for inspecting them; the colors are a visualization choice."}
        </p>
        <p className="caption">
          {mode === "seurat"
            ? "No cell dataset is loaded. This shows the workflow described by the Seurat tutorial."
            : "No encoder or image dataset is run here. This shows the DINOv2 paper’s feature-visualization workflow; colors and signs have no universal semantic label."}
        </p>
      </div>
    );
  }
  if (mode === "temporal") {
    return (
      <div className="experiment pv">
        <p className="eyebrow">FIT EARLIER · EVALUATE LATER</p>
        <div className="pv-timeline">
          {Array.from(
            { length: 8 },
            (_, i) => (
              <span
                key={i}
                className={i >= 6 ? "test" : i >= 6 - window ? "train" : ""}
              >
                t{i + 1}
                <small>
                  {i >= 6 ? "evaluate" : i >= 6 - window ? "fit" : "unused"}
                </small>
              </span>
            ),
          )}
        </div>
        <Slider
          label="Earlier periods in fitting window"
          value={window}
          set={setWindow}
          min={2}
          max={6}
        />
        <table className="pv-table">
          <tbody>
            <tr>
              <th>Longer window</th>
              <td>More history; may mix different regimes</td>
            </tr>
            <tr>
              <th>Shorter window</th>
              <td>More recent focus; less estimation data</td>
            </tr>
            <tr>
              <th>Later evaluation</th>
              <td>Apply stored mean and directions; inspect residuals</td>
            </tr>
          </tbody>
        </table>
        <p className="caption">
          Illustrative time blocks, not market measurements or performance
          results. Changing the window changes a modeling choice, not a proven
          forecast.
        </p>
      </div>
    );
  }
  const rows: Record<string, [string, string][]> = {
    metric: [["Observations", "Positions in centimeters"], [
      "Goal",
      "Recover locations with low squared distance",
    ], [
      "Equal cost",
      "A 1 cm error east and a 1 cm error north each cost 1 cm²",
    ], ["Decision", "Choose the metric before fitting"]],
    "choose-method": [
      ["PCA + predictor", "Directions learn feature variation"],
      [
        "Regularized original features",
        "Keep features; control model complexity",
      ],
      [
        "Supervised reduction",
        "Use the training target to choose a representation",
      ],
      ["Fair comparison", "Same held-out task and constraints"],
    ],
    "latent-model": [
      ["PCA", "Descriptive linear variance/reconstruction optimum"],
      [
        "Latent-variable model",
        "Adds assumptions about hidden variables and noise",
      ],
      ["Independence", "Not implied by zero covariance"],
      ["Causality", "Requires evidence beyond a fitted decomposition"],
    ],
    "decision-final": [
      ["Purpose", "What must the short representation preserve?"],
      ["Evidence", "Which held-out and domain checks support it?"],
      ["Boundary", "Which failure would change the decision?"],
      ["Report", "Data, scaling, k, loadings, scores, residuals"],
    ],
  };
  return (
    <div className="experiment pv">
      <p className="eyebrow">MAKE THE CLAIM MATCH THE TASK</p>
      <table className="pv-table">
        <tbody>
          {(rows[mode ?? "metric"] ?? rows["decision-final"]).map((
            [label, text],
          ) => (
            <tr key={label}>
              <th>{label}</th>
              <td>{text}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="caption">
        Use the scene’s choices to test the claim. These are decision criteria,
        not performance rankings.
      </p>
    </div>
  );
}

export function PracticalVisual({ s }: { s: Scene }) {
  switch (s.kind) {
    case "scale":
      return <ScaleVisual key={s.id} mode={s.mode} />;
    case "spectrum":
      return <SpectrumVisual key={s.id} s={s} />;
    case "outlier":
      return <OutlierVisual key={s.id} robust={s.mode === "robust"} />;
    case "nuisance":
      return <NuisanceVisual key={s.id} duplicate={s.mode === "duplicate"} />;
    case "curve":
      return <CurveVisual key={s.id} nonlinear={s.mode === "nonlinear"} />;
    case "rank":
      return <RankVisual key={s.id} sparse={s.mode === "sparse"} />;
    case "code":
      return <CodeVisual key={s.id} s={s} />;
    default:
      return <DecisionVisual key={s.id} mode={s.mode} />;
  }
}
