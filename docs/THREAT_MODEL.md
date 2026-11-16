# Threat Model & Limits — ScenarioFork

1. **No real-world verification:** the condition, plans, costs and durations are provided by the same decision owner. AI checks only whether the *text* explicitly meets the condition. It cannot certify compliance, pricing, timing or real-world feasibility.
2. **Role separation:** only the owner can change a draft, seal, evaluate and select. Post-seal options and rules are immutable. Evaluation and selection are one-shot.
3. **Validator equivalence:** validators independently assess the *complete boolean eligibility vector*. Missing options, extras, strings disguised as booleans and malformed outputs fail. Shared hallucinations remain possible. The Pareto calculation is deterministic and cannot be altered by the model.
4. **Mathematical invariants:** a frontier option cannot be strictly dominated on both minimization axes by another eligible option; identical cost/time pairs both survive; all-ineligible yields an empty frontier; selection is impossible outside the frontier.
5. **Privacy/operations:** public plans only; no secrets, payment, oracle access, staking, prediction, financial recommendation, browser fetch, inter-contract calls or external actions. Costs and durations must use consistent real-world units defined by the user.
