# Portal submission text — source + official Direct Mode QA verified

**Category:** Developer → Intelligent Contracts

**Title:** ScenarioFork — AI-Gated Pareto Frontier for Competing Plans

**Description (less than 1,000 characters):**

ScenarioFork is a GenLayer Intelligent Contract for comparing multiple plans without forcing one AI-chosen winner. An owner freezes a natural-language hard constraint and two to four proposed plans with stated cost and time. GenLayer's leader and validators independently determine which written plans meet the constraint, agreeing on the complete eligibility vector. Deterministic code then computes the Pareto frontier: every eligible alternative not strictly dominated on both cost and time is preserved. A plan can be cheaper but slower; another faster but more expensive. The owner can select only from this non-dominated set. Sealed plans cannot be changed, malformed AI output fails closed, and zero eligible options yields an empty set. This is transparent trade-off accounting based on self-reported inputs, not a prediction or independent certification.

**Evidence:** Public GitHub source and reproducible official GenLayer Direct Mode + GenVM lint test report: https://github.com/maho0638/scenariofork-genlayer/actions/runs/43862825800 . No live Studionet deployment or Explorer address has been verified; supply an Explorer link only if the review explicitly requires a signed network deployment.
