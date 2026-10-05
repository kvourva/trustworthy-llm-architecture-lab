# Trust boundaries

```mermaid
flowchart LR
  subgraph Untrusted[Untrusted inputs]
    Incident[Incident report]
    Evidence[Retrieved evidence]
    ProviderOutput[Provider output]
  end
  subgraph Controlled[Prototype-controlled components]
    Privacy[Privacy filter]
    Risk[Risk estimator]
    Retrieval[Retriever]
    Verify[Verifier]
    Policy[Policy engine]
    Audit[Minimal audit]
  end
  Human[Accountable human]
  Incident --> Privacy --> Risk
  Incident --> Retrieval
  Evidence --> Retrieval --> Verify
  ProviderOutput --> Verify
  Risk --> Policy
  Verify --> Policy --> Human
  Policy --> Audit
```

Incident and evidence text are untrusted data, not instructions. Provider
outputs are untrusted claims. The local prototype has no authentication,
authorization, tenant isolation, network egress policy, or secret management.
Do not expose it as a service until those controls and a threat model exist.
