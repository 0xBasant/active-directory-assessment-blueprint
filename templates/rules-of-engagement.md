# Rules of Engagement — Active Directory Security Assessment

## 1. Parties and authority

- Authorizing organization:
- Assessment provider:
- Authorization reference/agreement:
- Engagement ID:
- Version/date:
- Authorizing representative:

The authorizing organization represents that it owns the in-scope systems or has authority to permit the described testing.

## 2. Objectives and testing mode

- Business/security objectives:
- Starting personas:
- Mode by workstream: [Black / Gray / White / Mixed]
- Success criteria:

## 3. Scope

### Included

- Networks/source locations:
- Domains/forests/trusts:
- Entra tenants/cloud boundaries:
- Assets/applications:
- Accounts/personas:

### Excluded

- Networks/assets:
- Domains/forests/tenants:
- Accounts/data classes:
- Third parties:

Newly discovered assets, routes, trusts, domains, tenants, and third parties remain parked and are not authorized until added through the change process.

## 4. Time and sources

- Timezone:
- Start/end:
- Daily windows:
- Blackouts:
- Approved worker/source IPs:
- Retest window:

## 5. Technique matrix

States: `Allowed`, `Per-action approval`, `Simulation only`, `Prohibited`. Unlisted techniques are prohibited.

| Technique | State | Targets/limits | Approver/two-person rule |
|---|---|---|---|
| Discovery and read-only enumeration | | | |
| Authenticated graph collection | | | |
| Share content sampling | | | |
| Password spraying | | | |
| AS-REP/Kerberoasting | | | |
| Poisoning/coercion/relay | | | |
| Endpoint execution/temporary agent | | | |
| Local credential stores/memory/DPAPI | | | |
| Credential/ticket/certificate reuse | | | |
| Directory/AD CS object creation/change | | | |
| DCSync/password audit | | | |
| Golden/Silver ticket validation | | | |
| Cross-trust/hybrid movement | | | |

## 6. Operational limits

- Network/concurrency/query limits:
- Authentication budget and excluded accounts:
- Share/content sampling limits:
- Endpoint allowlist:
- Test-object prefix/expiry:
- Ticket/certificate lifetime:
- Cloud API limits:
- Worker egress/update endpoints:

## 7. Credentials and secrets

- Credentials will be dedicated, minimum-privilege, expiring, and transferred through:
- Raw secrets will not appear in this RoE, source control, tickets, ordinary logs, or report body.
- Credential material discovered during testing may be reused only when both the target and technique are authorized.
- Client rotation/escalation owner:

## 8. Data and evidence

- Classification:
- Storage/region:
- Permitted processors/providers:
- Collection minimization rules:
- Access list:
- Transfer channel:
- Retention and deletion dates:
- Password/hash/ticket/private-key handling:
- AI-processing rule:

## 9. Defenses and communication

- Exercise mode:
- Informed parties:
- Deconfliction marker/source:
- Primary contact:
- Emergency stop contact/channel:
- Status cadence:
- Urgent finding channel and response expectation:

## 10. Stop and incident conditions

Testing stops immediately for out-of-scope access, unexpected lockout, service degradation, replication/directory issues, real-incident collision, uncontrolled propagation, prohibited sensitive data, loss of scope enforcement, evidence/secret compromise, or client stop instruction.

On stop: halt new dispatch, preserve relevant audit evidence, notify the emergency contact, avoid uncoordinated cleanup, and follow client incident command. Resume requires documented approval.

## 11. Change control

Changes to scope, techniques, limits, sources, or time require:

- change ID/reason;
- affected section;
- risk review;
- authorized client and provider approvers;
- effective time;
- new immutable scope/RoE version.

Chat/email discussion without the named approval process does not modify authority.

## 12. Cleanup and closeout

The provider will maintain an artifact register and verify removal/revocation where possible. Residual artifacts or uncertain cleanup will be disclosed promptly with owner and mitigation. Test identities/tokens/certificates expire or are revoked according to the closeout plan.

## 13. Signatures

### Client authorization

- Name/title:
- Signature/date:

### Assessment provider

- Name/title:
- Signature/date:
