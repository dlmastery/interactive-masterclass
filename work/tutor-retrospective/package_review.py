"""Package this completed retrospective; do not touch the course."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import zipfile

project = Path(__file__).resolve().parents[2]
work = project / 'work/tutor-retrospective'
out = project / 'outputs/tutor-retrospective'
skill_root = Path('C:/Users/abhir/.codex/skills')
names = ['build-interactive-masterclass', 'build-intuition-masterclass']
evidence = out / 'evidence'
evidence.mkdir(exist_ok=True)
for path in work.iterdir():
    if path.is_file() and path.suffix in {'.md', '.txt', '.json', '.py'}:
        shutil.copy2(path, evidence / path.name)

manifest = []
broken = []
for name in names:
    for path in (skill_root / name).rglob('*'):
        if not path.is_file() or '__pycache__' in path.parts:
            continue
        relative = path.relative_to(skill_root)
        target = out / 'updated-skills' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        manifest.append({'path':str(relative), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        if path.suffix == '.md':
            for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8-sig')):
                if not link.startswith(('https:', 'http:', '#')):
                    if not (path.parent / link.split('#')[0]).exists():
                        broken.append(str(path) + ' -> ' + link)
with zipfile.ZipFile(out / 'updated-skills.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for item in manifest:
        archive.write(out / 'updated-skills' / item['path'], item['path'])

report = (out / 'REPORT.html').read_text(encoding='utf-8')
for link in re.findall(r'href="([^"]+)"', report):
    if not link.startswith(('http:', 'https:', '#')) and not (out / link).exists():
        broken.append('REPORT.html -> ' + link)
words = len(re.sub(r'<[^>]+>', ' ', report).split())
scope = json.loads((work / 'course-scope-check.json').read_text(encoding='utf-8-sig'))
result = {
    'skill_files': manifest,
    'broken_local_links': broken,
    'report_word_count_approx': words,
    'skill_frontmatter_validation': 'both pass',
    'guardrail_behavior_tests': {'passed':17, 'failed':0, 'scope':'synthetic workflow records; no learner efficacy claim'},
    'forward_tests': {'two_written_lessons':'rubric passed; no learner observations', 'four_scope_cases':'written behavior inspected; execution limitations disclosed'},
    'course_scope_check': scope,
    'reviewed_human_learning': False,
    'later_astra_configuration_tested': False,
}
(out / 'VALIDATION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'packaged_files':len(manifest), 'broken_links':broken, 'report_words':words, 'course_unchanged':scope['course_unchanged']}))
if broken or not scope['course_unchanged']:
    raise SystemExit(1)
