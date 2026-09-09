# ATTEMPTS — composition-gap lab notebook

Living trail of closed-loop candidates mined from the vulragrag-star OSS atlas (`SYNTHESIS.md`, `SHORTLIST.md`, `data/scored.jsonl` proceed=true, sector surveys).  
Priority: (1) can the loop stand in production, (2) external prior art beyond GitHub, (3) document every attempt.

**Methodology note (2026-09-09):** expanded from 8 → 30 attempts across research/agents, supply chain, edge/ZT, DevEx, data/ML-ops-lite, networking/DNS, security ops, backup/DR, package ecosystems, WASM, contrib governance, media/docs, homelab, observability, identity. Enumerate-all → filter → prioritize (see `CANDIDATE_BACKLOG.md`, `PRIORITY.md`). Multiple `pursue-candidate` survivors allowed.

Star counts and policies below are from `scored.jsonl` only (no invented stars).

---

## Attempt 1 — Local-first systems engineering lab (repro capsule)

### Idea / closed-loop claim
Assemble mature atlas parts into a **local-first lab OS** for systems/CLI/engineering experiments:  
`experiment.yaml` → hermetic sandbox → workflow runner → artifact+provenance store → query/verify → optional private share — with a run ledger a peer can replay. **Not** an LLM paper-writer; not a coding agent.

### Can the loop stand?
**Yes (narrowed).** Runnable E2E path exists today as glue:
1. Define experiment (Taskfile / Dagger module).
2. Execute in `kind` cluster and/or `gvisor`/`wasmtime` sandbox.
3. Capture outputs to `libsql` + `litestream` + optional `rclone` offsite.
4. Record metrics in `prometheus`; inspect with `yq`/`prql`/`fselect`.
5. Optional expose of a read-only dashboard via `zrok`/`sish` + `mkcert`.

Production-viable for a personal/small-team lab; not a multi-tenant SaaS without more work.

### Parts from atlas (concrete repos)
| Bucket | Repos (stars / policy from scored.jsonl) |
|---|---|
| sandbox | `google/gvisor` 19245 silent; `bytecodealliance/wasmtime` 18607 disclosure; `kubernetes-sigs/kind` 15478 silent; `dagger/dagger` 16230 silent; `jetify-com/devbox` 12342 silent; `youki-dev/youki` 7593 silent; `testcontainers/testcontainers-go` 4971 silent |
| workflow | `go-task/task` 16110 disclosure; `dagger/dagger` 16230 silent; `earthly/earthly` 12045 silent; `argoproj/argo-workflows` 16959 disclosure; `woodpecker-ci/woodpecker` 7831 silent |
| storage | `tursodatabase/libsql` 17208 silent; `benbjohnson/litestream` 14358 disclosure; `rclone/rclone` 59639 disclosure; `dgraph-io/badger` 15758 silent; `prometheus/prometheus` 66005 silent |
| harvest_fetch | `Orange-OpenSource/hurl` 19190 disclosure; `Y2Z/monolith` 15466 silent; `scrapy/scrapy` 64240 silent; `mr-karan/doggo` 4467 silent |
| query_analytics | `mikefarah/yq` 15934 disclosure; `PRQL/prql` 10910 silent; `jhspetersson/fselect` 4458 silent; `duckdb/duckdb-wasm` 2118 silent |
| identity_tls | `FiloSottile/mkcert` 59563 silent; `smallstep/certificates` 8843 silent |
| tunnel_edge | `openziti/zrok` 4668 silent; `antoniomika/sish` 4712 silent; `cloudflare/cloudflared` 15543 silent |
| editor_agent_ux | `neovim/neovim` 102213 disclosure; `jesseduffield/lazygit` 82122 disclosure; `amir20/dozzle` 14300 silent; `asciinema/asciinema` 17780 disclosure |
| policy_scan | `ast-grep/ast-grep` 15797 silent; `wagoodman/dive` 54538 silent; `zizmorcore/zizmor` 6458 disclosure |
| package_release | `astral-sh/uv` 89622 disclosure; `goreleaser/goreleaser` 16023 disclosure; `NixOS/nix` 17655 disclosure |

### Missing glue
- Single `labctl` that owns experiment identity, content-addressed run dirs, and policy profiles.
- Provenance schema (inputs hash → sandbox profile → outputs → promote/reject).
- Opinionated defaults that pin atlas-proceed versions; AgentScan/hard_ban deny-lists for outbound contrib.
- UX that is a lab notebook, not “another CI YAML”.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality assessment |
|---|---|---|---|
| Dagger | https://docs.dagger.io/ | Programmable local-first container pipelines | **Strong part**, not full lab OS (no experiment ledger + archive + share product) |
| OpenResearch | https://github.com/alphaXiv/OpenResearch ; https://openresearch.sh/ | Local-first research agent workspace, SQLite, experiment trees | Occupies **LLM science** loop; not systems-stack assembly |
| OmniScientist-V2 | https://github.com/tsinghua-fib-lab/OmniScientist-V2 | Local CLI research agent, ROM, verify pass | Literature/hypothesis product; different buyer |
| GPT Researcher | https://github.com/assafelovic/gpt-researcher ; https://gptr.dev | Autonomous web/local research reports | Report agent, not systems lab |
| AgentLabX / Inflexa | GitHub repos (2026) | Agent research / bio analysis with provenance | Early; domain-specific |
| machinable | https://machinable.org/comparison.html | Content-addressed experiment identity vs Snakemake/DVC/W&B | Conceptual prior art for identity; thin adoption vs Dagger/Nix |
| lab-in-a-box | https://github.com/BubblyWolf/lab-in-a-box | Kind + Argo + Prom/Grafana + Kyverno teaching stack | Closest **k8s learning** assembly; not general systems experiment lab |
| Scale VP build-systems essay | https://www.scalevp.com/blog/the-rise-of-advanced-build-systems | Market map: Dagger, Earthly, Nix, EngFlow… | Confirms build engines are products; **lab notebook layer** still under-productized |
| XScientist / AutoScientists | arXiv:2607.12301, arXiv:2605.28655 | Autonomous science orchestration papers | Research agents / paper loops — different claim |

