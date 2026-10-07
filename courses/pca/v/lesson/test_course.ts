/// <reference lib="deno.ns" />
import { scenes } from "./src/course.ts";
import { model, type Point } from "./src/math.ts";
// @deno-types="npm:@types/katex@0.16.7"
import katex from "katex";
function assert(ok: unknown, message: string): asserts ok {
  if (!ok) throw new Error(message);
}
Deno.test("Every delivered formula renders; scenes have complete narration and feedback", () => {
  assert(scenes.length >= 50, "Minimum requested scope missing");
  assert(
    new Set(scenes.map((s) => s.id)).size === scenes.length,
    "Duplicate scene IDs",
  );
  for (const s of scenes) {
    assert(s.notes.split(/\s+/).length >= 60, `${s.id}: narration too short`);
    for (
      const tex of [s.formula, ...(s.steps ?? []).map((x) => x[0])].filter(
        Boolean,
      )
    ) {
      katex.renderToString(tex!, { throwOnError: true, strict: "error" });
      assert(
        !/[\x00-\x08\x0b-\x1f]/.test(tex!),
        `${s.id}: control character in math`,
      );
    }
    if (s.choices) {
      assert(
        s.feedback?.length === s.choices.length,
        `${s.id}: feedback missing`,
      );
      assert(
        typeof s.correct === "number" && s.correct >= 0 &&
          s.correct < s.choices.length,
        `${s.id}: answer key out of range`,
      );
    }
  }
});
Deno.test("Browser geometry agrees with independent NumPy results", () => {
  const fixtures = JSON.parse(
    Deno.readTextFileSync(new URL("./math-fixtures.json", import.meta.url)),
  );
  for (const f of fixtures) {
    const actual = model(f.raw as Point[], f.angle);
    for (
      const key of [
        "mean",
        "cov",
        "eigenvalues",
        "variance",
        "loss",
        "scores",
        "reconstructed",
      ] as const
    ) {
      const flatten = (x: unknown): number[] =>
        Array.isArray(x) ? x.flat(Infinity) as number[] : [x as number];
      const a = flatten(actual[key]), b = flatten(f[key]);
      assert(a.length === b.length, `${key}: shape mismatch`);
      a.forEach((v, i) =>
        assert(Math.abs(v - b[i]) < 1e-8, `${key}: ${v} != ${b[i]}`)
      );
    }
  }
});
