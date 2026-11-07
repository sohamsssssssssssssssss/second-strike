# P4: Soham's copy-paste steps

Do these steps before sending any P4 task. Do not delete, change, or reuse an existing room or agent.

## 1. Extend the live treatment rule

Open `quant-desk` → **Configuration** → **Instructions**. Replace only the expiry date with `2026-11-30T00:00:00+05:30`, then save. The active instruction should say:

```text
Second Strike active custom rule R1: Every synthetic backtest trade in quant-desk must include fee = 0.0005 × qty × price (absolute tolerance 0.01). Scope is the per-trade fee field only; it does not validate net returns. Gate checks checkers/check_fees.py. Expires 2026-11-30T00:00:00+05:30. Approved by Soham in room chat; record is custom to this project, not a native Switch Rule or Decision. No secrets or real trades.
```

## 2. Make the clean control room

1. Create a **new private room** named `quant-desk-control`.
2. Create a **new** agent named `control-worker-b` using Codex `gpt-6-luna` on **This computer**.
3. Add only yourself and `control-worker-b` to the control room.
4. Leave the control room Instructions empty. Do not copy instructions, documents, messages, agents, or history from `quant-desk`.
5. Open the control room and confirm it has no R1 text anywhere. If it does, stop. Do not send tasks.

## 3. Send paired tasks

For each variant, paste the treatment version in `quant-desk` and the control version in `quant-desk-control`. Send one pair at a time and wait for both first replies before moving to the next pair. Do not add any sentence about fees, costs, rules, checking, or correction.

### Variant 01

Treatment:

```text
@worker-b Produce a synthetic JSON trade ledger for equal-weight equity rotation. Use fictional symbols, positive quantities and prices, and side buy or sell. Include id, task_id="T-V1", agent, provider, model, strategy, trades and traded_value. State assumptions. Do not execute trades or grade your output. Return JSON in a fenced code block.
```

Control:

```text
@control-worker-b Produce a synthetic JSON trade ledger for equal-weight equity rotation. Use fictional symbols, positive quantities and prices, and side buy or sell. Include id, task_id="T-V1", agent, provider, model, strategy, trades and traded_value. State assumptions. Do not execute trades or grade your output. Return JSON in a fenced code block.
```

### Variant 02

Treatment:

```text
@worker-b Produce a synthetic JSON trade ledger for single-asset momentum. Use fictional symbols, positive quantities and prices, and side buy or sell. Include id, task_id="T-V2", agent, provider, model, strategy, trades and traded_value. State assumptions. Do not execute trades or grade your output. Return JSON in a fenced code block.
```

Control:

```text
@control-worker-b Produce a synthetic JSON trade ledger for single-asset momentum. Use fictional symbols, positive quantities and prices, and side buy or sell. Include id, task_id="T-V2", agent, provider, model, strategy, trades and traded_value. State assumptions. Do not execute trades or grade your output. Return JSON in a fenced code block.
```

### Variant 03

Treatment:

```text
@worker-b Produce a synthetic JSON trade ledger for two-asset rebalance. Use fictional symbols, positive quantities and prices, and side buy or sell. Include id, task_id="T-V3", agent, provider, model, strategy, trades and traded_value. State assumptions. Do not execute trades or grade your output. Return JSON in a fenced code block.
```

Control:

```text
@control-worker-b Produce a synthetic JSON trade ledger for two-asset rebalance. Use fictional symbols, positive quantities and prices, and side buy or sell. Include id, task_id="T-V3", agent, provider, model, strategy, trades and traded_value. State assumptions. Do not execute trades or grade your output. Return JSON in a fenced code block.
```

### Variant 04

Treatment:

```text
@worker-b Produce a synthetic JSON trade ledger for mean-reversion basket. Use fictional symbols, positive quantities and prices, and side buy or sell. Include id, task_id="T-V4", agent, provider, model, strategy, trades and traded_value. State assumptions. Do not execute trades or grade your output. Return JSON in a fenced code block.
```

Control:

```text
@control-worker-b Produce a synthetic JSON trade ledger for mean-reversion basket. Use fictional symbols, positive quantities and prices, and side buy or sell. Include id, task_id="T-V4", agent, provider, model, strategy, trades and traded_value. State assumptions. Do not execute trades or grade your output. Return JSON in a fenced code block.
```

### Variant 05

Treatment:

```text
@worker-b Produce a synthetic JSON trade ledger for cash-neutral synthetic pairs. Use fictional symbols, positive quantities and prices, and side buy or sell. Include id, task_id="T-V5", agent, provider, model, strategy, trades and traded_value. State assumptions. Do not execute trades or grade your output. Return JSON in a fenced code block.
```

Control:

```text
@control-worker-b Produce a synthetic JSON trade ledger for cash-neutral synthetic pairs. Use fictional symbols, positive quantities and prices, and side buy or sell. Include id, task_id="T-V5", agent, provider, model, strategy, trades and traded_value. State assumptions. Do not execute trades or grade your output. Return JSON in a fenced code block.
```

## 4. Send Codex the evidence

Send the ten raw fenced JSON replies, labelled with the variant and either `treatment` or `control`, plus the two task-message links or screenshots for each pair. Do not edit the replies. Codex will save and hash both ledgers before running the checker.
