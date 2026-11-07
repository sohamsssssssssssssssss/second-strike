# Second-strike run — 7 Nov 2026, 18:23–18:46 IST

Room `rescue` (new): worker-b + gate, R1 text in room Instructions. Prompts = tasks/seeded/variant-0n.txt verbatim. Reviewer (Claude via computer use) triggered the gate with "@gate check Vn attempt K"; the gate ran harness/gate_reply.py and posted its feedback. The only feedback worker-b got was gate output. Max 2 attempts.

## Result
| Variant | Attempt 1 | Attempt 2 |
| --- | --- | --- |
| V1 | escalate | pass |
| V2 | escalate | pass |
| V3 | escalate | pass |
| V4 | escalate | pass |
| V5 | escalate | pass |

**First-try pass 0/5. Pass after one gate strike 5/5.**
Attempt-1 replies had no trade ids and no fees (and used `quantity`). After the gate's feedback (exact schema + R1 text), every resubmission had ids, `qty` and correct fees.

## Verification
- raw/: 10 files, saved and sha256-hashed by gate_reply.py before grading (log.jsonl).
- Offline replay: all 10 hashes match; check_fees.py reproduces every verdict.
- report.md = rescue_report.py output.

## Caveats
- Gate is triggered by a human mention, not autonomously.
- One shared room: V2–V5 first tries could see earlier gate feedback in history; they still escalated (0/5).
- Raw = text as the gate agent copied it, not a Mattermost API export.
- Setup: gate Auto mode switched On (approval prompts couldn't be answered in-thread). Gate can't write to ~/Documents, so it used its own R1 copy and eval dir (~/.switch/agents/…/second-strike-gate); results copied here. R1.after.json = that copy after the run (hits 0: escalations don't count as fee hits).
- An earlier V1 gate trigger failed (PermissionError on mkdir; nothing saved) and one was stopped at an approval prompt; neither produced a graded record.
- Same worker, same model; n=5. Shows the loop works, not general reliability.
