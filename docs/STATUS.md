# STATUS — P0 progress

**Date:** 2026-09-09 (Asia/Shanghai)  
**Scope:** PRIORITY.md P0 — Attempt **#1 labctl** harden + Attempt **#26 atlasgate** MVP

## Done

### labctl (#1)
- [x] `pip install -e labctl` / console script `labctl`
- [x] `init` / `run` / `replay` working end-to-end
- [x] Run records: `experiment_sha256`, `command`, `exit_code`, `stdout`/`stderr`, `duration_s`, `runtime` (+ requested/effective/note)
- [x] Ledger: `runs/<run_id>.json` + appending `ledger.jsonl`; `labctl ledger list`
- [x] `labctl pins` ← `data/atlas-proceed-sample.json`
- [x] `labctl deny-check owner/repo` ← `data/atlas-hard-leaves.json` (`hard_ban` / `agentscan`)
- [x] Data root via `SYSTEMS_LAB_ROOT` or walk-up for `data/`
- [x] Runtimes: `local` always; `wasmtime`/`kind`/`gvisor` use binary if present else clear fallback message
- [x] pytest coverage under `labctl/tests`
- [x] `examples/hello-experiment` runs (wasmtime → local fallback when binary absent)

### atlasgate (#26)
- [x] Package `atlasgate/` with CLI entrypoint `atlasgate`
- [x] `atlasgate check-repo owner/name` — non-zero on `hard_ban`/`agentscan`
- [x] `atlasgate trailer` — AI disclosure trailer text
- [x] `atlasgate scan-ci` — invoke `zizmor` if on PATH, else skip note
- [x] Shares data-path resolution with `labctl.paths` (import with standalone fallback)
- [x] pytest under `atlasgate/tests`

### Docs / git
- [x] README quick-start with working commands
- [x] This STATUS.md
- [x] Commit + push to `origin/main` (`dc88ca1`)

## Not in P0 (queued)
- Full kind pod-exec / gVisor sandbox profiles
- libsql/litestream ledger backend (#20 sibling)
- Contract harness (#23), dataset ledger (#9)

## Verify locally

```bash
export SYSTEMS_LAB_ROOT=/path/to/systems-lab
pip install -e ./labctl -e ./atlasgate
pytest labctl/tests atlasgate/tests
labctl run examples/hello-experiment
atlasgate check-repo sqlite/sqlite; echo exit:$?
atlasgate trailer | head -2
atlasgate scan-ci
```
