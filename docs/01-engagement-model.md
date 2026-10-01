# 1. Engagement Model

## Objective

An AD assessment should answer four business questions:

1. Can an attacker establish an initial foothold using realistic, approved conditions?
2. From that foothold, which identities, systems, and trust relationships allow horizontal or vertical movement?
3. Can a defensible chain reach critical assets, domain control, another forest, or a hybrid-cloud identity plane?
4. Which small set of remediations breaks the greatest number of verified paths?

The objective is not to execute every known AD technique. It is to prove material paths with the least operational impact and enough evidence for the client to reproduce, prioritize, and fix them.

## Testing modes

| Mode | Starting information and access | Best for | Important limitations |
|---|---|---|---|
| Black box | Approved network position and target boundaries; no credentials or internal diagrams | External-attacker realism, exposed services, unauthenticated weaknesses, password-policy resilience | May spend most time on initial access; provides poor coverage of post-compromise controls if no foothold is found |
| Gray box | Black-box inputs plus one or more dedicated, ordinary user accounts; optionally a managed workstation or VPN identity | Recommended default; assumed breach, identity relationships, shares, Kerberos, AD CS, delegation, and attack paths | Results depend on where the account and execution host are placed |
| White box | Architecture, inventories, policies, selected configuration exports, and dedicated accounts with approved elevated/read access | Maximum control coverage, configuration review, complex multi-forest/hybrid environments, compressed timelines | Less representative of an unknown attacker; elevated access can hide the true initial-access path |

### Recommended default: two-lane gray box

Run two logically separate lanes:

- **Lane A — zero-knowledge exposure:** unauthenticated discovery and initial-access checks from the agreed source segment.
- **Lane B — assumed breach:** start from a dedicated standard domain user and determine what a compromised employee account can reach.

This avoids treating “no initial foothold in the time box” as proof that the directory is safe, while still measuring unauthenticated exposure.

## Access and credential policy

The client should not be asked for a generic list of FTP, SSH, SMB, and RDP passwords. Those are protocols, not separate engagement prerequisites.

Request only the identities needed for the chosen mode:

| Credential/access item | Black box | Gray box | White box | Handling rule |
|---|---:|---:|---:|---|
| Dedicated ordinary AD user | No | Usually | Yes | Expiring, non-human account; no reuse of an employee password |
| Workstation/VPN access | Network position only | If needed | If needed | Dedicated device/session; log source IP |
| Local administrator on sample hosts | No | Optional opt-in | Optional | Use only to validate endpoint controls and lateral-movement assumptions |
| Privileged directory read account | No | Rare | Optional | Prefer read-only delegated access over Domain Admin |
| DCSync-capable account | No | Only for a separately authorized password audit | Only for a separately authorized password audit | High-impact secret; tightly time-bound and transferred out of band |
| Entra identity and MFA method | No | For hybrid/Entra scope | For hybrid/Entra scope | Dedicated test identity and approved MFA workflow |
| SSH/FTP/RDP/SMB credentials | Not supplied by default | Only when a named in-scope system requires them | Only when required by the test plan | Prefer a dedicated account; never request broad credential dumps |
| API/token for automation platform | No | If using platform automation | If using platform automation | Least privilege, rotation date, auditable owner |

Credentials should be transferred using the client-approved secrets manager or one-time encrypted channel, never in the questionnaire, email body, ticket, repository, or report. Record an identifier and privilege description in the test plan—not the secret itself.

## Engagement variants

### Internal AD security assessment

Focuses on on-premises Windows domains, Kerberos, LDAP, SMB/RPC, Group Policy, AD Certificate Services, endpoints, tiering, and forest trusts.

### Assumed-breach assessment

Begins with a low-privileged user or controlled shell and concentrates on privilege escalation, identity relationships, local-administrator reuse, credential exposure, lateral movement, and paths to business-critical systems.

### AD password audit

A distinct workstream that may require DCSync-equivalent rights or an offline, client-supplied dataset. It carries greater data-handling obligations than an ordinary pentest. Hashes and cracked values must have a defined transfer, processing, access, retention, and destruction plan.

### Hybrid AD/Entra assessment

Adds Entra Connect, synchronization identities, federation/SSO, cloud roles, application identities, Conditional Access, and paths that cross between on-premises AD and Entra ID. It requires explicit tenant scope and cloud API authorization.

## Success criteria

Agree measurable outcomes before testing. Examples:

- inventory at least 95% of client-provided in-scope domain controllers and domains;
- validate or refute specified high-risk hypotheses;
- produce evidence-backed paths from each approved starting persona to tier-zero assets;
- make no unapproved production changes;
- leave no test-created accounts, certificates, tickets, services, tasks, binaries, or policy changes;
- deliver prioritized remediation mapped to the verified graph and retest the agreed fixes.

“Domain Admin obtained” is not a sufficient success criterion. A high-quality engagement may be successful precisely because the controls prevent that outcome and the report explains why.

## Deliverables

- executive summary and business impact;
- confirmed asset and identity coverage;
- attack-path diagrams with starting condition, prerequisites, evidence, and impact;
- findings with confidence, severity, affected objects, detection evidence, and remediation;
- control observations, including where an attempted technique was blocked;
- artifact and cleanup register;
- retest results and residual-risk statement;
- optional machine-readable findings and defensive detection timeline.
