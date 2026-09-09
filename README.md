# systems-lab

Local-first **systems engineering lab OS**: compose mature OSS parts into a replayable experiment loop.

```
experiment → sandbox (kind | gVisor | wasmtime) → artifacts (libsql + litestream + rclone)
          → verify (prometheus / yq / prql) → optional share (zrok/sish + mkcert)
```

This is **not** an LLM paper-writer or coding agent. Those can *use* the lab; they are not the product.

## Architecture

**systems-lab = research hub** (survey + ATTEMPTS / BACKLOG / PRIORITY). Each pursue-candidate gets its **own implementation sibling repo** under `vulragrag-star`. We pursue **one at a time**, without rushing.

See **[docs/ORG.md](docs/ORG.md)** for the Attempt → repo mapping (`labctl`/`atlasgate` live here for now; pursue scaffolds `#23`/`#20`/`#9`/`#13`/`#29`/`#19` are live sibling repos).

## Research trail (read first)

- [docs/ORG.md](docs/ORG.md) — research hub vs sibling implementation repos (mapping table)
- [docs/ATTEMPTS.md](docs/ATTEMPTS.md) — every candidate (1–30): loop standability, prior art (GitHub **and** external), verdict, pursue/park/abandon
- [docs/CANDIDATE_BACKLOG.md](docs/CANDIDATE_BACKLOG.md) — full catalog table of all attempts
- [docs/PRIORITY.md](docs/PRIORITY.md) — ranked survivors (P0/P1/P2); **multiple** may be pursued in priority order (one implementation focus at a time)
- [docs/REPORT.md](docs/REPORT.md) — method, composition graph, recommendation + 2026-09-09 enumerate-all addendum
- [docs/STATUS.md](docs/STATUS.md) — P0 implementation progress + sibling-repo notes
- [data/PARTS.json](data/PARTS.json) — atlas capability → repos

**Multiple survivors.** Attempt 1 (systems lab) is P0, but the corrected methodology also keeps pursue-candidates with **live scaffolds**: atlasgate (#26, in-hub), [contract-harness](https://github.com/vulragrag-star/contract-harness) (#23), [ops-evidence](https://github.com/vulragrag-star/ops-evidence) (#20), [dataset-ledger](https://github.com/vulragrag-star/dataset-ledger) (#9), [docs-vault](https://github.com/vulragrag-star/docs-vault) (#13), [airgap-mirror](https://github.com/vulragrag-star/airgap-mirror) (#29), [edge-workers-lab](https://github.com/vulragrag-star/edge-workers-lab) (#19). Occupied loops (Chainloop, Octelium, Coder, AdGuard Home, ArchiveBox, Kubescape, …) stay abandoned.

## Status

P0 MVP (in this hub): hardened `labctl` (init/run/replay/ledger/pins/deny-check) + sibling `atlasgate` (check-repo/trailer/scan-ci). Glue over Task/Dagger/kind/wasmtime is intentional — we assemble parts, we do not reimplement them.

**Pursue scaffolds complete** (see [docs/STATUS.md](docs/STATUS.md) + [docs/ORG.md](docs/ORG.md)). Next: deepen one sibling at a time — not more greenfield scaffolds.

Identity for commits: Jason Wang \<vulragrag@gmail.com\> / GitHub `vulragrag-star`.

## Quick start

```bash
# from repo root
export SYSTEMS_LAB_ROOT="$PWD"   # optional; otherwise labctl/atlasgate walk up for data/
pip install -e ./labctl -e ./atlasgate
pip install pytest               # for tests

# labctl
labctl init demos/hello
labctl run demos/hello
labctl ledger list --path demos/hello
labctl replay <run-id> --path demos/hello
labctl pins --limit 10
labctl deny-check sqlite/sqlite

# example experiment (wasmtime falls back to local if binary missing)
labctl run examples/hello-experiment

# atlasgate
atlasgate check-repo yt-dlp/yt-dlp    # exit 1 (hard_ban)
atlasgate trailer
atlasgate scan-ci                     # runs zizmor if on PATH, else notes skip
```

### Tests

```bash
pytest labctl/tests atlasgate/tests
```

### Runtimes

| runtime   | behavior |
|-----------|----------|
| `local`   | subprocess (always) |
| `wasmtime`| `wasmtime run` when binary + `.wasm` command; else clear fallback to local |
| `kind`    | requires `kind` on PATH; otherwise clear fallback to local |
| `gvisor`  | requires `runsc`; otherwise clear fallback to local |

Atlas data files (`data/atlas-proceed-sample.json`, `data/atlas-hard-leaves.json`) are resolved via `SYSTEMS_LAB_ROOT` or by walking up from cwd for a `data/` directory.

## Moat / innovation (research claim)

- Atlas-grounded proceed pins + hard-leave deny list
- Multi-runtime hermetic defaults (gVisor + WASM + kind)
- Offline-first experiment ledger (content-addressed runs)
- Policy-pack siblings (disclosure/release gate, evidence notary) sharing the same atlas data

Not novel crypto/networking — composition + provenance UX.
