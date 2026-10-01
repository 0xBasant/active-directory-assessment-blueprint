# 3. Scope and Rules of Engagement

## Scope dimensions

Define scope across every dimension below. A list of IP ranges alone is insufficient for identity testing.

| Dimension | Examples |
|---|---|
| Network | CIDRs, sites, VLANs, VPNs, cloud networks, source addresses |
| Identity | DNS/NetBIOS domains, forests, trusts, Entra tenants, business units |
| Assets | Domain controllers, AD CS, endpoints, servers, appliances, applications |
| Accounts | Starting personas, excluded executives/service accounts, honey accounts |
| Technique | Discovery, spray, roast, relay, credential access, DCSync, ticket validation |
| Time | Date, timezone, daily windows, freeze periods, retest window |
| Data | Permitted evidence, prohibited content, maximum file/sample size |
| Impact | Read-only, authentication, configuration change, code execution, service restart |
| Third parties | MSPs, SaaS, subsidiaries, shared tenants, hosting providers |

## Inclusion and exclusion precedence

Use this order:

1. Legal authorization and explicit exclusions always win.
2. A named excluded asset remains excluded even if it appears inside an included CIDR.
3. Newly discovered domains, trusts, cloud tenants, and routes are **not automatically in scope**.
4. A new asset may be enumerated only to the minimum needed to identify it, then parked pending approval.
5. State-changing validation needs technique approval even when the asset itself is in scope.

Automated scope expansion must be bounded. A product feature that discovers adjacent networks is useful, but should never turn reachability into authorization.

## Technique permission matrix

Every technique group receives one of four states:

- **Allowed:** may run within documented limits.
- **Approval gate:** operator must present target, reason, expected effects, and cleanup plan before each execution.
- **Simulation only:** confirm exposure/configuration but do not perform the impactful action.
- **Prohibited:** do not attempt.

Recommended defaults:

| Technique | Default | Required guardrail |
|---|---|---|
| DNS, LDAP RootDSE, Kerberos, and SMB service discovery | Allowed | Rate/concurrency limits and exclusions |
| Authenticated directory/group/share enumeration | Allowed in gray/white box | Dedicated user and query rate limit |
| BloodHound-compatible collection | Allowed with limits | Collection-method list, object cap, secure graph deletion |
| Password spraying | Approval gate | Lockout-aware cap, test exclusions, SOC notification or blind-test plan |
| AS-REP/Kerberoast request and offline analysis | Approval gate | Approved accounts, no password disclosure in report |
| Share content sampling | Approval gate | Metadata first; content size/data-class limits |
| Name-resolution poisoning | Approval gate | Local segment boundary, duration, denylist, rollback |
| Authentication coercion/relay | Approval gate | Named sources/targets and protocol-specific safety review |
| New machine/user/certificate object | Approval gate | Unique prefix, owner, expiry, cleanup verification |
| Endpoint execution or temporary agent/RAT | Approval gate | Signed/hashed artifact, named hosts, kill switch, cleanup |
| SAM/LSA/LSASS/DPAPI access | Approval gate | Named hosts, memory/data handling, credential rotation decision |
| DCSync/NTDS access | Simulation by default | Separate password-audit authorization for execution |
| Golden/Silver ticket validation | Simulation by default | Lab or named test identity/service; short lifetime; purge verification |
| Cross-domain/forest movement | Approval gate | Target trust/domain separately in scope |
| Persistence or availability impact | Prohibited | Use tabletop or isolated lab instead |
| Destructive change, ransomware simulation, bulk data extraction | Prohibited unless separate exercise | Separate plan and executive authorization |

## Safe proof standard

Stop a path when the current evidence proves the risk. Prefer the least invasive proof:

1. Confirm vulnerable configuration or graph relationship.
2. Demonstrate access to a harmless canary object or synthetic record.
3. Validate privilege on a named test system/account.
4. Perform a state-changing or credential-access action only when the earlier levels cannot establish impact and approval is explicit.

Do not retrieve customer documents merely because a share is readable. Record ACLs and filenames first; inspect content only under the data-sampling rule.

## Stop conditions

All automation and operators must immediately stop new actions when any of these occur:

- an excluded asset, tenant, domain, or third party is reached;
- account lockout count meets the agreed threshold, or lockout policy is uncertain;
- unexpected service degradation, host instability, replication issue, or user impact;
- a safety limit is exceeded or the platform loses reliable scope enforcement;
- client emergency contact invokes stop;
- a real incident is detected or test activity can no longer be distinguished from one;
- highly sensitive data is encountered outside the approved sampling policy;
- persistence or uncontrolled propagation occurs;
- the evidence store, secret vault, or worker is suspected compromised.

Stopping means: halt the scheduler, preserve audit logs, avoid ad-hoc cleanup that could destroy evidence, notify the client, and follow the incident/escalation plan.

## Operational limits to record

- maximum concurrent hosts and requests per second;
- LDAP page size/query rate;
- SMB/RPC session rate;
- authentication attempts per account and per domain/window;
- port-scan timing profile and approved ports;
- maximum data read per file/share/host;
- endpoint execution allowlist;
- test-object naming prefix and expiry;
- ticket/certificate lifetimes;
- maximum cloud API rate;
- working hours and automatic pause times.

## Detection and collaboration modes

Choose one and document who knows what:

- **Announced/control validation:** SOC receives sources, windows, and technique schedule; best for verifying telemetry.
- **Purple team:** operator and defender coordinate in real time, correlating every material action to alerts/logs.
- **Limited-knowledge:** a small control group knows; SOC response is evaluated.
- **Blind:** tightly governed red-team exercise; requires a separate deconfliction and emergency process.

An ordinary AD assessment should default to announced or purple-team operation. A blind exercise materially changes risk and staffing.

## Change and artifact control

For each state-changing action, record:

- unique action ID and operator/automation identity;
- approved target and technique;
- before state;
- exact object/artifact created or modified;
- planned expiry and cleanup procedure;
- after state and independent cleanup verification;
- client acknowledgment when cleanup cannot be proven.

Use a recognizable engagement prefix for test objects. Never rely solely on automatic cleanup; reconcile actual artifacts against the register.
