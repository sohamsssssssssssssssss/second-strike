"""Freeze two first-submission ledgers and compare their R1 checker verdicts."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from checkers.check_fees import check


def freeze(path):
    raw = path.read_bytes()
    return {'file': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'ledger': json.loads(raw)}


def report(frozen):
    return {key: value for key, value in frozen.items() if key != 'ledger'} | {'r1': check(frozen['ledger'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rules_off', type=Path)
    parser.add_argument('rules_on', type=Path)
    args = parser.parse_args()
    try:
        # Freeze both raw submissions before either one reaches the checker.
        frozen = {'rules_off': freeze(args.rules_off), 'rules_on': freeze(args.rules_on)}
        result = {name: report(item) for name, item in frozen.items()}
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
        print(json.dumps({'verdict': 'escalate', 'error': str(error)}))
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
