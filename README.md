# systems-lab

Local-first **systems engineering lab OS**: compose mature OSS parts into a replayable experiment loop.

```
experiment → sandbox (kind | gVisor | wasmtime) → artifacts (libsql + litestream + rclone)
          → verify (prometheus / yq / prql) → optional share (zrok/sish + mkcert)
```

This is **not** an LLM paper-writer or coding agent. Those can *use* the lab; they are not the product.

## Research trail (read first)

- [docs/ATTEMPTS.md](docs/ATTEMPTS.md) — every candidate (1–30): loop standability, prior art (GitHub **and** external), verdict, pursue/park/abandon
- [docs/CANDIDATE_BACKLOG.md](docs/CANDIDATE_BACKLOG.md) — full catalog table of all attempts
- [docs/PRIORITY.md](docs/PRIORITY.md) — ranked survivors (P0/P1/P2); **multiple** may be pursued in priority order
- [docs/REPORT.md](docs/REPORT.md) — method, composition graph, recommendation + 2026-09-09 enumerate-all addendum
- [data/PARTS.json](data/PARTS.json) — atlas capability → repos

**Multiple survivors.** Attempt 1 (systems lab) is P0, but the corrected methodology also keeps pursue-candidates such as atlasgate (#26), API contract harness (#23), ops evidence (#20), dataset ledger (#9), docs vault (#13), airgap mirror (#29), and edge workers (#19). Occupied loops (Chainloop, Octelium, Coder, AdGuard Home, ArchiveBox, Kubescape, …) stay abandoned.

## Status

MVP scaffold: `labctl` CLI stubs + example experiment (Attempt 1 spine). Glue over Task/Dagger/kind/wasmtime is intentional — we assemble parts, we do not reimplement them. Sibling pursue items follow `PRIORITY.md` order.

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
- Policy-pack siblings (disclosure/release gate, evidence notary) sharing the same atlas data

Not novel crypto/networking — composition + provenance UX.
