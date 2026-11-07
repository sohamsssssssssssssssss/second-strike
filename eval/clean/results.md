# Clean matched run — 7 Nov 2026, 17:33–17:43 IST

Run by Claude via computer use in Switch Console. Prompts = tasks/seeded/variant-0n.txt verbatim, prefixed with the agent mention, each sent once. No retries, hints or edits.

## Setup (matched)
| | clean-treat | clean-control |
|---|---|---|
| Agent | worker-b | control-worker-fresh |
| Agent instructions | worker-b base text | same text, pasted verbatim |
| Model | gpt-6-luna | gpt-6-luna |
| Auto mode | Off | Off (changed from On) |
| Who can talk | Anyone (changed from "Me and my agents" for this run; reverted by Soham 17:54 IST) | Anyone |
| Room | new, created 17:32, no prior history | new, created 17:33, no prior history |
| Room Instructions | R1 text verbatim from quant-desk | blank |
| Sender | same Console user (admin) | same |
Only intended difference: R1 in room Instructions.

## Observed first replies (read from screen; NOT byte-exact — clipboard capture unavailable)
| Variant | Treatment: fee field? | Control: fee field? | Trade IDs? |
|---|---|---|---|
| V1 | No ("No fees, slippage…" assumption) | No | No / No |
| V2 | No ("fees and slippage are excluded") | No | No / No |
| V3 | No ("excluding fees and slippage") | No | No / No |
| V4 | No ("excluding fees and slippage") | No | No / No |
| V5 | No ("before fees and slippage") | No | No / No |

Both arms use `quantity`, not `qty`, and omit per-trade ids, so check_fees.py would escalate (exit 2) on all 10.

## Result
0/5 treatment and 0/5 control included fees. In fresh rooms, R1 delivered through room Instructions did NOT change worker behaviour.
The earlier treatment passes (V1,V3,V4,V5 in quant-desk) came from a room whose chat history contains the human correction, scribe draft and approval. This run suggests that history, not the Instructions field alone, drove fee inclusion. Not tested here: whether Instructions reach an agent added at room creation.

## Provenance gap
Raw payloads are visible in Mattermost channels clean-treat / clean-control. Export them (copy button per block) to eval/clean/raw/ and hash before any grading.
