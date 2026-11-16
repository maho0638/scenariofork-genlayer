# Verified evidence status — scenariofork-genlayer

Last checked: **2026-11-16**. Public code in `main` corresponds to the Studio-tested contract source.

## Complete automated QA

- Python compilation: **PASS**.
- Offline state-machine regression: **PASS 6/6**.
- Official GenLayer Direct Mode SDK (real GenVM, controlled LLM response fixtures): **PASS 5/5**.
- Official GenVM lint: **PASS**.
- Official Direct Mode and lint report: https://github.com/maho0638/scenariofork-genlayer/actions/runs/43862825800

## Actual hosted GenLayer Studionet

- Network RPC: `https://studio.genlayer.com/api` — chain ID **61999 verified by JSON-RPC before transactions**.
- Actual contract deployment: **PASS** — `0x8a6dED4D5f94f88CFA4eA95d7AfBAd31425Be8eF`.
- Accepted on-network transactions: **PASS** — 5 write transactions plus the deployment, with readbacks.
- Unmocked AI nondeterministic execution and validator consensus: **PASS** with `leader_only=false`.
- GitHub free runner `ubuntu-24.04`: **PASS 1/1 integration acceptance test**.
- Full real-network GitHub job and logs: https://github.com/maho0638/scenariofork-genlayer/actions/runs/43894948732
- Exact transaction hashes, observed state and security limits: [STUDIONET_PROOF.md](STUDIONET_PROOF.md).

## What this does and does not prove

This is a **real hosted Studionet execution**, not a local host mock, Direct Mode only, or a claim about Bradbury/mainnet. The test used an ephemeral GenLayer SDK-generated sender, with no user wallet keys or GitHub secrets. No value transfers. Successful receipts and state readbacks were checked; **separate transaction finality was not checked**. Studionet can reset. No guaranteed Community Points or mainnet security audit is claimed.

The deploy workflow in `main` is **manual-only** (`workflow_dispatch`), so commits/PRs cannot automatically redeploy or spend test resources. Portal submission: **NOT SUBMITTED**.
