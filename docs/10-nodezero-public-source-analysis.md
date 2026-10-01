# 10. NodeZero Public-Source Analysis

## Scope and confidence

This analysis uses Horizon3.ai's public documentation, public GitHub organization/repositories, vendor demonstrations, patents, and a published third-party research preprint. It does **not** include access to a customer NodeZero tenant, proprietary source code, internal telemetry, or a controlled hands-on comparison.

Accordingly:

- documented features and public code are labeled **verified product behavior**;
- vendor walkthrough performance is labeled **vendor demonstration/claim**;
- third-party research is labeled **independent observation**, with disclosed limitations;
- conclusions about the hidden planner/scheduler are labeled **architectural inference**.

## Short answer: how discovery is automated

NodeZero appears to automate AD discovery as a feedback loop:

```text
discover reachable assets and identity facts
        ↓
normalize them into a cyber-terrain/attack graph
        ↓
identify modules whose prerequisites are now satisfied
        ↓
apply configuration, safety, and scope controls
        ↓
run eligible modules, often concurrently where independent
        ↓
verify/record results and add newly learned facts to the graph
        ↺
```

The graph, module metadata, action logs, and reactive behavior are publicly evidenced. The exact internal scoring, scheduler code, fact schemas, and concurrency algorithm are proprietary; the loop above is an **architectural inference**, not leaked implementation detail.

## Deployment and initiation

**Verified product behavior:** an internal NodeZero test runs from a Linux host/container placed within an approved client network. Horizon3 documents a one-time command that validates the container runtime, obtains the image, and starts a test. A persistent Runner can poll the API/control plane and launch scheduled work. The public GraphQL API and `h3-cli` support programmatic targeting, scheduling, status, and results.

“Agentless” should be interpreted as no permanent agent required on every target. A worker/container is still needed, and certain approved paths may use an endpoint payload/RAT as part of validation.

## How each requested discovery category is likely handled

### 1. Hosts and network scope

**Verified product behavior:** NodeZero's Intelligent Scope can start from configured networks, explore adjacent address space under documented rules, and honor custom include/exclude settings. Horizon3 describes auto-expansion across private address space and repeated discovery until no additional devices are found.

**Vendor demonstrations:** public walkthroughs show ping/port/DNS/service discovery and explicitly reference Nmap in historical lab material.

**Architectural interpretation:** scanner observations become host/service entities. Deduplication likely correlates IP, DNS, protocol identity, and later directory identifiers. Scope expansion must still be bounded by the engagement authorization; product reachability does not itself authorize a newly found network.

### 2. Domain controllers, domains, and services

**Verified/vendor-public behavior:** DNS and service discovery identify common AD surfaces such as Kerberos, LDAP/LDAPS, Global Catalog, SMB/RPC, and DNS. Subsequent SMB/RPC/LDAP observations reveal domain names, controller roles, and directory context.

**Architectural interpretation:** modules do not need to “know AD” at startup. Discovering a domain/controller/service creates prerequisite facts that enable directory, Kerberos, SMB, BloodHound, AD CS, trust, and credential modules.

### 3. Users, groups, and computers

**Vendor demonstration:** the GOAD deep dive shows unauthenticated/null-session enumeration exposing users/computers in the lab, followed by authenticated relationship collection once a valid identity was found.

**Verified product behavior:** after obtaining a valid domain credential, NodeZero can invoke a BloodHound collector. BloodHound-compatible collection uses directory queries and selected endpoint methods to gather users, groups, computers, ACLs, sessions, delegation, local-admin relationships, and other graph edges.

The data source matters: null-session/RPC enumeration, LDAP directory reads, and endpoint relationship collection have different permissions, noise, freshness, and confidence.

### 4. Shares and exposed material

**Verified configuration behavior:** NodeZero exposes share-scanning controls in attack configuration.

