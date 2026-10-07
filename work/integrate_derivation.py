from pathlib import Path
p=Path('outputs/pca-studio/v/lesson/src/PcaScenes.tsx')
s=p.read_text(encoding='utf-8')
a=s.index('  if (s.scene === "maximum") {')
b=s.index('  if (s.scene === "coordinates") {',a)
s=s[:a]+'''  if (s.scene === "maximum") {
    return split(
      <EigenbasisLab c={c} angle={angle} setAngle={setAngle} />,
      <>{eq}<p>{n === 45 ? "The two eigenvalues are equal. Every allocation reaches the same bound. No single direction wins." : "The coefficients can be positive or negative. Their squares are nonnegative and sum to one. The variance is a weighted average of the eigenvalues."}</p><details><summary>Why can these axes describe every direction?</summary><p>A real symmetric matrix has an orthonormal basis of eigenvectors. Covariance matrices are symmetric. We use this theorem here; the picture lets you test it in two dimensions.</p></details><div className="try"><small>TRY TO BEAT THE BOUND</small><p>Turn through the whole circle. Can either squared weight be negative? Can their weighted average exceed the larger eigenvalue?</p></div></>,
      "derivation-layout",
    );
  }
'''+s[b:]
p.write_text(s,encoding='utf-8')
