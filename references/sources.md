# Source Register

Accessed 2026-10-01 unless otherwise stated. Links are grouped by evidentiary role. Vendor documentation verifies what the vendor publishes; it is not an independent measure of completeness, safety, or comparative performance.

## Horizon3.ai / NodeZero primary sources

| Source | What it supports | Evidence label |
|---|---|---|
| [Internal Pentest](https://docs.horizon3.ai/portal/test_types/internal/) | Containerized internal deployment, Intelligent Scope behavior, optional OSINT inputs, initiation workflow | Verified product behavior |
| [NodeZero host requirements](https://docs.horizon3.ai/quickstart/setup_host/manual_host/host_requirements/) | Supported Linux/container runtime, CPU/RAM/storage recommendations, network access, EDR warning | Verified product behavior |
| [Attack Configuration](https://docs.horizon3.ai/portal/features/attack_config/) | Technique controls for spray, shares, poisoning/relay, endpoint credential access, DCSync, tickets, machine accounts, AD CS, and related actions | Verified product behavior |
| [BloodHound integration](https://docs.horizon3.ai/portal/features/bloodhound/) | Valid-credential trigger, collection, ephemeral Neo4j 4.4.x, complex path analysis, backup behavior | Verified product behavior |
| [Cyanide module knowledge base](https://docs.horizon3.ai/knowledge_base/modules/cyanide/) | Responder/Intimidator/modified `ntlmrelayx`, poisoning/coercion/relay targets and correlation | Verified product behavior |
| [Active Directory Password Audit](https://docs.horizon3.ai/portal/test_types/ad_password_audit/) | DCSync-capable credential prerequisite, `secretsdump` verification, managed cracking workflow and categories | Verified product behavior |
| [Azure/Entra ID test](https://docs.horizon3.ai/portal/test_types/azure_entra_id/) | Gray-box hybrid prerequisites, Entra Connect, DCSync, `AZUREADSSOACC$`, Silver Ticket, AzureHound | Verified product behavior |
| [High Value Targeting](https://docs.horizon3.ai/portal/features/high_value_targeting/) | AWS Bedrock/Llama 4 Maverick, selected metadata, container placement, advisory/no-training claims | Verified product behavior |
| [AI in Horizon3.ai](https://horizon3.ai/ai-in-horizon3-ai/) | Cyber Terrain Map, graph reasoning, deterministic/classical ML/scoped GenAI product description | Verified vendor description |
| [Horizon3 Security Vision](https://horizon3.ai/horizon3-security-vision/) | Knowledge graph/Cyber Terrain Map and learning-loop description | Verified vendor description |
| [NodeZero GraphQL API](https://docs.horizon3.ai/api/) | Programmatic targets, schedules, results, CI/CD and JSON/API integration | Verified product behavior |
| [GraphQL API reference](https://docs.horizon3.ai/api/graphql/) | AttackVector DAG, nodes/edges, action/module metadata and related fields | Verified product behavior |
| [NodeZero Runner](https://docs.horizon3.ai/portal/runner/) | Persistent runner/control-plane workflow | Verified product behavior |
| [Touchless NodeZero CLI guide](https://docs.horizon3.ai/cli/guides/touchless-nodezero/) | Scheduled/touchless operation pattern | Verified product behavior |
| [NodeZero MCP](https://docs.horizon3.ai/portal/features/mcp/) | Natural-language interface to launch/manage test workflows | Verified product behavior |

## Horizon3.ai public source code

| Source | What it supports | Evidence label |
|---|---|---|
| [Horizon3.ai GitHub organization](https://github.com/horizon3ai) | Public repository inventory | Public source |
| [Cyanide repository](https://github.com/horizon3ai/cyanide) | Python source, modified Impacket/Responder directories, local databases, licensing | Public source |
| [`h3-cli` repository](https://github.com/horizon3ai/h3-cli) | Open CLI for GraphQL/API, runners, schedules, reports and automation | Public source |
| [`h3-cli` automatic credential injection guide](https://github.com/horizon3ai/h3-cli/blob/public/guides/auto-inject-creds.md) | Local encrypted secret/remote key and Runner injection pattern | Public source/documentation |

Repository counts, stars, branches, and default versions change; inspect the organization directly rather than relying on a count frozen in this document.

## Horizon3.ai technical demonstrations and research posts

| Source | What it supports | Evidence label/limitation |
|---|---|---|
| [NodeZero vs. GOAD: Technical Deep Dive](https://horizon3.ai/intelligence/blogs/nodezero-vs-goad-technical-deep-dive/) | Reactive multi-path demonstration; discovery, null-session data, BloodHound, roast/spray, AD CS, credential access, DCSync, trusts/tickets; ~14-minute claim | Vendor demonstration in a lab, not independent performance benchmark |
| [Hack The Box: Active](https://horizon3.ai/attack-research/n0-attack-paths/hack-the-box-active/) | Historical Nmap, CrackMapExec, `smbclient`, GPP, Impacket, Hashcat, SMB/Metasploit examples | Historical vendor lab walkthrough; not a current dependency manifest |
| [Hack The Box: Retro](https://horizon3.ai/attack-research/n0-attack-paths/hack-the-box-retro/) | NetExec/SMB, password spray, Certipy ESC1, prerequisite-driven path reactivation, RAT example | Vendor lab walkthrough; not a complete current capability list |

## Patents relevant to publicly described mechanisms

Patents show disclosed designs and claims; they do not prove that every described mechanism is deployed in every current product version.

| Source | Topic | Evidence label |
|---|---|---|
| [US Patent 12,732,530](https://patents.justia.com/patent/12732530) | Environment/context-informed password candidate generation and ordered probabilistic testing/feedback | Public patent disclosure |
| [US 2025/0132894 A1](https://patents.google.com/patent/US20250132894A1/en) | Privacy-oriented/k-anonymous hash comparison design using truncated hash bins and local matching | Public patent application |
| [US 2026/0142998 A1](https://patents.google.com/patent/US20260142998A1/en) | Contextual scoring/prioritization concepts | Public patent application |

## Independent/third-party observation

| Source | What it supports | Limitation |
|---|---|---|
| [Closing the Sim-to-Real Gap: An Evaluation Framework for Autonomous Cyber Defense Configuration of Commercial EDR (arXiv:2606.08168)](https://arxiv.org/abs/2606.08168) | Repeated NodeZero/`h3-cli` integration in an eight-host GOAD/Defender lab; reported 1–2-hour runs and non-deterministic module order/timing/path selection | Preprint about evaluating autonomous EDR defense configuration; laboratory environment; authors acknowledge Horizon3 support; not a broad comparative NodeZero benchmark |

## Primary sources for named open-source tools

These links identify the upstream projects. Their presence here does not mean every tool is a current NodeZero dependency.

- [BloodHound documentation](https://bloodhound.specterops.io/)
- [BloodHound source](https://github.com/SpecterOps/BloodHound)
- [Neo4j documentation](https://neo4j.com/docs/)
- [Fortra Impacket](https://github.com/fortra/impacket)
- [NetExec](https://github.com/Pennyw0rth/NetExec)
- [Nmap](https://nmap.org/)
- [Samba `smbclient` documentation](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html)
- [Certipy](https://github.com/ly4k/Certipy)
- [Hashcat](https://hashcat.net/hashcat/)
- [Responder](https://github.com/lgandx/Responder)

## OpenAI primary sources

Used only for the proposed reference architecture's model-selection and budget section; these are not claims about NodeZero's model stack.

- [OpenAI model catalog](https://developers.openai.com/api/docs/models)
- [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
- [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna)
- [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra)
- [OpenAI reasoning guide](https://developers.openai.com/api/docs/guides/reasoning)

Pricing and model availability can change; the repository records a 2026-10-01 snapshot and includes a dated estimator rather than a billing promise.

## Evidence gaps

The following were not publicly verifiable from the sources reviewed:

- proprietary NodeZero Core source code;
- exact scheduler, module dependency graph, scoring formula, or concurrency algorithm;
- complete current software bill of materials for all AD modules;
- exact model prompts, call frequency, token counts, or routing for NodeZero AI features;
- production-wide success rate, false-positive rate, cleanup rate, or noise benchmark;
- consistent behavior across every license tier, deployment type, and product release.

Any procurement or engineering decision that depends on these items should be validated through a controlled proof of value, contractual/security review, product telemetry, and direct vendor answers.