**Vendor demonstrations:** public lab walkthroughs show SMB discovery/enumeration and use of `smbclient`/CrackMapExec or NetExec lineage to identify shares and exposed configuration material. One GOAD path describes credentials in SYSVOL/script-related content; historical HTB material demonstrates Group Policy Preferences exposure.

**Architectural interpretation:** a safe module should enumerate share/ACL/file metadata first, create candidate facts, and retrieve only the content needed to verify an approved hypothesis. Public materials demonstrate capabilities, but do not establish the exact current parser or sampling limit for every NodeZero version.

### 5. Trusts and attack relationships

**Verified product behavior:** NodeZero integrates BloodHound/Neo4j-based graph analysis after valid domain access, and its attack results are represented as a directed acyclic attack-vector graph with nodes/actions/edges exposed through the API. Public materials describe paths across trust boundaries, and attack configuration includes cross-trust Golden Ticket behavior.

**Vendor demonstration:** the GOAD walkthrough follows child/parent and forest relationship paths.

**Architectural interpretation:** trusts are not merely a report field; they form edges that combine with credentials, ACLs, delegation, sessions, and host control. A new trust should be parked if the target domain/forest is not explicitly authorized.

### 6. Credentials and authentication material

NodeZero publicly documents multiple acquisition/validation classes:

- optional OSINT inputs such as domains, company names, weak terms, and Git-related information;
- configurable domain-user password guessing/spraying with attempt/window limits and an automated lockout stop condition;
- AS-REP and service-ticket/Kerberoast paths shown or documented in public materials;
- exposed secrets in shares/scripts/configuration;
- LLMNR/NBT-NS/mDNS poisoning, authentication coercion, capture, cracking/reuse, and NTLM relay through Cyanide;
- SAM, LSA, LSASS, and DPAPI credential access controlled by attack configuration;
- pass-the-hash/ticket and credential reuse in demonstrated paths;
- DCSync/domain credential dumping under explicit configuration;
- a separate AD Password Audit workflow using DCSync-authorized input and managed cracking.

These are not one monolithic “credential scan.” Each has different prerequisites and side effects. The orchestration value is correlating one result—for example, a credential or machine-account capability—with the next eligible path.

## Publicly identifiable tools and subsystems

| Tool/subsystem | Public evidence | Role visible in public material | Evidence limitation |
|---|---|---|---|
| BloodHound collector | Official feature documentation | Collect identity/host relationships | Exact current collector version/options can change |
| Neo4j 4.4.x | Official feature documentation | Ephemeral graph analysis during documented tests | Does not expose proprietary planner logic |
| Impacket | Public walkthroughs and Cyanide source | Kerberos, secrets/RPC/SMB, relay primitives | Module wrappers/current versions are not fully public |
| Modified `ntlmrelayx` | Cyanide docs/source | NTLM relay | Cyanide public code is only one subsystem |
| Responder | Cyanide docs/source | LLMNR/NBT-NS/mDNS poisoning | Bounded to local subnet in published documentation |
| Intimidator | Cyanide docs/source | Authentication coercion methods | Horizon3 custom component |
| Nmap | Historical public walkthrough | Host/service discovery | Walkthrough evidence is not a current all-module inventory |
| CrackMapExec/NetExec | Public walkthroughs | SMB/AD enumeration/authentication | Historical/lab usage and product internals differ |
| `smbclient` | Public walkthroughs | Share interaction | Historical/lab usage |
| Certipy | Retro walkthrough | AD CS discovery/enrollment/authentication | One lab path does not prove all current coverage |
| Hashcat | Historical walkthrough | Offline password analysis | Current managed audit workflow may differ |
| Metasploit | Historical walkthrough | Lab exploitation/validation | Historical example, not proof of current dependency |
| Cyanide | Official docs and public GitHub repo | Coordinated poison/coerce/relay/correlate workflow | Public subsystem, not full NodeZero core |
| NodeZero RAT | Public configuration/walkthroughs | Temporary remote action/validation | Proprietary behavior; approval/artifact risk |
| `h3-cli` and GraphQL API | Public source/docs | Scheduling, runners, reports, automation, MCP-related workflows | Control/API layer, not attack-engine source |

