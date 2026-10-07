export type Kind =
  | "geometry"
  | "triangle"
  | "covariance"
  | "mixture"
  | "live"
  | "spectrum"
  | "scale"
  | "outlier"
  | "nuisance"
  | "curve"
  | "code"
  | "decision"
  | "lens"
  | "eigen"
  | "rank"
  | "matrix"
  | "proof"
  | "center";
export type Scene = {
  id: string;
  chapter: number;
  title: string;
  question: string;
  body: string;
  takeaway: string;
  kind: Kind;
  mode?: string;
  angle?: number;
  formula?: string;
  steps?: [string, string][];
  prompt?: string;
  choices?: string[];
  correct?: number;
  feedback?: string[];
  notes: string;
  refresh?: [string, string];
  source?: string;
  rubric?: string[];
  example?: string;
};
export const chapters = [
  "Can one number describe a point?",
  "How do we keep the right detail?",
  "Why does covariance appear?",
  "Why do eigenvectors win?",
  "What if we keep more directions?",
  "How do we use PCA well?",
  "When does PCA mislead us?",
  "Can you explain and transfer it?",
];
import core from "./core.json" with { type: "json" };
import more from "./rank-svd.json" with { type: "json" };
import practice from "./practice.json" with { type: "json" };
import transfer from "./transfer.json" with { type: "json" };
export const scenes: Scene[] = [
  ...core,
  ...more,
  ...practice,
  ...transfer,
] as Scene[];
