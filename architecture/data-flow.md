# Data flow

```mermaid
flowchart LR
  Raw[Incident text] -->|synthetic input| Filter[PII filter]
  Filter --> Risk[Risk model]
  Filter --> Query[Retrieval query]
  Corpus[Synthetic evidence + provenance] --> Retrieval[Retriever]
  Query --> Retrieval
  Retrieval --> Context[Evidence IDs + source + score]
  Context --> Provider[LLM provider boundary]
  Provider --> Draft[Draft + extracted claims]
  Draft --> Verifier[Claim verifier]
  Context --> Verifier
  Risk --> Route[Oversight policy]
  Verifier --> Route
  Route --> Human[Human review]
  Route --> Store[Decision store]
  Route --> Audit[Minimal audit record]
```

Raw prompt text is not included in the audit event schema. Any implementation
that persists prompts or evidence must define purpose, retention, access, and
redaction controls before use.
