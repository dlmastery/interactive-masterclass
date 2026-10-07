import { useState } from "react";
import {
  Bars,
  Card,
  type Course,
  DataTable,
  Eq,
  f,
  type Lab,
  Metric,
  People,
  Plot,
  type Point,
  point,
  Practice,
  Range,
  type RecordAttempt,
  Tabs,
} from "./LabComponents.tsx";
type Props = {
  id: string;
  lab: Lab;
  course: Course;
  person: number;
  setPerson: (i: number) => void;
  angle: number;
  setAngle: (a: number) => void;
  record: RecordAttempt;
};
export function BridgeLab(
  { id, lab, course, person: p, setPerson, angle, setAngle, record }: Props,
) {
  const [mode, setMode] = useState(0),
    [step, setStep] = useState(0),
    [show, setShow] = useState(false);
  const b = lab.base,
    fr = b.frames[angle],
    people = <People selected={p} setSelected={setPerson} />;
  if (course.bridgeProblems[id]) {
    return <Practice problem={course.bridgeProblems[id]} record={record} />;
  }
  if (id === "vector" || id === "coordinates") {
    return (
      <>
        {people}
        {id === "vector"
          ? (
            <Tabs
              labels={["Point", "Position vector"]}
              value={mode}
              onChange={setMode}
            />
          )
          : (
            <label className="check">
              <input
                type="checkbox"
                checked={show}
                onChange={(e) => setShow(e.target.checked)}
              />Show coordinate guide lines
            </label>
          )}
        <Plot
          points={b.raw}
          selected={p}
          onSelect={setPerson}
          guides={id === "coordinates" ? show : false}
          vectors={mode ? [b.raw[p]] : undefined}
          vectorLabels={["x"]}
          bound={10}
          labels={["Test A · points", "Test B · points"]}
        />
        <Eq
          tex={String.raw`x_${lab.people[p]}=\begin{bmatrix}${
            f(b.raw[p][0], 0)
          }\\${f(b.raw[p][1], 0)}\end{bmatrix}\in\mathbb R^2`}
        />
      </>
    );
  }
  if (id === "sigma") {
    return (
      <>
        <Range
          label="People included in the sum"
          min={1}
          max={4}
          value={step + 1}
          suffix=""
          onChange={(v) => setStep(v - 1)}
        />
        <DataTable
          rows={b.raw.slice(0, step + 1)}
          selected={p}
          onSelect={setPerson}
        />
        <Eq
          tex={String.raw`\sum_{i=1}^{${step + 1}} x_{iA}=${
            b.raw.slice(0, step + 1).map((v) => f(v[0], 0)).join("+")
          }`}
        />
        <Card>
          {step === 3
            ? `All ${b.n} observations included. Mean = ${f(b.mean[0])}.`
            : "This is a partial sum. Add the remaining people before computing the full-group mean."}
        </Card>
      </>
    );
  }
  if (id === "subtract") {
    return (
      <>
        {people}
        <Tabs
          labels={["Test A coordinate", "Test B coordinate"]}
          value={mode}
          onChange={setMode}
        />
        <div className="large-number">
          {f(b.raw[p][mode], 0)} − {f(b.mean[mode], 0)} ={" "}
          <b>{f(b.points[p][mode], 0)}</b>
        </div>
        <Plot points={b.points} selected={p} onSelect={setPerson} guides />
        <Card>
          Person {lab.people[p]}: {point(b.raw[p])} → {point(b.points[p])}
        </Card>
      </>
    );
  }
  if (id === "square") {
    return (
      <>
        {people}
        <Tabs labels={["Test A", "Test B"]} value={mode} onChange={setMode} />
        <div className="squares">
          <div
            style={{
              width: `${Math.abs(b.points[p][mode]) * 75}px`,
              height: `${Math.abs(b.points[p][mode]) * 75}px`,
            }}
          >
            <span>{f(b.squared[p][mode], 0)} square units</span>
          </div>
        </div>
        <Eq
          tex={String.raw`(${f(b.points[p][mode], 0)})^2=${
            f(b.squared[p][mode], 0)
          }`}
        />
        <Bars
          values={b.squared.map((v) => v[mode])}
          labels={lab.people}
          highlight={p}
        />
      </>
    );
  }
  if (id === "signs") {
    const d = lab.covCases[mode];
    return (
      <>
        {people}
        <Tabs
          labels={["Together", "Opposite", "Cancelling"]}
          value={mode}
          onChange={(v) => {
            setMode(v);
            setShow(false);
          }}
        />
        <Card>
          <span>Person {lab.people[p]}</span>
          <div className="large-number">
            ({f(d.points[p][0], 0)}) × ({f(d.points[p][1], 0)})
          </div>
          <button onClick={() => setShow(true)}>Reveal this product</button>
          {show && (
            <strong className="large-number">
              {f(d.products[p][0][1], 0)}
            </strong>
          )}
        </Card>
        <Plot
          points={d.points}
          selected={p}
          onSelect={(i) => {
            setPerson(i);
            setShow(false);
          }}
          guides
        />
      </>
    );
  }
  if (id === "shape") {
    return (
      <>
        <Tabs
          labels={["Xc × Xc", "Xcᵀ × Xc", "Xc × Xcᵀ"]}
          value={mode}
          onChange={setMode}
        />
        <div className="shape-product">
          <Card>{mode === 1 ? "2 × 4" : "4 × 2"}</Card>
          <b>×</b>
          <Card>{mode === 2 ? "2 × 4" : "4 × 2"}</Card>
        </div>
        <Card>
          {mode === 0
            ? "Inside dimensions 2 and 4 disagree. This product is not defined."
            : mode === 1
            ? "Inside dimensions 4 and 4 match. The result is 2×2: one entry per feature pair."
            : "Inside dimensions 2 and 2 match. The result is 4×4: one entry per person pair, not the covariance matrix of features."}
        </Card>
      </>
    );
  }
  if (id === "transpose") {
    return (
      <>
        {people}
        <Tabs
          labels={["Xc · 4 rows × 2 columns", "Xcᵀ · 2 rows × 4 columns"]}
          value={mode}
          onChange={setMode}
        />
        {mode
          ? (
            <div className="transpose-table">
              <div>
                <b>Feature</b>
                {lab.people.map((s) => <b key={s}>{s}</b>)}
              </div>
              {[0, 1].map((j) => (
                <div key={j}>
                  <b>Test {j ? "B" : "A"}</b>
                  {b.points.map((v, i) => (
                    <span key={i} className={i === p ? "selected" : ""}>
                      {f(v[j], 0)}
                    </span>
                  ))}
                </div>
              ))}
            </div>
          )
          : <DataTable rows={b.points} selected={p} onSelect={setPerson} />}
        <Eq tex={course.bridges.transpose[4]} />
      </>
    );
  }
  if (id === "blend") {
    const frame = b.frames[[0, 45, 135][mode]];
    return (
      <>
        {people}
        <Tabs
          labels={["Test A alone", "Together", "Contrast"]}
          value={mode}
          onChange={setMode}
        />
        <Plot
          points={b.points}
          second={frame.projected}
          w={frame.w}
          selected={p}
          onSelect={setPerson}
        />
        <Card>
          Weights {point(frame.w)} → Person {lab.people[p]} score{" "}
          <strong>{f(frame.z[p])}</strong>
        </Card>
      </>
    );
  }
  if (id === "unitcircle") {
    return (
      <>
        <Plot
          points={[]}
          vectors={[fr.w]}
          vectorLabels={["w"]}
          bound={1.15}
          labels={["cos θ · horizontal weight", "sin θ · vertical weight"]}
        />
        <Range label="Unit direction angle" value={angle} onChange={setAngle} />
        <div className="metrics">
          <Metric name="cos θ" value={f(fr.w[0], 3)} />
          <Metric name="sin θ" value={f(fr.w[1], 3)} />
          <Metric name="Length" value="1" />
        </div>
        <Eq tex={course.bridges.unitcircle[4]} />
      </>
    );
  }
  if (id === "reverse") {
    return (
      <>
        <Tabs labels={["wᵀXcᵀ", "Xcᵀwᵀ"]} value={mode} onChange={setMode} />
        <div className="shape-product">
          <Card>{mode ? "2 × 4" : "1 × 2"}</Card>
          <b>×</b>
          <Card>{mode ? "1 × 2" : "2 × 4"}</Card>
        </div>
        <Card>
          {mode
            ? "The inside dimensions 4 and 1 do not match."
            : "The inside dimensions match. The product has shape 1×4, exactly the shape of zᵀ."}
        </Card>
        <button onClick={() => setShow(!show)}>Reveal the general rule</button>
        {show && <Eq tex={course.bridges.reverse[4]} />}
      </>
    );
  }
  if (id === "norm") {
    const v = mode ? b.axes[0] : [1, 1] as Point;
    return (
      <>
        <Tabs
          labels={["Direction (1,1)", "Normalize to length 1"]}
          value={mode}
          onChange={setMode}
        />
        <Plot
          points={[]}
          vectors={[v]}
          vectorLabels={["w"]}
          bound={1.8}
          labels={["Weight A", "Weight B"]}
        />
        <Eq
          tex={mode
            ? String.raw`\widehat w=(1/\sqrt2,1/\sqrt2),\quad\|\widehat w\|=1`
            : String.raw`w=(1,1),\quad\|w\|=\sqrt{1^2+1^2}=\sqrt2`}
        />
        <Card>Current weights: {point(v)}</Card>
      </>
    );
  }
  if (id === "matvec") {
    return (
      <>
        <Range
          label="Input direction angle"
          value={angle}
          onChange={setAngle}
        />
        <Tabs
          labels={["Output row A", "Output row B"]}
          value={mode}
          onChange={setMode}
        />
        <Eq
          tex={String.raw`(${f(b.cov[mode][0])})(${f(fr.w[0])})+(${
            f(b.cov[mode][1])
          })(${f(fr.w[1])})=${f(fr.sw[mode])}`}
        />
        <Plot
          points={[]}
          vectors={[fr.w, fr.sw]}
          vectorLabels={["input w", "output Sw"]}
          bound={7}
          labels={["Coordinate 1", "Coordinate 2"]}
        />
      </>
    );
  }
  if (id === "identity") {
    return (
      <>
        <Tabs
          labels={["λ = 0", "λ = 2/3", "λ = 10/3", "λ = 6"]}
          value={mode}
          onChange={setMode}
        />
        <Eq tex={course.bridges.identity[4]} />
        <Card>
          {mode === 1 || mode === 3
            ? (
              <>
                <strong>Determinant is zero.</strong>
                <p>
                  A nonzero vector can solve (S−λI)w=0. This candidate is an
                  eigenvalue.
                </p>
              </>
            )
            : (
              <>
                <strong>Determinant is nonzero.</strong>
                <p>
                  The only solution is w=0, which cannot be a direction. This
                  candidate is not an eigenvalue.
                </p>
              </>
            )}
        </Card>
        <MatrixSketch />
        <p className="quiet">
          Subtract λ only from the diagonal; off-diagonal entries stay
          unchanged.
        </p>
      </>
    );
  }
  if (id === "perpendicular") {
    const v = mode ? b.axes[0] : b.axes[1];
    return (
      <>
        <Tabs
          labels={["Use perpendicular PC2", "Duplicate PC1"]}
          value={mode}
          onChange={setMode}
        />
        <Plot
          points={[]}
          vectors={[b.axes[0], v]}
          vectorLabels={["PC1", mode ? "same PC1" : "PC2"]}
          bound={1.5}
          labels={["Weight A", "Weight B"]}
        />
        <Eq
          tex={mode ? String.raw`v_1^\top v_1=1` : String.raw`v_1^\top v_2=0`}
        />
        <Card>
          {mode
            ? "Same direction, same scores. No new coordinate was learned."
            : "A right angle. The second coordinate measures the remaining direction."}
        </Card>
      </>
    );
  }
  if (id === "trace") {
    return (
      <>
        <Tabs
          labels={[
            "Original feature variances",
            "Principal-component variances",
          ]}
          value={mode}
          onChange={setMode}
        />
        <Bars
          values={mode ? b.values : [b.cov[0][0], b.cov[1][1]]}
          labels={mode ? ["PC1", "PC2"] : ["Test A", "Test B"]}
        />
        <Metric name="Same total squared spread / (n−1)" value={f(b.total)} />
        <Eq tex={course.bridges.trace[4]} />
      </>
    );
  }
  if (id === "std") {
    const d = lab.scales[step].raw;
    return (
      <>
        <Range
          label="Multiply test B units by"
          min={1}
          max={10}
          value={step + 1}
          suffix="×"
          onChange={(n) => setStep(n - 1)}
        />
        <div className="metrics">
          <Metric name="B variance · units²" value={f(d.cov[1][1])} />
          <Metric name="B standard deviation · units" value={f(d.std[1])} />
        </div>
        <Eq tex={course.bridges.std[4]} />
        <Plot points={d.points} axes={d.axes} />
      </>
    );
  }
  if (id === "correlation") {
    const d = lab.covCases[mode];
    return (
      <>
        <Tabs
          labels={["Together", "Opposite", "Cancelling"]}
          value={mode}
          onChange={setMode}
        />
        <Plot points={d.points} selected={p} onSelect={setPerson} />
        <div className="metrics">
          <Metric name="Covariance · points²" value={f(d.cov[0][1])} />
          <Metric name="Correlation · no units" value={f(d.corr[0][1])} />
        </div>
        <Eq tex={course.bridges.correlation[4]} />
      </>
    );
  }
  return null;
}
function MatrixSketch() {
  return (
    <Eq
      tex={String
        .raw`I=\begin{bmatrix}1&0\\0&1\end{bmatrix},\quad S-\lambda I=\begin{bmatrix}10/3-\lambda&8/3\\8/3&10/3-\lambda\end{bmatrix}`}
    />
  );
}
