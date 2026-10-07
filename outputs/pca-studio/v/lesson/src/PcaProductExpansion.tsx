import { useState } from "react";
import { type Case, Eq, f } from "./LabComponents.tsx";
import "./product-expansion.css";

type Props = {
  c: Case;
  angle: number;
  person: number;
  setPerson: (n: number) => void;
  step: number;
};

/** Steps 0–1: distribute; 2: combine; 3+: sum observations and divide. */
export function ProductExpansion({ c, angle, person, setPerson, step }: Props) {
  const [selected, setSelected] = useState(1);
  const p = Math.max(0, Math.min(person, c.points.length - 1));
  const frame = c.frames[Math.round(angle)] ?? c.frames[0];
  const point = c.points[p];
  const factors = point.map((x, i) => frame.w[i] * x);
  const name = (i: number) => String.fromCharCode(65 + i);
  const symbols = ["w_1x_{i1}", "w_2x_{i2}"];
  const products = [0, 1, 2, 3].map((i) =>
    factors[Math.floor(i / 2)] * factors[i % 2]
  );
  const row = Math.floor(selected / 2), col = selected % 2;
  const records = c.points.map(([x, y]) => {
    const a = frame.w[0] * x, b = frame.w[1] * y;
    return [a * a, 2 * a * b, b * b, (a + b) ** 2];
  });
  const totals = [0, 1, 2, 3].map((j) =>
    records.reduce((sum, values) => sum + values[j], 0)
  );
  const selectedCross = selected === 1 || selected === 2;
  return (
    <div
      role="region"
      className="product-expansion"
      data-phase={Math.min(step, 4)}
      aria-label="Expand a squared score"
    >
      <div className="product-observations" aria-label="Choose an observation">
        {c.points.map((xy, i) => (
          <button
            key={i}
            aria-pressed={i === p}
            onClick={() => setPerson(i)}
          >
            {name(i)} <span>({f(xy[0], 2)}, {f(xy[1], 2)})</span>
          </button>
        ))}
      </div>
      <p className="product-context">
        Observation{" "}
        {name(p)}. Multiply each term by both terms in the other bracket.
      </p>
      <Eq tex="(w_1x_{i1}+w_2x_{i2})(w_1x_{i1}+w_2x_{i2})" />
      <div className="product-factors">
        {factors.map((value, i) => (
          <div key={i} className={row === i || col === i ? "lit" : ""}>
            <Eq
              tex={String.raw`${symbols[i]}\approx(${f(frame.w[i], 3)})(${
                f(point[i], 2)
              })`}
            />
            <strong>{f(value, 3)}</strong>
          </div>
        ))}
      </div>
      <div
        className={"product-grid " + (step >= 2 ? "combine" : "")}
        role="group"
        aria-label="Four products; select one to inspect it"
      >
        {products.map((value, i) => {
          const r = Math.floor(i / 2), k = i % 2, cross = r !== k;
          return (
            <button
              key={i}
              className={cross ? "cross-product" : "square-product"}
              aria-pressed={selected === i}
              onClick={() => setSelected(i)}
              aria-label={`Product ${r + 1}, ${k + 1}: ${f(value, 3)}`}
            >
              <small>
                {cross ? "Cross-product" : `${r ? "Second" : "First"} square`}
              </small>
              <Eq tex={`(${symbols[r]})(${symbols[k]})`} />
              <strong>{f(value, 3)}</strong>
            </button>
          );
        })}
      </div>
      <div
        className={"product-inspect " + (selectedCross ? "cross-product" : "")}
        role="status"
        aria-live="polite"
      >
        <Eq
          tex={String.raw`(${f(factors[row], 3)})(${
            f(factors[col], 3)
          })\approx${f(products[selected], 3)}`}
        />
        <p>
          {selectedCross
            ? "The orange products use the same two factors in reverse order. They are equal, including when they are negative."
            : "This term multiplies one weighted coordinate by itself. Its value cannot be negative."}
        </p>
      </div>
      {step >= 2 && (
        <div className="product-combined">
          <span>Combine the two orange products</span>
          <Eq
            tex={`w_1w_2x_{i1}x_{i2}+w_2w_1x_{i2}x_{i1}=2w_1w_2x_{i1}x_{i2}`}
          />
          <strong>
            {f(products[1], 3)} + {f(products[2], 3)} ≈ {f(records[p][1], 3)}
          </strong>
        </div>
      )}
      <div className="product-local-total">
        <span>One observation: squared score</span>
        <Eq
          tex={String.raw`z_${name(p)}^2\approx(${f(frame.z[p], 3)})^2\approx${
            f(records[p][3], 3)
          }`}
        />
      </div>
      {step >= 3 && (
        <div className="product-aggregate">
          <h3>Now add across all {c.n} observations</h3>
          <p>
            The direction weights stay fixed. Each row supplies new coordinates.
          </p>
          <div className="product-data-head" aria-hidden="true">
            <span>Row</span>
            <span>First square</span>
            <span>Both cross-products</span>
            <span>Second square</span>
            <span>Score²</span>
          </div>
          {records.map((values, i) => (
            <button
              key={i}
              className="product-data-row"
              aria-pressed={i === p}
              onClick={() => setPerson(i)}
              aria-label={`Inspect observation ${name(i)}, squared score ${
                f(values[3], 3)
              }`}
            >
              <strong>{name(i)}</strong>
              {values.map((v, j) => <span key={j}>{f(v, 3)}</span>)}
            </button>
          ))}
          <div className="product-data-row product-sums">
            <strong>Sum</strong>
            {totals.map((v, j) => <span key={j}>{f(v, 3)}</span>)}
          </div>
          <div className="product-variance">
            <span>All observations: sample variance</span>
            <Eq
              tex={String.raw`V(w)=\frac{\sum_i z_i^2}{n-1}\approx\frac{${
                f(totals[3], 3)
              }}{${c.n - 1}}\approx${f(totals[3] / (c.n - 1), 3)}`}
            />
          </div>
          {step >= 4 && <Eq tex="V(w)=w_1^2S_{11}+2w_1w_2S_{12}+w_2^2S_{22}" />}
        </div>
      )}
      <p className="product-note">
        Coordinates are centered. Displayed numbers are rounded; calculations
        use full precision.
      </p>
    </div>
  );
}
