"""Track tutorial gates and evidence freshness; does not grade teaching or call AI."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

STAGES = ('intake', 'research', 'debate', 'plan', 'pilot', 'build', 'review', 'delivery')


def stamp():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_state(path, state):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def load_state(directory):
    path = Path(directory).resolve() / 'run.json'
    state = json.loads(path.read_text(encoding='utf-8'))
    if state.get('schema') != 1 or list(state.get('gates', {})) != list(STAGES):
        raise ValueError('Unknown or malformed harness state.')
    return path, state


def freshness(gate):
    if gate['status'] != 'pass':
        return False, gate['status']
    if not gate.get('evidence'):
        return False, 'missing evidence'
    for item in gate['evidence']:
        path = Path(item['path'])
        if not path.is_file():
            return False, 'missing: ' + str(path)
        if digest(path) != item['sha256']:
            return False, 'changed: ' + str(path)
    return True, 'current'


def initialize(directory, topic, audience):
    root = Path(directory).resolve()
    root.mkdir(parents=True, exist_ok=True)
    path = root / 'run.json'
    if path.exists():
        raise ValueError('Run already exists; inspect or revise it instead of overwriting.')
    state = {
        'schema': 1, 'topic': topic, 'audience': audience, 'created_utc': stamp(),
        'execution_mode': 'coordinator-driven; evidence recorder only',
        'gates': {stage: {'status': 'pending', 'evidence': []} for stage in STAGES},
        'history': [],
    }
    write_state(path, state)
    return path


def record(directory, stage, status, evidence, note):
    path, state = load_state(directory)
    index = STAGES.index(stage)
    if not note.strip():
        raise ValueError('A concrete observation or revision reason is required.')
    if status == 'pass':
        for earlier in STAGES[:index]:
            fresh, reason = freshness(state['gates'][earlier])
            if not fresh:
                raise ValueError(f'Cannot pass {stage}: {earlier} is {reason}.')
        if not evidence:
            raise ValueError('A pass needs evidence from executed work.')
    files = []
    for value in evidence:
        item = Path(value).resolve()
        if item == path or not item.is_file():
            raise ValueError('Evidence must be an existing file other than run.json: ' + str(item))
        files.append({'path': str(item), 'sha256': digest(item)})
    event = {'stage': stage, 'status': status, 'note': note, 'evidence': files, 'time_utc': stamp()}
    state['gates'][stage] = event.copy()
    invalidated = []
    for later in STAGES[index + 1:]:
        if state['gates'][later]['status'] != 'pending':
            invalidated.append(later)
        state['gates'][later] = {'status': 'pending', 'evidence': []}
    state['history'].append({**event, 'invalidated': invalidated})
    write_state(path, state)
    return event


def report(directory):
    _, state = load_state(directory)
    rows = []
    prior_ok = True
    for stage in STAGES:
        gate = state['gates'][stage]
        fresh, reason = freshness(gate)
        effective = 'pass' if fresh and prior_ok else 'pending'
        if gate['status'] == 'revise':
            effective = 'revise'
        elif gate['status'] == 'pass' and not fresh:
            effective = 'stale'
        elif gate['status'] == 'pass' and not prior_ok:
            effective = 'dependency invalid'
        rows.append({'stage': stage, 'recorded': gate['status'], 'effective': effective, 'evidence': reason})
        prior_ok = prior_ok and fresh
    return {'topic': state['topic'], 'gates': rows, 'all_gates_current': prior_ok,
            'qualification': 'Gate records do not independently establish teaching quality.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    init = commands.add_parser('init')
    init.add_argument('run_dir')
    init.add_argument('--topic', required=True)
    init.add_argument('--audience', required=True)
    rec = commands.add_parser('record')
    rec.add_argument('run_dir')
    rec.add_argument('--stage', required=True, choices=STAGES)
    rec.add_argument('--status', required=True, choices=('pass', 'revise'))
    rec.add_argument('--evidence', nargs='*', default=[])
    rec.add_argument('--note', required=True)
    stat = commands.add_parser('status')
    stat.add_argument('run_dir')
    args = parser.parse_args()
    try:
        if args.command == 'init':
            result = {'created': str(initialize(args.run_dir, args.topic, args.audience))}
        elif args.command == 'record':
            result = record(args.run_dir, args.stage, args.status, args.evidence, args.note)
        else:
            result = report(args.run_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(2, str(error) + '\n')


if __name__ == '__main__':
    main()
