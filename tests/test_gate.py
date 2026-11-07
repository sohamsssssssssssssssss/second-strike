import json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / 'checkers' / 'gate.py'
LED = ROOT / 'eval' / 'ledgers'

class GateTests(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.rule = self.d / 'R1.json'
        shutil.copy(ROOT / 'rules' / 'R1.json', self.rule)
    def tearDown(self):
        shutil.rmtree(self.d)
    def run_gate(self, *args):
        r = subprocess.run([sys.executable, str(GATE), str(self.rule), *args], cwd=ROOT, capture_output=True, text=True)
        return r.returncode, json.loads(r.stdout)
    def test_active_pass_and_fail_counts_hits(self):
        self.assertEqual(self.run_gate(str(LED / 'ex_pass_fees.json'), '--now', '2026-11-10T00:00:00+05:30')[0], 0)
        self.assertEqual(self.run_gate(str(LED / 'ex_fail_fees.json'), '--now', '2026-11-10T00:00:00+05:30')[0], 1)
        self.assertEqual(json.loads(self.rule.read_text())['hits'], 1)
    def test_expired_not_enforced(self):
        code, out = self.run_gate(str(LED / 'ex_fail_fees.json'), '--now', '2026-12-01T00:00:00+05:30')
        self.assertEqual((code, out['rule_state']), (3, 'expired'))
    def test_revoke_then_not_enforced_and_logged(self):
        self.run_gate('--revoke', 'Soham')
        code, out = self.run_gate(str(LED / 'ex_fail_fees.json'), '--now', '2026-11-10T00:00:00+05:30')
        self.assertEqual((code, out['rule_state']), (3, 'revoked'))
        events = [json.loads(l)['event'] for l in (self.d / 'events.jsonl').read_text().splitlines()]
        self.assertEqual(events, ['revoked', 'skipped'])

if __name__ == '__main__':
    unittest.main()
