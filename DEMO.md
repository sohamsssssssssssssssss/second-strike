# Second Strike: 100-second demo shot list

Run terminal steps in a copy of the repo (`cp -R . ../second-strike-run`). The gate writes to `rules/`. No API keys or tokens on screen.

| Time | Shot | Say / show |
| --- | --- | --- |
| 0:00–0:10 | Problem | "A correction given to one agent does not reach the next." Show the seeded task and the worker ledger with no fee column. |
| 0:10–0:30 | Correction | Show worker-a's ledger missing fees. Show my rejection ("fees missing"). Show the scribe's draft: fee = 0.0005 × qty × price, tolerance 0.01. |
| 0:30–0:45 | Approval | Show my approval message. Show the R1 text in the room Instructions. Say: "Only this approval activates the rule." |
| 0:45–0:55 | Earlier quant-desk run | Show worker-b's ledger from the `quant-desk` room, which has the correction thread in its history. Label it on screen: "preliminary, not matched." |
| 0:55–1:05 | Clean run result (new) | Show the table in `eval/clean/results.md`, or the README table: fresh rooms, Instructions only, 0/5 treatment vs 0/5 control. Label on screen: "screen-read; raw export pending." Say: "Room Instructions alone did not carry the correction. So the gate enforces it." |
| 1:05–1:20 | Gate pass and fail | `python3 checkers/gate.py rules/R1.json eval/ledgers/ex_pass_fees.json` → pass, exit 0. Then `…ex_fail_fees.json` → fail, exit 1, `hits` goes to 1 in `rules/R1.json`. |
| 1:20–1:30 | Revoke | `python3 checkers/gate.py rules/R1.json --revoke Soham` → status revoked. Re-run the fail ledger → `not_enforced`, exit 3. Then `cat rules/events.jsonl`. Say: "Custom lifecycle, not a Switch command." |
| 1:30–1:40 | Results and limit | Show the headline in `README.md`. Say: "Clean run: 0 of 5 with Instructions alone, 0 of 5 control. Earlier quant-desk runs are preliminary. No causal claim." |

Show only what exists: the room messages, the R1 record, the clean-run table, the gate outputs, and the events log. Do not show the rule as a native Switch Rule or Decision.
