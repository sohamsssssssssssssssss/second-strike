"""Re-verify every recorded gate run: raw-file sha256 matches log.jsonl, and an
offline replay of checkers/check_fees.py reproduces each logged verdict.
Usage: python3 harness/verify_evidence.py   (exit 0 = all evidence reproduces)"""
import hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'checkers'))
import check_fees  # noqa: E402

FENCE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.S)


def replay(text):
    m = FENCE.search(text)
    if not m:
        start = text.find('{')
        if start < 0:
            return 'escalate'
        try:
            obj, _ = json.JSONDecoder().raw_decode(text[start:])
        except ValueError:
            return 'escalate'
    else:
        try:
            obj = json.loads(m.group(1))
        except ValueError:
            return 'escalate'
    try:
        return check_fees.check(obj)['verdict']
    except (ValueError, TypeError, ArithmeticError):
        return 'escalate'


def main():
    runs = sorted(p.parent for p in (ROOT / 'eval').glob('*/log.jsonl'))
    total = bad = 0
    for run in runs:
        for line in (run / 'log.jsonl').read_text().splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            raw = run / 'raw' / f"{e['variant']}-a{e['attempt']}.txt"
            data = raw.read_bytes()
            ok_hash = hashlib.sha256(data).hexdigest() == e['sha256']
            v = replay(data.decode('utf-8', 'replace'))
            ok = ok_hash and v == e['verdict']
            total += 1
            bad += not ok
            print(f"{'OK ' if ok else 'BAD'} {run.name:8} {e['variant']} a{e['attempt']} logged={e['verdict']:8} replay={v:8} hash={'match' if ok_hash else 'MISMATCH'}")
    print(f"\n{total - bad}/{total} recorded gate checks reproduce across {len(runs)} runs")
    return 1 if bad or not total else 0


if __name__ == '__main__':
    raise SystemExit(main())