The central proprietary value is not any one tool. It is the module packaging, prerequisites, state/graph correlation, safety configuration, prioritization, evidence, verification, cleanup, and reporting around them.

## Cyanide as a concrete automation example

Horizon3's public Cyanide repository and knowledge-base article describe a subsystem composed of:

- a message pump for coordinating components;
- Responder-based name-resolution poisoning;
- a custom “Intimidator” for coercion methods such as PetitPotam, ShadowCoerce, and PrinterBug-style behavior;
- a modified Impacket `ntlmrelayx`;
- persistent/correlated state in local databases;
- target selection based on prerequisites such as SMB signing disabled, AD CS relay exposure, or LDAP signing posture;
- capture, correlation, possible cracking, and reuse.

This shows the automation pattern clearly: specialized tools emit observations into shared state, and subsequent actions use correlated prerequisites. It also illustrates why the activity is high risk: broadcast/multicast poisoning, forced authentication, captured credentials, and relay can touch unintended assets without strong allow/deny lists and a kill switch.

## BloodHound/Neo4j role in NodeZero

**Verified product behavior:** after a valid domain credential is obtained, a collector runs and an ephemeral Neo4j 4.4.x instance supports complex attack-path identification. Horizon3 documents time-limited backup/download behavior for eligible users.

Likely workflow:

1. normalize a verified domain credential reference;
2. enable collector prerequisites;
3. collect approved directory/endpoint relationship classes;
4. load/merge relationships with previously discovered host/service/credential facts;
5. query paths to high-value targets;
6. verify actionable edges through modules;
7. update the path as edges succeed, fail, or become stale.

Steps 1–7 as a complete loop are partly **architectural inference**. The collector/Neo4j/complex-path facts themselves are documented.

## Impacket role in NodeZero

Public evidence shows several uses of Impacket or its components:

- `GetUserSPNs` in a historical Kerberoasting walkthrough;
- `secretsdump` in lab material and as a verification component described for the AD Password Audit;
- a modified `ntlmrelayx` in Cyanide;
- protocol behavior consistent with Impacket primitives across SMB/RPC/Kerberos examples.

The safe inference is that NodeZero wraps selected protocol primitives in modules with product state/evidence. It is not safe to infer that every current AD action uses stock Impacket or that every command in an old walkthrough remains in the product.

## Attack configuration and safety controls

**Verified product behavior:** Horizon3 documents configurable flags for AD attacks, man-in-the-middle techniques, hashing/cracking, password spraying, share scanning, machine-account creation, AD CS ESC4, DCSync/domain credential dumping, Golden Ticket cross-trust behavior, RAT use, SAM/LSA/LSASS/DPAPI access, poisoning, coercion, and relay.

The documented password-spray defaults/controls include a limited number of attempts over a configured time and a stop after multiple detected lockouts in a domain. Horizon3 also warns that some tests can leave artifacts if cleanup fails.

For a client engagement, vendor defaults do not replace the RoE. Disable everything not expressly approved, apply stricter client-specific limits, and independently reconcile artifacts.

## AD Password Audit

**Verified product behavior:** the separate audit requires a privileged cleartext or NTLM credential with DCSync rights. Documentation describes verifying with `secretsdump`, using DCSync to obtain NTLM material, transferring it to an ephemeral Horizon3 cloud VPC for cracking, and destroying the environment at completion. Candidate strategies include common terms, usernames/company terms, breach/dark-web-related data, custom input, and password reuse analysis.

This workflow has a substantially different risk profile from an ordinary internal pentest. It requires explicit client authorization for replication and off-premises processing, privacy/data-residency review, precise retention/destruction terms, and a plan for handling cracked values. The public documents should be checked against the current contract and deployment option before use.

## Hybrid Entra workflow

