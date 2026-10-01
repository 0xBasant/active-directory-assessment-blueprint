# Client Questionnaire — Active Directory Security Assessment

Do not place passwords, hashes, tickets, tokens, private keys, recovery codes, or other secrets in this document. Provide only credential identifiers and use the agreed secrets channel for values.

## 1. Engagement and contacts

- Legal entity authorizing the assessment:
- Business owner:
- Technical/identity owner:
- Change/ticket reference:
- Assessment mode: [Black box / Gray box / White box / Mixed]
- Desired business questions/outcomes:
- Primary technical contact and hours:
- 24×7 emergency stop contact and tested channel:
- SOC/incident contact:
- Third-party/MSP contacts, if applicable:

## 2. Timing

- Timezone:
- Earliest start / hard end:
- Daily permitted windows:
- Maintenance windows:
- Blackout/freeze/business-critical periods:
- Retest window:

## 3. Network scope

- Included CIDRs/sites/VLANs/VPN/cloud networks:
- Explicitly excluded ranges/hosts:
- Approved source hosts/IP addresses:
- Network segments requiring separate workers:
- Egress proxy/firewall requirements:
- DNS servers and approved name-resolution path:
- Fragile, legacy, OT, medical, safety, or unsupported systems:
- Shared/third-party networks reachable from scope:
- Is automatic discovery of adjacent private ranges allowed? If yes, define hard bounds:

## 4. Identity scope

- Included DNS/NetBIOS domains and forests:
- Explicitly excluded domains/forests/OUs:
- Included/excluded trusts:
- Approximate users/computers/servers/domain controllers:
- Domain/forest functional levels and Windows Server versions:
- AD sites and major geographic locations:
- Entra tenant IDs/domains included:
- Entra Connect/Cloud Sync/federation/seamless SSO present:
- Third-party or subsidiary identities sharing trusts/tenants:

## 5. Critical assets and objectives

- Tier-zero/domain/forest administration assets:
- AD CS certificate authorities and enrollment services:
- Backup, virtualization, endpoint-management, PAM, SIEM, and EDR infrastructure:
- Production/business-critical systems:
- Sensitive applications/data classes:
- Named high-value targets for attack-path analysis:
- Canary/test accounts, files, hosts, or services available for safe proof:

## 6. AD and authentication posture

- Domain and fine-grained password/lockout policies:
- MFA/smart card/Windows Hello requirements:
- LAPS deployment:
- Credential Guard/Remote Credential Guard posture:
- SMB signing policy:
- LDAP signing/channel binding/LDAPS posture:
- NTLM restrictions and legacy requirements:
- LLMNR/NBT-NS/mDNS posture:
- Local administrator model/tiering:
- Known delegation/AD CS/trust exceptions:

## 7. Starting access (no secret values)

### Gray/white-box test identity

- Credential reference ID:
- Type: [ordinary AD user / Entra user / local user / SSH / application / other]
- Expected privilege/groups:
- Assigned workstation/system, if any:
- Expiration/revocation time:
- MFA coordination:
- Secrets transfer channel:

### Optional additional identities

For each, state the specific test objective and minimum privilege. Do not provide a Domain Admin or DCSync-capable identity unless that separately approved objective genuinely requires it.

| Credential ref | Type/privilege | Objective | Expiry | Client owner |
|---|---|---|---|---|
| | | | | |

## 8. Technique decisions

Choose `Allowed`, `Per-action approval`, `Simulation only`, or `Prohibited`. Blank means prohibited.

| Technique group | Decision | Targets/limits | Required approver |
|---|---|---|---|
| Network/service discovery | | | |
| Anonymous SMB/LDAP/RPC enumeration | | | |
| Authenticated directory/BloodHound collection | | | |
| Share metadata/content search | | | |
| Password spray | | | |
| AS-REP/Kerberoast offline strength testing | | | |
| Name-resolution poisoning | | | |
| Authentication coercion/relay | | | |
| Machine/user/certificate object creation | | | |
| AD CS enrollment/authentication | | | |
| Endpoint execution/temporary agent | | | |
| SAM/LSA/LSASS/DPAPI access | | | |
| Credential/hash/ticket reuse | | | |
| DCSync/password audit | | | |
| Golden/Silver ticket validation | | | |
| Cross-domain/forest movement | | | |
| Entra/hybrid validation | | | |
| Configuration modification/persistence | | | |

## 9. Limits and stop conditions

- Maximum concurrent hosts/requests:
- Authentication attempts per account/domain/window:
- Accounts/categories excluded from any authentication attempt:
- Maximum share files/content bytes that may be inspected:
- Endpoint execution allowlist:
- Test-object naming prefix and maximum lifetime:
- Client health/availability signals to monitor:
- Additional immediate stop conditions:
- Who can authorize resume:

## 10. Defenses and deconfliction

- Mode: [Announced / Purple team / Limited knowledge / Blind]
- EDR/AV/NDR/SIEM products:
- Should worker/tool artifacts be allowlisted? Exactly what and for how long?
- Expected alert/response objectives:
- Existing incidents or exercises during the window:
- Real-incident deconfliction process:
- Logs the client can provide for correlation:

## 11. Data handling

- Evidence classification:
- Approved storage region/location:
- Encryption and access requirements:
- Prohibited data/content:
- Approved evidence transfer channel:
- Raw evidence retention:
- Credential/hash/password-audit retention:
- Final deletion/attestation requirements:
- May any assessment metadata be processed by an external AI service? If yes, define fields/provider/region/retention:

## 12. Reporting

- Report audiences:
- Severity/risk method:
- Required formats/integrations:
- Urgent-disclosure threshold and channel:
- Account-level weak-password notification process:
- Readout participants:
- Remediation owners and target dates:

## Client confirmation

The answers above describe intended scope and preferences but do not replace the signed authorization and RoE.

- Prepared by/date:
- Reviewed by/date:
- Outstanding questions:
