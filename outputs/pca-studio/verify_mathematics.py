"""Independent numerical checks for the PCA masterclass.

Run in the lesson environment:
uv run --with marimo-studio==0.2.3 --with numpy==2.5.3 verify_mathematics.py
"""
from pathlib import Path
import importlib.util
import json
import numpy as np

source = Path(__file__).with_name("pca_lesson.py")
spec = importlib.util.spec_from_file_location("pca_masterclass", source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
_, values = module.app.run()
lab, course = values["pca_lab"], values["pca_course_v2"]
assert len(course["slides"]) == 64
assert [s['id'] for s in course['slides']] == list(range(1,65))
assert sum(len(s['steps']) for s in course['slides']) == 79

base = lab["base"]
np.testing.assert_allclose(base["cov"], [[10 / 3, 8 / 3], [8 / 3, 10 / 3]])
np.testing.assert_allclose(base["values"], [6, 2 / 3])
np.testing.assert_allclose(base["ratio"], 0.9)
np.testing.assert_allclose(base["corr"], [[1, .8], [.8, 1]])

frames_checked = 0
for case in [base, lab["challenge"], values["sandbox_lab"], *values['pca_cov_v2'], *values['pca_edges_v2']]:
    xc = np.asarray(case["points"])
    cov = xc.T @ xc / (case["n"] - 1)
    for frame in case["frames"]:
        w = np.asarray(frame["w"])
        np.testing.assert_allclose(w @ w, 1, atol=2e-7)
        np.testing.assert_allclose(frame["z"], xc @ w, atol=1e-6)
        np.testing.assert_allclose(frame["variance"], w @ cov @ w, atol=1e-6)
        np.testing.assert_allclose(frame["variance"] + frame["loss"], case["total"])
        residual=xc-np.asarray(frame['projected'])
        np.testing.assert_allclose(np.sum(residual**2)/(case['n']-1),frame['loss'],atol=2e-6)
        t=np.array([-w[1],w[0]])
        np.testing.assert_allclose(frame['slope'],2*t@cov@w,atol=3e-6)
        assert frame['variance'] <= case['values'][0]+2e-6
        frames_checked += 1
    np.testing.assert_allclose(case["recon"][2]["raw"], case["raw"])
    np.testing.assert_allclose(case["recon"][1]["totalLoss"], case["values"][1])

for state in lab["scales"]:
    np.testing.assert_allclose(state["standard"]["cov"], [[1, .8], [.8, 1]])
    np.testing.assert_allclose(state["standard"]["angle"], 45)
total_bytes=0
for name in ['pca_course_v2','pca_cov_v2','pca_edges_v2','pca_model_v2','pca_scales_v2','sandbox_lab']:
    encoded_size = len(json.dumps(values[name]).encode("utf-8"))
    assert encoded_size < 1_000_000, (name, encoded_size)
    total_bytes += encoded_size
assert total_bytes < 1_000_000, total_bytes

xc=np.asarray(base['points'])
_,sigma,vt=np.linalg.svd(xc,full_matrices=False)
np.testing.assert_allclose(sigma**2/3,base['values'])
for a2 in np.linspace(0,1,101):
    w=np.sqrt(a2)*np.asarray(base['axes'][0])+np.sqrt(1-a2)*np.asarray(base['axes'][1])
    np.testing.assert_allclose(w@np.asarray(base['cov'])@w,6*a2+(2/3)*(1-a2),atol=1e-6)

print(f"PASS: 64 slides, 79 equation steps, {frames_checked} projection frames.")
print('Covariance, unit directions, scores, gradient, global bound, reconstruction, SVD, and standardization agree.')
print(f'Projected data total: {total_bytes:,} bytes.')
