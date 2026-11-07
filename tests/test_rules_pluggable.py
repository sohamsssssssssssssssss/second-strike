import json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / 'checkers' / 'gate.py'

GOOD = {'trades': [{'id': 1, 'symbol': 'A', 'side': 'buy', 'qty': 2, 'price': 50, 'fee': 0.05},
                   {'id': 2, 'symbol': 'B', 'side': 'sell', 'qty': 1, 'price': 100, 'fee': 0.05}],
        'traded_value': 200}


class PluggableRuleTests(unittest.TestCase):
    """A second rule (R2) runs through the unchanged gate: its checker is loaded from the rule file."""
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.rule = self.d / 'R2.json'
        r = json.loads((ROOT / 'rules' / 'R2.json').read_text())
        r['status'] = 'active'
        self.rule.write_text(json.dumps(r))
    def tearDown(self):
        shutil.rmtree(self.d)
    def gate(self, ledger, rule=None):
        f = self.d / 'l.json'; f.write_text(json.dumps(ledger))
        p = subprocess.run([sys.executable, str(GATE), str(rule or self.rule), str(f), '--now', '2026-11-10T00:00:00+05:30'],
                           cwd=ROOT, capture_output=True, text=True)
        return p.returncode, json.loads(p.stdout)
    def test_r2_pass(self):
        self.assertEqual(self.gate(GOOD)[0], 0)
    def test_r2_fail_reports_expected(self):
        bad = dict(GOOD, traded_value=201)
        code, out = self.gate(bad)
        self.assertEqual((code, out['rule_id'], out['offending_trades'][0]['expected']), (1, 'R2', '200'))
    def test_r2_missing_field_escalates(self):
        code, _ = self.gate({'trades': GOOD['trades']})
        self.assertEqual(code, 2)
    def test_draft_rule_not_enforced(self):
        draft = self.d / 'R2-draft.json'
        shutil.copy(ROOT / 'rules' / 'R2.json', draft)
        code, out = self.gate(GOOD, rule=draft)
        self.assertEqual((code, out['rule_state']), (3, 'inactive'))
    def test_checker_outside_repo_rejected(self):
        r = json.loads(self.rule.read_text()); r['checker'] = '/tmp/evil.py'; self.rule.write_text(json.dumps(r))
        self.assertEqual(self.gate(GOOD)[0], 2)


if __name__ == '__main__':
    unittest.main()
