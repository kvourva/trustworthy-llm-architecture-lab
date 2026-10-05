# ADR-003: Provenance-preserving retrieval and RAG

- **Status:** Accepted for prototype
- **Context:** Evidence grounding is necessary for regulatory and operational drafts, but generation alone does not establish facts.
- **Decision:** Start with TF-IDF lexical retrieval returning evidence ID, source, score, and rank. Pass retrieved evidence through an `LLMProvider` abstraction; use a deterministic mock locally.
- **Alternatives:** Dense embeddings only, hybrid search, direct LLM response without retrieval, provider SDK throughout the code.
- **Rationale:** Exact terminology is inspectable and offline; provider abstraction enables failure tests and replacement. Dense retrieval remains an optional comparison.
- **Positive consequences:** Stable provenance, no paid API requirement, explicit retrieval failure, isolated integration point.
- **Negative consequences:** Lexical mismatch misses paraphrases; mock behavior is not generative-model evidence; context selection can omit relevant sources.
- **Trustworthiness implications:** Returned source identifiers are provenance, not validation. Empty retrieval must remain empty and cannot be filled with invented citations.
- **Evaluation plan:** Precision@k, Recall@k, MRR, Hit Rate@k; failure, citation validity, unsupported-claim and provider-failure tests.
