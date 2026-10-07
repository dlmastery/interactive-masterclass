# Course map and inference coverage

| Chapter | Scenes | Question |
|---|---|---|
| 1 | 1–7 | Can one number describe a point? |
| 2 | 8–15 | How do we keep the right detail? |
| 3 | 16–24 | Why does covariance appear? |
| 4 | 25–34 | Why do eigenvectors win? |
| 5 | 35–46 | What if we keep more directions? |
| 6 | 47–58 | How do we use PCA well? |
| 7 | 59–72 | When does PCA mislead us? |
| 8 | 73–84 | Can you explain and transfer it? |

## Coverage witnesses

| Requested capability | Scenes |
|---|---|
| Purpose, geometry, encoder/decoder | 1–7 |
| JIT mean, dot product, Pythagoras, variance | 5–12; 21 |
| Covariance from squared projection, matrix shapes | 16–24 |
| Tangent/gradient/Lagrange necessary condition | 25–29 |
| Eigenbasis and global rank-one proof | 30–34 |
| Orthonormal scores, projection, global top-k bound | 35–40 |
| Exact loss, SVD, rank, code | 41–46 |
| Metric, scaling, whitening, k, fit/transform discipline | 47–58 |
| Limits → diagnosis → response → cost → alternatives | 59–67 |
| Documented Seurat, DINOv2, temporal examples | 68–70 |
| Native notebook live diagnosis | 71 |
| Practical decision | 72 |
| Six explanation lenses, new cases, delayed retrieval | 73–84 |

The learning route is organized by useful questions. Source-level inference dependencies are the route in ROUTE-SYNTHESIS.md; rebuilding an earlier mathematical definition reopens its later proof, code, narration, and assessment witnesses. The global rank-one proof is reached by scene32; foundations do not consume a separate prerequisite course.