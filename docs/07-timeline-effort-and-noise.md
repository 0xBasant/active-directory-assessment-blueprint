# 7. Timeline, Effort, and Noise

## Planning estimates

The wall-clock time of an automated test is not the engagement duration. Scoping, approvals, troubleshooting, analyst validation, cleanup, reporting, and retesting usually dominate.

| Environment | Illustrative characteristics | Active testing | Typical end-to-end engagement |
|---|---|---:|---:|
| Small | Up to ~500 endpoints, one forest, few sites, limited AD CS/hybrid complexity | 1–2 days | 5–7 business days |
| Medium | ~500–5,000 endpoints, multiple domains/sites, AD CS or hybrid identity | 2–5 days | 7–12 business days |
| Large/complex | 5,000+ endpoints, multiple forests/trusts, segmented networks, hybrid/cloud, change gates | 5–10+ days | 2–4+ weeks |

These are planning ranges, not promises. Count only in-scope assets. An environment with 200 highly segmented or fragile systems can take longer than one with 5,000 uniform endpoints.

## Phase estimate for a medium gray-box assessment

| Phase | Typical elapsed effort |
|---|---:|
| Discovery call, questionnaire, scope/RoE | 1–3 business days, often calendar-bound |
| Execution host, access, preflight | 0.5–1 day |
| Discovery and unauthenticated checks | 0.5–1.5 days |
| Authenticated collection and graph analysis | 0.5–1.5 days |
| Approval-gated path validation | 1–3 days |
| Cleanup and reconciliation | 0.25–1 day |
| Analyst validation and report | 2–4 days |
| Client readout | 0.5 day |
| Retest after fixes | 0.5–2 days |

Many activities overlap, but approvals and maintenance windows introduce idle calendar time.

## NodeZero timing evidence

- A Horizon3 vendor demonstration against the GOAD lab describes an autonomous chain completed in roughly 14 minutes. This is useful for seeing how modules can reactivate paths, but it is a controlled demonstration—not a production service-level objective.
- A 2026 research preprint integrating NodeZero through its CLI in an eight-host GOAD/Defender testbed reports pentest runs around 1–2 hours and notes non-determinism in module order, timing, and selected attack paths. The authors also acknowledge Horizon3 support.

Real production duration must be estimated from environment size, reachability, enabled checks, defensive blocking, rate limits, and approval gates. Do not sell a “14-minute AD pentest.”

## Noise model

Noise has at least four dimensions:

- **Network:** connections, packets, broadcast/multicast activity, bandwidth.
- **Authentication:** successes/failures, ticket requests, lockouts, relay/coercion.
- **Endpoint:** processes, file writes, service/task creation, memory access, EDR detections.
- **Directory/control-plane:** LDAP queries, object changes, replication requests, certificate issuance, cloud API activity.

### Relative noise and impact

| Activity | Relative noise | Main observable effects | Default control |
|---|---|---|---|
| DNS/SRV and targeted service discovery | Low | DNS queries, connection attempts | Scope and rate limit |
| LDAP RootDSE/basic directory queries | Low | DC query logs/traffic | Page/query limit |
| Targeted Nmap service/version checks | Low–medium | Many short connections, IDS signatures | Ports/hosts/timing profile |
| Authenticated directory collection | Medium | Concentrated LDAP queries | Method/domain/concurrency cap |
| BloodHound session/local-admin collection | Medium–high | LDAP plus RPC/SMB connections across hosts | Restrict methods and host set |
| SMB share enumeration | Medium | Authentication and tree-connect events | Metadata first, concurrency cap |
| Password spray | High identity risk | Failed logons/Kerberos/NTLM events and lockouts | Separate approval and lockout-aware stop |
| AS-REP/Kerberoast | Medium–high | Kerberos ticket events; bulk patterns are detectable | Named accounts and request cap |
| LLMNR/NBT-NS/mDNS poisoning | High | Broadcast replies and captured auth | Short window, local segment, allow/deny lists |
| Coercion/NTLM relay | High | RPC/SMB/HTTP/LDAP authentication chains | Named sources/targets; kill switch |
| Endpoint agent/RAT or remote execution | High | Process/file/service/task and EDR telemetry | Named hosts, artifact register, approval |
| SAM/LSA/LSASS/DPAPI access | Very high | Sensitive process/store access and likely EDR alerts | High-impact gate; minimal sample |
| DCSync | Very high | Directory replication behavior from a non-DC | Separate authorization |
| Ticket/certificate forgery validation | High | Authentication anomalies and issued/used credentials | Test identity/service, short lifetime, purge |
| AD object/template/policy modification | Very high | Replicated directory state change | Simulation default; before/after + cleanup |

“Low noise” is not “invisible,” and “high noise” does not automatically mean unsafe. Noise should be deliberate, bounded, and observable.

## Authentication safety budget

Before any online credential attempt, calculate a per-domain budget from the real lockout policy, replication behavior, existing failed-attempt state, and critical-account exclusions. A simplistic “N attempts below threshold” rule can still lock users out because other services or attackers may already have consumed the budget.

Minimum controls:

- exclude tier-zero, service, shared, emergency, executive, and fragile accounts unless specifically approved;
- prefer dedicated canary/test users for control validation;
- count attempts centrally across every module and worker;
- space attempts beyond the observation window when approved;
- stop on any unexpected lockout or policy inconsistency;
- never let an LLM choose or expand the attempt count.

Horizon3 publicly documents configurable spray attempts/windows and an automated stop after detecting multiple locked accounts. That is a useful pattern, but the client's RoE can and should be stricter.

## Performance and efficiency metrics

Measure automation by defensible outcomes, not number of exploits:

- asset/domain/controller coverage against known inventory;
- verified paths per analyst-hour;
- false-positive and stale-edge rate;
- percent of actions with complete provenance and cleanup status;
- time from new fact to eligible path;
- number of high-risk actions prevented by policy;
- mean time for a human to review an approval request;
- detection coverage per technique;
- remediation path reduction and retest closure rate;
- operational incidents and unplanned artifacts (target: zero).

## Factors that extend the schedule

- unknown or changing scope;
- unreliable VPN/DNS/time synchronization;
- segmented networks requiring multiple workers;
- multiple forests/tenants and third-party approvals;
- rate limits or fragile legacy/OT assets;
- EDR blocking that requires a control-validation decision;
- complicated AD CS, delegation, or hybrid identity;
- manual approval queues and limited maintenance windows;
- high volumes of candidate paths requiring validation;
- cleanup failures or incident investigation;
- client delays providing inventory or dedicated identities.

## Staffing

For an ordinary medium engagement, plan for:

- one lead AD assessor accountable for decisions and findings;
- a second reviewer/operator for high-impact actions and peer review;
- client identity/infrastructure owner;
- client SOC/detection representative for announced or purple-team work;
- engagement/project owner for scope and schedule;
- optional cloud identity specialist for hybrid scope.

Automation reduces repetitive effort. It does not eliminate the need for accountable operators, client owners, and independent review.
