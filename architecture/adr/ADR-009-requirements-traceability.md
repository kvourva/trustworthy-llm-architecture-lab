# ADR-009: Machine-readable concern-to-evaluation trace

- **Status:** Accepted
- **Context:** Prose-only requirements are difficult to check for missing implementation and evaluation links.
- **Decision:** Keep stakeholder concerns, requirements, and a CSV traceability matrix in version control; use stable requirement IDs across architecture, tests, and metrics.
- **Alternatives:** Prose-only mapping, external requirements platform, model-based goal notation.
- **Rationale:** CSV/YAML are portable, independently cloneable, reviewable, and suitable for a structural integrity test.
- **Positive consequences:** Trace gaps can be detected without a hosted service; links remain near implementation.
- **Negative consequences:** Duplicated labels can drift; structural checks cannot assess semantic correctness and maintenance has a cost.
- **Trustworthiness implications:** A completed link chain is evidence of documentation coverage only, not satisfaction of a concern.
- **Evaluation plan:** Check every requirement ID has a component, test, and metric link; inspect CSV and YAML consistency.
