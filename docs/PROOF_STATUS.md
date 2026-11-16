# Proof status — scenariofork-genlayer

Verification snapshot: 2026-11-16.

- Python 3.13 `compileall`: **PASS**.
- Offline pytest: **PASS (6/6)** on local Python 3.13 and official GitHub Actions ubuntu-24.04.
- Official GenLayer `genlayer-test` Direct Mode: **PASS (5/5)** on [GitHub Actions run 43862825800](https://github.com/maho0638/scenariofork-genlayer/actions/runs/43862825800), official genlayer-test==0.29.2 with v0.2.16 SDK runner pin and controlled LLM response fixtures.
- GenVM lint: **PASS (3 checks)** on the same official [GitHub Actions run 43862825800](https://github.com/maho0638/scenariofork-genlayer/actions/runs/43862825800).
- Public Studionet signed deploy/consensus/readback: **NOT EXECUTED** (not authorized; no transaction submitted).
- GitHub: **PUBLISHED** to https://github.com/maho0638/scenariofork-genlayer (all 11 source/test/docs files; fetched source equality confirmed).
- Explorer contract address: **NONE**.
- Portal submission: **NOT SUBMITTED**.

Verified on isolated free ubuntu-24.04 QA PR #2. The successful test workflow is now copied to `main` with **workflow_dispatch-only** trigger (no automatic deploy or secret usage). The test-only runner pin selects a real official GenVM release and does not falsify outputs. No signed StudioNet deployment/write/readback or Explorer evidence is claimed; obtain that if Portal review requires live proof.
