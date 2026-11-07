"""Summarise a gate_reply log: per-variant attempt 1 and 2 verdicts, first-try vs second-strike totals."""
import argparse
import json
from pathlib import Path


def report(lines):
    first, dupes = {}, []
    for line in lines:
        if not line.strip():
            continue
        e = json.loads(line)
        key = (e['variant'], e['attempt'])
        if key in first:
            dupes.append(f'{key[0]} a{key[1]}')
        else:
            first[key] = e['verdict']  # first entry per attempt is the record
    variants = sorted({v for v, _ in first})
    rows = ['| Variant | Attempt 1 | Attempt 2 |', '| --- | --- | --- |']
    rows += [f"| {v} | {first.get((v, 1), '—')} | {first.get((v, 2), '—')} |" for v in variants]
    x = sum(first.get((v, 1)) == 'pass' for v in variants)
    y = sum('pass' in (first.get((v, 1)), first.get((v, 2))) for v in variants)
    n = len(variants)
    rows += ['', f'first-try pass {x}/{n}, pass by second strike {y}/{n}']
    if dupes:
        rows.append(f"Ignored duplicate entries: {', '.join(dupes)}")
    return '\n'.join(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('log', type=Path)
    print(report(p.parse_args().log.read_text().splitlines()))


if __name__ == '__main__':
    main()
