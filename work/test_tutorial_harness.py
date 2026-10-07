"""Exercise workflow integrity, not wording matches or pedagogical claims."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

source = Path('outputs/build-interactive-masterclass/scripts/harness.py').resolve()
spec = importlib.util.spec_from_file_location('harness', source)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


class HarnessChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir='work')
        self.root = Path(self.temp.name).resolve()
        h.initialize(self.root, 'PCA', '20-year-old')
        self.evidence = self.root/'observation.txt'
        self.evidence.write_text('Observed evidence', encoding='utf-8')

    def tearDown(self):
        self.temp.cleanup()

    def add(self, stage):
        h.record(self.root, stage, 'pass', [self.evidence], 'Actual observation recorded')

    def test_no_skipping_research_or_pilot(self):
        with self.assertRaises(ValueError):
            self.add('build')

    def test_pass_requires_existing_evidence(self):
        with self.assertRaises(ValueError):
            h.record(self.root, 'intake', 'pass', [], 'Unsupported claim')
        with self.assertRaises(ValueError):
            h.record(self.root, 'intake', 'pass', [self.root/'missing'], 'Missing artifact')

    def test_changed_evidence_blocks_progress(self):
        self.add('intake')
        self.evidence.write_text('Changed requirements', encoding='utf-8')
        with self.assertRaises(ValueError):
            self.add('research')
        self.assertEqual(h.report(self.root)['gates'][0]['effective'], 'stale')

    def test_missing_evidence_invalidates_status(self):
        self.add('intake')
        self.evidence.unlink()
        self.assertFalse(h.report(self.root)['all_gates_current'])

    def test_revision_invalidates_dependents_preserves_history(self):
        for stage in h.STAGES:
            self.add(stage)
        self.assertTrue(h.report(self.root)['all_gates_current'])
        h.record(self.root, 'plan', 'revise', [], 'Learner cannot follow core transition')
        state = json.loads((self.root/'run.json').read_text(encoding='utf-8'))
        self.assertEqual(state['gates']['build']['status'], 'pending')
        self.assertEqual(len(state['history']), 9)
        self.assertIn('review', state['history'][-1]['invalidated'])

    def test_rereview_allows_recovery(self):
        self.add('intake')
        self.evidence.write_text('New inspected evidence', encoding='utf-8')
        self.add('intake')
        self.add('research')
        self.assertEqual(h.report(self.root)['gates'][1]['effective'], 'pass')

    def test_existing_run_not_overwritten(self):
        with self.assertRaises(ValueError):
            h.initialize(self.root, 'Another topic', 'Different audience')


if __name__ == '__main__':
    unittest.main(verbosity=2)
