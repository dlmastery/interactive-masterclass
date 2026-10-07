import importlib.util
from pathlib import Path
import numpy as np

path=Path('outputs/pca-studio/pca_lesson.py').resolve()
spec=importlib.util.spec_from_file_location('pca_lesson',path)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
outputs, d=module.app.run()
X, S, W = d['Xc'], d['S'], d['W']
np.testing.assert_allclose(X.mean(axis=0),0,atol=1e-12)
np.testing.assert_allclose(S,[[4,3],[3,4]],atol=1e-12)
np.testing.assert_allclose(d['eigenvalues'],[7,1],atol=1e-12)
np.testing.assert_allclose(W.T@W,np.eye(2),atol=1e-12)
np.testing.assert_allclose(S@W,W*d['eigenvalues'],atol=1e-12)
np.testing.assert_allclose(np.cov(d['scores'],rowvar=False),np.diag([7,1]),atol=1e-12)
np.testing.assert_allclose(d['scores']@W.T,X,atol=1e-12)
np.testing.assert_allclose(d['cloud']['reconstructionLoss'],1,atol=1e-12)
np.testing.assert_allclose(d['cloud']['retained'],.875,atol=1e-12)
np.testing.assert_allclose(d['cloud']['variance']+d['cloud']['loss'],np.trace(S),atol=1e-12)
example_S=np.array([[10,8],[8,10]])/3
np.testing.assert_allclose(d['example_S'],example_S,atol=1e-12)
np.testing.assert_allclose(np.linalg.eigvalsh(example_S),[2/3,6],atol=1e-12)
assert abs(d['example']['ratio']-.9)<1e-12
for degrees in (0,17,45,90,135,180):
    direction=np.array([np.cos(np.deg2rad(degrees)),np.sin(np.deg2rad(degrees))])
    score=X@direction
    kept=np.var(score,ddof=1)
    residual=X-np.outer(score,direction)
    np.testing.assert_allclose(kept,np.dot(direction,S@direction),atol=1e-12)
    np.testing.assert_allclose(kept+np.sum(residual**2)/47,8,atol=1e-12)
print('PASS: centering, covariance, eigenpairs, orthogonality, diagonal score covariance, full reconstruction, discarded-variance loss, 90% worked example, and six projection directions.')
