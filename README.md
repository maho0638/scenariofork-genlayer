# ScenarioFork — Consensus-Gated Pareto Decision Frontier

**A GenLayer Intelligent Contract that preserves trade-offs instead of picking an AI-favored winner.** Independently verified natural-language hard constraints filter alternatives; deterministic code then computes the genuine non-dominated options on explicitly declared cost and time.

## The novel primitive

A decision owner defines a frozen context and one non-negotiable plain-language condition. They register 2–4 alternative plans with declared positive cost and duration values. Once sealed, GenLayer validators independently evaluate whether *each plan* explicitly satisfies the same condition. Plans violating it, or missing enough information, fail closed.

Among the eligible plans, a deterministic **Pareto frontier** keeps every option for which no other eligible option is **no worse on both metrics and strictly better on at least one**. A low-cost slow plan and a higher-cost fast plan can *both* survive. The decision owner may choose **only** from this frontier; no AI can choose a single winner or rewrite the quantitative metrics.

## Example

Frozen condition: `All customer records must remain in an EU data-center region.`

| Option | Plan | Cost (declared units) | Days (declared units) | Expected outcome |
| --- | --- | ---: | ---: | --- |
| fast | EU Frankfurt, automated | 80 | 4 | Frontier |
| cheap | EU Paris, manual | 40 | 10 | Frontier |
| slow | EU Dublin, manual | 90 | 12 | Dominated |
| unsafe | US data center | 10 | 2 | Ineligible |

The rule is about **plans as written**, not independent verification of actual hosting location. Cost/time are caller-supplied comparables using one unit system chosen off-chain; no prediction, accounting or third-party certification is claimed.

## Contract API

- `open_decision(id, question, hard_rule)` — frozen rule plus SHA-256.
- `add_option(id, option_id, label, plan, cost_units, time_units)` — decision-owner-only, up to four.
- `seal_decision(id)` — freezes 2–4 options for evaluation.
- `evaluate(id)` — GenLayer leader and validators independently calculate exactly the same eligibility vector; deterministic Pareto frontier stored.
- `select_frontier_option(id, option_id)` — owner-only single choice from frontier.
- `get_decision`, `get_option` — public JSON views.

Contract: [`contracts/ScenarioFork.py`](contracts/ScenarioFork.py).

## Why different from existing repositories?

This does **not** use the one-shot PASS/FAIL rubrics of RubricLedger/TenderLens, winner-take-all ranking of ResearchArena, or money-settlement flows of ResolveGraph. The economically important result is a **set of incomparable constrained choices**, not an AI-selected label or single ranking. A decision may legitimately have **zero** eligible options, preventing forced conclusions.

## Trust and security boundaries

See [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md). The model checks textual plans against the user-authored rule. It does not retrieve or certify external facts. Malicious self-reported plans or understated budgets cannot be detected automatically. LLM agreement can be wrong. Validators independently reassess the eligibility **vector**; neither leader nor validator may edit costs/durations. Unauthorized or post-seal changes and a second selection are blocked.

## Test without spending testnet GEN

```bash
python -m pip install pytest
python -m pytest -q tests/offline
```

Offline host-mock tests are **not** GenVM tests. An optional, **manual-only**, GitHub Actions job runs official GenLayer SDK Direct Mode tests and GenVM lint; it never deploys or signs anything.

## Proof status

- Offline state-machine tests: see [`docs/PROOF_STATUS.md`](docs/PROOF_STATUS.md).
- Official SDK, lint, Studionet Explorer: **not claimed until observed**.
- Portal contribution needs a valid repository plus a real Explorer deployment of the matching source revision.

See [`SUBMISSION_DRAFT.md`](SUBMISSION_DRAFT.md) after on-chain verification. No promise of approval or points.
