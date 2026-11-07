"""Rule-aware gate: loads a rule record, enforces lifecycle, then runs its checker.
Exit 0 pass, 1 fail, 2 escalate, 3 rule inactive (expired/revoked) -> not enforced.
Usage: gate.py rules/R1.json LEDGER [--now ISO]
       gate.py rules/R1.json --revoke BY   (append-only event log in rules/events.jsonl)"""
import argparse, importlib.util, json, sys
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_fees

CHECKERS = {'checkers/check_fees.py': check_fees}
ROOT = Path(__file__).resolve().parents[1]


def load_checker(path):
    """Any rule names its checker file; it is loaded by path, so a new rule needs no gate change."""
    if path not in CHECKERS:
        target = (ROOT / path).resolve()
        if ROOT not in target.parents or target.suffix != '.py':
            raise ValueError(f'Checker must be a .py file inside the repo: {path}')
        spec = importlib.util.spec_from_file_location(target.stem, target)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        CHECKERS[path] = mod
    return CHECKERS[path]


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')


def log(rule_path, event):
    with (rule_path.parent / 'events.jsonl').open('a') as f:
        f.write(json.dumps(event) + '\n')


def state(rule, now):
    if rule.get('status') == 'revoked' or rule.get('revoked_at'):
        return 'revoked'
    if rule.get('expiry') and now >= datetime.fromisoformat(rule['expiry']):
        return 'expired'
    return 'active' if rule.get('status') == 'active' else 'inactive'


def revoke(rule_path, by):
    rule = json.loads(rule_path.read_text())
    ts = now_iso()
    rule.update(status='revoked', revoked_at=ts, revoked_by=by)
    rule_path.write_text(json.dumps(rule, indent=2) + '\n')
    log(rule_path, {'ts': ts, 'rule': rule['id'], 'event': 'revoked', 'by': by})
    return {'rule_id': rule['id'], 'status': 'revoked', 'by': by}


def run(rule_path, ledger, ledger_ref, now=None, error=None):
    """Gate one parsed ledger (or a parse error) against the rule. Returns (result, exit code)."""
    rule = json.loads(rule_path.read_text())
    st = state(rule, now or datetime.now(timezone.utc))
    if st != 'active':
        log(rule_path, {'ts': now_iso(), 'rule': rule['id'], 'event': 'skipped', 'state': st, 'ledger': str(ledger_ref)})
        return {'rule_id': rule['id'], 'verdict': 'not_enforced', 'rule_state': st}, 3
    try:
        if error is not None:
            raise ValueError(error)
        res = load_checker(rule['checker']).check(ledger)
    except (ValueError, TypeError, ArithmeticError) as e:
        res = {'rule_id': rule['id'], 'verdict': 'escalate', 'error': str(e)}
    if res['verdict'] == 'fail':
        rule['hits'] = rule.get('hits', 0) + 1
        rule['last_fired'] = now_iso()
        rule_path.write_text(json.dumps(rule, indent=2) + '\n')
    log(rule_path, {'ts': now_iso(), 'rule': rule['id'], 'event': 'checked', 'verdict': res['verdict'], 'ledger': str(ledger_ref)})
    return res, {'pass': 0, 'fail': 1}.get(res['verdict'], 2)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('rule', type=Path)
    p.add_argument('ledger', type=Path, nargs='?')
    p.add_argument('--now')
    p.add_argument('--revoke', metavar='BY')
    a = p.parse_args()
    if a.revoke:
        print(json.dumps(revoke(a.rule, a.revoke)))
        return 0
    if not a.ledger:
        p.error('ledger required')
    ledger, error = None, None
    try:
        ledger = json.loads(a.ledger.read_text())
    except (OSError, ValueError) as e:
        error = str(e)
    res, code = run(a.rule, ledger, a.ledger, datetime.fromisoformat(a.now) if a.now else None, error)
    print(json.dumps(res))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
