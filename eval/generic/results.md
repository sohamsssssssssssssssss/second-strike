# Generic-retry arm — 7 Nov 2026, 22:53–23:00 IST

Question (from an independent review): does the gate's *exact* feedback matter, or would any "try again" work?
Room `generic-retry` (new): control-worker-fresh (Codex gpt-6-luna, same base instructions as worker-b, never shown gate feedback before) + gate; R1 in room Instructions. Same 5 frozen prompts. Gate ran the same check (`run generic`) but posted only:
"R1 gate: <verdict> (Vn, attempt K). Your ledger does not meet the team rule. Please fix your mistakes and resubmit the full ledger as JSON in a fenced code block." — no error, no schema, no rule text.

## Result
| Variant | Attempt 1 | Worker's response to generic feedback |
| --- | --- | --- |
| V1–V5 | escalate (no ids, no fees, `quantity`) | asked the gate which rule/field failed; did not resubmit |

**Final compliance 0/5** (no resubmissions). Compare the rescue run with exact gate feedback: 0/5 first try → **5/5** after one strike.
A generic "fix it" did not produce a fix; the worker declined to guess. The exact error + schema + rule text is what converts a failure into a fix.

## Caveats
- Different worker agent from the rescue run (control-worker-fresh vs worker-b), chosen because worker-b had already seen gate feedback; same model and base instructions. n=5.
- Gate triggered by reviewer mention. Raw = text as the gate agent copied it; log.jsonl hashes saved before grading.
