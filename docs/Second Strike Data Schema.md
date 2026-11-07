# Second Strike: Data Schema

Owner: Soham. Draft v1, 4 Nov 2026. There is no server database. Switch holds the room's History, Rules, Tasks and Decisions; this schema covers only what we store ourselves, as plain JSON files and CSVs in the repo so a clone reproduces everything. If it later needs a database, SQLite with the same fields is a direct fit.

VERIFY: what Switch already stores for Rules and Decisions. Where Switch has a native record, reference its id here instead of duplicating the fields.

> **Status, 7 Nov 2026.** Original schema. Current claims are in `README.md`.
> - **Implemented:** `rules/R1.json` with `id`, `status`, `expiry` (spec: `expires_at`), `hits`, `last_fired`, `revoked_at`, `revoked_by`, `approved_by`, `approval_message`, `draft_message`, `activated_at`. `rules/events.jsonl` (spec path: `eval/events.jsonl`), written append-only by `checkers/gate.py`, one line per check, skip, or revoke. Ledgers in `eval/ledgers/` with fee fields only. SHA-256 manifests in `eval/frozen_hashes.txt` and `eval/live_hashes.txt`.
> - **Not implemented:** `decision_ref` (no native Decision), `overrides`, `created_by`, `created_at`, `eval/pairs/`, `eval/runs/`, pair outcome classification, and a `sha256` field inside ledger files.
> - **Not validated by the checker:** ledger `traded_value`, provenance, and top-level agent/model fields.

## 1. Entities at a glance

| Entity | Stored in | Purpose |
| --- | --- | --- |
| Rule | `rules/<id>.json` | The rule, its checker, status and counters |
| Ledger | `eval/ledgers/<id>.json` | A backtest submission from an agent |
| Trade (inside Ledger) | same file | One trade with its fee |
| Submission event | `eval/events.jsonl` | Each time a ledger is gated |
| Pair | `eval/pairs/<id>.json` | One paired first-submission test |
| Eval run | `eval/results.md` and `eval/runs/<id>.json` | Aggregated counts |
| Decision reference | field on Rule | Link to the Switch Decision |

## 2. Rule

```json
{
  "id": "R1",
  "title": "Apply 5 bps trading cost per trade",
  "what": "Every trade in a backtest ledger includes a cost of 5 bps of notional.",
  "why": "Ledgers without costs overstate returns.",
  "scope": "backtest ledgers in room quant-desk",
  "expires_at": "2026-11-30",
  "checker": "checkers/check_fees.py",
  "passing_example": "eval/ledgers/ex_pass_fees.json",
  "failing_example": "eval/ledgers/ex_fail_fees.json",
  "status": "active",
  "hits": 0,
  "overrides": 0,
  "last_fired": null,
  "created_by": "scribe",
  "approved_by": "reviewer",
  "decision_ref": "<Switch Decision id>",
  "revoked_by": null,
  "created_at": "2026-11-04T00:00:00+05:30"
}
```

- `status`: `draft`, `active`, `revoked`, `expired`, `flagged`.
- `checker`: a script path, or the string `nl` for a natural-language rule evaluated by the gate agent.
- `hits`: times the rule blocked a submission. `overrides`: times a human overrode that block.

## 3. Ledger

```json
{
  "id": "L-0007",
  "task_id": "T-S2",
  "agent": "worker-b",
  "provider": "opencode",
  "model": "<model name>",
  "strategy": "S2",
  "submitted_at": "2026-11-05T11:00:00+05:30",
  "sha256": "<hash of the trades array>",
  "trades": [
    { "id": 1, "symbol": "ABC", "side": "buy", "qty": 100, "price": 100.0, "fee": 5.0 }
  ],
  "traded_value": 100000.0,
  "labels": { "flawed": false, "flaw_class": null, "split": "valid" }
}
```

- `sha256` is computed and stored when the ledger is frozen, before the gate runs. It proves the paired test compared untouched first submissions.
- `labels.split`: `valid`, `unseen_variant`, `seed` or `example`.
- Fee check: `fee` should equal `qty * price * 0.0005` within 0.01.

## 4. Submission event

One JSON line per gate run, append-only.

```json
{
  "ts": "2026-11-05T11:01:00+05:30",
  "ledger_id": "L-0007",
  "rule_id": "R1",
  "verdict": "pass",
  "detail": "0 offending trades",
  "actor": "gate",
  "human_override": false
}
```

`verdict` is `pass`, `fail` or `escalate`.

## 5. Pair (paired first-submission test)

```json
{
  "id": "P-003",
  "task_id": "T-V3",
  "agent_with_rule": { "ledger_id": "L-0021", "provider": "opencode" },
  "agent_without_rule": { "ledger_id": "L-0022", "provider": "codex" },
  "frozen_before_gate": true,
  "outcome": "worker-learned"
}
```

`outcome` is one of `worker-learned`, `gate-rescued`, `correct-without-rule`. Classification is computed by the harness from the frozen ledgers and gate verdicts, not typed by hand.

## 6. Eval run

```json
{
  "id": "E-001",
  "n_unseen_variants": 5,
  "caught": 0,
  "n_valid": 10,
  "false_blocks": 0,
  "pairs": { "worker_learned": 0, "gate_rescued": 0, "correct_without_rule": 0 },
  "notes": ""
}
```

The zeros are placeholders. Real values are written by the harness and reported as raw counts with n. No results exist yet.

## 7. Relationships

- A Rule has one Decision reference (Switch) and many Submission events.
- A Ledger has many Submission events (one per active rule checked).
- A Pair references exactly two Ledgers.
- An Eval run aggregates Pairs and Submission events.

## 8. Integrity rules

- Ledgers are immutable once `sha256` is set. Fix by creating a new ledger.
- Submission events are append-only.
- A rule cannot become `active` unless its activation test passed (passing example passes, failing example fails).
- Revoking sets `status` to `revoked` and records `revoked_by`; the record is never deleted.
- Eval ledgers are not edited after results are seen.

## 9. Future work

Moved here on 7 Nov 2026. Original wording kept.

- `decision_ref` on Rule: "Link to the Switch Decision." Not established.
- `overrides` counter and `flagged` status (§2, §8). Not implemented.
- `eval/pairs/<id>.json` and `eval/runs/<id>.json` (§1, §5, §6). Not implemented.
- Pair outcome classification computed by a harness (§5). Not implemented.
- Ledger `sha256` field (§3). Hashes exist in manifests instead.
