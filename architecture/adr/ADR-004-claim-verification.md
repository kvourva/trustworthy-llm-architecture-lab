# ADR-004: Three-way claim verification

- **Status:** Accepted for baseline
- **Context:** RAG drafts may contain unsupported, contradictory, or evidence-linked claims.
- **Decision:** Use an explicit SUPPORTED / CONTRADICTED / UNKNOWN lexical overlap baseline and route non-supported outputs for review.
- **Alternatives:** No verification, semantic embedding threshold, optional NLI model, human-only review.
- **Rationale:** The simple baseline is deterministic and makes its limits testable; an NLI model is future comparative work.
- **Positive consequences:** Unknown is distinct from contradiction; failures can be surfaced rather than silently accepted.
- **Negative consequences:** Overlap and negation heuristics miss entailment, scope, temporal conditions, and nuanced contradictions.
- **Trustworthiness implications:** Verification is another fallible predictive mechanism, never factual proof. Do not interpret provider confidence as calibrated probability.
- **Evaluation plan:** Supported, contradictory, and unknown fixtures; unsupported-claim rate and verification latency.
