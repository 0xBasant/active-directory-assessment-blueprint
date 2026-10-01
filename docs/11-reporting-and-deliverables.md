# 11. Reporting and Deliverables

## Reporting principles

- Separate verified facts from hypotheses and untested possibilities.
- Explain complete attack paths, not just isolated tool output.
- Minimize and redact sensitive evidence.
- Record defensive blocks as useful outcomes.
- Map remediation to path reduction and ownership.
- State coverage and limitations clearly.
- Make cleanup status visible.

## Deliverable package

### Executive report

Keep it decision-oriented:

- assessment mode, authorized starting conditions, dates, and coverage;
- most important verified paths and affected business functions;
- what prevented exploitation and where controls worked;
- remediation themes ranked by path reduction and urgency;
- material limitations and residual risk;
- retest recommendation.

Avoid equating the number of findings with security quality.

### Technical report

Include:

- exact scope and testing configuration;
- methodology and tool/module versions;
- asset/identity coverage against expected inventory;
- attack-path diagrams with numbered evidence steps;
- individual findings using the repository template;
- failed/blocked tests relevant to control assurance;
- detection/telemetry timeline;
- artifact and cleanup register;
- excluded/unreachable/untested areas;
- prioritized remediation roadmap;
- appendices with redacted evidence references.

### Machine-readable package

If requested, provide normalized findings with stable IDs, affected entity IDs, severity, evidence references, remediation owner/status, and retest result. Do not include raw secrets. Define the schema/version and integrity-protect the export.

### Defensive validation package

For purple-team work, provide:

- UTC action timeline, source, target, and test ID;
- expected Windows/domain/AD CS/network/EDR events;
- whether the SOC detected, triaged, escalated, and contained;
- telemetry gaps and recommended detection improvements;
- deconfliction notes for real incidents.

## Attack-path reporting

Represent a path as:

`starting condition → verified relationship/action → intermediate control → impact`

For each step, record:

- fact/evidence ID and timestamp;
- identity and target;
- required privileges/preconditions;
- whether it was observed, calculated, simulated, or executed;
- control response;
- confidence/freshness;
- remediation that breaks the edge.

Do not draw an executed red line through edges that were only inferred. Use a distinct visual/state for:

- observed configuration;
- analytically reachable candidate;
- executed/verified edge;
- blocked edge;
- out-of-scope/unvalidated edge.

## Severity and prioritization

Combine:

- achieved or credibly demonstrated impact;
- required starting access;
- reliability and prerequisites;
- exposure/likelihood;
- blast radius and affected business services;
- detectability and existing compensating controls;
- number of paths the weakness enables;
- remediation difficulty and dependency.

CVSS can support a score for a technical weakness, but it does not express an AD graph well. Add path context and high-value-target impact.

## Credential and sensitive-data reporting

Never place plaintext passwords, full hashes, Kerberos tickets, private keys, session tokens, or unredacted personal/customer content in the main report.

Use statements such as:

- “A credential for `service-account category` was recovered and independently verified against the named in-scope service.”
- “12 of 430 authorized password hashes met the agreed weak-password criteria; 7 showed reuse across two or more identities.”

If a client requires account-level notification, deliver it through a separate encrypted, access-limited channel with an immediate remediation/rotation workflow.

## Evidence quality

Evidence must be:

- attributable to an action, source, target, tool/module version, and operator/automation identity;
- time-normalized, preferably UTC;
- sufficient to support the claim without collecting unnecessary data;
- integrity-protected and access controlled;
- redacted for reports while retaining a secure reference to raw material if authorized;
- reproducible or explainably non-reproducible;
- tied to cleanup/artifacts when relevant.

Screenshots are supplemental, not the sole structured record.

## Cleanup closeout

Attach an artifact register containing:

- accounts, groups/memberships, computers, certificates, templates/CA changes;
- files/binaries, services, tasks, registry/configuration changes;
- Kerberos tickets, credential caches, password-audit datasets, private keys;
- worker/container/images and local evidence;
- cloud/API tokens and test applications/roles;
- status: never created, removed and verified, expired/revoked and verified, or residual.

The client and assessment lead should sign off on residual artifacts and compensating actions.

## Retest report

For every retested finding:

- original finding and path edge(s);
- remediation claimed;
- exact limited retest method;
- result: fixed, partially fixed, not fixed, unable to test, or accepted risk;
- alternate path discovered, if any;
- evidence and date;
- residual risk.

Do not overwrite the original result. Preserve history and issue a new retest state.
