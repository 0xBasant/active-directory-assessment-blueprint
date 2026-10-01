# 5. Active Directory Test Catalog

This catalog is a planning aid, not permission to execute. The RoE state and approval gate govern every test. “Proof” means the least invasive evidence sufficient to support the finding.

## Discovery and directory posture

| Area | What is evaluated | Safer proof | Typical risk/noise |
|---|---|---|---|
| Domain/DC discovery | DNS SRV, domain/forest names, controller roles and reachable services | Correlated DNS/service observations | Low |
| Host/service inventory | Live systems, management and identity protocols, versions where needed | Targeted probes within rate limits | Low–medium |
| Anonymous exposure | SMB/LDAP/RPC enumeration, null sessions, exposed shares | Read-only metadata/query result | Low–medium |
| SMB posture | Signing, dialects, guest/null access, share permissions | Negotiation and ACL metadata | Low–medium |
| LDAP posture | Signing, channel binding, LDAPS certificates, anonymous bind | Connection/config result | Low |
| Directory hygiene | Stale accounts, privileged memberships, password flags, descriptions, SPNs | Authenticated read queries | Low–medium |
| Trusts and topology | Domain/forest trust direction, transitivity, SID filtering, sites | Directory objects plus client confirmation | Low |
| Group Policy | Links, permissions, scripts, preference exposure, unsafe deployment paths | ACL/content metadata; redacted sample if authorized | Medium |

## Authentication and credential resilience

| Technique/objective | Preconditions | Safe validation approach | Default gate |
|---|---|---|---|
| Password spray | Known users, policy/lockout limits, approved candidates | Tiny lockout-aware set; stop before threshold; exclude critical accounts | Approval |
| AS-REP roasting | Account without Kerberos preauthentication | Request only approved accounts; offline strength test; no plaintext in report | Approval |
| Kerberoasting | Service principal and domain authentication | Request service ticket; offline strength analysis; minimize accounts/work factor | Approval |
| Reused/default credentials | Approved target service and candidate | One bounded validation per candidate/target class | Approval |
| Secrets in shares/configuration | Read access to approved location | Metadata/search rules first; minimum redacted sample | Approval for content |
| Local secret exposure | Approved endpoint and elevated access | Inspect protection/configuration before extracting material | Approval |
| Password audit | Explicit password-audit workstream and lawful authority | Client-side/offline controlled processing, minimum disclosure, formal destruction | Separate authorization |

Password cracking is best treated as an exposure measurement. Report affected account categories, strength patterns, reuse, and remediation; do not circulate plaintext passwords.

## Kerberos and delegation

| Area | Question answered | Preferred proof | Escalation note |
|---|---|---|---|
| Service accounts/SPNs | Are service keys vulnerable to offline recovery or excessive privilege? | Configuration + bounded ticket/strength validation | Rotate/reconfigure test account if value recovered |
| Preauthentication | Can selected accounts be attacked offline without an initial password? | Flag + bounded request | Avoid bulk targeting |
| Unconstrained delegation | Can a host receive reusable delegated credentials? | Directory setting and placement/path evidence | Coercion is a separate gate |
| Constrained delegation | Can protocol transition/delegation reach an unintended service? | Relationship graph + named test service | Ticket use is approval-gated |
| Resource-based constrained delegation | Can an identity modify a target's allowed-to-act relationship? | ACL/path proof; create/modify only with approval | Machine-account creation may be a prerequisite and artifact |
| Pass-the-ticket | Does an obtained ticket grant unintended access? | Named test identity/service and minimal resource | Treat ticket as secret; purge cache |
| Golden Ticket | Would KRBTGT key control permit domain ticket forgery? | Key exposure + configuration/path is usually sufficient | Actual forgery is simulation by default |
| Silver Ticket | Would a service-account key permit service-ticket forgery? | Key exposure + service scope is usually sufficient | Actual ticket only for named test service |

Golden/Silver tickets are not ordinary privilege-escalation checks. A safe engagement normally demonstrates that the relevant signing key could be obtained and explains the impact. Actual forgery adds forensic artifacts and risk without necessarily adding business evidence.

## AD Certificate Services (AD CS)

Assess:

- certificate authority discovery and hierarchy;
- enterprise CA and template permissions;
- enrollment rights and manager/approval/signature requirements;
- subject/SAN control and authentication-capable EKUs;
- template or CA object write permissions;
- web enrollment and relay-relevant exposure;
- issuance policies and application policy mappings;
- certificate/private-key storage and renewal behavior;
- revocation and cleanup capability.

Use the current Certified Pre-Owned/AD CS taxonomy supported by the selected tool version. Do not claim that a platform covers every `ESC` class simply because it covers some. Public NodeZero materials specifically demonstrate or document selected paths including ESC1, ESC3, ESC4, ESC8, and ESC11; coverage changes and must be verified against the current product release.

