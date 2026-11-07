import contextlib, hashlib, io, json, shutil, sys, tempfile, unittest
from pathlib import Path
from unittest import mock
from harness import gate_reply, rescue_report

ROOT = Path(__file__).resolve().parents[1]
MISSING_FEE = {'id': 'L1', 'trades': [{'id': 1, 'symbol': 'SYN1', 'side': 'buy', 'qty': 100, 'price': 100}]}
GOOD = {'id': 'L2', 'trades': [{'id': 1, 'symbol': 'SYN1', 'side': 'buy', 'qty': 100, 'price': 100, 'fee': 5}]}
# Shape of the clean-run / control replies: `quantity`, no trade ids.
NO_IDS = {'id': 'L3', 'trades': [{'symbol': 'KORVA', 'side': 'buy', 'quantity': 15, 'price': 24.0}]}


def fenced(obj, tag='json'):
    return f'Here is the ledger.\n```{tag}\n{json.dumps(obj)}\n```\nAssumptions: synthetic.'


class GateReplyTests(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.rule = self.d / 'R1.json'
        rule = json.loads((ROOT / 'rules' / 'R1.json').read_text())
        rule['expiry'] = '2099-01-01T00:00:00+05:30'  # keep tests independent of the real expiry date
        self.rule.write_text(json.dumps(rule))
        self.n = 0

    def tearDown(self):
        shutil.rmtree(self.d)

    def submit(self, text, variant='V1', attempt=1):
        self.n += 1
        msg = self.d / f'msg{self.n}.txt'
        msg.write_bytes(text.encode())
        argv = ['gate_reply.py', '--rule', str(self.rule), '--run', 'rescue', '--variant', variant,
                '--attempt', str(attempt), '--eval-dir', str(self.d / 'eval'), str(msg)]
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, 'argv', argv), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = gate_reply.main()
        return code, (json.loads(out.getvalue()) if out.getvalue() else None)

    def raw(self, variant='V1', attempt=1):
        return self.d / 'eval' / 'rescue' / 'raw' / f'{variant}-a{attempt}.txt'

    def test_fenced_and_bare_extraction(self):
        for i, text in enumerate((fenced(GOOD), fenced(GOOD, ''), f'Ledger: {json.dumps(GOOD)} done')):
            with self.subTest(i=i):
                code, out = self.submit(text, attempt=i + 1)
                self.assertEqual((code, out['verdict']), (0, 'pass'))

    def test_no_json_escalates_and_raw_saved(self):
        code, out = self.submit('I could not produce a ledger.')
        self.assertEqual((code, out['verdict']), (2, 'escalate'))
        self.assertIn('no JSON', out['feedback'])
        self.assertEqual(self.raw().read_text(), 'I could not produce a ledger.')

    def test_hash_written_before_grading(self):
        text = fenced(MISSING_FEE)
        real_run = gate_reply.gate.run
        def checked_run(*args, **kwargs):
            self.assertEqual(self.raw().read_bytes(), text.encode())  # raw exists before the gate runs
            return real_run(*args, **kwargs)
        with mock.patch.object(gate_reply.gate, 'run', checked_run):
            _, out = self.submit(text)
        self.assertEqual(out['sha256'], hashlib.sha256(text.encode()).hexdigest())
        log = [json.loads(l) for l in (self.d / 'eval' / 'rescue' / 'log.jsonl').read_text().splitlines()]
        self.assertEqual((log[0]['sha256'], log[0]['verdict']), (out['sha256'], 'fail'))
        self.assertNotIn('feedback', log[0])

    def test_missing_ids_escalate_lists_schema(self):
        code, out = self.submit(fenced(NO_IDS))
        self.assertEqual((code, out['verdict']), (2, 'escalate'))
        for field in ('`id` (unique)', '`symbol`', '`side` (buy|sell)', '`qty` > 0', '`price` > 0', '`fee`'):
            self.assertIn(field, out['feedback'])
        self.assertTrue(out['feedback'].rstrip().endswith(json.loads(self.rule.read_text())['what']))

    def test_fail_lists_expected_fees(self):
        code, out = self.submit(fenced(MISSING_FEE))
        self.assertEqual((code, out['verdict']), (1, 'fail'))
        self.assertIn('| 1 | 5.0000 | missing |', out['feedback'])
        self.assertEqual(out['offending'][0]['expected_fee'], '5.0000')

    def test_same_attempt_refused(self):
        self.submit(fenced(MISSING_FEE))
        code, out = self.submit(fenced(GOOD))
        self.assertEqual((code, out), (4, None))
        self.assertEqual(self.raw().read_text(), fenced(MISSING_FEE))

    def test_report_totals(self):
        self.submit(fenced(MISSING_FEE), 'V1', 1)
        self.submit(fenced(GOOD), 'V1', 2)
        self.submit(fenced(GOOD), 'V2', 1)
        text = rescue_report.report((self.d / 'eval' / 'rescue' / 'log.jsonl').read_text().splitlines())
        self.assertIn('| V1 | fail | pass |', text)
        self.assertIn('first-try pass 1/2, pass by second strike 2/2', text)


if __name__ == '__main__':
    unittest.main()
