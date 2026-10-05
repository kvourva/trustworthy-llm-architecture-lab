# Trustworthiness taxonomy

The following working taxonomy maps each attribute to an observable concern
and a conservative design response. It is a research framing, not a claim of
complete coverage or legal compliance.

| Attribute | Scenario concern | Design mechanism / evidence |
|---|---|---|
| Transparency | Staff cannot tell which evidence informed a draft | Preserve retrieved source IDs and expose recommendation status |
| Accountability | Responsibility for acting is unclear | Named human approval route and audit events |
| Privacy | Customer details may enter prompts or logs | Synthetic PII filter; minimise audit fields |
| Security | Untrusted incident text may cross service boundaries | Treat incident text as data; bounded provider and service interfaces |
| Reliability | HIGH/CRITICAL incidents may be missed | Per-class recall, false-negative analysis, conservative escalation |
| Human oversight | Consequential action must remain with a person | HIGH approval, CRITICAL human escalation; no automatic execution |
| Traceability | Concerns are disconnected from tests and metrics | Requirement IDs link YAML, CSV, architecture, tests, and experiments |
| Explainability | A risk label lacks a comprehensible basis | TF-IDF linear baseline and transparent evidence/verification outcomes |

Security is addressed architecturally here; this prototype is not a security
assessment or production-ready control system.