Preferred proof order:

1. configuration and permission evidence;
2. path calculation to a named impact;
3. enrollment with a dedicated test identity/template path;
4. authentication only to a harmless test resource;
5. revoke/delete issued material and verify the directory/CA state.

## ACL and object-control paths

Evaluate excessive rights over users, groups, computers, OUs, GPOs, certificate templates/CAs, DNS, and domain roots. Relevant relationships include the ability to:

- reset a password or write sensitive attributes;
- add a group member or change group ownership/ACL;
- link/modify a GPO or its underlying files;
- change delegation or service-principal attributes;
- create computer objects or control an existing one;
- grant replication rights;
- modify certificate-service configuration.

An ACL edge alone can become stale or conditional. Confirm inheritance, deny entries, object type, current principal/token, and target before reporting an exploitable path.

## Endpoint and post-access controls

| Control area | Questions | Safe first step |
|---|---|---|
| Local privilege | Which groups/rights/configurations can elevate the current identity? | Read configuration and token state |
| Services/tasks | Are privileged services or tasks modifiable? | ACL and path checks; no restart/change |
| Software/deployment | Can writable files/shares become privileged execution? | Permission/path proof |
| Local admin reuse | Does one identity administer multiple hosts? | Authz checks on a named sample |
| Sessions | Do higher-value identities expose reachable sessions? | Relationship/telemetry; no credential access |
| SAM/LSA secrets | Would local secret stores yield reusable credentials? | Protection/configuration assessment |
| LSASS/Credential Guard | Are interactive secrets exposed in memory? | Check controls/configuration first |
| DPAPI/browser/app secrets | Can current context decrypt reusable material? | Inventory types and permissions before extraction |
| LAPS | Are local passwords deployed, protected, and readable only by intended principals? | Schema/ACL/configuration checks |
| Remote management | Are SMB, WinRM, RDP, SSH, WMI/DCOM paths appropriately limited? | Reachability and authorization check |
| EDR response | Does the defense detect/block approved test behavior? | Coordinate a harmless canary action |

SAM/LSA/LSASS/DPAPI extraction, endpoint agents, service creation, task creation, process injection, and defensive-control bypass all require explicit permission. A proof that shows they *would* succeed can be enough.

## Lateral movement

Test whether an obtained identity or approved foothold can reach peer systems through:

- reused local-administrator or service credentials;
- SMB/WinRM/RDP/SSH/WMI/DCOM or management platforms;
- remote service/task/software deployment permissions;
- shared administrative tiers and active privileged sessions;
- writable shares, scripts, package repositories, or management content;
- delegation and certificate-based authentication;
- database/application linked identities.

Reachability is not the same as authorization, and authorization is not the same as permission to execute. The graph should represent these separately.

## Domain, replication, and trust impact

### DCSync

Test whether any non-domain-controller principal has directory replication rights and whether that produces a path to high-value credentials. Reading ACLs is low impact; issuing replication requests and handling returned password material is high impact. Execute only under a separately approved path or password-audit workstream.

### Domain controller secret access

Evaluate backup access, volume snapshots, deployment systems, and administrative routes that could expose NTDS/SYSTEM material. Do not copy a full database when permission/path evidence or a controlled canary proves the finding.

### Golden Ticket

Evaluate whether KRBTGT key material is obtainable, whether the account has been rotated correctly, and how monitoring responds. Actual ticket forging is normally unnecessary. If authorized, use a dedicated test principal representation, shortest practical lifetime, one named service, and purge it immediately.

### Silver Ticket

Evaluate whether a service-account key can forge authentication to a particular service and whether service-side validation/monitoring catches it. Restrict any actual validation to a named test service.

### Trust paths

Assess trust direction/type/transitivity, SID filtering, selective authentication, delegated administration, and identities/groups crossing boundaries. A discovered trusted domain/forest is parked until the client confirms it is in scope.

## Hybrid AD/Entra paths

When explicitly scoped, assess:

- Entra Connect/Cloud Sync hosts and accounts;
- password hash sync, pass-through authentication, federation, seamless SSO, and certificate/key material;
- `AZUREADSSOACC` and analogous service-account exposure;
- mapping from on-premises control to cloud roles/applications and vice versa;
- Conditional Access, legacy authentication, privileged roles, application/service principals, and managed identities;
- cloud API auditability and tenant boundaries.

Hybrid tests require both on-premises and cloud authorization. Do not infer tenant scope from a synchronized domain name.

## Evidence for every test

Record:

- test ID and hypothesis;
- source persona/host and target entity;
- prerequisite facts and their provenance;
- RoE state and approval ID;
- start/end time and tool/module version;
- normalized result plus minimal raw evidence reference;
- observed detection/defensive outcome;
- operational impact and artifacts;
- cleanup status;
- confidence and alternative explanation.
