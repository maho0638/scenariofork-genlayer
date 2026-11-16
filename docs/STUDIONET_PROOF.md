# Real Studionet acceptance proof — scenariofork-genlayer

**Observed on 2026-11-16, not simulated.** GitHub Actions executed the official `gltest` Studio Mode against the stable hosted GenLayer Studionet RPC `https://studio.genlayer.com/api`. A JSON-RPC `eth_chainId` check confirmed **61999** before any network writes.

- Successful public GitHub Actions run: https://github.com/maho0638/scenariofork-genlayer/actions/runs/43894948732
- Tested contract source: [contracts/ScenarioFork.py](../contracts/ScenarioFork.py) (source file in `main` unchanged from QA run)
- Network: GenLayer Studionet (temporary hosted development network, **not Bradbury**)
- Contract deployed and read back: `0x8a6dED4D5f94f88CFA4eA95d7AfBAd31425Be8eF`
- Ephemeral SDK-generated sender (address only): `0x0F563Bd293656E74d6C50ff1e687A24F5268f53D`
- Integration test: **PASS 1/1 (55.93 s)**
- Recorded post-consensus state: `EVALUATED; eligible {"cheap":true,"fast":true}; frontier ["cheap","fast"]`

## Real accepted transaction receipts

- **open_decision**: `0x92fb457d6e3e4def4031da9e582b18a59258042f23d18807aa722215006a81f0`
- **add_option fast**: `0xebd76f042622b3f2381f7761d5f9b057f043ef8a504d7feada138eb3c22aaccb`
- **add_option cheap**: `0x664089617780de60f8e69bb4e1d2e4a124e9a5d6b09d934ce1ca61724035bae4`
- **seal_decision**: `0x34232a7376e0674aa662d1a394d174b267c5d86d6d0b3d6eeceaa718a8960cf2`
- **evaluate**: `0xb7b91229da33ae073aaabb6999026e6cf953f1e4561aa38bc6d41a637ea86be3`

## Scope and limitations

- The test runs on GitHub's free `ubuntu-24.04` runner, with `genlayer-test==0.29.2` and `genlayer-py==0.16.3`.
- Genuine remote contract deployment, write transaction receipts, on-network readbacks and one AI/validator consensus call. `leader_only=false`, **no LLM response mocks** in this Studio test.
- No user's wallet keys, repository secrets, paid cloud service, mainnet or Bradbury activity. Generated temporary test account key is never printed or stored.
- Receipt success was verified using `tx_execution_succeeded` and readbacks; **separate post-acceptance finality check was not conducted**. Do not claim mainnet readiness or unrestricted reproducibility; this hosted network can reset.
- Existing separate Direct Mode SDK tests and GenVM static lint have also passed; see [PROOF_STATUS.md](PROOF_STATUS.md).
- Portal: **not submitted**.

Run the network test again only by explicitly using the `workflow_dispatch` manual workflow; do not introduce automatic network deployment triggers.
