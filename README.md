# Active Directory Assessment & Automation Blueprint

An authorization-first playbook for scoping, conducting, automating, and reporting an Active Directory (AD) security assessment. It also documents what can be verified publicly about Horizon3.ai NodeZero's AD testing approach and turns those observations into a vendor-neutral reference architecture.

This repository is a planning and governance artifact. It deliberately contains no exploit payloads, credential-dumping implementation, ticket-forging code, or unattended offensive runner. Testing techniques named here must be used only under written authorization and the agreed rules of engagement (RoE).

## What is included

| Need | Document |
|---|---|
| Executive overview and engagement choices | [Engagement model](docs/01-engagement-model.md) |
| Technical, legal, and operational prerequisites | [Prerequisites and client intake](docs/02-prerequisites-and-client-intake.md) |
| Scope, exclusions, safety gates, and stop conditions | [Scope and rules of engagement](docs/03-scope-and-rules-of-engagement.md) |
| End-to-end testing workflow | [Testing methodology](docs/04-testing-methodology.md) |
| AD, Kerberos, AD CS, trust, and post-access test catalog | [AD test catalog](docs/05-ad-test-catalog.md) |
| BloodHound, Neo4j, Impacket, and supporting tools | [Tooling](docs/06-tooling.md) |
| Duration, effort, network noise, and operational impact | [Timeline, effort, and noise](docs/07-timeline-effort-and-noise.md) |
| Safe automation and human approval architecture | [Automation architecture](docs/08-automation-architecture.md) |
| Model routing, token estimates, and cost calculator | [AI model and token budget](docs/09-ai-models-and-token-budget.md) |
| Public-source NodeZero analysis | [NodeZero analysis](docs/10-nodezero-public-source-analysis.md) |
| Evidence, reporting, cleanup, and retesting | [Reporting and deliverables](docs/11-reporting-and-deliverables.md) |
| Risks, mitigations, and go/no-go checklist | [Safety and risk register](docs/12-safety-and-risk-register.md) |

Reusable engagement artifacts are under [`templates/`](templates). The proposed system design is under [`architecture/`](architecture), and all research links—with evidence labels—are in [`references/sources.md`](references/sources.md).

## Recommended default engagement

For most organizations, use a **gray-box, assumed-breach assessment**:

- Deploy an isolated execution host in an approved internal segment.
- Supply one dedicated, expiring, ordinary domain-user account through an approved secrets channel.
- Begin with safe enumeration and graph collection.
- Require explicit approval for password spraying, name-resolution poisoning, authentication coercion/relay, credential material access, endpoint payloads, DCSync, forged tickets, cross-trust movement, and cloud/hybrid actions.
- Use automation for repeatable discovery, parsing, attack-graph maintenance, evidence capture, and known-safe validation.
- Keep an accountable human operator at every material-impact gate.

Do **not** ask a client to email ordinary employee passwords or provide a blanket Domain Admin credential. Black-box work should begin without credentials; gray/white-box work should use dedicated, expiring accounts with the minimum access required by the approved scenario.

## Quick start for an engagement lead

1. Send [`templates/client-questionnaire.md`](templates/client-questionnaire.md).
2. Complete and sign [`templates/rules-of-engagement.md`](templates/rules-of-engagement.md).
3. Tailor [`templates/test-plan.md`](templates/test-plan.md) and record every excluded/high-impact technique.
4. Run the preflight and go/no-go checks in [`docs/12-safety-and-risk-register.md`](docs/12-safety-and-risk-register.md).
5. Record evidence using [`templates/evidence-log.csv`](templates/evidence-log.csv) and findings using [`templates/finding-template.md`](templates/finding-template.md).
6. Estimate AI usage with `python3 tools/token_cost_estimator.py --help`.

## Evidence standard

The NodeZero section uses four labels:

- **Verified product behavior** — supported by Horizon3.ai documentation or public source code.
- **Vendor demonstration/claim** — useful evidence, but not an independent benchmark.
- **Independent observation** — published by a third party; limitations are stated.
- **Architectural inference** — a reasoned design interpretation, not a claim about undisclosed implementation.

## Repository status

- Research snapshot: **2026-10-01**
- NodeZero access level: public documentation, public GitHub repositories, published demonstrations, patents, and independent research; no customer tenant or proprietary source-code access
- AI pricing/model snapshot: official OpenAI documentation on **2026-10-01**; verify again before budgeting

## Local validation

```bash
python3 tools/validate_repository.py
python3 -m unittest discover -s tools -p 'test_*.py'
```

The optional [GitHub Actions template](templates/github-actions-validate.yml) runs the same checks. CI is not enabled in this repository; enabling it requires placing the template under `.github/workflows/` with workflow-write access.

## Responsible-use notice

All examples are deliberately procedural rather than executable. Operators remain responsible for authorization, applicable law, customer change-control, data handling, evidence minimization, and stopping when safety conditions are breached. See [DISCLAIMER.md](DISCLAIMER.md).
