# Priority ranking — pursue survivors

**Date:** 2026-09-09 (Asia/Shanghai)  
**Input:** attempts with `decision=pursue-candidate` **or** (loop stands AND verdict open/thin-overlap).  
**Axes (1–5):** standability · gap clarity · part readiness · fill-soon risk⁻¹ (higher = safer) · buildability.  
**Score** = sum (max 25). Do **not** collapse to a single pursue unless only one survives.

Parked modules (#6, #25, #28, #30) are noted as attachable, not ranked as P0 products.

---

## Ranked survivors

| Pri | id | name | stand | gap | parts | fill⁻¹ | build | **Σ** | Notes |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| **P0** | 1 | Local-first systems engineering lab | 5 | 4 | 5 | 3 | 5 | **22** | Core spine; labctl already stubbed; shared ledger for siblings |
| **P0** | 26 | Atlas AI disclosure+release gate | 5 | 4 | 4 | 3 | 5 | **21** | Atlas dataset is unique moat; ships as `atlasgate` without full lab OS |
| **P1** | 23 | Multi-protocol API contract harness | 4 | 4 | 4 | 3 | 4 | **19** | Reuses Attempt-1 ledger; Hurl-first wedge |
| **P1** | 20 | Immutable ops evidence ledger | 5 | 3 | 4 | 3 | 4 | **19** | Natural evidence backend for #1/#23/#26 |
| **P1** | 9 | Data/ML-ops-lite dataset ledger | 4 | 3 | 4 | 2 | 4 | **17** | Scope away from DuckLake; sibling of #1 |
| **P2** | 13 | Media/docs vault (non-LLM) | 3 | 3 | 4 | 3 | 3 | **16** | Share vault schema with #1; avoid ArchiveBox/LLM claims |
| **P2** | 29 | Multi-ecosystem airgap package mirror | 3 | 4 | 4 | 3 | 2 | **16** | Harder glue (polyglot); clear gap vs uv-pack-only |
| **P2** | 19 | Self-hosted edge workers platform | 3 | 3 | 4 | 2 | 2 | **14** | Higher sandbox/ops burden; start after P0/P1 |

---

## Scoring rationale (brief)

### P0
1. **#1 Systems lab** — Highest part readiness; concrete E2E already documented; differentiates from Dagger (engine) and OpenResearch (LLM science). Fill risk medium (Dagger Cloud / lab-in-a-box sideways).
2. **#26 Atlasgate** — Can ship independently of full lab OS; moat is atlas proceed/leave + disclosure policy composition. Adjacent tools (Commit Check, assisted-by, chaoss/disclosure) do **not** consume the atlas scored set.

### P1
3. **#23 API contract harness** — Clear open gap between Hurl/grpcurl parts and Speedscale; ledger shared with #1.
4. **#20 Ops evidence notary** — immudb is ready; productize schema+verify CLI for lab/ops events (not SSCS Chainloop clone).
5. **#9 Dataset ledger** — Thin vs DuckLake; pursue only as personal dataset+job ledger tied to #1 run identity.

### P2
6. **#13 Non-LLM docs vault** — Valid gap if strictly non-LLM + content-addressed; easy to accidentally rebuild ArchiveBox/DEEP.
7. **#29 Airgap mirror** — Open polyglot gap; buildability lower (matrix hell); valuable later for offline lab profiles.
8. **#19 Edge workers OS** — Real gap around workerd assembly; safety (gVisor) and control-plane glue are heavier.

---

## Explicit non-goals (this cycle)

- Do **not** greenfield: #2 supply-chain, #3/#27 ZTNA, #4 Coder, #10 DNS, #11 Kymaros-space, #12 XTP, #14 Kubescape, #15 IdP, #16 ArchiveBox, #17/#21 toolchain managers, #18 Speedscale-space, #24 RAG.
- Parked attachables: #6 contrib sandbox → module under #26/#1; #28 CLI notebook → #1 UX; #30 research harness → #1 API; #25 image diet → ignore unless requested.

---

## Suggested pursuit order (execution)

**One implementation focus at a time** (research hub stays in systems-lab; each graduate gets a sibling repo — see [ORG.md](ORG.md)).

1. Harden **#1 labctl** ledger + proceed pins (done in this hub).
2. Ship **#26 atlasgate** MVP (trailer + zizmor + leave deny) — in-tree for now; may split later.
3. **#23** → sibling repo [`vulragrag-star/contract-harness`](https://github.com/vulragrag-star/contract-harness) (creating now; Hurl + grpcurl + content-addressed run ledger).
4. **#20** → planned sibling `vulragrag-star/ops-evidence` (immudb evidence writer).
5. **#9** → planned sibling `vulragrag-star/dataset-ledger` (dataset identity on shared ledger ideas).
6. Queue **#13 / #29 / #19** after P0/P1 prove composition UX (repos TBD later).

Multiple survivors may be pursued **in this priority order**; do not pretend only one idea remains — but do not rush parallel greenfield repos.
