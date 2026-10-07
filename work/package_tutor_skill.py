from pathlib import Path
import hashlib
import json
import shutil
import zipfile

source = Path('outputs/build-interactive-masterclass').resolve()
target = Path(r'C:\Users\abhir\.codex\skills\build-interactive-masterclass')
if target.exists():
    raise SystemExit('Skill target already exists; review before replacing.')
shutil.copytree(source, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
files = [p for p in source.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
for p in files:
    assert p.read_bytes() == (target/p.relative_to(source)).read_bytes()
archive = source.parent/'build-interactive-masterclass.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in files:
        z.write(p, Path(source.name)/p.relative_to(source))
report = {
    'skill': source.name,
    'installed_path': str(target),
    'automatic_discovery': 'default allowed; explicit invocation also available',
    'structural_validator': 'pass',
    'harness_tests': {'passed': 7, 'scope': ['skipped gate rejection', 'missing evidence rejection', 'changed evidence rejection', 'missing evidence detection', 'revision invalidates dependent gates', 're-review recovery', 'existing run preservation']},
    'creator_scenario_review': [
        {'case': 'PCA masterclass for a 20-year-old', 'decision': 'Full harness; geometry first; local mathematics bridges; core proof protected.'},
        {'case': 'Interactive tutorial on historical causation', 'decision': 'Full harness; sources and causal alternatives; no forced geometry, equations, or PCA widget.'},
        {'case': 'Fix one label in an existing lesson', 'decision': 'Small edit and affected validation; no full research/debate cycle.'},
        {'case': 'Videos inaccessible, transcripts available', 'decision': 'Use substantive accessible sources; label transcript-only visual limitations; no claim of watching.'},
        {'case': 'Only sentence lengths checked', 'decision': 'Do not claim 80% full STE compatibility.'}
    ],
    'independent_forward_test': 'not executed',
    'pedagogical_efficacy': 'not established by these checks',
    'files': {str(p.relative_to(source)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
}
(source.parent/'tutorial-skill-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Installed {len(files)} files at {target}')
print(f'Archive: {archive} ({archive.stat().st_size:,} bytes)')
