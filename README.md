# systems-lab

Local-first **systems engineering lab OS**: compose mature OSS parts into a replayable experiment loop.

```
experiment → sandbox (kind | gVisor | wasmtime) → artifacts (libsql + litestream + rclone)
          → verify (prometheus / yq / prql) → optional share (zrok/sish + mkcert)
```

This is **not** an LLM paper-writer or coding agent. Those can *use* the lab; they are not the product.

## Research trail (read first)

- [docs/ATTEMPTS.md](docs/ATTEMPTS.md) — every candidate: loop standability, prior art (GitHub **and** external), verdict, pursue/park/abandon
- [docs/REPORT.md](docs/REPORT.md) — method, composition graph, recommendation
- [data/PARTS.json](data/PARTS.json) — atlas capability → repos

**Only Attempt 1 is pursued.** Supply-chain verify, ZT personal edge, Coder-class DevEx, etc. were abandoned after prior-art hits (Chainloop, Octelium, …).

## Status

MVP scaffold: `labctl` CLI stubs + example experiment. Glue over Task/Dagger/kind/wasmtime is intentional — we assemble parts, we do not reimplement them.

Identity for commits: Jason Wang \<vulragrag@gmail.com\> / GitHub `vulragrag-star`.

## Quick start (stub)

```bash
pip install -e ./labctl   # or: python -m labctl --help
labctl init demos/hello
labctl run demos/hello
labctl replay <run-id>
```

## Moat / innovation (research claim)

- Atlas-grounded proceed pins + hard-leave deny list
- Multi-runtime hermetic defaults (gVisor + WASM + kind)
- Offline-first experiment ledger (content-addressed runs)

Not novel crypto/networking — composition + provenance UX.