**Verified product behavior:** Horizon3 describes its Entra hybrid test as gray box and requests an Entra credential plus a privileged on-premises AD credential with DCSync capability. Public documentation describes LDAP(S), Entra Connect discovery, replication of the `AZUREADSSOACC$` credential, Silver Ticket behavior, and AzureHound collection.

This is a high-privilege test design. It should be a distinct, explicitly approved hybrid workstream—not the default credential package for a routine AD assessment.

## AI and decision-making

**Verified product description:** Horizon3 says NodeZero combines its Cyber Terrain Map/knowledge graph, deterministic logic, classical ML, and scoped generative AI. Public HVT documentation describes an advisory AWS Bedrock/Llama 4 Maverick component that receives selected identity/relationship metadata and does not modify assets. Public marketing also names an “Exploit Suggester & Try Harder Agent.”

What cannot be verified publicly:

- the exact percentage of decisions made by deterministic rules, graph algorithms, ML, or an LLM;
- prompts, token counts, model-call frequency, confidence thresholds, or fallback behavior;
- all model providers/versions used across every feature;
- exact exploit-ranking or path-replanning algorithm.

It would be inaccurate to describe NodeZero simply as “an AI autonomously hacking AD.” The strongest public evidence supports a graph/module automation engine with scoped AI assistance.

## API, CLI, Runner, and recurring automation

**Verified product behavior:**

- GraphQL API for programmatic configuration, targets/schedules, and results;
- public `h3-cli` for interacting with the API, including schedules, runners, reports, and other workflows;
- Runner that polls with a limited API credential and launches NodeZero;
- documented touchless/scheduled operation;
- credential-injection guidance for scheduled work;
- an MCP interface that can bridge natural-language requests to test-management functions.

These components automate deployment and lifecycle. They do not remove the need for scope versioning, approvals, and client change control. Natural language must not become an authorization bypass.

## Performance claims and independent evidence

- **Vendor demonstration:** the patched GOAD scenario with Defender enabled and no starting credential is reported as completing an extensive chain in about 14 minutes. It includes discovery, null-session information, exposed secrets, spray/roast, BloodHound, several AD vulnerabilities, endpoint credential access, DCSync, and trust/ticket paths. It is a demonstration environment and should not be generalized to client duration or success rate.
- **Independent observation with caveat:** a 2026 research preprint used NodeZero through `h3-cli` for repeated tests in an eight-host GOAD/Defender environment. It reports approximately 1–2-hour tests and notes non-deterministic module order, timing, and attack-path selection. The paper acknowledges support from Horizon3, so it is informative but not a fully independent product benchmark.

## What a buyer should validate in a proof of value

- exact asset/domain/forest/tenant scope enforcement and exclusion behavior;
- credential storage, location, encryption, tenant separation, and deletion;
- which modules are deterministic, ML-driven, or GenAI-assisted;
- per-technique enablement and whether material actions require human approval;
- observed traffic/authentication/endpoint/directory noise under agreed profiles;
- BloodHound collection methods, data lifetime, and export/delete behavior;
- artifacts created by each module and cleanup evidence;
- EDR/AV handling without disabling client protections broadly;
- GraphQL/CLI/Runner privilege model and audit records;
- false-positive/stale-edge handling and proof quality;
- data residency for password audit and AI features;
- repeatability across multiple runs and behavior when modules are blocked;
- report quality, remediation path reduction, and retest workflow.

## Bottom line

NodeZero's public materials support a credible picture of event-driven, graph-informed automation that composes open-source/proprietary modules, updates its knowledge as actions succeed, and can reactivate paths when prerequisites appear. BloodHound/Neo4j, Impacket-derived components, network/SMB/AD CS tooling, Cyanide, a worker/Runner, and API/CLI automation are all publicly evidenced in some form.

The full planner is proprietary. A responsible internal design should reproduce the *engineering pattern*—typed state, module prerequisites, deterministic policy, bounded workers, evidence, and human gates—rather than attempting to clone undocumented internals or letting an LLM execute unrestricted offensive commands.

See [`../references/sources.md`](../references/sources.md) for the source register and evidence labels.
