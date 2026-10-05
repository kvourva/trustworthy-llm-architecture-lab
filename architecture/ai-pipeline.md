# AI pipeline

```mermaid
sequenceDiagram
  actor Staff as Human staff
  participant Incident as Incident Service
  participant Privacy as Privacy Filter
  participant Risk as Risk Service
  participant Retrieval
  participant LLM as LLM Service
  participant Verify as Verification Service
  participant Policy as Policy Engine
  participant Audit as Audit Service
  Staff->>Incident: incident + question
  Incident->>Privacy: minimize synthetic PII
  Privacy->>Risk: filtered text
  Privacy->>Retrieval: filtered question
  Retrieval-->>LLM: evidence with source IDs
  LLM-->>Verify: draft and claims
  Verify-->>Policy: three-way verification outcome
  Risk-->>Policy: estimated risk tier
  Policy-->>Staff: advisory / approval / escalation route
  Incident->>Audit: minimal event
  Verify->>Audit: verification outcome
  Policy->>Audit: routing outcome
```

Failure at retrieval yields insufficient evidence; provider failure is
contained; unsupported or contradicted claims require review. These are
prototype contracts, not a production availability guarantee.
