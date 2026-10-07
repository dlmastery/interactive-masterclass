def make_pca_case(raw, with_frames=True):
    raw = np.asarray(raw, dtype=float)
    n = len(raw)
    mu = raw.mean(0)
    xc = raw - mu
    cov = xc.T @ xc / (n - 1)
    vals, vec = np.linalg.eigh(cov)
    vals, vec = vals[::-1], vec[:, ::-1]
    vec *= np.where(vec[0] < 0, -1, 1)
    z = xc @ vec
    total = float(np.trace(cov))
    pack = lambda a: np.asarray(a).round(7).tolist()
    result = dict(raw=pack(raw), points=pack(xc), mean=pack(mu), cov=pack(cov),
        sums=pack(xc.T @ xc), values=pack(vals), axes=pack(vec.T), scores=pack(z),
        std=pack(np.sqrt(np.diag(cov))),corr=pack(cov / np.outer(np.sqrt(np.diag(cov)),np.sqrt(np.diag(cov)))),scoreCov=pack(z.T @ z / (n - 1)), scoreProducts=pack(z[:, 0] * z[:, 1]),
        total=total, ratio=float(vals[0] / total), n=n,
        angle=float(np.degrees(np.arctan2(vec[1, 0], vec[0, 0])) % 180),
        squared=pack(xc**2), signedSums=pack(xc.sum(0)), squaresSums=pack((xc**2).sum(0)),
        products=pack(np.einsum('ij,ik->ijk', xc, xc)),
        singular=pack(np.sqrt(np.maximum(vals, 0) * (n - 1))),
        recon=[], frames=[])
    for k in range(3):
        xhat = z[:, :k] @ vec[:, :k].T
        loss = np.sum((xc - xhat)**2, axis=1)
        result['recon'].append(dict(points=pack(xhat), raw=pack(xhat+mu),
            loss=pack(loss), totalLoss=float(loss.sum()/(n-1)),
            ratio=float(vals[:k].sum()/total)))
    if with_frames:
        for angle in range(181):
            theta = np.deg2rad(angle)
            w = np.array([np.cos(theta), np.sin(theta)])
            score = xc @ w
            projected = np.outer(score, w)
            residual = xc - projected
            kept = score**2
            lost = np.sum(residual**2, axis=1)
            sw = cov @ w
            tangent = np.array([-w[1], w[0]])
            result['frames'].append(dict(w=pack(w), sw=pack(sw), z=pack(score),
                terms=pack(xc*w), projected=pack(projected), residual=pack(residual),
                kept=pack(kept), lost=pack(lost), lengths=pack(np.sum(xc**2,axis=1)),
                variance=float(kept.sum()/(n-1)), loss=float(lost.sum()/(n-1)),
                sumSquares=float(kept.sum()), ratio=float(kept.sum()/(n-1)/total),
                slope=float(2*tangent@cov@w), turn=float(tangent@sw),
                eigen=bool(abs(tangent@sw)<1e-6)))
    return result

None
