# Composition-gap research — REPORT

**Atlas:** vulragrag-star OSS terrain (`/workspace/oss-atlas`)  
**Date:** 2026-09-09 (Asia/Shanghai)  
**Outputs:** `REPORT.md` · `PARTS.json` · `ATTEMPTS.md`  
**Constraint:** research only — no GitHub PRs/forks; stars/policies only from `scored.jsonl`.

---

## 1. Method (how the atlas was mined)

1. **Coverage read** — `SYNTHESIS.md`: 1193 scored / **786 proceed** across eight sectors; hard leaves include sqlite, kanidm, openbao, AgentScan circles, multiple AI bans.
2. **Shortlist sanity** — `SHORTLIST.md` (100 repos) for sector-balanced famous parts (cli, devops, editors, python, db, compilers, security, networking).
3. **Proceed extract** — all `proceed=true` rows from `data/scored.jsonl` → `proceed.json` (786). Fields used: `full_name`, `stars`, `sector`, `policy`, `why`, `bug_class_hint`.
4. **Capability bucketing** — keyword + sector fallback into ten reusable buckets (see §2 / `PARTS.json`). Multi-label allowed (e.g. `dagger` in sandbox+workflow).
5. **Sector survey skim** — `/home/box/oss-contributor-playbook/survey/by-sector/*.md` proceed tables for midband fills (e.g. `octelium`, `guac`, `cargo-crev`, tunnel midband).
6. **Closed-loop ideation** — ask where **many mature parts exist** but **no widely adopted open product** owns end-to-end assembly (“零件齐了、总装没人做”).
7. **Standability filter (priority #1)** — for each idea: is there a concrete runnable path (compose/CLI) that a small team could ship without inventing a new runtime/crypto/network stack?
8. **Competitive scan (priority #2)** — WebSearch + WebFetch **beyond GitHub**: product sites, HN, blogs, arXiv, vendor docs (Chainloop, GUAC, Octelium, Wiredoor, Dagger docs, nXsi, machinable, ScaleVP, OpenHands blog, etc.).
9. **Lab notebook (priority #3)** — every candidate logged in `ATTEMPTS.md` with fixed fields, including abandons.

---

## 2. Composition graph (capability buckets)

| Bucket | Atlas proceed hits (keyword pass) | Role in a closed loop |
|---|---:|---|
| sandbox | 17 | Isolation: gVisor, kind, WASM, Dagger/devbox |
| workflow | 18 | Task/CI/GitOps engines |
| storage | 18 | Sync, embedded DB, backup, metrics TSDB |
| identity_tls | 17 | mkcert, step-ca, OIDC/IAM, mesh identity |
| tunnel_edge | 21 | frp/ziti/zrok/sish/DNS edge |
| package_release | 47 | uv/bun/nix/goreleaser/buildx/… |
| policy_scan | 14 | kyverno/clair/zizmor/dive/dockle/… |
| query_analytics | 11 | prometheus/superset/prql/yq/… |
| harvest_fetch | 11 | scrapy/monolith/hurl/doggo/… |
| editor_agent_ux | 35 | neovim/coder/lazygit/dozzle/… |

Full repo lists with stars/policies: **`PARTS.json`**. Scenario→repo maps for the top three preferred themes live under `scenario_part_maps`.

**Policy note (AgentScan / AI bans):** proceed set is already filtered to `silent`/`disclosure`. Hard leaves relevant to assembly: `sqlite/sqlite` (agentic ban — prefer `tursodatabase/libsql`), `kanidm`/`openbao` (hard_ban — use `dex`/`zitadel`/`gopass`/`sealed-secrets` instead), AgentScan orgs (svelte/astro/nuxt/aiohttp/vite-plus) — never farm those. Disclosure homes (`zizmor`, `goreleaser`, `flux`, `pomerium`, `rclone`, `litestream`, …) need Assiste/d disclosure trailers if AI-assisted.

---

## 3. Candidate closed loops (ranked)

Ranking axes: **part readiness**, **gap clarity**, **small-team buildability from existing deps**, **differentiation from AutoGPT/OpenHands-class agents**.

| Rank | Scenario | Part readiness | Gap clarity | Buildability | vs agents | Outcome |
|---|---|---|---|---|---|---|
| 1 | Local-first **systems engineering lab** | very high | medium→high if narrowed | high | strong (lab OS ≠ coding agent) | **pursue** |
| 2 | Supply-chain verify loop | high | low (occupied) | high | medium | abandon |
| 3 | Zero-trust personal edge | very high | low (occupied) | medium | strong | abandon |
| 4 | Secure remote DevEx | high | none (Coder) | n/a | weak | abandon |
| 5 | Observability+backup | high | none (commodity) | high | n/a | abandon |
| 6 | Agent-safe OSS contrib sandbox | medium | low–medium | medium | medium | park |
| 7 | WASM hermetic capsule | medium | low | medium | weak | abandon |
| 8 | GitOps platform-in-a-box | high | none (lab-in-a-box) | high | n/a | abandon |

Detail: `ATTEMPTS.md`.

---

## 4. Deep dive — TOP 2

### 4.1 TOP 1 — Local-first systems engineering lab (pursue)

**Closed-loop claim (narrowed):**  
A personal/small-team **lab OS** where an experiment is a first-class object: hermetic execute → content-addressed artifacts → provenance ledger → query/verify → optional private share. Driver may be human, Task, Dagger, or an external agent — the product owns **reproducibility infrastructure**, not LLM paper writing.

**Exact parts (atlas):** see Attempt 1 table — core spine:

```
go-task/task + dagger/dagger
    → google/gvisor | kubernetes-sigs/kind | bytecodealliance/wasmtime
    → tursodatabase/libsql + benbjohnson/litestream + rclone/rclone
    → prometheus/prometheus + mikefarah/yq + PRQL/prql
    → FiloSottile/mkcert + openziti/zrok|antoniomika/sish
    → asciinema/asciinema + amir20/dozzle + jesseduffield/lazygit
    → ast-grep/ast-grep + zizmorcore/zizmor (when experiments touch CI)
```

**Missing glue:** `labctl` + run identity schema + pinned proceed profiles + deny-list of atlas hard leaves + notebook UX.

**Threat / policy notes:**
- Do not embed `sqlite` upstream patches; use libsql.
- Prefer disclosure-compliant wrappers around disclosure-policy tools.
- Sandbox defaults: no host docker socket to untrusted experiment code; gVisor/WASM preferred over privileged DinD.
- Optional Attempt-6 module: AgentFence-like apply gate when lab drives contrib.

**MVP architecture:**

```
┌─────────────┐   ┌──────────────────┐   ┌────────────────────┐
│ experiment  │──▶│ runner           │──▶│ artifact store     │
│ YAML/PRQL   │   │ task/dagger      │   │ libsql+litestream  │
└─────────────┘   │ + gvisor|kind|   │   │ + rclone mirror    │
                  │   wasmtime       │   └─────────┬──────────┘
                  └────────┬─────────┘             │
                           ▼                       ▼
                  ┌──────────────────┐   ┌────────────────────┐
                  │ evidence         │   │ verify/query       │
                  │ asciinema/logs/  │   │ prometheus/yq/prql │
                  │ dive reports     │   └────────────────────┘
                  └────────┬─────────┘
                           ▼
                  ┌──────────────────┐
                  │ optional share   │
                  │ zrok/sish+mkcert │
                  └──────────────────┘
```

### 4.2 TOP 2 — Supply-chain verify loop (abandon as greenfield)

**Why it ranked #2 on parts:** atlas security+devops proceed density is excellent (clair, kyverno, zizmor, goreleaser, ko, flux, dive, dockle, oras, immudb…).

**Why not pursue:** external scan shows the **assembly product already exists**:
- Chainloop (evidence store + contracts + Sigstore) → Dependency-Track / GUAC fan-out  
- GUAC product site positions exactly as “tools stop at SBOM; we graph them”  
- ReARM/Sbomify commercial layers; lab-in-a-box already demos local signing+SBOM  

**Missing glue for a newbie product = already Chainloop’s job.** Small-team differentiation vs OpenSSF stack is weak.

---

## 5. Recommendation — ONE scaffold

### Pursue: **Local-first systems engineering lab** (Attempt 1, narrowed)

**Why this over supply-chain verify and zero-trust personal edge (user’s preferred shortlist):**

| Preferred theme | Loop stands? | Prior-art gap? | Call |
|---|---|---|---|
| Local-first repro research/engineering lab | **Yes** if scoped as **systems lab OS**, not LLM scientist | **Yes** — Dagger/OpenResearch/lab-in-a-box leave composition+ledger gap | **pursue** |
| Supply-chain verify loop | Yes | **No** — Chainloop+GUAC+DT | abandon |
| Zero-trust personal edge | Yes | **No** — Octelium/Pangolin/Wiredoor/OpenZiti | abandon |

**Why not AutoGPT/OpenHands competitors:** those optimize *agent behavior* (code edits, tool use). This optimizes *experiment physics* (sandbox profile, hashes, archive, replay). An OpenHands session can be a *client* of the lab; it is not a substitute.

**Scaffold first slice (suggested, not implemented here):**
1. `labctl init|run|replay|export` over Task+Dagger.
2. Default runtimes: kind + wasmtime; optional gVisor.
3. Ledger in libsql; litestream to local disk; rclone optional.
4. Ship atlas `proceed` pin file + `leave` deny list as data.

**Do not scaffold** ZT edge or supply-chain control plane as greenfield — join/extend occupied products if needed later.

---

## 6. Competitor scan — autonomous research agents vs systems-stack assembly

| Product | Sources | Misses vs systems-stack assembly |
|---|---|---|
| GPT Researcher | GitHub + gptr.dev | Web/local report agent; no gVisor/kind/litestream/rclone lab spine |
| OpenResearch | openresearch.sh + GitHub | Strong local science workspace; not atlas systems parts composition |
| OmniScientist-V2 | GitHub + arXiv lineage | Literature/ROM/`verify`; not tunnel/PKI/edge/devops assembly |
| OpenHands | openhands.dev blog + GitHub | Coding-agent control plane; sandbox for *agents*, not experiment lab OS |
| Aider / Cline | 2026 comparison articles | Pair-programming loops; no multi-capability atlas assembly |
| XScientist / AutoScientists | arXiv 2607.12301 / 2605.28655 | Autonomous science papers; claim space ≠ systems CLI lab |
| Dagger | docs.dagger.io | Excellent engine **part**; not notebook+archive+share product |
| Chainloop / GUAC | docs.chainloop.dev ; guac.sh | Occupy supply-chain assembly — reason Attempt 2 dies |
| Octelium / Pangolin / Wiredoor | octelium.com ; wiredoor.net ; HN | Occupy ZT personal edge — reason Attempt 3 dies |

**Conclusion:** “Autonomous research agent” OSS is crowded on the **LLM science/coding** axis. The open composition gap that still **stands as a production loop** is a **systems engineering lab OS** that total-assembles atlas parts without pretending to be AutoGPT.

---

## Success checklist

- [x] `REPORT.md` — method, graph, ranked scenarios, deep dives, one recommendation  
- [x] `PARTS.json` — capability→repos with atlas names/stars/policies  
- [x] `ATTEMPTS.md` — 8 attempts, external prior art, pursue/park/abandon  
- [x] No PRs/forks; no fabricated stars  