### Verdict
**thin-overlap → open gap (narrowed).** Build engines and LLM research agents are occupied; a **systems-experiment lab OS** that composes atlas sandbox/storage/tunnel/scan parts with a replayable ledger is not a widely adopted open product.

### If open: filled soon? moat? innovation?
- Risk of fill: Dagger Cloud / OpenResearch expanding sideways; lab-in-a-box clones.
- Moat: atlas-grounded proceed/leave policy pack + hermetic multi-runtime (gVisor+WASM+kind) defaults + offline-first archive story.
- Innovation: composition + provenance UX, not novel crypto/networking.

### Decision
**pursue-candidate** (narrowed claim only — see PRIORITY.md; one of several survivors).

---

## Attempt 2 — Supply-chain verify closed loop

### Idea / closed-loop claim
`source → build (ko/buildx/goreleaser) → SBOM/sign/scan (clair/dive/dockle/zizmor) → admit (kyverno) → deploy (flux) → evidence store` as one local-first product for maintainers.

### Can the loop stand?
**Yes.** Parts compose into a real path (CI recipes + admission). Atlas has build, scan, policy, workflow; signing/SBOM hubs (cosign/syft) are thinner in proceed set (`oras-project/oras` 2420 proceed; `aquasecurity/trivy-operator` 1935 proceed; `crev-dev/cargo-crev` 2332 proceed).

### Parts from atlas
`goreleaser/goreleaser`, `ko-build/ko`, `docker/buildx`, `podman-container-tools/buildah`, `oras-project/oras`, `quay/clair`, `wagoodman/dive`, `goodwithtech/dockle`, `zizmorcore/zizmor`, `kyverno/kyverno`, `kubescape/kubescape`, `aquasecurity/kube-bench`, `fluxcd/flux2`, `tektoncd/pipeline`, `cert-manager/cert-manager`, `bitnami/sealed-secrets`, `codenotary/immudb`, `google/gvisor`, `kubernetes-sigs/kind`, `guacsec/guac` (midband proceed in security survey).

### Missing glue
Opinionated single binary/UI; air-gap key management; maintainer-scale defaults (not enterprise control plane).

### Prior art found
| Name | URL | What they do | Quality |
|---|---|---|---|
| Chainloop | https://github.com/chainloop-dev/chainloop ; https://docs.chainloop.dev/ | OSS evidence store + contracts + Sigstore/in-toto; fans out to Dependency-Track/GUAC | **Occupies the product layer** |
| GUAC | https://guac.sh/guac/ ; https://docs.guac.sh/guac/ | OpenSSF graph over SBOMs/attestations/vulns | Mature aggregation layer |
| Dependency-Track | (OWASP; via Chainloop docs) | Continuous SBOM analysis | De-facto SCA platform |
| ReARM / Reliza | https://rearmhq.com/comparisons/ | Release governance on top of SBOM tools | Commercial/product positioning |
| Sbomify | https://sbomify.com/features/generate-collaborate-analyze/ | SBOM hub narrative | Product site prior art |
| lab-in-a-box | GitHub | Local kind stack with Trivy/cosign/SBOM in GHA | Teaching assembly already exists |
| Medium 2026 SSCS primer | kawaldeepsingh.medium.com (2026) | Industry roadmap SBOM/Sigstore/SLSA | Shows tooling maturity / crowded |

### Verdict
**occupied.**

### If open…
N/A — would be filled by Chainloop/GUAC ecosystem deepening, not a greenfield small-team wedge.

### Decision
**abandon** (contrib-into-existing only).

---

## Attempt 3 — Zero-trust personal edge

### Idea / closed-loop claim
One product: identity + TLS + tunnel + DNS edge + optional remote DevEx for a personal/homelab edge without inbound ports.

### Can the loop stand?
**Yes.** `openziti/ziti`+`zrok` or `frp`/`sish`/`cloudflared` + `mkcert`/`pomerium`/`dex`/`zitadel` + `pi-hole`/`unbound` is a known working architecture.

### Parts from atlas
`openziti/ziti` 4381; `openziti/zrok` 4668; `fatedier/frp` 109273; `antoniomika/sish` 4712; `cloudflare/cloudflared` 15543; `ginuerzh/gost` 18214; `rathole-org/rathole` 14123; `pi-hole/pi-hole` 60796; `NLnetLabs/unbound` 4859; `coredns/coredns` 14299; `pomerium/pomerium` 4997 disclosure; `FiloSottile/mkcert` 59563; `dexidp/dex` 11083; `zitadel/zitadel` 14959 disclosure; `oauth2-proxy/oauth2-proxy` 14929 disclosure; `octelium/octelium` 4039 (networking midband proceed); `DefGuard/defguard` 2821; `coder/code-server` 79236; `coder/coder` 14399.

### Missing glue
Installer UX, opinionated homelab profiles — but vendors already ship this.

### Prior art found
| Name | URL | What they do | Quality |
|---|---|---|---|
| OpenZiti / NetFoundry | https://github.com/openziti/ziti/ ; https://netfoundry.io/ ; HN threads id=43278032, 43281146 | Full ZT overlay + commercial productization | **Platform occupied** |
| zrok | https://zrok.io/ ; HN id=41252922, 34709487 | Sharing on OpenZiti | Product exists |
| Octelium | https://octelium.com/solutions/ngrok-open-source-self-hosted-alternative ; HN Show id=44412207 | Unified FOSS ZTNA/ngrok/Teleport/Tailscale alternative on k8s | **Strong occupation** of “assembled personal/edge ZT” |
| Pangolin | https://github.com/fosrl/Pangolin | Identity-aware WG reverse proxy | Active assembled product |
| Wiredoor | https://www.wiredoor.net/ | Self-hosted ingress+WG+OAuth2-proxy | Assembled product |
| Homelab blogs | budgethomelab.com Authelia+Tailscale guide | Recipe culture fills DIY gap | Recipes ≠ product, but demand met |
| unsubbed.co Wiredoor writeup | https://unsubbed.co/tools/wiredoor/ | Competitive landscape CF Tunnel/Pangolin/ngrok | Confirms crowded |

### Verdict
**occupied.**

### Decision
**abandon.**

---

## Attempt 4 — Secure remote DevEx workstation

