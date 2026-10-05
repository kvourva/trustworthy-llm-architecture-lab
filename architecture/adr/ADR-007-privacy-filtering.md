# ADR-007: Synthetic privacy filtering

- **Status:** Accepted for synthetic experiments only
- **Context:** Personal data could flow into retrieval, providers, or audit records.
- **Decision:** Demonstrate regex detection/redaction of synthetic email and phone patterns; never use real PII in fixtures.
- **Alternatives:** No filtering, external DLP service, named-entity recognition, structured field allow-list.
- **Rationale:** A small deterministic fixture supports precision/recall/leakage experiments without introducing personal data.
- **Positive consequences:** Local, inspectable, reproducible behavior; redaction can be tested before provider boundaries.
- **Negative consequences:** Regex misses variants and may over-redact innocuous number strings; no legal compliance claim.
- **Trustworthiness implications:** Treat as a research probe only; privacy is not solved by masking two patterns.
- **Evaluation plan:** Synthetic precision, recall, false positives, leakage rate; extend utility tests in E6 before any stronger claims.
