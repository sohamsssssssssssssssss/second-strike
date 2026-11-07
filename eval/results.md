# P4 results — updated 7 November 2026

## Preserved live observations

| Variant | Treatment | Control | Matched comparison |
| --- | --- | --- | --- |
| V1 | Checker pass | Checker escalate; public room | Not admissible |
| V2 | Not captured/run | Earlier reply visible; not captured or graded | Incomplete |
| V3 | First reply preserved, hashed before grading; pass | User supplied reply omits fees and uses quantity; not graded here | Preliminary only |
| V4 | First reply preserved, hashed before grading; pass | First reply preserved, hashed before grading; escalate | Preliminary only |
| V5 | First reply preserved, hashed before grading; pass | First reply preserved, hashed before grading; escalate | Preliminary only |

Four preserved treatment variants pass. Three captured control variants (V1, V4, V5) escalate for missing trade IDs; they also omit fees and use quantity instead of qty. An escalation is not a clean fee-only failure. V4 control also reports traded_value 906 against trade notionals totaling 905. Raw outputs must remain unchanged.

No causal effect or completed five-pair evaluation is claimed. Historical runtime equivalence is unverified, control history exists, and sender identities differ. The current worker-b configuration was independently read on 7 November as gpt-6-luna; current settings do not prove historical runtime. V1 treatment was checked once before its first recorded hash, an audit limitation. V3 duplicate responses were not substituted for the preserved first treatment.

## Frozen checker validation

Previously verified: all 15 frozen fingerprints match; all ten valid fixtures pass, with zero false blocks. Five local tests passed. These checks validate the checker and saved examples, not live learning.

## Pending

Capture remaining V2 evidence; inspect control configuration; establish a clean matched run if a causal comparison is required; preserve first responses and hashes before checker grading. UI navigation currently leaves the page unchanged, and direct coordinate clicks have returned noWindowsAvailable. No new tests are claimed as sent during this blocked inspection.

## Control settings confirmed — 7 November, 02:38

The supplied screenshot and fresh UI read confirm control-worker-fresh is configured for gpt-6-luna, with default reasoning, verbosity, reasoning summary and web search, matching worker-b’s current advanced configuration. This resolves current configured-model matching only; historical runtime remains unverified. Control agent instructions are blank; worker-b has synthetic-ledger instructions. Control auto mode is on, whereas worker-b auto mode was off. Control addressing is Anyone; worker-b addressing is Me and my agents. These differences are recorded, not silently changed. Room navigation again left the settings page unchanged.
