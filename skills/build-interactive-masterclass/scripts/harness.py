"""Check tutorial workflow records. Does not verify truth, learning, or tool use."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODES = {
    'audit': {'inspect', 'research', 'review', 'report'},
    'plan': {'inspect', 'research', 'plan', 'review', 'report'},
    'build': {'inspect', 'research', 'plan', 'review', 'report', 'implement', 'pilot', 'deliver'},
}
CLAIMS = {'artifact', 'correctness', 'interaction', 'visual', 'teaching-review',
          'simulated-learner', 'human-learning', 'retention', 'learner-tested'}
RELATIONS = {'author', 'author-informed', 'fresh-context', 'human'}
EVIDENCE = {'tool-observation', 'author-review', 'simulated-review',
            'human-study', 'source-inspection'}
LIMIT = 'Records are attestations. This tool does not verify truth, learning, independence, or prevent direct tool edits.'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def hashed(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def resolve(base, path):
    p = Path(path)
    return (p if p.is_absolute() else base / p).resolve()


def save(path, state):
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    tmp.replace(path)


def event(state, kind, value):
    entry = {'seq': len(state['history']) + 1, 'kind': kind, 'value': json.loads(json.dumps(value)),
             'time_utc': datetime.now(timezone.utc).isoformat()}
    state['history'].append(entry)
    return entry['seq']


def contract(path):
    path = Path(path).resolve()
    c, base = read(path), path.parent
    require(c.get('schema') == 2 and c.get('mode') in MODES, 'Expected schema 2 and a known mode.')
    require(nonempty(c.get('topic')) and nonempty(c.get('audience')), 'Topic and audience required.')
    roots = [resolve(base, p) for p in c.get('scope_roots', [])]
    require(bool(roots), 'At least one permitted output root is required.')
    nodes = {n['id']: n for n in c.get('nodes', [])}
    require(nodes and len(nodes) == len(c['nodes']), 'Node IDs must be unique.')
    for key, n in nodes.items():
        require(nonempty(key) and n.get('kind') in {'inference', 'artifact', 'check', 'pilot', 'delivery', 'report'}, 'Invalid node.')
        require(n.get('action') in MODES['build'], 'Unknown action: ' + key)
        require(isinstance(n.get('depends_on'), list) and set(n['depends_on']) <= nodes.keys(), 'Unknown dependencies: ' + key)
        require(isinstance(n.get('inputs'), list) and isinstance(n.get('outputs'), list), 'Input/output lists required: ' + key)
        require(n.get('required_claims') and set(n['required_claims']) <= CLAIMS, 'Claim types required: ' + key)
        if n.get('critical') and n['kind'] == 'inference':
            require('teaching-review' in n['required_claims'], 'Critical inference needs teaching review: ' + key)
            require(n['inputs'], 'Critical inference needs an input artifact: ' + key)
        if n['kind'] == 'pilot':
            require('teaching-review' in n['required_claims'], 'Pilot needs teaching review: ' + key)
            require(n['inputs'], 'Pilot needs an input artifact: ' + key)
        for output in n['outputs']:
            dest = resolve(base, output)
            require(any(dest.is_relative_to(r) for r in roots), 'Output outside permitted roots: ' + str(dest))
        require(n['outputs'] or n['action'] in {'inspect', 'review', 'research'}, 'Mutating/reporting action needs scoped outputs: ' + key)
    def visit(key, active):
        require(key not in active, 'Dependency cycle at ' + key)
        result = set()
        for dep in nodes[key]['depends_on']:
            result |= {dep} | visit(dep, active | {key})
        return result
    ancestors = {k: visit(k, set()) for k in nodes}
    critical = {k for k, n in nodes.items() if n['kind'] == 'inference' and n.get('critical')}
    for key, n in nodes.items():
        if n['kind'] == 'delivery' or n['action'] == 'deliver':
            require(n['kind'] == 'delivery' and n['action'] == 'deliver', 'Delivery kind/action must agree.')
            require(critical <= set(n.get('covers', [])) <= ancestors[key], 'Delivery must cover and depend on every critical inference: ' + key)
    return c, nodes, ancestors, base


def initialize(directory, contract_path):
    root = Path(directory).resolve()
    root.mkdir(parents=True, exist_ok=True)
    path = root / 'run.json'
    require(not path.exists(), 'Run exists; do not overwrite history.')
    cp = Path(contract_path).resolve()
    c, _, _, base = contract(cp)
    state = {'schema': 2, 'contract': str(cp), 'policy': {
        'mode': c['mode'], 'scope_roots': [str(resolve(base, p)) for p in c['scope_roots']]},
        'receipts': {}, 'findings': {}, 'history': []}
    event(state, 'init', {'contract_hash': sha(cp)})
    save(path, state)
    return {'created': str(path), 'qualification': LIMIT}


def load(directory):
    path = Path(directory).resolve() / 'run.json'
    s = read(path)
    require(s.get('schema') == 2, 'Legacy schema 1 is status-only; start a new run without promoting passes.')
    c, nodes, ancestors, base = contract(s['contract'])
    policy = {'mode': c['mode'], 'scope_roots': [str(resolve(base, p)) for p in c['scope_roots']]}
    require(policy == s['policy'], 'Run mode/scope is pinned; changing the file cannot grant authority.')
    require(all(set(i['nodes']) <= nodes.keys() and all(st['pilot_node'] in nodes for st in i['strategies']) for i in s['findings'].values()), 'Contract cannot remove nodes referenced by issue history.')
    return path, s, c, nodes, ancestors, base


def snapshot(key, c, nodes, base):
    n = nodes[key]
    inputs = {str(resolve(base, p)): sha(resolve(base, p)) if resolve(base, p).is_file() else 'missing' for p in n['inputs']}
    dependencies = {d: snapshot(d, c, nodes, base)['revision'] for d in n['depends_on']}
    revision = hashed({'topic': c['topic'], 'audience': c['audience'], 'node': n,
                       'inputs': inputs, 'dependencies': dependencies})
    return {'revision': revision, 'input_hashes': inputs}


def evidence(items, base):
    require(isinstance(items, list) and items, 'Evidence hashes required.')
    result = []
    for item in items:
        path = resolve(base, item['path'])
        require(path.is_file() and sha(path) == item.get('sha256'), 'Missing or changed evidence: ' + str(path))
        result.append({'path': str(path), 'sha256': item['sha256']})
    return result


def validate_receipt(file, c, nodes, base):
    file = Path(file).resolve()
    r = read(file)
    require(r.get('node') in nodes and r.get('claim_type') in CLAIMS, 'Unknown node/claim.')
    require(r.get('outcome') == 'pass', 'Acceptance receipt must report pass; use findings for failures.')
    require(all(nonempty(r.get(k)) for k in ('scenario', 'observed_result')), 'Scenario and observed result required.')
    reviewer = r.get('reviewer', {})
    require(reviewer.get('relationship') in RELATIONS and all(nonempty(reviewer.get(k)) for k in ('id', 'context')), 'Reviewer relationship and context required.')
    require(r.get('evidence_type') in EVIDENCE and isinstance(r.get('limitations'), list), 'Evidence type and limitations required.')
    current = snapshot(r['node'], c, nodes, base)
    require('missing' not in current['input_hashes'].values(), 'A reviewed input is missing.')
    require(r.get('revision') == current['revision'] and r.get('input_hashes') == current['input_hashes'], 'Receipt does not bind current inputs/dependencies.')
    if r['claim_type'] == 'simulated-learner':
        require(r['evidence_type'] == 'simulated-review', 'Simulated learner claim needs simulated-review evidence.')
    if r['claim_type'] in {'human-learning', 'retention', 'learner-tested'}:
        counts = r.get('human_evidence', {})
        require(r['evidence_type'] == 'human-study', 'Human claim requires human-study evidence, not a simulation.')
        require(all(type(counts.get(k)) is int and counts[k] > 0 for k in ('participants', 'tasks')), 'Positive participant/task counts required.')
        if r['claim_type'] == 'retention':
            require(isinstance(counts.get('delay_days'), (int, float)) and counts['delay_days'] > 0, 'Retention needs a positive observed delay.')
    r['evidence'] = evidence(r.get('evidence'), file.parent)
    return {'data': r, 'path': str(file), 'sha256': sha(file)}


def fresh(receipt, current):
    try:
        require(receipt['data']['revision'] == current['revision'], 'Inputs or dependencies changed.')
        require(sha(receipt['path']) == receipt['sha256'], 'Receipt changed.')
        evidence(receipt['data']['evidence'], Path('.'))
        return True, 'current'
    except (OSError, ValueError):
        return False, 'stale inputs, receipt, or evidence'


def affected(issue, key, ancestors):
    return bool(set(issue['nodes']) & ({key} | ancestors[key]))


def unresolved(issue, c, nodes, base):
    if issue['status'] == 'open':
        return True
    return any(not fresh(r, snapshot(r['data']['node'], c, nodes, base))[0]
               for r in issue.get('resolution', []))


def inspect_state(s, c, nodes, ancestors, base):
    result = {}
    def visit(key):
        if key in result:
            return result[key]
        n, snap = nodes[key], snapshot(key, c, nodes, base)
        blockers = ['dependency: ' + d for d in n['depends_on'] if visit(d)['state'] != 'accepted']
        blockers += ['finding: ' + i for i, issue in s['findings'].items() if unresolved(issue, c, nodes, base) and issue['severity'] == 'blocking' and affected(issue, key, ancestors)]
        if n['action'] not in MODES[c['mode']]:
            blockers.append('action outside run mode')
        recorded = s['receipts'].get(key, {})
        checks = {claim: fresh(recorded[claim], snap) if claim in recorded else (False, 'unverified') for claim in n['required_claims']}
        state = 'blocked' if blockers else 'accepted' if all(v[0] for v in checks.values()) else 'stale' if any(v[1].startswith('stale') for v in checks.values()) else 'unverified'
        result[key] = {**snap, 'state': state, 'blockers': blockers, 'claims': {k: v[1] for k, v in checks.items()}}
        return result[key]
    for key in nodes:
        visit(key)
    return result


def permit_loaded(s, c, nodes, ancestors, base, key, action):
    require(key in nodes and nodes[key]['action'] == action, 'Action does not match the declared node.')
    require(action in MODES[c['mode']], 'Action outside run mode.')
    statuses = inspect_state(s, c, nodes, ancestors, base)
    require(all(statuses[d]['state'] == 'accepted' for d in nodes[key]['depends_on']), 'Unaccepted or stale prerequisite.')
    for issue in s['findings'].values():
        if unresolved(issue, c, nodes, base) and affected(issue, key, ancestors) and failed_count(issue) >= 2:
            require(strategy_ready(issue, s, statuses), 'Strategy review required; changed hypothesis and fresh pilot needed before another local repair.')
    return {'permitted': action, 'node': key, 'outputs': nodes[key]['outputs'], **snapshot(key, c, nodes, base), 'qualification': LIMIT}


def permit(directory, key, action):
    _, s, c, n, a, b = load(directory)
    return permit_loaded(s, c, n, a, b, key, action)


def record(directory, file):
    path, s, c, nodes, ancestors, base = load(directory)
    r = validate_receipt(file, c, nodes, base)
    key, claim = r['data']['node'], r['data']['claim_type']
    permit_loaded(s, c, nodes, ancestors, base, key, nodes[key]['action'])
    require(not any(unresolved(i, c, nodes, base) and i['severity'] == 'blocking' and affected(i, key, ancestors) for i in s['findings'].values()), 'Open blocking finding prevents acceptance.')
    r['seq'] = event(s, 'receipt', {'node': key, 'claim': claim, 'receipt': r})
    s['receipts'].setdefault(key, {})[claim] = r
    save(path, s)
    return {'recorded': claim, 'node': key, 'qualification': LIMIT}


def finding(directory, file):
    path, s, _, nodes, _, _ = load(directory)
    i = read(file)
    require(nonempty(i.get('id')) and i['id'] not in s['findings'], 'Stable, unused finding ID required; history cannot be reset.')
    require(i.get('nodes') and set(i['nodes']) <= nodes.keys(), 'Finding needs affected nodes.')
    require(i.get('severity') in {'blocking', 'nonblocking'} and nonempty(i.get('observation')), 'Finding needs severity and an observation.')
    i.update(status='open', attempts=[], strategies=[])
    s['findings'][i['id']] = i
    i['opened_seq'] = event(s, 'finding', i.copy())
    save(path, s)
    return {'opened': i['id']}


def failed_count(issue):
    boundary = issue.get('active_strategy', 0)
    return sum(a['outcome'] == 'failed' and a['epoch'] == boundary for a in issue['attempts'])


def strategy_ready(issue, s, statuses):
    if not issue['strategies']:
        return False
    st = issue['strategies'][-1]
    if st['seq'] <= issue.get('active_strategy', 0):
        return False
    pilot = statuses[st['pilot_node']]
    receipts = s['receipts'].get(st['pilot_node'], {})
    try:
        evidence(st['evidence'], Path('.'))
        return pilot['state'] == 'accepted' and pilot['input_hashes'] != st['pilot_inputs_before'] and all(receipts[k]['seq'] > st['seq'] for k in pilot['claims'])
    except (ValueError, OSError):
        return False


def strategy(directory, file):
    path, s, c, nodes, ancestors, base = load(directory)
    value = read(file)
    issue = s['findings'][value['issue']]
    require(unresolved(issue, c, nodes, base) and failed_count(issue) >= 2, 'Strategy transition requires two failed attempts on an open issue.')
    pilot = value.get('pilot_node')
    require(pilot in nodes and nodes[pilot]['kind'] == 'pilot', 'A declared pilot node is required.')
    require(not affected(issue, pilot, ancestors), 'New pilot must be evaluable without accepting the failed branch.')
    require(nonempty(value.get('hypothesis')), 'New hypothesis required.')
    value['evidence'] = evidence(value.get('evidence'), Path(file).resolve().parent)
    require(not issue['strategies'] or value['evidence'] != issue['strategies'][-1]['evidence'], 'Strategy evidence must change; a string reset is insufficient.')
    value['pilot_before'] = snapshot(pilot, c, nodes, base)['revision']
    value['pilot_inputs_before'] = snapshot(pilot, c, nodes, base)['input_hashes']
    value['seq'] = event(s, 'strategy', value.copy())
    issue['strategies'].append(value)
    save(path, s)
    return {'strategy_recorded': value['seq'], 'next': 'Change pilot artifact; collect fresh required pilot reviews. The issue remains open.'}


def repair(directory, file):
    path, s, c, nodes, ancestors, base = load(directory)
    value = read(file)
    issue = s['findings'][value['issue']]
    require(unresolved(issue, c, nodes, base), 'Issue is already closed.')
    issue['status'] = 'open'
    require(value.get('outcome') in {'failed', 'resolved'} and nonempty(value.get('change')), 'Repair needs outcome and causal change.')
    statuses = inspect_state(s, c, nodes, ancestors, base)
    if failed_count(issue) >= 2:
        require(strategy_ready(issue, s, statuses), 'Strategy review required; changed hypothesis and fresh pilot needed before another local repair.')
        issue['active_strategy'] = issue['strategies'][-1]['seq']
    value['evidence'] = evidence(value.get('evidence'), Path(file).resolve().parent)
    if value['outcome'] == 'resolved':
        files = value.get('resolution_receipts', [value.get('resolution_receipt')])
        receipts = [validate_receipt(resolve(Path(file).resolve().parent, f), c, nodes, base) for f in files]
        require(set(issue['nodes']) <= {r['data']['node'] for r in receipts}, 'Resolution must review every affected node.')
        for receipt in receipts:
            require(value['issue'] in receipt['data'].get('resolves', []), 'Resolution must explicitly address this finding.')
            require(receipt['data']['claim_type'] in nodes[receipt['data']['node']]['required_claims'], 'Resolution claim must match the affected obligation.')
        issue['status'] = 'resolved'
        value['resolution'] = receipts
        issue['resolution'] = receipts
    value['epoch'] = issue.get('active_strategy', 0)
    value['seq'] = event(s, 'repair', value.copy())
    issue['attempts'].append(value)
    save(path, s)
    return {'issue': value['issue'], 'status': issue['status'], 'failed_attempts_in_epoch': failed_count(issue), 'total_attempts': len(issue['attempts'])}


def status(directory):
    s = read(Path(directory) / 'run.json')
    if s.get('schema') == 1:
        return {'schema': 1, 'legacy_read_only': True, 'recorded_gates': s.get('gates', {}), 'qualification': 'Legacy records are not promoted to schema-2 acceptance. ' + LIMIT}
    _, s, c, nodes, ancestors, base = load(directory)
    return {'schema': 2, 'mode': c['mode'], 'nodes': inspect_state(s, c, nodes, ancestors, base),
            'findings': {k: {'recorded': i['status'], 'status': 'open' if unresolved(i, c, nodes, base) else 'resolved', 'failed_attempts_in_epoch': failed_count(i), 'total_attempts': len(i['attempts'])} for k, i in s['findings'].items()},
            'manifest_coverage': 'Only declared inputs and evidence files are hashed; unregistered changes are outside this guarantee.', 'qualification': LIMIT}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    for name in ('init', 'status', 'check', 'record', 'finding', 'repair', 'strategy'):
        cmd = sub.add_parser(name)
        cmd.add_argument('run_dir')
        if name == 'init':
            cmd.add_argument('--contract', required=True)
        elif name == 'check':
            cmd.add_argument('--node', required=True)
            cmd.add_argument('--action', required=True)
        elif name != 'status':
            cmd.add_argument('--file', required=True)
    args = p.parse_args()
    try:
        if args.command == 'init':
            result = initialize(args.run_dir, args.contract)
        elif args.command == 'status':
            result = status(args.run_dir)
        elif args.command == 'check':
            result = permit(args.run_dir, args.node, args.action)
        else:
            result = globals()[args.command](args.run_dir, args.file)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as err:
        p.exit(2, str(err) + '\n')


if __name__ == '__main__':
    main()

