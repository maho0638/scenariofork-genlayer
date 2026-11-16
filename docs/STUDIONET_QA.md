# Studio integration acceptance (QA only)
Manual-only GitHub workflow connects to stable official Studionet, ID 61999,
using a freshly generated ephemeral account in the official GenLayer testing
suite. No user private keys, user balances, real currency transfers, GitHub
secrets, mainnet, Bradbury, or Vercel involvement.

One deployment, 5 genuine write operations (register decision, two options,
seal, AI evaluate), and state readbacks. Leader-only bypass disabled, LLM mocks
disabled. Inaccessible RPC, absent faucet funding, consensus disagreement, or
revert must FAIL rather than be represented as success.
