export type Point = [number, number];
export const RAW: Point[] = [[8, 7], [7, 8], [5, 4], [4, 5]];
export const dot = (a: Point, b: Point) => a[0] * b[0] + a[1] * b[1];
export function model(raw: Point[], angle = 45) {
  const n = raw.length,
    mean = raw.reduce(
      (s, p) => [s[0] + p[0] / n, s[1] + p[1] / n] as Point,
      [0, 0] as Point,
    );
  const points = raw.map((p) => [p[0] - mean[0], p[1] - mean[1]] as Point);
  const cov = [[0, 0], [0, 0]];
  for (const p of points) {
    for (let i = 0; i < 2; i++) {
      for (let j = 0; j < 2; j++) cov[i][j] += p[i] * p[j] / (n - 1);
    }
  }
  const t = angle * Math.PI / 180, w: Point = [Math.cos(t), Math.sin(t)];
  const scores = points.map((p) => dot(p, w));
  const reconstructed = points.map((_, i) =>
    [scores[i] * w[0], scores[i] * w[1]] as Point
  );
  const losses = points.map((p, i) =>
    dot([p[0] - reconstructed[i][0], p[1] - reconstructed[i][1]], [
      p[0] - reconstructed[i][0],
      p[1] - reconstructed[i][1],
    ])
  );
  const variance = scores.reduce((s, z) => s + z * z, 0) / (n - 1),
    loss = losses.reduce((s, z) => s + z, 0) / (n - 1);
  const trace = cov[0][0] + cov[1][1],
    delta = Math.hypot(cov[0][0] - cov[1][1], 2 * cov[0][1]);
  const eigenvalues = [(trace + delta) / 2, (trace - delta) / 2];
  const bestAngle =
    (Math.atan2(2 * cov[0][1], cov[0][0] - cov[1][1]) * 90 / Math.PI + 180) %
    180;
  return {
    mean,
    points,
    cov,
    w,
    scores,
    reconstructed,
    losses,
    variance,
    loss,
    total: trace,
    eigenvalues,
    bestAngle,
  };
}
export const fixed = (x: number, d = 2) =>
  Math.abs(x) < 1e-9 ? "0" : x.toFixed(d);
