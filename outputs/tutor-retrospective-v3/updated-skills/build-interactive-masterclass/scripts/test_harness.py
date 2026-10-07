"""Synthetic guardrail behavior tests; these are not course or learner receipts."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).with_name('harness.py')
spec = importlib.util.spec_from_file_location('harness_v2', SOURCE)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


class Workflow(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='test-harness-v2-')
        self.root = Path(self.temp.name)
        self.run = self.root / 'run'
        self.counter = 0
        for name in ('bridge', 'lesson', 'source', 'pilot'):
            (self.root / (name + '.txt')).write_text('Synthetic ' + name, encoding='utf-8')
        def node(id, kind, action, input, deps=(), claims=('artifact',)):
            return {'id': id, 'kind': kind, 'action': action, 'depends_on': list(deps),
                    'inputs': [input], 'outputs': [id + '-output.txt'],
                    'required_claims': list(claims)}
        self.contract = {
            'schema': 2, 'mode': 'build', 'topic': 'TEST FIXTURE, not PCA',
            'audience': 'Synthetic contract', 'scope_roots': [str(self.root)],
            'nodes': [
                {**node('bridge', 'inference', 'review', 'bridge.txt', claims=('teaching-review',)), 'critical': True},
                node('reference', 'artifact', 'research', 'source.txt'),
                node('lesson', 'artifact', 'implement', 'lesson.txt', ('bridge',)),
                node('pilot', 'pilot', 'pilot', 'pilot.txt', claims=('teaching-review', 'interaction')),
                {**node('release', 'delivery', 'deliver', 'lesson.txt', ('lesson',)), 'covers': ['bridge']},
            ],
        }
        self.cp = self.write('contract.json', self.contract)
        h.initialize(self.run, self.cp)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, value):
        path = self.root / name
        path.write_text(json.dumps(value, indent=2), encoding='utf-8')
        return path

    def evidence(self):
        self.counter += 1
        p = self.root / f'observed-{self.counter}.txt'
        p.write_text('Synthetic regression observation; not actual student work.', encoding='utf-8')
        return [{'path': str(p), 'sha256': h.sha(p)}]

    def receipt(self, node, claim=None, **extra):
        snap = h.status(self.run)['nodes'][node]
        n = next(n for n in self.contract['nodes'] if n['id'] == node)
        data = {
            'node': node, 'claim_type': claim or n['required_claims'][0], 'outcome': 'pass',
            'revision': snap['revision'], 'input_hashes': snap['input_hashes'],
            'scenario': 'Synthetic workflow regression only.',
            'observed_result': 'Fixture supplied the expected transition.',
            'reviewer': {'id': 'test-fixture', 'relationship': 'author', 'context': 'Synthetic test author; not independent.'},
            'evidence_type': 'author-review', 'evidence': self.evidence(),
            'limitations': ['No actual learning or course quality assessed.'],
            **extra,
        }
        return self.write(f'receipt-{self.counter}.json', data)

    def accept(self, node):
        n = next(n for n in self.contract['nodes'] if n['id'] == node)
        for claim in n['required_claims']:
            h.record(self.run, self.receipt(node, claim))

    def issue(self):
        path = self.write('finding.json', {
            'id': 'wrong-model', 'nodes': ['bridge'], 'severity': 'blocking',
            'observation': 'Synthetic wrong explanation blocks the bridge.',
        })
        h.finding(self.run, path)
        return path

    def failed(self):
        p = self.write('repair.json', {
            'issue': 'wrong-model', 'outcome': 'failed',
            'change': 'Synthetic causal repair remained insufficient.',
            'evidence': self.evidence(),
        })
        return h.repair(self.run, p)

    def new_strategy(self):
        p = self.write('strategy.json', {
            'issue': 'wrong-model', 'pilot_node': 'pilot',
            'hypothesis': 'A distinct representation may expose the missing relation.',
            'evidence': self.evidence(),
        })
        return h.strategy(self.run, p)

    def test_critical_dependency_blocks_skip_and_delivery(self):
        with self.assertRaisesRegex(ValueError, 'prerequisite'):
            h.record(self.run, self.receipt('lesson'))
        with self.assertRaises(ValueError):
            h.permit(self.run, 'release', 'deliver')
        self.contract['nodes'][-1]['covers'] = []
        self.write('contract.json', self.contract)
        with self.assertRaisesRegex(ValueError, 'critical inference'):
            h.status(self.run)

    def test_graph_rejects_unknown_dependency_cycle_and_delivery_disguise(self):
        self.contract['nodes'][0]['depends_on'] = ['missing']
        self.write('contract.json', self.contract)
        with self.assertRaisesRegex(ValueError, 'Unknown dependencies'):
            h.contract(self.cp)
        self.contract['nodes'][0]['depends_on'] = ['lesson']
        self.write('contract.json', self.contract)
        with self.assertRaisesRegex(ValueError, 'cycle'):
            h.contract(self.cp)
        self.contract['nodes'][0]['depends_on'] = []
        self.contract['nodes'][-1]['kind'] = 'artifact'
        self.write('contract.json', self.contract)
        with self.assertRaisesRegex(ValueError, 'kind/action'):
            h.contract(self.cp)

    def test_mode_scope_and_pinned_policy(self):
        with self.assertRaisesRegex(ValueError, 'match'):
            h.permit(self.run, 'reference', 'implement')
        self.contract['mode'] = 'audit'
        self.write('contract.json', self.contract)
        with self.assertRaisesRegex(ValueError, 'pinned'):
            h.status(self.run)
        audit = self.root / 'audit'
        h.initialize(audit, self.cp)
        with self.assertRaisesRegex(ValueError, 'mode'):
            h.permit(audit, 'lesson', 'implement')
        self.contract['nodes'][0]['outputs'] = [str(self.root.parent / 'outside.txt')]
        self.write('contract.json', self.contract)
        with self.assertRaisesRegex(ValueError, 'outside'):
            h.contract(self.cp)

    def test_source_change_invalidates_dependents_not_other_branch(self):
        for node in ('bridge', 'reference', 'lesson', 'release'):
            self.accept(node)
        (self.root / 'bridge.txt').write_text('Changed bridge content.', encoding='utf-8')
        status = h.status(self.run)['nodes']
        self.assertEqual(status['bridge']['state'], 'stale')
        self.assertEqual(status['lesson']['state'], 'blocked')
        self.assertEqual(status['release']['state'], 'blocked')
        self.assertEqual(status['reference']['state'], 'accepted')

    def test_receipt_requires_scenario_provenance_and_exact_input_binding(self):
        for field in ('scenario', 'observed_result', 'reviewer', 'input_hashes'):
            p = self.receipt('bridge')
            data = h.read(p)
            data.pop(field)
            self.write(p.name, data)
            with self.assertRaises((ValueError, KeyError)):
                h.record(self.run, p)
        p = self.receipt('bridge')
        (self.root / 'bridge.txt').write_text('Changed after review.', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'current inputs'):
            h.record(self.run, p)

    def test_changed_evidence_and_receipt_invalidate_acceptance(self):
        p = self.receipt('bridge')
        h.record(self.run, p)
        ev = Path(h.read(p)['evidence'][0]['path'])
        ev.write_text('Changed report.', encoding='utf-8')
        self.assertEqual(h.status(self.run)['nodes']['bridge']['state'], 'stale')
        p = self.receipt('bridge')
        h.record(self.run, p)
        data = h.read(p)
        data['observed_result'] = 'Rewritten after acceptance.'
        self.write(p.name, data)
        self.assertEqual(h.status(self.run)['nodes']['bridge']['state'], 'stale')

    def test_blocking_issue_reopens_acceptance_and_preserves_other_branch(self):
        for node in ('bridge', 'lesson', 'reference'):
            self.accept(node)
        self.issue()
        state = h.status(self.run)['nodes']
        self.assertEqual(state['bridge']['state'], 'blocked')
        self.assertEqual(state['lesson']['state'], 'blocked')
        self.assertEqual(state['reference']['state'], 'accepted')
        with self.assertRaisesRegex(ValueError, 'blocking finding'):
            h.record(self.run, self.receipt('bridge'))

    def test_two_failed_repairs_need_changed_pilot_not_string_reset(self):
        self.issue()
        self.failed()
        self.failed()
        with self.assertRaisesRegex(ValueError, 'Strategy review required'):
            self.failed()
        self.new_strategy()
        self.accept('pilot')  # A later receipt alone is not a changed pilot.
        with self.assertRaisesRegex(ValueError, 'Strategy review required'):
            h.permit(self.run, 'bridge', 'review')
        self.contract['nodes'][3]['hypothesis_label'] = 'Renaming a strategy is not a new prototype.'
        self.write('contract.json', self.contract)
        self.accept('pilot')
        with self.assertRaisesRegex(ValueError, 'Strategy review required'):
            h.permit(self.run, 'bridge', 'review')
        (self.root / 'pilot.txt').write_text('Changed prototype for the new hypothesis.', encoding='utf-8')
        self.accept('pilot')
        self.assertEqual(h.permit(self.run, 'bridge', 'review')['permitted'], 'review')
        self.failed()
        self.failed()
        with self.assertRaisesRegex(ValueError, 'Strategy review required'):
            self.failed()  # The same successful pilot cannot reset repeatedly.
        finding = h.read(self.run / 'run.json')['findings']['wrong-model']
        self.assertEqual(len(finding['attempts']), 4)
        self.assertEqual(h.failed_count(finding), 2)

    def test_resolution_requires_new_issue_specific_current_review(self):
        self.accept('bridge')
        self.issue()
        generic = self.receipt('bridge')
        r = {'issue': 'wrong-model', 'outcome': 'resolved', 'change': 'Corrected the relation.',
             'evidence': self.evidence(), 'resolution_receipt': str(generic)}
        p = self.write('resolve.json', r)
        with self.assertRaisesRegex(ValueError, 'explicitly address'):
            h.repair(self.run, p)
        specific = self.receipt('bridge', resolves=['wrong-model'])
        r['resolution_receipt'] = str(specific)
        h.repair(self.run, self.write('resolve.json', r))
        self.assertEqual(h.status(self.run)['findings']['wrong-model']['status'], 'resolved')
        Path(h.read(specific)['evidence'][0]['path']).unlink()
        self.assertEqual(h.status(self.run)['findings']['wrong-model']['status'], 'open')
        self.assertEqual(h.status(self.run)['nodes']['bridge']['state'], 'blocked')

    def test_history_does_not_mutate_with_later_attempts(self):
        self.issue()
        before = h.read(self.run / 'run.json')['history'][1]
        self.failed()
        after = h.read(self.run / 'run.json')['history'][1]
        self.assertEqual(before, after)
        self.assertEqual(after['value']['attempts'], [])

    def test_resolving_teaching_finding_does_not_bypass_other_required_claim(self):
        self.contract['nodes'][0]['required_claims'].append('correctness')
        self.write('contract.json', self.contract)
        self.issue()
        specific = self.receipt('bridge', 'teaching-review', resolves=['wrong-model'])
        r = {'issue': 'wrong-model', 'outcome': 'resolved', 'change': 'Synthetic teaching repair.',
             'evidence': self.evidence(), 'resolution_receipt': str(specific)}
        h.repair(self.run, self.write('resolve.json', r))
        h.record(self.run, specific)
        state = h.status(self.run)['nodes']
        self.assertEqual(state['bridge']['claims']['correctness'], 'unverified')
        self.assertEqual(state['bridge']['state'], 'unverified')
        with self.assertRaisesRegex(ValueError, 'prerequisite'):
            h.record(self.run, self.receipt('lesson'))

    def test_human_claims_require_human_type_counts_and_remain_attestations(self):
        self.accept('bridge')
        p = self.receipt('bridge', 'learner-tested')
        with self.assertRaisesRegex(ValueError, 'human-study'):
            h.record(self.run, p)
        p = self.receipt('bridge', 'learner-tested', evidence_type='human-study',
                         human_evidence={'participants': 0, 'tasks': 1})
        with self.assertRaisesRegex(ValueError, 'counts'):
            h.record(self.run, p)
        p = self.receipt('bridge', 'learner-tested', evidence_type='human-study',
                         human_evidence={'participants': 2, 'tasks': 3})
        result = h.record(self.run, p)
        self.assertIn('does not verify truth', result['qualification'])
        p = self.receipt('bridge', 'retention', evidence_type='human-study',
                         human_evidence={'participants': 2, 'tasks': 3})
        with self.assertRaisesRegex(ValueError, 'delay'):
            h.record(self.run, p)

    def test_delivery_does_not_require_human_efficacy(self):
        for node in ('bridge', 'lesson', 'release'):
            self.accept(node)
        state = h.status(self.run)
        self.assertEqual(state['nodes']['release']['state'], 'accepted')
        self.assertNotIn('learner-tested', state['nodes']['release']['claims'])

    def test_simulated_claim_and_empty_critical_artifact_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'simulated-review'):
            h.record(self.run, self.receipt('bridge', 'simulated-learner'))
        self.contract['nodes'][0]['inputs'] = []
        self.write('contract.json', self.contract)
        with self.assertRaisesRegex(ValueError, 'input artifact'):
            h.status(self.run)

    def test_legacy_readable_but_not_writable_or_promoted(self):
        legacy = self.root / 'legacy'
        legacy.mkdir()
        (legacy / 'run.json').write_text(json.dumps({'schema': 1, 'gates': {'delivery': {'status': 'pass'}}}), encoding='utf-8')
        state = h.status(legacy)
        self.assertTrue(state['legacy_read_only'])
        self.assertNotIn('nodes', state)
        with self.assertRaisesRegex(ValueError, 'status-only'):
            h.record(legacy, self.receipt('bridge'))

    def test_cli_errors_return_failure_without_receipt_write(self):
        p = self.receipt('lesson')
        result = subprocess.run([sys.executable, str(SOURCE), 'record', str(self.run), '--file', str(p)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('prerequisite', result.stderr)
        self.assertEqual(h.read(self.run / 'run.json')['receipts'], {})

    def test_windows_bom_and_malformed_json_exit_cleanly(self):
        self.cp.write_text(json.dumps(self.contract), encoding='utf-8-sig')
        self.assertEqual(h.status(self.run)['mode'], 'build')
        malformed = self.write('malformed.json', [])
        result = subprocess.run([sys.executable, str(SOURCE), 'record', str(self.run), '--file', str(malformed)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)


