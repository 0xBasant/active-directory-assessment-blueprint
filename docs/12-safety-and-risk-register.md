# 12. Safety and Risk Register

## Go/no-go checklist

Testing is **no-go** if any mandatory answer is “no”:

- [ ] Written authorization is current and names the testing provider.
- [ ] Scope includes networks, identity boundaries, assets, techniques, time, and data—not only IPs.
- [ ] Exclusions and third-party ownership have been reviewed.
- [ ] Source workers/addresses and time zone are recorded.
- [ ] Emergency contacts can be reached through a tested channel.
- [ ] Stop conditions, kill switch, and incident procedure are understood.
- [ ] Authentication and concurrency budgets are configured centrally.
- [ ] Every high-impact technique is disabled, simulated, or has explicit approval requirements.
- [ ] Test identities are dedicated, expiring, and transferred through an approved secrets channel.
- [ ] Evidence storage, access, transfer, retention, and deletion are configured.
- [ ] Backup/restore and replication health are confirmed where state change is possible.
- [ ] Cleanup/artifact tracking is active.
- [ ] Worker DNS, time, routing, target allowlist, and audit logging pass preflight.
- [ ] Client accepts unresolved risks in writing.

## Risk register

| Risk | Example cause | Potential impact | Required mitigation | Stop trigger |
|---|---|---|---|---|
| Out-of-scope access | Auto-discovered route/trust, incorrect CIDR, shared tenant | Unauthorized testing/legal impact | Explicit entity scope, exclusions, fail-closed discovery parking | Any excluded/unknown ownership target reached |
| Account lockout | Spray retries, competing failures, policy mismatch | User/service outage | Central auth budget, exclusions, lockout-state monitoring, dedicated users | Any unexpected lockout or threshold reached |
| Service degradation | Aggressive scans, fragile LDAP/SMB/device | Availability impact | Rate/concurrency caps, fragile-asset list, maintenance windows | Health alert or client report |
| Replication/directory impact | Object/ACL/template changes | Authentication/identity outage | Simulation default, before/after capture, two-person gate, backups | Replication error or unexpected state |
| Credential exposure | Logs, command lines, reports, model prompts | Compromise and privacy breach | Vault/broker, redaction, restricted evidence, rotation plan | Secret observed outside approved boundary |
| Excessive data access | Automated share searching | Confidentiality/privacy breach | Metadata first, content/type/size limits, stop on sensitive class | Prohibited/highly sensitive data encountered |
| Endpoint instability/detection | Agent, remote execution, memory access | EDR quarantine or host outage | Named hosts, approved artifact, kill switch, client coordination | Quarantine, crash, or abnormal behavior |
| Poisoning/relay spillover | Broadcast protocols, broad relay list | Unintended authentication/access | Local segment, allow/deny lists, short duration, kill switch | Any non-approved source/target captured |
| Ticket/certificate persistence | Long lifetimes, failed purge/revocation | Continued unauthorized access | Test identity/service, shortest lifetime, register and revoke/purge | Cannot verify invalidation |
| Cleanup failure | Tool crash, lost state, partial change | Residual access/artifacts | Independent artifact ledger/check, client notification | Residual high-risk artifact |
| AI hallucination | Invented edge or unsafe plan | Wrong action/finding | Fact-ID grounding, schema validation, deterministic policy, human review | Model output conflicts with scope/evidence |
| Prompt injection | Malicious banner/filename/directory text | Data leakage or unsafe recommendation | Treat discovered text as data, isolate/retrieve/minimize, no direct tool authority | Model attempts unauthorized instruction |
| Supply-chain compromise | Unpinned image/tool/dependency | Worker/customer compromise | Signed/pinned artifacts, SBOM, scans, isolated build | Integrity verification failure |
| Real incident collision | Actual attacker active during test | Confusion/evidence loss | Deconfliction channel, preserved logs, incident procedure | Indicators cannot be attributed safely |
| Third-party/cloud spillover | Trust/SaaS/tenant association | Contract and data risk | Separate owner authorization and tenant boundary | Newly identified third-party boundary |

## High-impact action checklist

Before password spraying, poison/coerce/relay, endpoint execution, credential-store access, DCSync, ticket/certificate forgery, directory/AD CS changes, or cross-trust/hybrid validation:

- [ ] Action and targets are explicitly permitted in current scope/RoE.
- [ ] Prerequisites are supported by verified, fresh facts.
- [ ] The same risk cannot be proven with a less invasive method.
- [ ] Exact source identity/worker and target are named.
- [ ] Blast radius, expected logs/artifacts, and business impact are understood.
- [ ] Authentication/data/concurrency/time limits are configured.
- [ ] Required operator/client/two-person approval is recorded and unexpired.
- [ ] The SOC/deconfliction posture matches the exercise plan.
- [ ] Kill switch and rollback/cleanup are ready.
- [ ] Evidence will be minimal, redacted, and securely stored.

## Technique-specific controls

### Password spray

- Centralize attempts across tools/workers.
- Exclude critical/service/emergency/honey accounts as agreed.
- Use a client-approved candidate set; do not let a model invent guesses.
- Account for existing failure state and replication/window behavior.
- Stop at the first anomalous lockout or authentication-system degradation.

### Poisoning, coercion, and relay

- Bound source subnet, protocols, capture duration, and relay targets.
- Maintain source/target denylist and never relay to an unconfirmed host.
- Do not capture more authentication material than necessary.
- Avoid production certificate/directory changes when configuration proof suffices.

### Endpoint credential material

- Use a named sample host and named objective.
- Check Credential Guard/EDR/configuration first.
- Do not collect unrelated interactive users' material.
- Define immediate rotation/escalation if a real credential is recovered.
- Store dumps/artifacts separately with shortest retention.

### DCSync and password audit

- Obtain separate authorization for replication of credential material.
- Confirm data residency and processing provider/location.
- Minimize attributes/accounts if technically possible.
- Never send raw hashes or plaintext values to an LLM.
- Provide access logs and destruction evidence.

### Golden/Silver tickets

- Prefer proving key exposure and resulting capability without forging.
- If actual validation is necessary, use a named test identity/service and shortest lifetime.
- Prevent broad group/authorization claims beyond the objective.
- Purge caches, rotate affected test keys/accounts if required, and verify invalidation.

### AD CS

- Separate discovery, enrollment, authentication, and configuration modification approvals.
- Use a test identity and retain certificate serial/issuer/expiry in the artifact register.
- Protect private key/PFX as a credential.
- Revoke/delete test material and verify directory/CA state.

## Incident procedure

If a stop condition occurs:

1. Halt new dispatch and revoke worker leases.
2. Do not destroy logs or rush cleanup before the client decides whether incident preservation is needed.
3. Notify the emergency contact with UTC time, source, target, action ID, observed effect, and current state.
4. Separate test-attributable actions from unknown activity.
5. Preserve minimum relevant evidence with integrity controls.
6. Follow client incident command for containment/recovery.
7. Resume only with documented authorization and updated risk controls.

## Closeout acceptance

Before declaring the engagement complete:

- [ ] All jobs are stopped and workers are accounted for.
- [ ] Artifact register is reconciled independently.
- [ ] Secrets/tickets/certificates/tokens/test accounts are revoked, expired, rotated, or handed to the client with an owner.
- [ ] Residual artifacts and failed cleanup are disclosed.
- [ ] Evidence retention and deletion dates are recorded.
- [ ] Reports contain no prohibited secrets or customer content.
- [ ] Client has received urgent issues through the agreed channel.
- [ ] Retest scope and dates are agreed or explicitly declined.
