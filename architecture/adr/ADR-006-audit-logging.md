# ADR-006: Minimal structured audit events

- **Status:** Accepted for prototype
- **Context:** Traceability and accountability need reconstructable outcomes, while raw text retention increases privacy exposure.
- **Decision:** Append structured JSONL events containing event type, requirement ID, component, outcome, and timestamp; omit raw incident/prompt text.
- **Alternatives:** No audit, full request/response logging, database-backed tamper-evident store.
- **Rationale:** Minimal fields demonstrate trace links without retaining user text; JSONL is dependency-free for experiments.
- **Positive consequences:** Human-readable, testable event schema, lower exposure than full-prompt logs.
- **Negative consequences:** Local file is not durable, access-controlled, tamper-evident, or production-scale.
- **Trustworthiness implications:** Auditability and data minimisation conflict; minimal logging reduces but does not eliminate risk.
- **Evaluation plan:** Verify required fields and absence of raw PII/prompt text; production integrity and retention need a separate design.
