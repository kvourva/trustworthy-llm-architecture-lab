# System context

```mermaid
flowchart LR
  Operator[Logistics operator] -->|Incident and question| Assistant[Incident support system]
  Manager[Logistics manager] <-->|Review / approval| Assistant
  Compliance[Compliance officer] <-->|Evidence review| Assistant
  Customer[Customer] -->|Reported issue| Assistant
  Assistant -->|Advisory draft and provenance| Operator
  Regulator[Regulator] -. audit request .-> Audit[Audit records]
  Assistant --> Audit
  Sources[Synthetic policy / procedure evidence] --> Assistant
```

The system supports human triage and drafting. It does not make autonomous
logistics decisions or execute transport, release, or customer-account actions.
External evidence sources and stakeholders are trust boundaries.
