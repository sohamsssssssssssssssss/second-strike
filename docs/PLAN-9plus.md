# Second Strike — plan to 9+ (7 Nov 2026, from 18:05 IST; deadline 23:59)

Goal: show the product's namesake loop live in Switch: worker submits -> gate checks with approved R1 -> on fail, gate returns exact errors + rule -> worker resubmits ("second strike") -> gate re-checks. Measure first-try vs after-feedback pass rate.

## Owners
- Claude Code (CC): repo code, tests, docs.
- Claude (chat, computer use): Switch/Mattermost UI, live runs, evidence export.
- Soham: approvals, sign-ins, video, submission.

## Phases
| # | What | Owner | Done when | ETA |
|---|---|---|---|---|
| A | `harness/gate_reply.py`: raw message -> save raw + sha256 BEFORE grading -> extract fenced JSON -> gate -> verdict JSON + worker feedback text; append to `eval/rescue/log.jsonl`. `harness/rescue_report.py`: log -> first-try vs second-strike table. Tests. | CC | tests pass; dry run on eval/clean-like sample | 18:50 |
| B | Gate agent instructions: on "@gate check <Vn> attempt <k>", save the worker's latest ledger reply verbatim, run gate_reply.py, post feedback; on fail/escalate mention @worker-b with feedback. | Claude | gate posts a verdict in a test room | 19:15 |
| C | Rescue run: new room `rescue` (worker-b + gate, R1 in Instructions). V1–V5, max 2 attempts each. Reviewer (Claude) triggers gate by mention; no other hints. | Claude | 5 variants logged, raw hashed | 20:15 |
| D | Exact export of clean-treat, clean-control, rescue via Mattermost API (Soham signs into browser pane once). Hash; reconcile with screen-read table. | Claude | eval/clean/raw + eval/rescue/raw populated | 20:45 |
| E | README/DEMO: headline = clean run (Instructions alone 0/5) + rescue result (first-try x/5 -> after one gate strike y/5). Limits. | CC | reviewed by Claude | 21:15 |
| F | Push public GitHub repo; video; check form; submit. | Soham (+CC push) | submitted | 23:00 |

## Rules
- Never edit/retry-select outputs; first reply per attempt is the record. Malformed stays malformed.
- Gate trigger by human mention is disclosed (not autonomous). Only feedback = gate output.
- Gate mutates rules/R1.json (hits/last_fired) and rules/events.jsonl: that is product behaviour; snapshot R1.json before phase C.
- No new claims without a logged artifact.