### Idea / closed-loop claim
Browser/SSH remote IDE + sandbox + identity-aware ingress as one OSS product.

### Can the loop stand?
**Yes** — but the loop is already a product (`coder/coder`).

### Parts from atlas
`coder/coder`, `coder/code-server`, `Eugeny/tabby`, `google/gvisor`, `kubernetes-sigs/kind`, `pomerium/pomerium`, `FiloSottile/mkcert`, `oauth2-proxy/oauth2-proxy`.

### Missing glue
Little — Coder already wires WireGuard tunnel, templates, auth.

### Prior art found
| Name | URL | Assessment |
|---|---|---|
| Coder | https://coder.com/ ; https://github.com/coder/coder | Self-hosted CDE + agents — **occupied** |
| code-server comparison | https://selfhosting.sh/compare/coder-vs-code-server/ | Clear product split |
| Baytech Coder analysis 2025 | baytechconsulting.com blog | Market positioning vs Codespaces/Gitpod |
| Teleport (adjacent) | product category PAM/SSH | Access plane, not full CDE |

### Verdict
**occupied.**

### Decision
**abandon.**

---

## Attempt 5 — Homelab observability + backup closed loop

### Idea / closed-loop claim
Prometheus/logs + encrypted offsite backup + restore verification as one OSS product.

### Can the loop stand?
**Yes** via compose.

### Parts from atlas
`prometheus/prometheus`, `amir20/dozzle`, `rclone/rclone`, `benbjohnson/litestream`, `velero-io/velero`, exporters in storage midband.

### Missing glue
Grafana/Loki not all in proceed shortlist; restore-verify UX.

### Prior art found
| Name | URL | Assessment |
|---|---|---|
| nXsi Homelab Monitoring Stack | https://www.nxsi.io/products/homelab-monitoring-stack | Packaged compose product |
| nXsi Homelab Backup Stack | https://www.nxsi.io/products/homelab-backup-stack | Restic+restore verification product |
| DIY templates | https://github.com/juliusjoska/docker-homelab-templates ; DEV.to guides | Commodity recipes |
| Medium/homelab blogs | secnate.medium.com etc. | Saturated DIY content |

### Verdict
**occupied** (commodity + paid compose packs).

### Decision
**abandon.**

---

## Attempt 6 — Agent-safe OSS contribution sandbox (atlas-policy aware)

### Idea / closed-loop claim
Closed loop for agent-assisted contrib: load atlas proceed/leave → sandbox edit → policy/scan (`zizmor`, `ast-grep`) → disclosure trailer → human apply. Respect AgentScan/hard_ban.

### Can the loop stand?
**Partial → yes for personal use.** Runtime sandbox + diff gate works; “production” multi-user SaaS does not without trust work.

### Parts from atlas
`google/gvisor`, `canonical/lxd`, `kubernetes-sigs/kind`, `zizmorcore/zizmor`, `ast-grep/ast-grep`, `jesseduffield/lazygit`, `go-task/task`, `Orange-OpenSource/hurl`, plus atlas leave signals (sqlite/kanidm/openbao/agentscan orgs from SYNTHESIS).

### Missing glue
Atlas policy pack as first-class input; per-repo CONTRIBUTING adapters; non-bypassable apply gate.

### Prior art found
| Name | URL | Assessment |
|---|---|---|
| AgentFence | https://github.com/balyakin/agentfence | Shadow workspace + scanners + apply gate — **direct overlap** |
| Agent Sandbox | https://github.com/AgentOpsSec/agent-sandbox | Temp workspace + diff apply |
| Agent-Gate | https://github.com/sjh9714/Agent-Gate | Checkout-free PR policy gate |
| Open Agent Security | https://github.com/mateaix/openagentsecurity | Diff risk evidence gates |
| Mike McQuaid sandvault setup | https://mikemcquaid.com/sandboxed-agent-worktrees-my-coding-and-ai-setup-in-2026/ | Practitioner blog; Homebrew AI PR barriers |
| OpenHands / Aider / Cline | openhands.dev ; comparisons 2026 | Coding agents, not atlas leave/proceed governance |

### Verdict
**thin-overlap.** Emerging tool cluster already shipping sandbox+gate; atlas-specific policy pack is a feature, not a moat-sized product.

