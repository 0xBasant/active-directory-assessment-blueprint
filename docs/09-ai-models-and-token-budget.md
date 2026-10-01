# 9. AI Models and Token Budget

## Recommendation

Use a routed, multi-tier model strategy:

- **GPT-6 Luna** for high-volume, low-risk normalization assistance, classification, deduplication, small graph summaries, and report boilerplate.
- **GPT-6.1 Sol** as the recommended default for attack-path review, conflicting evidence, safer-test selection, remediation synthesis, and final report drafting.
- **GPT-6 Astra** only for rare, genuinely novel or ambiguous escalations where evaluation shows that the higher cost improves correctness.

The product's authoritative state, parsers, policy, approvals, and cleanup must remain deterministic. A model proposes and explains; it does not grant itself execution authority.

This recommendation is based on the official OpenAI model catalog and reasoning guidance available on 2026-10-01. Verify names, availability, context limits, and prices before procurement.

## Current official model snapshot

| Model | Suggested role | Context / max output | Input / cached input / output per 1M tokens |
|---|---|---|---:|
| GPT-6 Luna | Efficient high-volume worker | 1.05M / 128K | $0.10 / $0.01 / $0.50 |
| GPT-6.1 Sol | Default reasoning and synthesis | 1.05M / 128K | $2.00 / $0.10 / $10.00 |
| GPT-6 Astra | Escalation model for hardest cases | 1.05M / 128K | $10.00 / $1.00 / $50.00 |

