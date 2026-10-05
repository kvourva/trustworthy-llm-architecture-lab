# ADR-008: Optional dense retrieval

- **Status:** Accepted as an optional adapter; not a core runtime requirement
- **Context:** Lexical search may fail on semantic paraphrases; embedding search adds a model and dependency burden.
- **Decision:** Keep a Sentence Transformer adapter isolated behind the same retrieval result shape; do not download weights in core install/tests.
- **Alternatives:** Lexical-only, dense-only, hybrid reciprocal-rank fusion.
- **Rationale:** A swappable adapter permits comparison while retaining core reproducibility and provenance conventions.
- **Positive consequences:** Enables later paraphrase evaluation with evidence IDs and ranked scores.
- **Negative consequences:** Model/package versions, memory, latency, and download availability affect reproducibility; not run by default.
- **Trustworthiness implications:** Similarity is relevance ranking, not source authority or factual support.
- **Evaluation plan:** Same labelled queries and corpus as lexical retrieval; Precision@k, Recall@k, MRR, Hit Rate@k, latency, and failure cases.