### Decision
**park** (possible module inside Attempt 1, not standalone #1).

---

## Attempt 7 — Offline WASM / hermetic toolchain capsule

### Idea / closed-loop claim
Pin WASM+linker+JS/Python toolchains into a reproducible offline build capsule product.

### Can the loop stand?
**Partial.** `wasmtime`+`tinygo`+`bun`+`mold`+`goreleaser` run; product boundary unclear vs Nix/Dagger.

### Parts from atlas
`bytecodealliance/wasmtime`, `tinygo-org/tinygo`, `oven-sh/bun`, `rui314/mold`, `wasm-bindgen/wasm-bindgen`, `NixOS/nix`, `goreleaser/goreleaser`, `youki-dev/youki`.

### Prior art found
Dagger, Earthly, Nix + Determinate Systems, Obelisk.build (hermetic fabric), ScaleVP build-systems market map — **occupied by build systems**.

### Verdict
**occupied.**

### Decision
**abandon.**

---

## Attempt 8 — Personal GitOps platform-in-a-box

### Idea / closed-loop claim
One-command local production-like platform: kind + Flux/Argo + Kyverno + observability + sealed secrets.

### Can the loop stand?
**Yes.**

### Parts from atlas
`kubernetes-sigs/kind`, `fluxcd/flux2`, `argoproj/argo-workflows`, `kyverno/kyverno`, `bitnami/sealed-secrets`, `prometheus/prometheus`, `amir20/dozzle`, `GoogleContainerTools/skaffold`.

### Prior art found
lab-in-a-box (Kind+Argo+Prom+Kyverno+Trivy/cosign) — **already the assembly**; plus official kind/Flux tutorials.

### Verdict
**occupied.**

### Decision
**abandon.**

---

## Attempt 9 — Local-first data / ML-ops-lite dataset ledger

### Idea / closed-loop claim
Personal/small-team dataset → transform → feature snapshot → train/eval stub → metrics archive without Kubeflow: content-addressed datasets, embedded SQL catalog, SQL transforms, metrics archive.

### Can the loop stand?
**Yes (narrow).** E2E: rclone/opendal land Parquet/CSV → libsql (+ optional duckdb-wasm/datafusion) catalog+transform → task/dagger job → prometheus + litestream → query with prql/yq.

### Parts from atlas
`tursodatabase/libsql`, `benbjohnson/litestream`, `rclone/rclone`, `apache/opendal`, `apache/datafusion`, `duckdb/duckdb-wasm`, `asg017/sqlite-vec`, `go-task/task`, `dagger/dagger`, `prometheus/prometheus`, `PRQL/prql`, `mikefarah/yq`, `astral-sh/uv`, `replicate/cog`.

### Missing glue
Dataset identity schema; feature-snapshot promotion UX; non-DuckLake opinionated defaults; training adapters without claiming full MLOps.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| DuckLake | https://ducklake.select/ ; https://github.com/duckdb/ducklake | SQL catalog + Parquet lakehouse (v1.0 Apr 2026) | Strong occupation of lakehouse format |
| DuckDB MLOps essay | https://medium.com/@Modexa/duckdb-for-mlops-faster-data-prep-without-the-drama-940dcdbad86f | DuckDB as feature staging | Pattern, not product |
| libSQL DuckLake PoC | https://github.com/duckdb/ducklake/issues/1066 | Turso/libsql catalog backend proposal | Confirms libsql adjacency |
| Cog | https://github.com/replicate/cog | Model packaging | Part, not dataset ledger |

### Verdict
**thin-overlap.** Lakehouse format occupied by DuckLake; a personal dataset ledger + atlas sandbox job runner (systems-flavored) is thinner.

### If open/thin: fill-soon / moat / innovation
- Fill-soon: DuckLake + Turso catalog; MotherDuck-class UX.
- Moat: atlas proceed pins + multi-runtime job profiles from Attempt 1.
- Innovation: composition of catalog+job+archive, not new query engine.

### Decision
**pursue-candidate** (scoped as dataset/experiment ledger sibling to Attempt 1, not another DuckLake).

---
## Attempt 10 — Personal DNS privacy & policy control plane

### Idea / closed-loop claim
One product: adblock + recursive privacy resolver + encrypted upstream + local authority + metrics.

### Can the loop stand?
**Yes.** pi-hole/coredns + unbound + dnscrypt-proxy + smartdns + Prometheus is a known architecture.

### Parts from atlas
`pi-hole/pi-hole`, `coredns/coredns`, `NLnetLabs/unbound`, `DNSCrypt/dnscrypt-proxy`, `pymumu/smartdns`, `kubernetes-sigs/external-dns`, `prometheus/prometheus`, `miekg/dns`.

### Missing glue
Installer UX — vendors already ship it.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| AdGuard Home | https://github.com/AdguardTeam/AdGuardHome | Built-in DoH/DoT/DNSCrypt, DHCP, per-client | Occupies all-in-one |
| Pi-hole + Unbound guides | https://selfhosting.sh/foundations/network-wide-ad-blocking/ | Recipe culture | Commodity |
| SmartDNS | https://github.com/pymumu/smartdns | Fast multi-upstream resolver | Part |
| CoreDNS-at-home | https://sarah-robin.com/blog/coredns-at-home | Declarative CoreDNS control plane | Recipe |

### Verdict
**occupied.**

### If open/thin: fill-soon / moat / innovation
N/A

### Decision
**abandon.**

---
## Attempt 11 — Continuous backup → restore-verify DR loop

### Idea / closed-loop claim
Backup is not done until scheduled restore into sandbox passes health checks and records RTO evidence.

### Can the loop stand?
**Yes.** Velero/restic → kind/throwaway NS → checks → Prometheus; litestream+rclone for SQLite path.

### Parts from atlas
`velero-io/velero`, `rclone/rclone`, `benbjohnson/litestream`, `kubernetes-sigs/kind`, `prometheus/prometheus`, `amir20/dozzle`, `codenotary/immudb`, `go-task/task`.

### Missing glue
Cross-tool adapter (k8s + SQLite + files) as one product.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| Kymaros | https://kymaros.io/ | Continuous Velero restore validation operator | Occupies k8s restore-verify |
| Homelab Velero series | https://serard.dev/content/blog/homelab-k8s/32-velero-for-backup.html | Dogfood CronJob recipes | Strong recipes |
| nXsi Homelab Backup | https://www.nxsi.io/products/homelab-backup-stack | Packaged restic+verify | Product pack |
| OneUptime Velero DR 2026 | https://oneuptime.com/blog/post/2026-01-27-velero-disaster-recovery/view | DR runbook maturity | Guide |

### Verdict
**occupied** (k8s) / commodity (homelab packs).

### If open/thin: fill-soon / moat / innovation
N/A — join Kymaros/nXsi rather than greenfield.

### Decision
**abandon.**

---
## Attempt 12 — Local WASM plugin host + registry loop

### Idea / closed-loop claim
Host apps load untrusted plugins via WASM with capability limits; build/push/test registry for plugins.

### Can the loop stand?
**Yes** via Extism+wasmtime; product layer already exists (XTP).

### Parts from atlas
`bytecodealliance/wasmtime`, `extism/extism`, `cloudflare/workerd`, `tinygo-org/tinygo`, `wasm-bindgen/wasm-bindgen`, `youki-dev/youki`, `wasm-micro-runtime/wasm-micro-runtime`.

### Missing glue
Little — XTP ships registry/CLI.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| Extism | https://extism.org/ | Universal Wasm plugin framework | Strong part |
| XTP (Dylibso) | https://xtp.dylibso.com/ | Managed marketplace/registry on Extism | Occupies product |
| Bytes.dev #343 | https://bytes.dev/archives/343 | Market narrative for Extism plugins | Commentary |

### Verdict
**occupied.**

### If open/thin: fill-soon / moat / innovation
N/A

### Decision
**abandon.**

---
## Attempt 13 — Systems media/docs ingest → durable vault (non-LLM)

### Idea / closed-loop claim
Fetch/crawl → normalize (images/PDF/HTML) → content-addressed vault → query — without claiming RAG/LLM product.

### Can the loop stand?
**Partial → yes for personal/research ops.** scrapy/hurl/monolith → ImageMagick/pdf.js → libsql+rclone vault → fselect/yq/prql.

### Parts from atlas
`scrapy/scrapy`, `Orange-OpenSource/hurl`, `Y2Z/monolith`, `ImageMagick/ImageMagick`, `mozilla/pdf.js`, `tursodatabase/libsql`, `rclone/rclone`, `jhspetersson/fselect`, `mikefarah/yq`, `go-task/task`.

### Missing glue
Format router + vault schema + dedupe; pandoc not in proceed set (acceptable external).

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| Firecrawl AnyDoc | https://www.firecrawl.dev/blog/anydoc-and-pdf-inspector | Fast local doc→MD parsers | Strong parts, not vault product |
| ArchiveBox | https://archivebox.io/ | Self-hosted web archive manager | Occupies web archive |
| DEEP / Zurvan | GitHub local-first AI doc engines | LLM knowledge engines | Occupy LLM axis |
| AnyDoc pipeline essay | https://medium.com/@info.booststash/i-spent-a-week-building-a-document-pipeline-around-firecrawls-anydoc-here-s-how-to-actually-use-it-e223e102f8ec | Routing pattern | Guide |

### Verdict
**thin-overlap.** ArchiveBox owns bookmarks/web; AnyDoc owns parsing; a systems vault (hash ledger + transform jobs + offline query, no LLM) is under-productized.

### If open/thin: fill-soon / moat / innovation
- Fill-soon: ArchiveBox expanding transforms; Firecrawl Parse SaaS.
- Moat: atlas job runner + content-addressed ledger shared with Attempt 1.
- Innovation: non-LLM provenance vault UX.

### Decision
**pursue-candidate.**

---
## Attempt 14 — Continuous security posture ops loop

### Idea / closed-loop claim
Cluster/CI continuous scan → triage → admit/deny → evidence store as one product.

### Can the loop stand?
**Yes** — Kubescape already is that product for k8s.

### Parts from atlas
`kubescape/kubescape`, `quay/clair`, `wagoodman/dive`, `zizmorcore/zizmor`, `aquasecurity/kube-bench`, `kyverno/kyverno`, `aquasecurity/tracee`, `greenbone/openvas-scanner`.

### Missing glue
Little for k8s — Kubescape operator covers continuous scan.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| Kubescape | https://kubescape.io/ | CNCF continuous scan/runtime platform | Occupied |
| Chainloop/GUAC | https://docs.chainloop.dev/ ; https://guac.sh/ | Supply-chain evidence | Occupied (Attempt 2) |

### Verdict
**occupied.**

### If open/thin: fill-soon / moat / innovation
N/A

### Decision
**abandon.**

---
## Attempt 15 — Small-team identity + secrets spine

### Idea / closed-loop claim
OIDC IdP + local PKI + sealed secrets + password store as one installer for 5–50 people (avoid hard_ban openbao/kanidm).

### Can the loop stand?
**Yes.** Zitadel/Dex + step-ca/mkcert + sealed-secrets + gopass.

### Parts from atlas
`zitadel/zitadel`, `dexidp/dex`, `oauth2-proxy/oauth2-proxy`, `smallstep/certificates`, `FiloSottile/mkcert`, `bitnami/sealed-secrets`, `gopasspw/gopass`, `cert-manager/cert-manager`.

### Missing glue
Installer UX — vendors and Helm recipes already ship it.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| ZITADEL self-hosted | https://zitadel.com/self-hosted | Full CIAM product | Occupied |
| Zitadel Helm+secrets guides | https://citizix.com/how-to-deploy-zitadel-on-kubernetes-with-helm-and-traefik/ | IdP+secrets assembly | Recipe |

### Verdict
**occupied.**

### If open/thin: fill-soon / moat / innovation
N/A

### Decision
**abandon.**

---
## Attempt 16 — Personal web harvest → durable archive

### Idea / closed-loop claim
Crawl/bookmark ingest → multi-format archive → search/export.

### Can the loop stand?
**Yes** — ArchiveBox is the product; scrapy pipes in.

### Parts from atlas
`scrapy/scrapy`, `Y2Z/monolith`, `Orange-OpenSource/hurl`, `rclone/rclone`, `tursodatabase/libsql`.

### Missing glue
Little — ArchiveBox owns assembly.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| ArchiveBox | https://archivebox.io/ | Self-hosted web archiving | Occupied |
| ArchiveBox vs Wallabag | https://selfhosting.sh/compare/archivebox-vs-wallabag/ | Category split archive vs read-later | Comparison |

### Verdict
**occupied.**

### If open/thin: fill-soon / moat / innovation
N/A

### Decision
**abandon.**

---
## Attempt 17 — Python polyglot monorepo DevEx OS

### Idea / closed-loop claim
One product wrapping uv workspaces + ruff + pytest + hooks + release as Python Cargo.

### Can the loop stand?
**Partial.** Parts compose; product boundary is recipes + Astral tooling.

### Parts from atlas
`astral-sh/uv`, `astral-sh/ruff`, `pytest-dev/pytest`, `evilmartians/lefthook`, `typicode/husky`, `conventional-changelog/commitlint`, `go-task/task`, `goreleaser/goreleaser`, `Nuitka/Nuitka`, `PyO3/maturin`.

### Missing glue
Opinionated monorepo template — already blog-saturated.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| uv workspaces guides 2026 | https://www.danilchenko.dev/posts/uv-workspaces-monorepo/ | Recipe saturation | Guides |
| Botmonster uv+Ruff monorepo | https://botmonster.com/coding/python-monorepo-uv-workspaces-ruff/ | Production monorepo story | Guide |
| Pants + uv + Ruff | https://developersvoice.com/blog/python/modern-python-monorepo-uv-ruff-pants-guide/ | Scale monorepo stack | Guide |

### Verdict
**occupied** (tooling + blogware).

### If open/thin: fill-soon / moat / innovation
N/A

### Decision
**abandon.**

---
## Attempt 18 — Network traffic capture → replay → regress loop

### Idea / closed-loop claim
Capture prod-like traffic → replay against candidate → diff/regress → evidence.

### Can the loop stand?
**Yes** with GoReplay; commercial closes AI loop.

### Parts from atlas
`probelabs/goreplay`, `zeek/zeek`, `Orange-OpenSource/hurl`, `fullstorydev/grpcurl`, `esnet/iperf`, `prometheus/prometheus`, `kubernetes-sigs/kind`.

### Missing glue
AI triage/PR loop is Speedscale's job.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| GoReplay | https://goreplay.org/ | OSS+PRO traffic replay | Occupies capture/replay |
| Speedscale BYOC | https://speedscale.com/byoc/ | Closed loop capture→fix→PR | Occupies product |
| Zeek | https://zeek.org/ | Network monitor | Part |

### Verdict
**occupied.**

### If open/thin: fill-soon / moat / innovation
N/A

### Decision
**abandon.**

---
## Attempt 19 — Self-hosted edge workers platform (workerd + tunnel + PKI)

### Idea / closed-loop claim
Local/edge JS/Wasm workers runtime + TLS + private share tunnel as homelab/edge FaaS without Cloudflare control plane.

### Can the loop stand?
**Partial → yes for single-node.** workerd + caddy/mkcert + zrok/sish + optional wasmtime/extism; operator supplies orchestration.

### Parts from atlas
`cloudflare/workerd`, `bytecodealliance/wasmtime`, `extism/extism`, `caddyserver/caddy`, `FiloSottile/mkcert`, `openziti/zrok`, `antoniomika/sish`, `cloudflare/cloudflared`, `amir20/dozzle`, `prometheus/prometheus`, `google/gvisor`.

### Missing glue
Deploy/version control plane; multi-node scheduling; KV/R2 substitutes; sandboxing depth (gVisor/VM per CF guidance).

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| workerd | https://github.com/cloudflare/workerd ; https://blog.cloudflare.com/workerd-open-source-workers-runtime/ | Runtime part, not full platform | Strong part |
| Self-host workerd analysis | https://flaviocopes.com/workerd/ | Lists missing CF platform pieces | Analysis |
| Extism/XTP | https://extism.org/ | Plugin layer | Occupied adjacent (Attempt 12) |

### Verdict
**thin-overlap → open gap (narrow).** Runtime exists; opinionated single-node edge workers OS (pins + tunnel + PKI + logs) is under-productized vs recipes.

### If open/thin: fill-soon / moat / innovation
- Fill-soon: CF/miniflare ecosystem; Deno self-host.
- Moat: atlas sandbox defaults (gVisor around workerd) + private share defaults.
- Innovation: assembly + safety defaults, not new isolate engine.

### Decision
**pursue-candidate.**

---
## Attempt 20 — Immutable ops evidence / audit ledger

### Idea / closed-loop claim
Every lab run, deploy, restore-test, and scan writes tamper-evident evidence with client verification — personal/small-team ops notary.

### Can the loop stand?
**Yes.** immudb ingest from Task/CI + optional libsql index + litestream/rclone mirror + asciinema attachments.

### Parts from atlas
`codenotary/immudb`, `tursodatabase/libsql`, `benbjohnson/litestream`, `rclone/rclone`, `asciinema/asciinema`, `prometheus/prometheus`, `go-task/task`, `google/trillian`.

### Missing glue
Opinionated evidence schema for systems-lab events; verify CLI UX; retention policies.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| immudb | https://immudb.io/ ; BusinessWire 2026 1.11 audit logging | Immutable DB + audit feature | Strong database part |
| PGaudit+immudb | https://immudb.io/blog/pgaudit-and-immudb-the-dynamic-duo-for-tamper-proof-postgresql-audit-trails | PG trail pattern | Pattern |
| Chainloop | https://docs.chainloop.dev/ | SSCS evidence store | Occupies supply-chain, not general lab ops |

### Verdict
**thin-overlap.** immudb occupies storage; Chainloop occupies SSCS; a systems-lab evidence notary composing atlas runs is open-ish.

### If open/thin: fill-soon / moat / innovation
- Fill-soon: immudb examples; Chainloop broadening.
- Moat: schema tied to Attempt 1 run identity + atlas policy.
- Innovation: productized verify UX for lab/ops events.

### Decision
**pursue-candidate.**

---
## Attempt 21 — Polyglot toolchain capsule (devbox/nix/uv/bun)

### Idea / closed-loop claim
One product that pins polyglot toolchains reproducibly for any repo.

### Can the loop stand?
**Yes** — Devbox/Nix already are the product.

### Parts from atlas
`jetify-com/devbox`, `NixOS/nix`, `pkgxdev/pkgx`, `astral-sh/uv`, `oven-sh/bun`, `nvm-sh/nvm`, `volta-cli/volta`, `mamba-org/mamba`.

### Missing glue
Little.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| Devbox vs Nix 2026 | https://briandetering.net/2026/05/28/best-dev-environment-managers-2026/ | Devbox/Nix/mise crowned | Occupied |
| 1337skills env managers | https://1337skills.com/blog/2026-07-18-reproducible-dev-environments-2026-devbox-devenv-devpod/ | Market map | Occupied |

### Verdict
**occupied.**

### If open/thin: fill-soon / moat / innovation
N/A

### Decision
**abandon.**

---
## Attempt 22 — Homelab GitOps lite (revisit of Attempt 8)

### Idea / closed-loop claim
Minimal Flux+kind+secrets+logs without full platform-in-a-box teaching stack.

### Can the loop stand?
**Yes**, but lab-in-a-box and tutorials already cover it.

### Parts from atlas
`kubernetes-sigs/kind`, `fluxcd/flux2`, `bitnami/sealed-secrets`, `stakater/Reloader`, `amir20/dozzle`, `prometheus/prometheus`.

### Missing glue
Little.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| lab-in-a-box | https://github.com/BubblyWolf/lab-in-a-box | Kind+Argo+Prom+Kyverno assembly | Occupied |

### Verdict
**occupied.**

### If open/thin: fill-soon / moat / innovation
N/A

### Decision
**abandon.**

---
## Attempt 23 — Multi-protocol API contract harness (HTTP + gRPC + ledger)

### Idea / closed-loop claim
Local-first: Hurl scenarios + grpcurl probes + optional traffic snippets → hermetic run → diff ledger → promote/reject — without becoming Speedscale.

### Can the loop stand?
**Yes (narrow).** hurl for HTTP; grpcurl for gRPC smoke; task/dagger orchestrates; results in libsql+litestream; optional goreplay fixture import.

### Parts from atlas
`Orange-OpenSource/hurl`, `fullstorydev/grpcurl`, `go-task/task`, `dagger/dagger`, `tursodatabase/libsql`, `benbjohnson/litestream`, `probelabs/goreplay`, `mikefarah/yq`, `kubernetes-sigs/kind`.

### Missing glue
Unified scenario format bridging Hurl+gRPC; golden response store; breaking-change report UX (Buf external OK).

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| Hurl | https://hurl.dev/ ; GitHub issue #3411 | HTTP scenario part; gRPC still roadmap | Strong HTTP part |
| grpcurl | https://github.com/fullstorydev/grpcurl | gRPC curl part, not test harness | Part |
| QASkills gRPC 2026 | https://qaskills.sh/blog/grpc-api-testing-complete-guide-2026 | Recipe: grpcurl+ghz+buf | Guide |
| Speedscale / GoReplay | https://speedscale.com/ ; https://goreplay.org/ | Traffic replay occupied | Different claim |

### Verdict
**thin-overlap → open gap.** Parts exist; unified HTTP+gRPC contract harness with content-addressed run ledger is not a widely adopted OSS product.

### If open/thin: fill-soon / moat / innovation
- Fill-soon: Hurl gRPC support; Bruno/Postman; Buf Studio.
- Moat: shared ledger with Attempt 1; offline-first.
- Innovation: composition + ledger, not new protocol client.

### Decision
**pursue-candidate.**

---
## Attempt 24 — Local systems knowledge base (sqlite-vec vault)

### Idea / closed-loop claim
Ingest docs/code notes → hybrid FTS+vector → query for humans/agents.

### Can the loop stand?
**Yes**, but RAG products already flood this.

### Parts from atlas
`asg017/sqlite-vec`, `tursodatabase/libsql`, `manticoresoftware/manticoresearch`, `scrapy/scrapy`, `mozilla/pdf.js`.

### Missing glue
Embedding provider wiring — products already ship it.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| sqlite-vec | https://github.com/asg017/sqlite-vec | Vector extension part | Part |
| local-rag-mcp | https://github.com/Gilligan-Tech-Inc/local-rag-mcp | SQLite hybrid RAG MCP | Occupied |
| OpenClaw / DEEP / Zurvan | PingCAP blog ; GitHub | Local RAG/memory products | Occupied |

### Verdict
**occupied** (as product); keep as library dependency only.

### If open/thin: fill-soon / moat / innovation
N/A

### Decision
**abandon.**

---
## Attempt 25 — Container image diet / rebuild loop

### Idea / closed-loop claim
dive/dockle findings → automated rebuild with ko/buildx → re-scan → admit.

### Can the loop stand?
**Partial.** Tools compose in CI; little differentiation vs Trivy/Copacetic/Kubescape patching.

### Parts from atlas
`wagoodman/dive`, `goodwithtech/dockle`, `ko-build/ko`, `docker/buildx`, `podman-container-tools/buildah`, `goreleaser/goreleaser`, `quay/clair`.

### Missing glue
Opinionated rebuild policy engine.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| Kubescape + Copacetic | https://kubescape.io/ | Image vuln+patch platform | Crowded |
| Dive CLI culture | https://github.com/wagoodman/dive | Image exploration part | Part |

### Verdict
**thin-overlap** but weak wedge.

### If open/thin: fill-soon / moat / innovation
- Fill-soon: Kubescape patching deepening.
- Moat: weak standalone.
- Innovation: low.

### Decision
**park.**

---
## Attempt 26 — Atlas-aware disclosure + release governance gate

### Idea / closed-loop claim
Closed loop for assisted OSS contrib: trailer enforcement, CI workflow scan, release tooling, atlas proceed/leave policy check, human sign-off.

### Can the loop stand?
**Yes for maintainer tooling.** Hooks and CI gates work today; atlas policy pack is the differentiator.

### Parts from atlas
zizmorcore/zizmor, conventional-changelog/commitlint, evilmartians/lefthook, goreleaser/goreleaser, ast-grep/ast-grep, go-task/task, plus atlas proceed/leave data.

### Missing glue
Single atlasgate CLI; per-policy profiles; PR checklist adapters.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| Commit Check | commit-check.com blog 2026-07-06 | CI forbid/ignore tool signatures | Strong adjacent |
| assisted-by plugin | github.com/bcmyguest/assisted-by | Kernel trailer enforcement | Adjacent |
| rai-lint | DEV.to anchildress1 | RAI footer enforcement | Adjacent |
| chaoss/disclosure | github.com/chaoss/disclosure | Disclosure signal scanner | Adjacent |
| gestate | pypi.org/project/gestate | min-release-age across package managers | Adjacent |

### Verdict
**thin-overlap.** Attribution gates emerging; atlas proceed/leave plus disclosure plus zizmor plus release as one policy pack is not shipped as a product.

### If open/thin: fill-soon / moat / innovation
- Fill-soon: Commit Check require mode; kernel tooling spread.
- Moat: atlas scored dataset as policy input.
- Innovation: policy composition across contrib, CI, release.

### Decision
**pursue-candidate.**

---
## Attempt 27 — Lightweight personal overlay mesh (Nebula-centric)

### Idea / closed-loop claim
Nebula/frp + Caddy + mkcert as a poor-man Tailscale product.

### Can the loop stand?
**Yes**, but Octelium/Pangolin/Wiredoor/OpenZiti occupy assembled ZTNA (Attempt 3).

### Parts from atlas
`slackhq/nebula`, `fatedier/frp`, `rathole-org/rathole`, `caddyserver/caddy`, `FiloSottile/mkcert`.

### Missing glue
Installer — vendors occupy.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| Octelium / Pangolin / Wiredoor | octelium.com ; wiredoor.net | Assembled ZTNA products | Occupied (Attempt 3) |
| Nebula | github.com/slackhq/nebula | Overlay mesh part | Part |

### Verdict
**occupied.**

### If open/thin: fill-soon / moat / innovation
N/A

### Decision
**abandon.**

---
## Attempt 28 — CLI observability notebook (asciinema + metrics + tasks)

### Idea / closed-loop claim
Record CLI sessions + scrape metrics + attach to experiment runs as a notebook for systems work.

### Can the loop stand?
**Partial.** Naturally a module of Attempt 1, not a standalone product.

### Parts from atlas
`asciinema/asciinema`, `amir20/dozzle`, `wtfutil/wtf`, `prometheus/prometheus`, `go-task/task`, `jesseduffield/lazygit`.

### Missing glue
Attachment schema into lab ledger.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| Asciinema | asciinema.org | Session recorder part | Part |
| Dozzle | dozzle.dev | Log viewer part | Part |

### Verdict
**thin-overlap** as standalone; better as feature of Attempt 1.

### If open/thin: fill-soon / moat / innovation
- Fold into Attempt 1 UX.

### Decision
**park** (fold into Attempt 1).

---
## Attempt 29 — Multi-ecosystem airgap package mirror

### Idea / closed-loop claim
One operator tool: sync/pin/verify offline mirrors for uv + bun + Nix closures + OCI via oras/rclone.

### Can the loop stand?
**Partial → yes per ecosystem; polyglot unification is the gap.**

### Parts from atlas
astral-sh/uv, oven-sh/bun, NixOS/nix, rclone/rclone, oras-project/oras, Homebrew/brew, pkgxdev/pkgx, go-task/task, codenotary/immudb.

### Missing glue
Unified manifest; cross-ecosystem verify; platform matrix packing.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| uv-pack | github.com/davnn/uv-pack | Offline uv env pack | Python-only |
| zuv | github.com/HamzaYslmn/zuv | Single-file uv bundles | Python-only |
| Airgap uv guide | alephnull.sk blog | Manual recipe | Guide |
| Nix offline discourse | discourse.nixos.org | Closure copy recipes | No polyglot product |

### Verdict
**thin-overlap → open gap** for polyglot offline mirror; single-ecosystem tools exist; enterprise mirror appliances occupy commercial.

### If open/thin: fill-soon / moat / innovation
- Fill-soon: Astral offline features; corporate mirror appliances.
- Moat: OSS small-team polyglot + atlas pins.
- Innovation: unified sync/verify UX across ecosystems.

### Decision
**pursue-candidate.**

---
## Attempt 30 — Research harness over systems lab (non-LLM product claim)

### Idea / closed-loop claim
Scripts or agents drive Attempt-1 lab runs with harvest and verify — product remains the lab, not an AutoGPT competitor.

### Can the loop stand?
**Partial.** Useful architecture; product identity collapses into Attempt 1 + Attempt 6 module.

### Parts from atlas
Attempt 1 spine + scrapy/scrapy + Orange-OpenSource/hurl + ast-grep/ast-grep + sandbox parts.

### Missing glue
Stable lab API / MCP surface.

### Prior art found (external + GitHub)
| Name | URL | What they do | Quality |
|---|---|---|---|
| OpenHands / OpenResearch / GPT Researcher | openhands.dev ; openresearch.sh ; gptr.dev | Occupy agent claim space | Different buyer if claimed as agent product |

### Verdict
**thin-overlap** as naming; park as API surface of Attempt 1.

### If open/thin: fill-soon / moat / innovation
- Keep as API, not product name.

### Decision
**park.**

---

## Attempt scoreboard (full)

| # | Candidate | Loop stands? | Verdict | Decision |
|---|---|---|---|---|
| 1 | Local-first systems engineering lab | yes (narrow) | thin-overlap → open gap | **pursue-candidate** |
| 2 | Supply-chain verify loop | yes | occupied | abandon |
| 3 | Zero-trust personal edge | yes | occupied | abandon |
| 4 | Secure remote DevEx | yes | occupied | abandon |
| 5 | Observability+backup (compose pack) | yes | occupied | abandon |
| 6 | Agent-safe OSS contrib sandbox | partial/yes | thin-overlap | park |
| 7 | WASM hermetic capsule | partial | occupied | abandon |
| 8 | GitOps platform-in-a-box | yes | occupied | abandon |
| 9 | Data/ML-ops-lite dataset ledger | yes (narrow) | thin-overlap | **pursue-candidate** |
| 10 | Personal DNS privacy plane | yes | occupied | abandon |
| 11 | Continuous backup restore-verify | yes | occupied | abandon |
| 12 | WASM plugin host+registry | yes | occupied | abandon |
| 13 | Media/docs vault (non-LLM) | partial/yes | thin-overlap | **pursue-candidate** |
| 14 | Continuous security posture ops | yes | occupied | abandon |
| 15 | Identity+secrets spine | yes | occupied | abandon |
| 16 | Web harvest→archive | yes | occupied | abandon |
| 17 | Python monorepo DevEx OS | partial | occupied | abandon |
| 18 | Traffic capture→replay→regress | yes | occupied | abandon |
| 19 | Self-hosted edge workers platform | partial/yes | thin-overlap | **pursue-candidate** |
| 20 | Immutable ops evidence ledger | yes | thin-overlap | **pursue-candidate** |
| 21 | Polyglot toolchain capsule | yes | occupied | abandon |
| 22 | Homelab GitOps lite | yes | occupied | abandon |
| 23 | Multi-protocol API contract harness | yes (narrow) | thin-overlap → open | **pursue-candidate** |
| 24 | Local sqlite-vec knowledge base | yes | occupied | abandon |
| 25 | Container image diet/rebuild | partial | thin-overlap | park |
| 26 | Atlas AI disclosure+release gate | yes | thin-overlap | **pursue-candidate** |
| 27 | Lightweight Nebula mesh | yes | occupied | abandon |
| 28 | CLI observability notebook | partial | thin-overlap | park |
| 29 | Multi-ecosystem airgap package mirror | partial/yes | thin-overlap → open | **pursue-candidate** |
| 30 | Research harness over lab | partial | thin-overlap | park |

**Survivors (pursue-candidate):** 1, 9, 13, 19, 20, 23, 26, 29 — ranked in `PRIORITY.md`. Parked modules (6, 25, 28, 30) may attach to survivors.
