"""Gate one worker reply: save raw + sha256 before grading, extract the JSON ledger, run the R1 gate,
print verdict JSON with worker feedback, and append to eval/<run>/log.jsonl.
Exit codes follow gate.py (0 pass, 1 fail, 2 escalate, 3 not enforced); 4 = attempt already recorded."""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'checkers'))
import gate

SCHEMA = 'Each trade needs: `id` (unique), `symbol`, `side` (buy|sell), `qty` > 0, `price` > 0, `fee`.'


def extract(text):
    """Return (ledger, error). Fenced ```json first, then any ``` block, then first top-level {...}."""
    m = re.search(r'```json[^\n]*\n(.*?)```', text, re.S) or re.search(r'```[^\n]*\n(.*?)```', text, re.S)
    try:
        if m:
            return json.loads(m.group(1)), None
        start = text.find('{')
        if start < 0:
            return None, 'no JSON'
        return json.JSONDecoder().raw_decode(text, start)[0], None
    except ValueError as e:
        return None, f'invalid JSON: {e}'


def feedback(res, rule_state, variant, attempt, what):
    verdict = res['verdict']
    lines = [f'**R1 gate: {verdict}** ({variant}, attempt {attempt})', '']
    if verdict == 'fail':
        lines += ['| id | expected_fee | found |', '| --- | --- | --- |']
        lines += [f"| {t['id']} | {t['expected_fee']} | {t['found_fee'] if t['found_fee'] is not None else 'missing'} |"
                  for t in res['offending_trades']]
        lines.append('')
    elif verdict == 'escalate':
        lines += [f"Error: {res.get('error')}", '', SCHEMA, '']
    elif verdict == 'not_enforced':
        lines += [f'Rule state: {rule_state}. Not enforced.', '']
    return '\n'.join(lines + [f'R1: {what}'])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rule', type=Path, required=True)
    p.add_argument('--run', required=True)
    p.add_argument('--variant', required=True)
    p.add_argument('--attempt', type=int, required=True)
    p.add_argument('--eval-dir', type=Path, default=ROOT / 'eval')
    p.add_argument('message', type=Path)
    a = p.parse_args()

    data = a.message.read_bytes()
    run_dir = a.eval_dir / a.run
    raw_path = run_dir / 'raw' / f'{a.variant}-a{a.attempt}.txt'
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with raw_path.open('xb') as f:  # first reply per attempt is the record; never overwrite
            f.write(data)
    except FileExistsError:
        print(json.dumps({'error': f'{raw_path} already recorded'}), file=sys.stderr)
        return 4
    sha = hashlib.sha256(data).hexdigest()  # hashed before any parsing or grading

    ledger, error = extract(data.decode('utf-8', 'replace'))
    res, code = gate.run(a.rule, ledger, raw_path, error=error)
    rule_state = res.get('rule_state', 'active')
    what = json.loads(a.rule.read_text())['what']
    out = {'variant': a.variant, 'attempt': a.attempt, 'sha256': sha, 'verdict': res['verdict'],
           'rule_state': rule_state, 'offending': res.get('offending_trades', [])}
    entry = {'ts': datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds'), **out}
    if 'error' in res:
        entry['error'] = res['error']
    with (run_dir / 'log.jsonl').open('a') as f:
        f.write(json.dumps(entry) + '\n')
    print(json.dumps(out | {'feedback': feedback(res, rule_state, a.variant, a.attempt, what)}, indent=2))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