These are Standard processing rates for requests with at most 272K input tokens. For these models, the published long-context tier applies above 272K input tokens per request: 2× input/cache rates and 1.5× output rates for that request. Fast, Batch/Flex, and regional processing can also change rates. The calculator estimates aggregate tokens at the Standard short-context rate; it does not infer these adjustments, cache writes, tool charges, storage, or networking. [Official model pricing](https://developers.openai.com/api/docs/models/gpt-6.1-sol)

Reasoning tokens are billed as output tokens. OpenAI's reasoning guide recommends leaving substantial headroom—at least 25,000 tokens when first experimenting with a reasoning model—and using `max_output_tokens` to cap reasoning plus visible output. Do not set the cap that high for every routine event; evaluate each task class and use the smallest reliable budget.

## What NodeZero publicly says about AI

Horizon3 describes a hybrid architecture using knowledge graphs/“Cyber Terrain Map,” deterministic logic, classical machine learning, and scoped generative AI. Its public High Value Targeting documentation says that feature uses AWS Bedrock with Llama 4 Maverick in a dedicated container adjacent to the NodeZero Core, receives selected usernames/hostnames/BloodHound relationship metadata, does not train on customer data, and provides advisory output rather than modifying assets.

Horizon3 has not publicly disclosed a complete per-test model call pattern or token budget. Therefore, the estimates below are for the proposed reference architecture—not a claim about NodeZero's usage.

## Do not send raw telemetry to the model

The main token and security optimization is architectural:

1. Parse known tools deterministically into typed facts.
2. Redact secrets and sensitive content.
3. Deduplicate and correlate identities/assets.
4. Retrieve only the subgraph relevant to one decision.
5. Use compact schemas and stable IDs.
6. Cache static instructions and environment summaries.
7. Ask the model for a bounded structured output.
8. Validate output against a schema and policy before use.

Raw Nmap, LDAP, BloodHound, SMB, EDR, and tool logs can be huge, repetitive, and hostile. Treat all discovered text as untrusted content that can contain prompt injection. Never include password/hash/ticket/private-key values in a model request.

## Task routing

| Task | Model tier | Typical input | Typical output/reasoning | Human review |
|---|---|---:|---:|---|
| Classify one normalized event batch | Luna | 1K–8K | 200–1K | Sampled |
| Merge/entity ambiguity recommendation | Luna or Sol | 2K–12K | 500–2K | Required for consequential merge |
| Summarize a relevant subgraph | Luna | 5K–30K | 1K–4K | Optional/advisory |
| Rank candidate safe tests | Sol | 5K–25K | 2K–8K | Required before action gate |
| Analyze contradictory path evidence | Sol | 10K–50K | 3K–12K | Required |
| Draft one finding/remediation | Sol | 5K–20K | 1K–5K | Required |
| Novel architecture/chain review | Astra, only if justified | 20K–100K | 5K–25K | Senior review |

These ranges are starting hypotheses. Instrument actual input, cached input, reasoning, and visible output by task type; then evaluate accuracy, safety, latency, and cost.

## Illustrative per-engagement budgets

The following assumes normalized facts, retrieval, batching, caching, no secrets, and model calls at decision/report boundaries—not one call per packet or host.

| Size | Luna input/output | Sol input/output | Illustrative API model cost* |
|---|---:|---:|---:|
| Small | 1.5M / 0.25M | 0.5M / 0.15M | ~$2.78 |
| Medium | 6M / 1M | 2M / 0.8M | ~$13.10 |
| Large/complex | 30M / 5M | 10M / 3M | ~$55.50 |

\*Using the model prices in the snapshot table, treating all listed input as uncached and all output—including reasoning—as output-priced tokens. This excludes Astra escalations, retries, cache writes, storage, external tools, platform/hosting, network, and human labor. Real use can be far higher if raw data is repeatedly sent, and lower with effective caching/routing.

Model API cost will generally be a small part of the total assessment cost. Engineering, licenses, isolated compute, password-audit compute, evidence protection, analyst time, and customer coordination dominate.

## Per-run budget controls

Set budgets at four levels:

- **Request:** maximum input and output/reasoning tokens; timeout; schema.
- **Task class:** maximum calls, allowed model tiers, retry policy, and acceptable latency.
- **Engagement:** total token/cost ceiling with warning and hard-stop thresholds.
- **Tenant/month:** aggregate budget, concurrency, and escalation allowance.

When the budget is exhausted, fail into deterministic processing and an analyst queue. Never skip policy or lower the evidence standard to save tokens.

## Model gateway controls

- strict allowlist of use cases and models;
- per-engagement tenant isolation;
- redaction and data-class policy before requests;
- no raw secrets or unrestricted file contents;
- retrieval limited by current scope and operator permission;
- tool calling only through the same deterministic job/policy interface;
- structured response schemas and validation;
- prompt-injection defenses that treat discovered content as data;
- audit record of model, version/snapshot, parameters, token use, retrieved fact IDs, and response;
- evaluation suite for hallucinated edges, unsafe action recommendations, missed exclusions, and remediation correctness;
- analyst feedback stored as labeled evaluation data—not automatically as execution policy.

## Reasoning effort strategy

- Use no/low reasoning for deterministic transformations or simple classification.
- Use medium/high for path explanation, conflicting observations, and remediation tradeoffs.
- Use `xhigh` only for a small escalation queue after evaluations demonstrate value; official guidance calls out security/code review and deep research as potential fits.
- Use the most capable model as a teacher/reviewer while developing evals, then route routine tasks to the smallest model that meets the acceptance threshold.

## Evaluation before production

Create a gold dataset of redacted, authorized lab engagements containing:

- true/false/stale graph edges;
- incomplete and conflicting tool results;
- excluded targets and ambiguous ownership;
- high-impact actions with safer alternatives;
- prompt injection embedded in hostnames, file names, banners, and directory descriptions;
- finding narratives with known evidence and remediations;
- cases where the correct answer is “insufficient evidence” or “do not run.”

Score factual grounding, citation to fact IDs, unsafe recommendations, scope violations, sensitive-data leakage, schema validity, analyst correction rate, latency, and token cost. A fluent narrative is not proof of reliable security judgment.

## Cost calculator

Run:

```bash
python3 tools/token_cost_estimator.py --model gpt-6.1-sol \
  --input-tokens 2000000 --output-tokens 800000
```

Counts may be aggregated across many requests; the example does not represent one 2M-token request. For cached input, specify the cached portion separately and exclude it from `--input-tokens`. Apply the calculator only to requests using the Standard short-context rate, or adjust the resulting budget for other pricing tiers.

## Official references

- [OpenAI model catalog](https://developers.openai.com/api/docs/models)
- [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
- [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna)
- [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra)
- [OpenAI reasoning guide](https://developers.openai.com/api/docs/guides/reasoning)

The broader source register is in [`../references/sources.md`](../references/sources.md).
