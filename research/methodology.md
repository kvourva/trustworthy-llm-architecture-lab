# Methodology

This repository uses design-science-style artefact construction followed by
controlled, reproducible experiments on explicitly synthetic data. The
research object is the traceability method and comparative behavior of
mechanisms, not a deployable logistics product.

## Procedure

1. Derive role-based concerns and classify them with the eight-attribute
   taxonomy (currently analyst-generated; stakeholder interviews are future
   work).
2. Express concerns as prioritized, verifiable YAML requirements and map them
   through a CSV trace matrix to architecture, implementation, tests, and
   metrics.
3. Generate deterministic synthetic incident records with fixed seeds and
   disclose class and lexical biases.
4. Compare simple baselines and optional heavier mechanisms on fixed data
   splits; report macro and per-class measures, especially HIGH/CRITICAL misses.
5. Preserve provenance and explicit failure outcomes in retrieval/RAG.
6. Measure oversight and privacy behavior only under documented synthetic
   assumptions.
7. Interpret results conservatively and report missing optional runs; do not
   impute empirical results.

## Component decision template

For each mechanism, document what/why, research question and requirement,
method and simpler baseline, alternatives, assumptions, failure modes,
evaluation, architectural trade-off, and what can and cannot be concluded.
ADRs and learning notes instantiate this template.

Metrics are operational definitions, not proxies for trust itself. For
example, evidence coverage does not establish evidence truth, and audit event
completeness does not establish accountability in practice.
