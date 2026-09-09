# Organization — research hub vs implementation repos

**Date:** 2026-09-09 (Asia/Shanghai)  
**Owner:** Jason Wang \<vulragrag@gmail.com\> / GitHub `vulragrag-star`

## Architecture

**systems-lab** is the **survey / research hub**. It holds the composition-gap trail:

| Doc | Role |
|---|---|
| [ATTEMPTS.md](ATTEMPTS.md) | Every candidate (1–30): loop, prior art, verdict, pursue/park/abandon |
| [CANDIDATE_BACKLOG.md](CANDIDATE_BACKLOG.md) | Full catalog table |
| [PRIORITY.md](PRIORITY.md) | Ranked survivors (P0/P1/P2) and suggested pursuit order |
| [STATUS.md](STATUS.md) | Implementation progress notes for in-hub work |
| [REPORT.md](REPORT.md) | Method and recommendation |

Implementation **subprojects** are **separate GitHub repositories** under the `vulragrag-star` org/user. Each pursue-candidate that graduates from research gets its own sibling repo.

This repo may still host early glue for P0 (`labctl`, `atlasgate`) until those are split out; newer pursue-candidates land in their own repos from day one.

## Mapping: Attempt → implementation repo

| Attempt | Name | Repo | Status |
|---:|---|---|---|
| **#1** | Local-first systems engineering lab (`labctl`) | [vulragrag-star/systems-lab](https://github.com/vulragrag-star/systems-lab) | **Live here** (research hub + labctl) |
| **#26** | Atlas AI disclosure+release gate (`atlasgate`) | [vulragrag-star/systems-lab](https://github.com/vulragrag-star/systems-lab) | **Live here** for now (sibling package in-tree) |
| **#23** | Multi-protocol API contract harness | [vulragrag-star/contract-harness](https://github.com/vulragrag-star/contract-harness) | **Scaffold live** |
| **#20** | Immutable ops evidence ledger | [vulragrag-star/ops-evidence](https://github.com/vulragrag-star/ops-evidence) | **Scaffold live** |
| **#9** | Data/ML-ops-lite dataset ledger | [vulragrag-star/dataset-ledger](https://github.com/vulragrag-star/dataset-ledger) | **Scaffold live** |
| **#13** | Media/docs vault (non-LLM) | [vulragrag-star/docs-vault](https://github.com/vulragrag-star/docs-vault) | **Scaffold live** |
| **#29** | Multi-ecosystem airgap package mirror | [vulragrag-star/airgap-mirror](https://github.com/vulragrag-star/airgap-mirror) | **Scaffold live** |
| **#19** | Self-hosted edge workers platform | [vulragrag-star/edge-workers-lab](https://github.com/vulragrag-star/edge-workers-lab) | **Scaffold live** |

Parked / abandoned attempts do not get implementation repos unless ATTEMPTS.md is updated with a new prior-art scan and a pursue decision.

## How to work

1. Read ATTEMPTS → PRIORITY → STATUS (and this ORG map) before coding.
2. Prefer composing upstream CLIs over forking or reimplementing occupied products.
3. Link each sibling repo back to its Attempt section in systems-lab.
4. One deepen focus at a time after scaffolds; queue the rest.

Identity for commits: Jason Wang \<vulragrag@gmail.com\> with `Signed-off-by`.
