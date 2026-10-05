# ADR-005: Risk-tiered human oversight

- **Status:** Accepted for policy prototype
- **Context:** Review-all reduces throughput; review-none risks severe incidents bypassing human attention.
- **Decision:** LOW is advisory, MEDIUM advisory with warning, HIGH requires human approval, and CRITICAL requires human escalation. No tier permits automatic consequential execution.
- **Alternatives:** Full routing automation, approval for every item, confidence-only escalation, random audit sampling.
- **Rationale:** Risk-tiered rules are explicit, configurable, and auditable for an initial study.
- **Positive consequences:** Policy outcomes are deterministic and latency/escalation can be measured under assumptions.
- **Negative consequences:** Upstream misclassification can under-escalate; review delay and reviewer behavior are not represented.
- **Trustworthiness implications:** Human oversight does not fix missed risk; human remains accountable and execution stays out of scope.
- **Evaluation plan:** Automation of recommendation routing, escalation rate, HIGH/CRITICAL false negatives, latency with stated approval-delay assumptions.
