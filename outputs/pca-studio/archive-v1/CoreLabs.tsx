/// <reference path="./marimo-studio.d.ts" />
import { useState } from "react";
import {
  Bars,
  Budget,
  Card,
  type Case,
  type Course,
  DataTable,
  Eq,
  f,
  type Lab,
  Matrix,
  Metric,
  People,
  percent,
  Plot,
  type Point,
  point,
  Practice,
  Prediction,
  Range,
  type RecordAttempt,
  Steps,
  Tabs,
} from "./LabComponents.tsx";
import { Assessment } from "./Assessment.tsx";
type Props = {
  id: number;
  lab: Lab;
  course: Course;
  sandbox?: Case;
  person: number;
  setPerson: (i: number) => void;
  angle: number;
  setAngle: (a: number) => void;
  record: RecordAttempt;
  jumpCore: (n: number) => void;
};
export function CoreLab(
  {
    id,
    lab,
    course: c,
    sandbox,
    person: p,
    setPerson,
    angle,
    setAngle,
    record,
    jumpCore,
  }: Props,
) {
  const [mode, setMode] = useState(0),
    [step, setStep] = useState(0),
    [value, setValue] = useState(0),
    [show, setShow] = useState(false),
    [reason, setReason] = useState("");
  const b = lab.base,
    fr = b.frames[angle],
    labels = lab.people,
    people = <People selected={p} setSelected={setPerson} />;
  const rotation = (
    <Range label="Direction angle" value={angle} onChange={setAngle} />
  );
  const plot = (
    <Plot
      points={b.points}
      second={fr.projected}
      w={fr.w}
      selected={p}
      onSelect={setPerson}
      onAngle={setAngle}
    />
  );
  const metrics = (
    <div className="metrics">
      <Metric name="Score variance" value={f(fr.variance)} />
      <Metric name="Spread retained" value={percent(fr.ratio)} />
      <Metric name="Lost spread" value={f(fr.loss)} />
    </div>
  );
  if (id === 0) {
    return (
      <>
        <Prediction problem={c.practices.mission} record={record} />
        <div className="pair-preview">
          <Card>
            <b>Person A</b>
            <span>{point(b.raw[0])}</span>
          </Card>
          <Card>
            <b>Person B</b>
            <span>{point(b.raw[1])}</span>
          </Card>
        </div>
        <p className="quiet">Target: {c.passTest}</p>
      </>
    );
  }
  if (id === 1) {
    return (
      <>
        <div className="mini-split">
          <DataTable rows={b.raw} selected={p} onSelect={setPerson} />
          <Plot
            points={b.raw}
            selected={p}
            onSelect={setPerson}
            labels={["Test A · points", "Test B · points"]}
            bound={10}
          />
        </div>
        <Card>
          Selected person {labels[p]}: {point(b.raw[p])}. One row → one point.
        </Card>
      </>
    );
  }
  if (id === 2) {
    return (
      <>
        <Tabs labels={["Test A", "Test B"]} value={mode} onChange={setMode} />
        <Bars
          values={b.raw.map((v) => v[mode])}
          labels={labels}
          highlight={p}
        />
        <Card>
          <Eq
            tex={String.raw`\mu_${mode ? "B" : "A"}=\frac{${
              b.raw.map((v) => f(v[mode], 0)).join("+")
            }}{${b.n}}=${f(b.mean[mode])}`}
          />
        </Card>
        <Plot
          points={b.raw}
          mean={b.mean}
          selected={p}
          onSelect={setPerson}
          bound={10}
          labels={["Test A · points", "Test B · points"]}
        />
      </>
    );
  }
  if (id === 3) {
    const state = lab.centers[value];
    return (
      <>
        {people}
        <Plot
          points={state.points}
          mean={state.mean}
          bound={10}
          selected={p}
          onSelect={setPerson}
          labels={["Test A · translated points", "Test B · translated points"]}
        />
        <Range
          label="Mean subtracted"
          value={value}
          min={0}
          max={20}
          onChange={setValue}
          suffix=" / 20"
        />
        <Card>
          {point(b.raw[p])} − {f(state.fraction)} × {point(b.mean)} ={" "}
          <strong>{point(state.points[p])}</strong>
        </Card>
      </>
    );
  }
  if (id === 4) {
    return (
      <>
        {people}
        <Tabs
          labels={["Signed deviations", "Squared deviations"]}
          value={mode}
          onChange={setMode}
        />
        <Bars
          values={b.points.map((v, i) => mode ? b.squared[i][0] : v[0])}
          labels={labels}
          highlight={p}
        />
        <div className="metrics">
          <Metric
            name={mode ? "Sum of squares" : "Signed sum"}
            value={f(mode ? b.squaresSums[0] : b.signedSums[0])}
          />
          <Metric name="Sample variance of A" value={f(b.cov[0][0])} />
        </div>
        <Eq tex={c.equations.variance} />
      </>
    );
  }
  if (id === 5) {
    return (
      <>
        <Tabs
          labels={["Attempt", "Fresh redo"]}
          value={mode}
          onChange={setMode}
        />
        <Practice
          key={mode}
          problem={c.practices[mode ? "nminusRedo" : "nminus"]}
          record={record}
        />
        <details>
          <summary>After attempting: why n−1 corrects bias</summary>
          <p>
            When the population mean is unknown, using the sample mean pulls the
            squared distances downward on average. Under independent sampling
            with finite variance, dividing the sum by n−1 makes its expected
            value equal the population variance. The zero-sum constraint
            explains the lost degree of freedom; unbiasedness is the statistical
            reason for this denominator.
          </p>
        </details>
      </>
    );
  }
  if (id === 6 || id === 7) {
    const d = lab.covCases[mode];
    return (
      <>
        <Tabs
          labels={["Together", "Opposite", "Cancelling"]}
          value={mode}
          onChange={setMode}
        />
        <div className="mini-split">
          <Plot points={d.points} selected={p} onSelect={setPerson} />
          <div>
            {people}
            <Card>
              <b>Person {labels[p]}</b>
              <Eq
                tex={String.raw`${f(d.points[p][0])}\times(${
                  f(d.points[p][1])
                })=${f(d.products[p][0][1])}`}
              />
            </Card>
            <Bars
              values={d.products.map((v) => v[0][1])}
              labels={labels}
              highlight={p}
            />
            <Metric name="Sample covariance" value={f(d.cov[0][1])} />
          </div>
        </div>
        <Eq
          tex={String.raw`S_{AB}=\frac{${
            d.products.map((v) => `(${f(v[0][1], 0)})`).join("+")
          }}{${d.n - 1}}=${f(d.cov[0][1])}`}
        />
      </>
    );
  }
  if (id === 8 || id === 9) {
    const row = Math.floor(mode / 2), col = mode % 2;
    return (
      <>
        <Matrix data={b.cov} active={mode} onSelect={setMode} />
        {id === 9 && (
          <Tabs
            labels={["1 · Transpose", "2 · Multiply", "3 · Divide"]}
            value={step}
            onChange={setStep}
          />
        )}
        <div className="mini-split">
          <div>
            <DataTable
              rows={b.points}
              headers={["Centered A", "Centered B"]}
              selected={p}
              onSelect={setPerson}
            />
            <p className="quiet">
              Selected entry: {row ? "B" : "A"} compared with {col ? "B" : "A"}
            </p>
          </div>
          <div>
            <Bars
              values={b.products.map((v) => v[row][col])}
              labels={labels}
              highlight={p}
            />
            <Card>
              {id === 9 && step === 0
                ? (
                  <Eq
                    tex={String.raw`X_c^\top\ (2\times4)\quad X_c\ (4\times2)`}
                  />
                )
                : (
                  <Eq
                    tex={String.raw`${
                      b.points.map((v) => `(${f(v[row], 0)})(${f(v[col], 0)})`)
                        .join("+")
                    }=${f(b.sums[row][col], 0)}`}
                  />
                )}
              <Eq
                tex={id === 9 && step < 2
                  ? `(X_c^\top X_c)_{${row + 1}${col + 1}}=${
                    f(b.sums[row][col])
                  }`
                  : String.raw`S_{${row + 1}${col + 1}}=\frac{${
                    f(b.sums[row][col], 0)
                  }}{3}=${f(b.cov[row][col])}`}
              />
            </Card>
          </div>
        </div>
      </>
    );
  }
  if (id === 11) {
    return (
      <>
        {people}
        <div className="projection-layout">
          <div>{plot}</div>
          <div className="projection-meters">
            {metrics}
            <button onClick={() => setShow(!show)}>
              {show ? "Hide best axis" : "Show the best axis"}
            </button>
            {show && (
              <p className="quiet">
                Best {f(b.angle, 1)}°. Gap: {f(b.values[0] - fr.variance)}.
              </p>
            )}
          </div>
        </div>
        {rotation}
      </>
    );
  }
  if (id === 10 || id === 12) {
    return (
      <>
        {people}
        {plot}
        {rotation}
        {id === 12
          ? (
            <Card>
              <Eq
                tex={String.raw`z_${labels[p]}=(${f(fr.w[0])})(${
                  f(b.points[p][0])
                })+(${f(fr.w[1])})(${f(b.points[p][1])})`}
              />
              <Eq
                tex={String.raw`=${f(fr.terms[p][0])}+(${f(fr.terms[p][1])})=${
                  f(fr.z[p])
                }`}
              />
            </Card>
          )
          : id === 10
          ? (
            <Card>
              Person {labels[p]}: original {point(b.points[p])} → one score{" "}
              <strong>{f(fr.z[p])}</strong> → shadow {point(fr.projected[p])}
            </Card>
          )
          : (
            <>
              {metrics}
              <button onClick={() => setShow(!show)}>
                {show ? "Hide best axis" : "Show the best axis"}
              </button>
              {show && (
                <p className="result-box">
                  Best axis: {f(b.angle, 1)}°. Its variance is{" "}
                  {f(b.values[0])}. Your gap: {f(b.values[0] - fr.variance)}.
                </p>
              )}
            </>
          )}
      </>
    );
  }
  if (id === 13) {
    return (
      <>
        <Steps steps={c.varianceSteps} />
        {rotation}
        <div className="mini-split">
          <DataTable
            rows={fr.z.map((z, i) => [z, fr.kept[i]])}
            headers={["Score z", "Squared score"]}
            selected={p}
            onSelect={setPerson}
          />
          <Card>
            <Metric
              name="Sum of squares / (n−1)"
              value={`${f(fr.sumSquares)} / ${b.n - 1}`}
            />
            <Metric name="Same value as wᵀSw" value={f(fr.variance)} />
          </Card>
        </div>
      </>
    );
  }
  if (id === 14) {
    const r = lab.ruler[value];
    return (
      <>
        <Range
          label="Length of weight vector"
          min={1}
          max={6}
          value={value + 1}
          suffix="×"
          onChange={(v) => setValue(v - 1)}
        />
        <div className="mini-split">
          <Plot
            points={[]}
            vectors={[r.w]}
            vectorLabels={["w"]}
            bound={7}
            labels={["Weight A", "Weight B"]}
          />
          <div>
            <Eq tex={c.equations.constraint} />
            <Metric name="wᵀw" value={f(r.norm2)} />
            <Metric name="Score variance" value={f(r.variance)} />
            <button className="primary" onClick={() => setValue(0)}>
              Normalize to length 1
            </button>
          </div>
        </div>
        <DataTable
          rows={r.z.map((z) => [z])}
          headers={["Score using this ruler"]}
        />
      </>
    );
  }
  if (id === 15) {
    return (
      <>
        <Plot
          points={[]}
          vectors={[fr.w, fr.sw]}
          vectorLabels={["w", "Sw"]}
          bound={7}
          labels={["Coordinate 1", "Coordinate 2"]}
        />
        {rotation}
        <Tabs
          labels={["Try 0°", "Try 45°", "Try 135°"]}
          value={angle === 0 ? 0 : angle === 45 ? 1 : angle === 135 ? 2 : -1}
          onChange={(i) => setAngle([0, 45, 135][i])}
        />
        <Card>
          <span>w = {point(fr.w)} · Sw = {point(fr.sw)}</span>
          <strong>
            {fr.eigen
              ? "No sideways turning: an eigenvector."
              : "The direction turns: not an eigenvector."}
          </strong>
        </Card>
      </>
    );
  }
  if (id === 16) {
    const a = [0, 45, 135][mode], frame = b.frames[a], w = frame.w;
    return (
      <>
        <Tabs
          labels={["Horizontal", "Together", "Contrast"]}
          value={mode}
          onChange={setMode}
        />
        <Matrix data={b.cov} />
        <Eq
          tex={String.raw`S\begin{bmatrix}${f(w[0], 3)}\\${
            f(w[1], 3)
          }\end{bmatrix}=\begin{bmatrix}${f(frame.sw[0], 3)}\\${
            f(frame.sw[1], 3)
          }\end{bmatrix}`}
        />
        <Plot
          points={[]}
          vectors={[w, frame.sw]}
          vectorLabels={["w", "Sw"]}
          bound={7}
          labels={["Coordinate 1", "Coordinate 2"]}
        />
        <Card>
          {frame.eigen
            ? `Same direction. Stretch factor = ${f(frame.variance)}.`
            : "Horizontal input acquires a vertical component. One stretch factor cannot explain this."}
        </Card>
      </>
    );
  }
  if (id === 17) {
    const m = lab.mixtures[value];
    return (
      <>
        <Eq tex={c.equations.mix} />
        <Range
          label="Share a² assigned to PC1"
          value={value}
          max={100}
          suffix="%"
          onChange={setValue}
        />
        <Bars
          values={[m.first, m.second]}
          labels={["PC1 contribution", "PC2 contribution"]}
        />
        <div className="metrics">
          <Metric name="a²" value={f(m.p)} />
          <Metric name="b²" value={f(1 - m.p)} />
          <Metric name="Mixed variance" value={f(m.variance)} />
        </div>
        <Card>{f(b.values[1])} ≤ {f(m.variance)} ≤ {f(b.values[0])}</Card>
      </>
    );
  }
  if (id === 18) {
    const pts = mode
      ? b.scores.map((v) => [show ? -v[0] : v[0], v[1]] as Point)
      : b.points;
    return (
      <>
        <Tabs
          labels={["Original coordinates", "PCA coordinates"]}
          value={mode}
          onChange={setMode}
        />
        <label className="check">
          <input
            type="checkbox"
            checked={show}
            onChange={(e) => setShow(e.target.checked)}
          />Flip PC1 sign
        </label>
        <div className="mini-split">
          <Plot
            points={pts}
            selected={p}
            onSelect={setPerson}
            labels={mode ? ["PC1 score", "PC2 score"] : undefined}
          />
          <DataTable
            rows={pts}
            headers={mode ? ["PC1", "PC2"] : ["Centered A", "Centered B"]}
            selected={p}
            onSelect={setPerson}
          />
        </div>
        <Matrix
          data={mode ? b.scoreCov : b.cov}
          prefix={mode ? "Cov(Z)" : "S"}
        />
      </>
    );
  }
  if (id === 19) {
    return (
      <>
        <Tabs
          labels={["Keep 0", "Keep 1", "Keep 2"]}
          value={mode}
          onChange={setMode}
        />
        <Bars values={b.values} labels={["PC1 variance", "PC2 variance"]} />
        <Budget ratio={b.recon[mode].ratio} />
        <div className="metrics">
          <Metric name="Total variance" value={f(b.total)} />
          <Metric
            name="Variance retained"
            value={percent(b.recon[mode].ratio)}
          />
        </div>
        <Eq
          tex={String.raw`\frac{\lambda_1}{\lambda_1+\lambda_2}=\frac{${
            f(b.values[0])
          }}{${f(b.total)}}=${percent(b.ratio).replace("%", String.raw`\%`)}`}
        />
      </>
    );
  }
  if (id === 20) {
    const r = b.recon[mode];
    return (
      <>
        {people}
        <Tabs
          labels={["Mean only", "One component", "Both components"]}
          value={mode}
          onChange={setMode}
        />
        <Plot
          points={b.raw}
          second={r.raw}
          selected={p}
          onSelect={setPerson}
          bound={10}
          labels={["Test A · original units", "Test B · original units"]}
        />
        <Card>
          <span>
            Person {labels[p]}: original <b>{point(b.raw[p])}</b>
          </span>
          <span>
            Reconstruction <b>{point(r.raw[p])}</b>
          </span>
          <span>
            Squared distance lost <b>{f(r.loss[p])}</b>
          </span>
        </Card>
      </>
    );
  }
  if (id === 21) {
    return (
      <>
        {people}
        <Plot
          points={b.points}
          second={fr.projected}
          selected={p}
          onSelect={setPerson}
          w={fr.w}
          onAngle={setAngle}
          triangle
        />
        {rotation}
        <div className="identity">
          <Metric name="Original²" value={f(fr.lengths[p])} />
          <b>=</b>
          <Metric name="Kept²" value={f(fr.kept[p])} />
          <b>+</b>
          <Metric name="Lost²" value={f(fr.lost[p])} />
        </div>
        <Card>
          Across everyone: {f(b.total)} = {f(fr.variance)} + {f(fr.loss)}{" "}
          <span className="quiet">All three totals are divided by n−1.</span>
        </Card>
      </>
    );
  }
  if (id === 22) {
    return (
      <>
        <Range
          label="Required variance retained"
          value={value || 90}
          min={1}
          max={100}
          suffix="%"
          onChange={setValue}
        />
        <Tabs
          labels={["k = 0", "k = 1", "k = 2"]}
          value={mode}
          onChange={setMode}
        />
        <Budget ratio={b.recon[mode].ratio} />
        <Metric name="Lost spread / (n−1)" value={f(b.recon[mode].totalLoss)} />
        <Card>
          {b.recon[mode].ratio * 100 + 1e-6 < (value || 90)
            ? "This choice misses your target."
            : mode > 0 && b.recon[mode - 1].ratio * 100 + 1e-6 >= (value || 90)
            ? "Target met, but a smaller k also meets it."
            : "Target met with the smallest sufficient k."}
        </Card>
      </>
    );
  }
  if (id === 23 || id === 24) {
    const d = lab.scales[value][show ? "standard" : "raw"];
    return (
      <>
        <Range
          label="Multiply test B units by"
          min={1}
          max={10}
          value={value + 1}
          suffix="×"
          onChange={(v) => setValue(v - 1)}
        />
        {id === 24 && (
          <label className="check">
            <input
              type="checkbox"
              checked={show}
              onChange={(e) => setShow(e.target.checked)}
            />Standardize both features
          </label>
        )}
        <div className="mini-split">
          <Plot
            points={d.points}
            axes={d.axes}
            selected={p}
            onSelect={setPerson}
            labels={show
              ? ["A · standard deviations", "B · standard deviations"]
              : ["Test A · points", "Test B · rescaled points"]}
          />
          <div>
            <Matrix data={d.cov} />
            <Metric name="PC1 angle" value={`${f(d.angle, 1)}°`} />
            <Metric name="Variance retained" value={percent(d.ratio)} />
          </div>
        </div>
        <Eq tex={id === 24 ? c.equations.standard : c.equations.matrix} />
      </>
    );
  }
  if (id === 25) {
    const d = lab.edgeCases[mode];
    return (
      <>
        <Tabs
          labels={["Original", "Add one outlier", "Circular cloud"]}
          value={mode}
          onChange={setMode}
        />
        <Plot points={d.points} axes={d.axes} />
        <div className="metrics">
          <Metric name="Largest eigenvalue" value={f(d.values[0])} />
          <Metric name="Second eigenvalue" value={f(d.values[1])} />
          <Metric name="PC1 share" value={percent(d.ratio)} />
        </div>
        <Card>
          {mode === 0
            ? "A clear longest direction."
            : mode === 1
            ? "The squared-distance objective pays a large price for missing the faraway point."
            : "Equal eigenvalues: the displayed axes are one valid choice among infinitely many."}
        </Card>
      </>
    );
  }
  if (id === 26) {
    const d = lab.nuisance;
    return (
      <>
        <Tabs
          labels={["Original features", "Only PC1 retained"]}
          value={mode}
          onChange={setMode}
        />
        <label className="check">
          <input
            type="checkbox"
            checked={show}
            onChange={(e) => setShow(e.target.checked)}
          />Reveal the two categories
        </label>
        <Plot
          points={mode ? d.recon[1].points : d.points}
          axes={d.axes}
          category={show}
        />
        <Budget ratio={d.ratio} />
        <Card>
          {mode
            ? "The top and bottom categories now land on exactly the same four positions."
            : "Categories differ by vertical position. The large horizontal spread is unrelated to the category."}
        </Card>
      </>
    );
  }
  if (id === 27) {
    const d = lab.challenge, frame = d.frames[value];
    return (
      <>
        <Plot
          points={d.points}
          second={frame.projected}
          w={frame.w}
          onAngle={(v) => {
            if (!show) setValue(v);
          }}
        />
        <Range
          label="Your proposed angle"
          value={value}
          onChange={(v) => {
            if (!show) setValue(v);
          }}
        />
        <Metric name="Retained spread" value={percent(frame.ratio)} />
        <label className="reason-label">
          Why this axis?<textarea
            aria-label="Reason for your chosen axis"
            value={reason}
            disabled={show}
            onChange={(e) => setReason(e.target.value)}
            placeholder="Describe what happens to the projected scores."
          />
        </label>
        <button
          className="primary"
          disabled={!reason.trim() || show}
          onClick={() => {
            setShow(true);
            record({
              question: "Find PC1 in the rotated cloud",
              answer: `${value} degrees`,
              reason,
              correct: d.values[0] - frame.variance < .02,
            });
          }}
        >
          Submit this axis
        </button>
        {show && (
          <Card>
            {d.values[0] - frame.variance < .02
              ? "Your axis is close to the maximum."
              : "There is still more spread to keep."} Best axis ≈{" "}
            {f(d.angle, 1)}°. Your written reason still needs review.
          </Card>
        )}
      </>
    );
  }
  if (id === 28) {
    const d = sandbox;
    if (!d) return <p>Waiting for the notebook sandbox…</p>;
    const frame = d.frames[value];
    return (
      <>
        <div className="native-controls">
          <marimo-cell name="masterclass_controls" />
        </div>
        <div className="mini-split">
          <Plot
            points={d.points}
            second={frame.projected}
            w={frame.w}
            onAngle={setValue}
          />
          <div>
            <Matrix data={d.cov} />
            <Metric name="New mean" value={point(d.mean)} />
            <Metric name="PC1 angle" value={`${f(d.angle, 1)}°`} />
          </div>
        </div>
        <Range label="Sandbox direction" value={value} onChange={setValue} />
        <Budget ratio={frame.ratio} />
        <p className="quiet">
          Move a score slider and release it to commit. Then drag the axis;
          those frames come from the new notebook calculation.
        </p>
      </>
    );
  }
  if (id === 29) {
    return (
      <>
        <Steps steps={c.svdSteps} />
        <Tabs
          labels={["Keep one singular direction", "Keep both"]}
          value={mode}
          onChange={setMode}
        />
        <Bars
          values={b.singular}
          labels={["Singular value σ₁", "Singular value σ₂"]}
        />
        <Card>
          {mode + 1} retained direction{mode ? "s" : ""} ·{" "}
          {percent(b.recon[mode + 1].ratio)} of variance · reconstruction loss
          {" "}
          {f(b.recon[mode + 1].totalLoss)}
        </Card>
      </>
    );
  }
  if (id === 30) {
    return (
      <>
        <Steps steps={c.calculusSteps} />
        <Tabs
          labels={["Differentiate in a", "Differentiate in b"]}
          value={mode}
          onChange={setMode}
        />
        <Eq
          tex={mode
            ? String.raw`\partial_b f=2S_{AB}a+2S_{BB}b`
            : String.raw`\partial_a f=2S_{AA}a+2S_{AB}b`}
        />
        <Card>
          {mode
            ? "Hold a fixed; change only the b coordinate."
            : "Hold b fixed; change only the a coordinate."}
        </Card>
      </>
    );
  }
  return <Assessment course={c} record={record} jumpCore={jumpCore} />;
}
