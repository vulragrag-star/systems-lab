# ATTEMPTS — composition-gap lab notebook

Living trail of closed-loop candidates mined from the vulragrag-star OSS atlas (`SYNTHESIS.md`, `SHORTLIST.md`, `data/scored.jsonl` proceed=true, sector surveys).  
Priority: (1) can the loop stand in production, (2) external prior art beyond GitHub, (3) document every attempt.

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
**pursue** (narrowed claim only — see REPORT recommendation).

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

## Attempt scoreboard

| # | Candidate | Loop stands? | Verdict | Decision |
|---|---|---|---|---|
| 1 | Local-first systems engineering lab | yes (narrow) | thin-overlap → open gap | **pursue** |
| 2 | Supply-chain verify loop | yes | occupied | abandon |
| 3 | Zero-trust personal edge | yes | occupied | abandon |
| 4 | Secure remote DevEx | yes | occupied | abandon |
| 5 | Observability+backup | yes | occupied | abandon |
| 6 | Agent-safe OSS contrib sandbox | partial/yes | thin-overlap | park |
| 7 | WASM hermetic capsule | partial | occupied | abandon |
| 8 | GitOps platform-in-a-box | yes | occupied | abandon |

Only Attempt 1 clears **loop stands AND real gap** under a narrowed non-LLM, non-CDE, non-ZTNA claim.
