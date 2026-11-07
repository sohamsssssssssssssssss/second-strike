# Second Strike: 95-second demo shot list

Run the terminal step in a copy of the repo (`cp -R . ../second-strike-run`). The gate writes to `rules/`. No API keys or tokens on screen.

| Time | Shot | Say / show |
| --- | --- | --- |
| 0:00–0:10 | Problem | "A correction given to one agent does not reach the next." Show the seeded task and the worker ledger with no fee column. |
| 0:10–0:30 | Correction | Show worker-a's ledger missing fees. Show my rejection ("fees missing"). Show the scribe's draft: fee = 0.0005 × qty × price, tolerance 0.01. |
| 0:30–0:45 | Approval | Show my approval message. Show the R1 text in the room Instructions. Say: "Only this approval activates the rule." |
| 0:45–0:55 | Clean run result | Show the clean-run table (README or `eval/clean/results.md`): fresh rooms, Instructions only, 0/5 treatment vs 0/5 control. Label on screen: "screen-read; raw export pending." Say: "Room Instructions alone did not carry the correction." |
| 0:55–1:15 | Live second strike (`rescue` room) | Show worker-b's V1 attempt 1: no trade IDs, no fees, `quantity`. Show me posting "@gate check V1 attempt 1". Show the gate's reply: escalate, the exact error, the per-trade schema, and the R1 text. Show worker-b's attempt 2 with `id`, `qty`, and `fee`. Show "@gate check V1 attempt 2" and the gate's pass. Say: "The gate runs when I mention it. Its output is the only feedback." |
| 1:15–1:25 | Revoke (terminal, on a copy) | `python3 checkers/gate.py rules/R1.json --revoke Soham` → status revoked. Then `python3 checkers/gate.py rules/R1.json eval/ledgers/ex_fail_fees.json` → `not_enforced`, exit 3. Then `cat rules/events.jsonl`. Say: "Custom lifecycle, not a Switch command." |
| 1:25–1:35 | Results and limit | Show the README Results table. Say: "Instructions alone, 0 of 5. With the gate, 0 of 5 first try, 5 of 5 after one strike. Rule and schema in the prompt, 5 of 5, but nobody checks it. Five variants, one worker, one model. No generic-retry comparison." |

Show only what exists: the room messages, the R1 record, the clean-run table, the rescue room thread, the README Results table, and the events log. Do not show the rule as a native Switch Rule or Decision.
