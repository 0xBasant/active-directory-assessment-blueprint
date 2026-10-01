# Finding: [Concise title]

## Summary

- **Finding ID:** [AD-001]
- **Status:** [Confirmed / Partially confirmed / Simulated / Retest]
- **Severity:** [Critical / High / Medium / Low / Informational]
- **Confidence:** [High / Medium / Low]
- **Affected entities:** [Stable IDs and human-readable names]
- **Attack-path objective:** [High-value target/business impact]

## Starting condition

[State the assumed/obtained identity, network position, host, and required access.]

## Description and impact

[Explain the weakness and the business/security effect without overstating unexecuted steps.]

## Verified path

1. [Observed/calculated/executed step and evidence ID]
2. [Step]
3. [Impact]

Clearly mark any step that was calculated or simulated but not executed.

## Evidence

| Evidence ID | UTC time | Source/target | What it proves | Sensitivity/redaction |
|---|---|---|---|---|
| [EV-001] | [timestamp] | [entities] | [claim] | [classification] |

Do not include plaintext passwords, full hashes, tickets, private keys, tokens, or unnecessary customer content.

## Detection/control response

[Alerts, blocks, logs, response time, or telemetry gap.]

## Operational effects and artifacts

[Authentication attempts, state changes, objects/files/certificates/tickets created, cleanup status.]

## Remediation

### Immediate containment

[Short-term steps.]

### Durable correction

[Root-cause fix, ownership, validation.]

### Path reduction

[Which path edges and other related paths this correction removes.]

## References

[Primary defensive/vendor references; do not paste exploit instructions.]

## Retest

- **Date:** [UTC]
- **Method:** [Minimum authorized validation]
- **Result:** [Fixed / Partial / Not fixed / Unable / Accepted]
- **Evidence:** [IDs]
- **Residual risk:** [Statement]
