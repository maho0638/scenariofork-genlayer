# Portal submission text — source + official Direct Mode QA verified

**Category:** Developer → Intelligent Contracts

**Title:** ScenarioFork — AI-Gated Pareto Frontier for Competing Plans

**Description (less than 1,000 characters):**

ScenarioFork is a GenLayer Intelligent Contract for comparing multiple plans without forcing one AI-chosen winner. An owner freezes a natural-language hard constraint and two to four proposed plans with stated cost and time. GenLayer's leader and validators independently determine which written plans meet the constraint, agreeing on the complete eligibility vector. Deterministic code then computes the Pareto frontier: every eligible alternative not strictly dominated on both cost and time is preserved. A plan can be cheaper but slower; another faster but more expensive. The owner can select only from this non-dominated set. Sealed plans cannot be changed, malformed AI output fails closed, and zero eligible options yields an empty set. This is transparent trade-off accounting based on self-reported inputs, not a prediction or independent certification.

**Evidence:** Public source: https://github.com/maho0638/scenariofork-genlayer . Real Studionet network integration: https://github.com/maho0638/scenariofork-genlayer/actions/runs/43894948732 . Contract deployed on chain ID 61999: `0x8a6dED4D5f94f88CFA4eA95d7AfBAd31425Be8eF`. Exact accepted write receipts, readbacks and consensus result: https://github.com/maho0638/scenariofork-genlayer/blob/main/docs/STUDIONET_PROOF.md . Separate on-chain finality and Explorer deep link were not claimed; no Portal submission has been made.
