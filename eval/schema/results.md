# Comparison arm (schema up front) — 7 Nov 2026, 19:57–20:15 IST

Room `schema-arm` (new): worker-b only during generation, R1 in room Instructions, no gate. Prompt = tasks/seeded/variant-0n.txt verbatim + the exact text the gate gives on failure:
"Each trade needs: id (unique), symbol, side (buy|sell), qty > 0, price > 0, fee. R1: Each synthetic backtest trade must include a fee equal to 0.0005 * qty * price, within an absolute tolerance of 0.01."
After all 5 replies, gate was added and graded each first reply (run `schema`, no feedback to worker).

## Result
First-try pass **5/5** (see report.md). Hashes in log.jsonl; raw in raw/.

## What this means
The fix is the explicit rule + schema reaching the worker at task time. Room Instructions did not deliver it (clean run 0/5). The gate delivers it on failure (rescue 0/5 -> 5/5) and verifies every output deterministically; putting it in the prompt also works (5/5) but relies on every requester writing it and nobody checks.

## Caveats
- First gate trigger used the rescue run name and was refused (exit 4, no overwrite). That trigger message contained the text "@worker-b", which pinged worker-b; any reply it made is not graded.
- Gate instructions were edited before grading to accept a run name. Same caveats as rescue: human-triggered gate, agent-copied raw text, n=5.
