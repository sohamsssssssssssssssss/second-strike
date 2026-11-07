# Second Strike: Rules and Guardrails

Owner: Soham. Draft v1, 4 Nov 2026. Two kinds of rules live here: (A) rules for how the project is built, claimed and submitted, and (B) rules for how the product's own agents and rules behave. Give section A to any coding agent (Codex, OpenCode) as standing context.

## A. Build and submission guardrails

### A1. Honesty of claims

- Claim only what `eval/results.md` shows. Report raw counts with n, never bare percentages.
- Do not claim "impossible without Switch". The honest claim: a local rules file can store the text; Switch adds multi-vendor agents reading the same Rules, one-tap approval logged as a Decision where the team already works, and a shared audit trail.
- Do not claim "cross-vendor" if both workers are Codex. Say "same vendor, different models".
- Do not claim agents never make the same mistake twice, or any "100% passing" result.
- Do not present the mechanism as novel. Credit prior art (rules files, Cursor Bugbot, CodeRabbit learnings, Reflexion-style work). The contribution is the team-room, multi-vendor, human-approved, auditable packaging.
- Report messy results as they are (for example 3 of 5 caught, 1 false block). Never tune the eval set after seeing results.

### A2. Hackathon compliance

- Build the Switch setup and workflow during the event (4-7 Nov 2026). Existing libraries, templates and agents are fine. Do not reuse pre-hackathon work as the main submission.
- Switch must be central, and the README must show how it is used.
- Be able to explain every file you submit. Do not submit AI output you have not read and understood. State in the README which parts agents wrote and what you verified.
- Confirm in the WeMakeDevs Discord whether one project may be entered in both Track 1 and Track 2 before submitting to both.
- Check the submission form requirements before the final day.

### A3. Engineering guardrails for coding agents

- Read the Switch docs and the example template before writing any Switch code. Do not invent Switch APIs. If something is not documented, say so and stop.
- Mark anything unverified as VERIFY in code comments and in the tracker.
- Keep checkers deterministic, offline and dependency-light. No network calls inside a checker.
- Every checker has at least one passing and one failing fixture, and unit tests.
- Do not edit eval ledgers after results are seen. Fix by adding new ledgers.
- Freeze and hash first-submission ledgers before the gate runs.
- Keep scope small: one finished project beats two half-finished ones. Life Room is built only after Track 1 is done.
- Prompts to coding agents are lean and start with a short context brief.

### A4. Secrets and privacy

- No API keys, tokens or personal data in the repo, logs, README, screenshots or the demo video.
- Keys live in environment variables or the Console's own settings. Add a `.gitignore` entry for any local env file.
- Check Gemini quota before long runs; space runs and label them.
- Do not push the parked Goose branch (`feat/goose-provider`) as part of this submission.

## B. Product rules for agents and rules

### B1. Separation of duties

- A worker never grades its own output. The gate is a separate agent or script.
- Where the stack allows, the gate uses a different model family from the worker it checks.
- The scribe drafts rules; it never approves them. Only a human approves (one-tap Decision).

### B2. Rule quality

- Every rule has: what, why, scope, expiry, a passing example and a failing example.
- A rule is activated only if its checker passes the passing example and fails the failing example. Otherwise activation is refused.
- Prefer deterministic checkers. Use natural-language evaluation only when no script is feasible.
- Rules are narrow in scope and have an expiry date, so stale rules do not silently accumulate.

### B3. Gate behaviour

- Verdicts are `pass`, `fail` or `escalate`. When a natural-language rule is ambiguous, the gate escalates to a human; it never guesses to block or pass.
- A block always names the rule id and shows the checker output so the worker and the human can see why.
- Every gate run is logged as an append-only event.

### B4. Human control

- Any teammate can revoke a rule in chat; the revoke is logged as a Decision.
- A human override of a block flags the rule for review.
- Revoked and expired rules are kept as records, never deleted.

### B5. Scope limits for the demo

- Agents only touch seeded or synthetic data. No real trading, no real money, no real bookings.
- Backtest figures in the demo are illustrative; the README says so.

## C. Definition of done

- Room runs from the template; a clone reproduces the demo (dry-run mode available).
- Paired first-submission test and mini eval results saved with raw counts.
- README matches the results file and lists known limits.
- 60s demo video recorded with no secrets on screen.
- Submitted before 7 Nov 2026, 11:59 PM IST (target 6 PM).
