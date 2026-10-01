# 2. Prerequisites and Client Intake

## Mandatory prerequisites

Testing must not begin until all of the following exist:

- signed authorization identifying the authorizing organization and testing provider;
- approved scope and exclusions, including third-party systems and shared infrastructure;
- rules of engagement with technique-level permissions;
- source IP addresses/hosts and testing window;
- primary and emergency client contacts with authority to stop testing;
- agreed evidence classification, retention period, transfer method, and deletion owner;
- backup/restore confirmation for systems on which state-changing validation is permitted;
- lockout, availability, and safety thresholds;
- a documented incident procedure that distinguishes expected test activity from a real compromise.

## Information to request

### Organization and environment

- legal entity, business owner, technical owner, SOC contact, and change ticket;
- number of users, endpoints, servers, sites, domains, forests, and domain controllers;
- domain/forest functional levels and supported Windows Server versions;
- IP ranges, VLANs, VPN path, egress controls, proxies, DNS servers, and jump hosts;
- network diagrams and trust relationships for white-box work;
- AD CS presence, certificate authorities, web enrollment, Network Device Enrollment Service, and certificate templates;
- Entra tenants, Entra Connect/Cloud Sync, federation, privileged access systems, and cloud boundaries;
- critical assets: tier zero, identity infrastructure, backup, virtualization, EDR, management, finance, healthcare, engineering, and production systems;
- legacy protocols/systems and fragile assets such as medical, industrial, OT, or unsupported Windows devices.

### Policies and operations

- domain and fine-grained password/lockout policies;
- maintenance windows and blackout periods;
- EDR/AV/NDR/SIEM products and whether this is a blind, announced, or collaborative exercise;
- current alerts/incidents and business operations that could be confused with the test;
- prohibited data classes and actions;
- preferred severity method and reporting format;
- ticketing, evidence transfer, and remediation owners.

### Credentials and access

For black-box work, request no credential. For gray/white-box work, request dedicated, expiring test identities—not real users' credentials.

The minimum useful gray-box package is usually:

- one standard AD user with no intentional privileged group memberships;
- its expected organizational unit, group memberships, and expiration time;
- an approved network position representative of an employee workstation;
- optionally, one sample workstation assignment for validating endpoint controls;
- for hybrid scope, one test Entra user and a coordinated MFA mechanism.

Additional access should be modular and optional:

- a second user in a different business unit to compare segmentation;
- a local-admin account on a small sample of hosts for endpoint-control verification;
- a read-only/delegated directory account for configuration coverage;
- a DCSync-capable, short-lived identity only for a separately signed password-audit workstream;
- approved SSH, RDP, database, application, or appliance access only for explicitly named systems.

## Execution-host requirements

For a vendor-neutral internal assessment worker:

- supported, patched Linux host or hardened assessment appliance;
- 4 CPU cores and 16 GB RAM recommended for ordinary environments; scale memory/CPU for large graphs and parallel enumeration;
- at least 80 GB encrypted SSD space if storing scanner images, graph data, and evidence locally;
- Docker/Podman if the selected tools are containerized;
- reliable DNS, time synchronization, and approved reachability to in-scope segments;
- outbound access only to approved update, license, reporting, or control-plane endpoints;
- unique host identity, restricted administration, full command/audit logging, and encrypted storage;
- no unrelated services or customer data;
- an agreed disposal/reimage process after evidence handoff.

NodeZero's published internal host guidance specifically lists Ubuntu 20.04+ or RHEL 9+, Docker 20.10+ or Podman 4+, 2 cores/8 GB minimum, 4 cores/16 GB recommended, and 40 GB/80 GB storage minimum/recommended. Horizon3 advises against installing endpoint protection on its NodeZero host because security controls can interrupt simulated malicious actions. That is a **product-specific recommendation**, not a universal reason to disable client defenses. For a vendor-neutral worker, isolate and monitor the host; any EDR exception must be explicit, minimal, time-bound, and approved.

## Network and identity readiness

Before launch, validate without performing exploitation:

- the worker source IP matches the RoE;
- system time is accurate enough for Kerberos;
- intended DNS servers resolve the in-scope domains;
- approved domain controllers and required ports are reachable;
- routing cannot accidentally reach excluded customers, subsidiaries, lab networks, or cloud tenants;
- logging is active on the worker and the client can identify its traffic;
- test accounts authenticate as expected and have only the documented access;
- stop-channel contacts respond to a preflight message;
- the secrets channel works, without copying secrets into assessment notes.

## Secrets handling requirements

- Keep secrets in a dedicated vault with access logs and an expiry date.
- Pass a secret to a tool only at runtime; do not place it in command history, source code, environment dumps, screenshots, or report text.
- Store hashes, Kerberos tickets, certificates, private keys, memory artifacts, and cracked passwords as secrets.
- Separate evidence identifiers from secret values. For example, record `CRED-004 verified for DOMAIN\\test.user`, not its password.
- Use encryption in transit and at rest; restrict access to named operators.
- Destroy secrets and high-risk artifacts after the retention period and provide an attestation if required.

## Client questionnaire decision rules

The questionnaire in [`../templates/client-questionnaire.md`](../templates/client-questionnaire.md) is intentionally broad. During scoping:

- mark unknown answers as discovery objectives rather than forcing guesses;
- distinguish “in scope for enumeration” from “approved for state-changing validation”;
- identify third-party ownership before any test traffic;
- place techniques with material availability or identity risk into an explicit opt-in table;
- state whether defensive teams are informed, partially informed, or blind;
- never treat silence or an unchecked box as approval.

## Preflight output

Produce a one-page go/no-go record containing:

- authorization/version and change-ticket reference;
- final targets/exclusions and source addresses;
- approved window and timezone;
- test identities by identifier and privilege (no secret values);
- enabled technique groups and human approval gates;
- escalation contacts and tested communication channel;
- worker health, DNS/time/reachability checks;
- unresolved risks and the person accepting each risk;
- decision, timestamp, and approver.
