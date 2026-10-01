# 6. Tooling

The toolchain should be modular. No single tool provides reliable discovery, authorization control, path analysis, execution, evidence, cleanup, and reporting.

## Recommended layers

| Layer | Example tools/components | Purpose |
|---|---|---|
| Scope/control plane | Engagement database, policy engine, scheduler, approval queue | Enforce targets, techniques, limits, and human gates |
| Network discovery | Nmap or equivalent targeted scanner; DNS tooling | Hosts, services, domain infrastructure |
| AD/SMB interaction | NetExec/CrackMapExec lineage, Samba clients, LDAP/Kerberos/RPC libraries | Authentication and controlled enumeration |
| Protocol primitives | Impacket, native Windows administration APIs | SMB/RPC/Kerberos/LDAP operations and validation |
| Graph collection/analysis | BloodHound collectors and BloodHound/Neo4j-compatible graph layer | Identity relationships and path analysis |
| AD CS | Certipy and/or equivalent review tools | CA/template discovery and approved validation |
| Offline strength | Hashcat or approved cracking service | Bounded password-strength analysis |
| Endpoint validation | Native, signed, auditable scripts/tools approved by the client | Local controls and canary validation |
| Evidence/reporting | Structured event store, object storage, report generator | Provenance, replay, findings, cleanup |
| AI advisory | Tool-calling model behind retrieval, policy, and approval gates | Summarization, triage, path explanation, remediation |

Tool availability and licensing change. Pin versions, retain hashes/SBOMs, test in a lab, and document whether each component is open source, commercial, or internally developed.

## BloodHound and Neo4j

### What they do

BloodHound-style collectors gather directory and endpoint relationships such as group membership, ACL control, sessions, local-admin rights, delegation, certificate-service relationships, and trusts. A graph engine stores principals/assets as nodes and relationships as edges so path queries can answer questions such as “How can this ordinary user reach a tier-zero target?”

Neo4j is a graph database historically used by BloodHound. Current BloodHound deployments may package graph/storage components differently, so follow the installed version's architecture rather than assuming a particular database release.

### How to use them safely

- Select only approved collection methods; “all” can cause substantial LDAP/RPC/SMB activity.
- Constrain domains, OUs, hosts, concurrency, and collection duration.
- Encrypt graph data because it contains a high-value map of the environment.
- Version each collection and preserve relationship provenance.
- Validate important edges before acting; session data and local-admin relationships can become stale.
- Delete graph data according to the evidence-retention schedule.

### How NodeZero uses them publicly

Horizon3 documents that after obtaining a valid domain credential, NodeZero runs a BloodHound collector and, in the documented implementation, uses an ephemeral Neo4j 4.4.x instance during the test. The graph supports complex attack-path discovery. That public detail verifies the use of graph analytics; it does not reveal the proprietary orchestration algorithm.

## Impacket

Impacket provides Python implementations and examples for Windows network protocols. Relevant capabilities include SMB/RPC interaction, Kerberos ticket requests, directory replication/secrets operations, remote-management patterns, and NTLM relay primitives.

In this blueprint, Impacket should sit behind a controlled adapter:

- typed inputs from the fact graph rather than arbitrary operator strings;
- scope and approval checks before execution;
- per-action timeouts, rate limits, and target allowlists;
- structured parsing with tool version and command provenance;
- secret redaction before logs reach the evidence/report/AI layers;
- explicit artifact/cleanup declarations.

Public Horizon3 materials mention or incorporate Impacket components including `GetUserSPNs`, `secretsdump`, and a modified `ntlmrelayx` in Cyanide. This supports the conclusion that protocol libraries are wrapped as modules rather than that NodeZero is simply “running Impacket.”

## NetExec/CrackMapExec, SMB clients, and Nmap

- **Nmap:** host/service discovery and selective characterization. Avoid broad version/script scans by default; tune timing and ports to the hypothesis.
- **NetExec/CrackMapExec lineage:** authentication and service/host enumeration across common enterprise protocols. Use low concurrency and separate “can authenticate” from “authorized to execute.”
- **Samba `smbclient` or native clients:** share listing and bounded file access. Start with ACL/metadata; enforce file count/size/data-class limits.

Horizon3's public historical lab walkthroughs reference Nmap, CrackMapExec/NetExec, and `smbclient`. These demonstrations establish tool use in those examples, not necessarily the exact implementation in every current NodeZero module.

## Certipy and AD CS analysis

Certipy can discover AD CS authorities/templates and evaluate multiple misconfiguration paths. Put enrollment, certificate issuance, authentication, template modification, and CA modification behind separate permissions. Treat PFX/private keys as credentials and revoke/delete test certificates when the engagement ends.

Horizon3's public Retro walkthrough references Certipy for discovery, request, and authentication in a lab path. Current NodeZero coverage should be verified from current release documentation rather than inferred from a single walkthrough.

## Hashcat and password analysis

Offline cracking can measure weak credentials without repeated online authentication, but it materially increases data sensitivity. Controls should include:

- explicit authorization and approved hash types/accounts;
- isolated cracking environment and bounded time/work factors;
- prohibited candidate categories, if any;
- no plaintext values in ordinary logs/reports;
- remediation statistics rather than a password list;
- documented rotation/escalation and destruction.

Horizon3's older public lab content references Hashcat, while its current AD Password Audit documentation describes a managed cloud cracking workflow. Treat product-current behavior and historical lab tooling separately.

## Poisoning, coercion, and relay tooling

Responder-style name-resolution poisoning and Impacket-style relay are noisy and can affect unintended systems. A controlled implementation needs:

- local-segment and target boundaries;
- responder/service denylist;
- protocol and destination allowlist;
- duration and capture limits;
- deduplication and correlation before reuse;
- a real-time kill switch;
- secret handling and cleanup.

Horizon3 has published **Cyanide**, which combines a message-pump architecture, Responder, a custom “Intimidator” coercion component, and modified Impacket `ntlmrelayx`. Its documentation describes correlating poisoned/coerced authentication with relay targets such as SMB signing-disabled hosts, AD CS web enrollment, or LDAP configurations. This is the clearest public example of NodeZero wrapping open-source protocol capabilities in a coordinated subsystem.

## Commercial platform versus an internal stack

### Commercial platform advantages

- maintained module compatibility and content updates;
- integrated scheduling, evidence, attack paths, and reporting;
- safety defaults and repeatability;
- lower engineering/operations burden.

### Internal orchestration advantages

- transparent policy logic and full customization;
- tight integration with internal asset, identity, and approval systems;
- direct control over data residency and evidence;
- tool choice is not tied to one vendor.

### Internal orchestration costs

- continuous testing across Windows/AD versions and defenses;
- parsers that survive output/version changes;
- secrets, cleanup, telemetry, and safety engineering;
- legal/tool licensing review;
- operational ownership when a module causes impact.

Do not estimate an internal clone as “a few scripts around BloodHound and Impacket.” The expensive part is reliable state, safety, orchestration, evidence, and maintenance.

## Tool acceptance checklist

Before adding any tool/module:

- Is its license compatible with distribution and commercial use?
- Is the binary/image pinned, hashed, scanned, and attributable?
- Are inputs typed and scope checked?
- Can it consume or expose secrets, and where do they flow?
- What traffic, events, and endpoint artifacts does it create?
- Does it modify state? If so, can before/after state and cleanup be proven?
- Can it be stopped and timed out safely?
- Does its output parse deterministically, including partial failure?
- Is there a lab test for success, failure, exclusion, and cleanup?
- Can a human understand the proposed action before approving it?
