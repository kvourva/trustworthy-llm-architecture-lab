# Container view

```mermaid
flowchart LR
  Staff[Human staff] --> API[API Gateway]
  API --> Incident[Incident Service]
  Incident --> Privacy[Privacy Filter]
  Privacy --> Risk[ML Risk Service]
  Privacy --> Transformer[Optional Transformer Risk Service]
  Incident --> Retrieval[Retrieval Service]
  Retrieval --> LLM[LLM Service / Provider]
  LLM --> Verify[Verification Service]
  Risk --> Policy[Policy Engine]
  Verify --> Policy
  Policy --> Approval[Human Approval Gateway]
  Policy --> Decision[Decision Store]
  Incident --> Audit[Audit Service]
  Retrieval --> Audit
  Verify --> Audit
  Policy --> Audit
```

The containers are responsibility boundaries, not independently deployed
processes in this prototype. `src/trustworthy_llm/` supplies in-process
components and contract boundaries; network/API, authentication, durable
storage, and access control remain future work.
