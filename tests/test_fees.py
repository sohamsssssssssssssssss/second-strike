import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path
from checkers.check_fees import check


class FeeTests(unittest.TestCase):
    def setUp(self):
        self.ledger = {'trades': [{'id': 1, 'symbol': 'ABC', 'side': 'buy', 'qty': 1000, 'price': 100, 'fee': 50}]}

    def test_correct_fee(self):
        self.assertEqual(check(self.ledger)['verdict'], 'pass')

    def test_missing_and_incorrect_fee(self):
        for fee in (None, 0, 49.98, -50):
            with self.subTest(fee=fee):
                self.ledger['trades'][0]['fee'] = fee
                self.assertEqual(check(self.ledger)['verdict'], 'fail')

    def test_rounding_boundary(self):
        for fee, verdict in ((49.99, 'pass'), (50.01, 'pass'), (50.011, 'fail')):
            self.ledger['trades'][0]['fee'] = fee
            self.assertEqual(check(self.ledger)['verdict'], verdict)

    def test_bad_inputs_escalate(self):
        for field, value in (('fee', 'NaN'), ('fee', True), ('qty', -1), ('price', 'Infinity'), ('side', 'hold')):
            ledger = copy.deepcopy(self.ledger)
            ledger['trades'][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                check(ledger)
        with self.assertRaises(ValueError):
            check({'trades': []})
        self.ledger['trades'] *= 2
        with self.assertRaises(ValueError):
            check(self.ledger)

    def test_paired_harness_freezes_hashes(self):
        root = Path(__file__).parents[1]
        result = subprocess.run(
            [sys.executable, 'harness/paired_test.py', 'eval/ledgers/ex_fail_fees.json', 'eval/ledgers/ex_pass_fees.json'],
            cwd=root, capture_output=True, text=True, check=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(report['rules_off']['r1']['verdict'], 'fail')
        self.assertEqual(report['rules_on']['r1']['verdict'], 'pass')
        self.assertEqual(len(report['rules_off']['sha256']), 64)


if __name__ == '__main__':
    unittest.main()
