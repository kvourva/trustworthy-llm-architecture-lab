# Research Questions (Phase 1)

> Status: Phase 1 – research framing only. No datasets, models, retrieval, RAG, verification, oversight or experiments exist yet. Nothing in this document is a result.

## 0. Framing and scope

**System under study.** An AI-assisted logistics *incident-management* system: it helps human staff (operators, managers, compliance officers) triage and respond to incidents such as shipment delays, supplier disruptions, customs problems, route changes, damaged shipments, dangerous goods, warehouse incidents, customer-data incidents and regulatory questions.

**The system supports humans. It is not an autonomous logistics decision maker.** Every recommendation is advisory; accountability for any action stays with a named human role. Where later phases model "automation", this means automation of *recommendation drafting and routing*, not of consequential decisions.

**Terminology** (used consistently across the repository):

| Term | Meaning here |
|---|---|
| Trust concern | A stakeholder-stated worry about the system (e.g. "I cannot tell why it rated this incident LOW"). |
| Trustworthiness attribute | One of: transparency, accountability, privacy, security, reliability, human oversight, traceability, explainability. |
| Requirement | A verifiable statement derived from a trust concern. |
| Architecture driver | A requirement or quality attribute that materially constrains design. |
| AI/ML mechanism | A technique (classifier, retriever, verifier, policy, filter) intended to satisfy a requirement. |
| Trace chain | Stakeholder → Trust Concern → Requirement → Quality Attribute → Architecture Driver → AI/ML Mechanism → Architecture Decision → Component → Test → Metric. |

**Stakeholders:** logistics operator, logistics manager, compliance officer, regulator, customer, Data Protection Officer (DPO), AI engineer, software architect.

**Cross-cutting assumptions (all RQs).**
- A1. Initial data are clearly labelled synthetic; findings are about the *method and architecture*, not real logistics operations.
- A2. Stakeholder concerns are initially elicited from literature and role-based reasoning, not from interviews (no real stakeholder study yet).
- A3. Risk levels (LOW/MEDIUM/HIGH/CRITICAL) are a modelling choice, not a legal classification.

**Cross-cutting limitation.** Because data are synthetic and stakeholders are role-modelled, no conclusion may be generalised to real logistics organisations without further validation.

---

## RQ1 (Primary)

> How can stakeholder trust concerns in LLM-enabled logistics systems be systematically translated into requirements, AI mechanisms and architectural decisions?

### Motivation
Trust in LLM-enabled systems is often addressed ad hoc (add a disclaimer, add a filter). Concerns from different stakeholders get lost between elicitation and implementation, leaving mechanisms that nobody can justify against a concern. A systematic translation makes design decisions defensible and auditable.

### Scope
In scope: a repeatable method that maps concerns → requirements → mechanisms → decisions for this one domain. Out of scope: proving the method is optimal, or that it generalises to other domains.

### Sub-questions
- RQ1.1 Which trust concerns can be derived per stakeholder role, and how are they classified into the eight trustworthiness attributes?
- RQ1.2 Can each concern be expressed as a requirement with a verification method and metric (i.e. is it operationalisable)?
- RQ1.3 How many requirements map to a concrete AI/ML mechanism versus a non-AI architectural measure (e.g. audit log, access control)?
- RQ1.4 Is the translation reproducible, i.e. would two independent analysts produce substantially the same mapping?

### How it will be investigated
Structured artefact construction (requirements, taxonomy, ADRs) following the trace chain; completeness and consistency checks on the artefacts; inter-rater comparison of a sample mapping (if a second analyst is available — otherwise reported as a limitation).

### Twelve-point scientific working rule
1. **What:** a concern-to-decision translation method and its artefacts.
2. **Why:** make trust design decisions justified rather than ad hoc.
3. **RQ:** RQ1 (primary).
4. **Trust requirement:** all eight attributes (coverage question).
5. **Why appropriate:** design-science style artefact construction suits a "how can" question.
6. **Simpler baseline:** informal checklist of trust features with no explicit mapping.
7. **Alternatives:** goal modelling (e.g. i*/KAOS), quality-attribute scenarios, assurance cases, STRIDE/privacy threat modelling.
8. **Assumptions:** A1–A3; the taxonomy is sufficiently complete.
9. **Failure modes:** concerns invented rather than elicited; mapping is subjective; requirements untestable.
10. **Evaluation:** requirement coverage (share of concerns with ≥1 requirement, share of requirements with verification method and metric), mapping agreement.
11. **Trade-off:** explicit traceability costs documentation effort and can create false assurance that "mapped = satisfied".
12. **Can conclude:** whether the method yields complete, consistent, verifiable mappings in this scenario. **Cannot conclude:** that the resulting system is trustworthy or that the method suits other domains.

---

## RQ2

> How do classical ML, transformer-based NLP and LLM-based approaches differ in reliability, complexity and transparency?

### Motivation
Method choice is often driven by fashion. For incident-risk classification and recommendation, a simpler model may be sufficient and more transparent.

### Scope
Comparison on tasks defined in later phases: incident-risk classification (LOW/MEDIUM/HIGH/CRITICAL), evidence retrieval, recommendation generation and claim verification. Models are deliberately small and open; no claim is made about frontier LLMs.

### Sub-questions
- RQ2.1 Reliability: predictive quality (macro-F1, per-class recall for HIGH/CRITICAL), stability across seeds and robustness to paraphrase.
- RQ2.2 Complexity: training/inference cost, memory, dependencies, operational effort.
- RQ2.3 Transparency: can the model's behaviour be inspected (feature weights vs. attention vs. none)?
- RQ2.4 Is the accuracy gain, if any, of the more complex approach justified by its cost and opacity?

### How it will be investigated
Controlled comparison (experiments E1, E3) on identical splits and seeds: dummy baseline → TF-IDF + LogisticRegression / LinearSVC → small transformer encoder → mock/optional LLM provider.

### Twelve-point rule
1. **What:** a comparison across three model families.
2. **Why:** justify (or reject) added complexity.
3. **RQ:** RQ2.
4. **Trust requirement:** reliability, transparency, explainability.
5. **Why appropriate:** same data/metrics make differences attributable to the method.
6. **Baseline:** majority-class DummyClassifier; TF-IDF + LinearSVC.
7. **Alternatives:** tree ensembles, other encoders, zero-shot LLM classification.
8. **Assumptions:** synthetic text is a usable proxy for method comparison; hyperparameter tuning effort is comparable across models.
9. **Failure modes:** synthetic data are lexically easy so all models saturate; unfair tuning; data leakage.
10. **Evaluation:** metrics above, plus latency and memory.
11. **Trade-off:** accuracy/semantic robustness vs. cost and interpretability.
12. **Can conclude:** relative behaviour on this synthetic task. **Cannot conclude:** absolute performance in real operations, or general superiority of any family.

---

## RQ3

> Which trustworthiness requirements create conflicting architectural drivers?

### Motivation
Trust attributes pull against each other (e.g. explainability vs. latency; traceability/audit vs. privacy; human oversight vs. throughput). Making conflicts explicit allows deliberate, documented trade-offs.

### Scope
Pairwise analysis among the requirements and drivers in `requirements/` (future phase) and the resulting ADRs. Not an exhaustive formal conflict analysis.

### Sub-questions
- RQ3.1 Which requirement pairs conflict, and on which architectural dimension (latency, cost, data retention, coupling, complexity)?
- RQ3.2 Are conflicts resolvable by design (e.g. tiering by risk level) or only by prioritisation?
- RQ3.3 Can any conflicts be quantified experimentally (e.g. latency cost of verification, privacy filter vs. recall)?

### How it will be investigated
Conflict matrix over trust attributes/requirements, grounded in ADR "negative consequences"; quantification where experiments E4–E6 provide measurements.

### Twelve-point rule
1. **What:** a conflict analysis of architecture drivers.
2. **Why:** trade-offs should be explicit and defensible.
3. **RQ:** RQ3.
4. **Trust requirement:** all, especially privacy, traceability, human oversight, explainability.
5. **Why appropriate:** ATAM-style trade-off analysis is established for architecture.
6. **Baseline:** assume no conflicts (implement every requirement independently).
7. **Alternatives:** formal goal-conflict analysis, stakeholder voting/prioritisation.
8. **Assumptions:** requirements are stated precisely enough to compare.
9. **Failure modes:** conflicts missed or exaggerated; analyst bias.
10. **Evaluation:** conflict matrix reviewed against ADRs; measured costs where available.
11. **Trade-off:** tiered designs reduce conflict but add policy complexity.
12. **Can conclude:** which conflicts appear in this design and scenario. **Cannot conclude:** the list is complete.

---

## RQ4

> How does risk-based human oversight affect automation and system latency?

### Motivation
Oversight is a core trust mechanism, but if every item needs approval, the system's value disappears; if too few do, high-risk errors pass unchecked.

### Scope
Configurable policy per risk level (LOW: recommendation permitted; MEDIUM: recommendation with warning; HIGH: human approval required; CRITICAL: automatic execution prohibited). Latency is *simulated or measured processing latency* plus modelled human-approval delay; real human behaviour is out of scope.

### Sub-questions
- RQ4.1 How do automation rate and escalation rate change under different policies/thresholds?
- RQ4.2 How many HIGH/CRITICAL incidents are mis-routed to a lower tier (high-risk false negatives) under each policy?
- RQ4.3 What is the latency overhead of oversight, using explicit assumptions for approval delay?

### How it will be investigated
Experiment E5: full automation vs. risk-based oversight over the same incident stream; sensitivity analysis over assumed approval delays and classifier error rates.

### Twelve-point rule
1. **What:** a configurable risk-tiered oversight policy.
2. **Why:** balance safety against workload.
3. **RQ:** RQ4.
4. **Trust requirement:** human oversight, accountability, reliability.
5. **Why appropriate:** the policy is simple, inspectable and measurable.
6. **Baseline:** full automation of recommendations; and "approve everything".
7. **Alternatives:** uncertainty-based escalation, sampling audits, confidence thresholds.
8. **Assumptions:** upstream risk label is available; approval delay is a modelled parameter.
9. **Failure modes:** misclassified risk bypasses oversight; approver fatigue and automation bias are not captured.
10. **Evaluation:** automation rate, escalation rate, high-risk false negatives, latency.
11. **Trade-off:** safety vs. throughput; oversight is only as good as the risk estimate that triggers it.
12. **Can conclude:** system-level trade-offs under stated assumptions. **Cannot conclude:** anything about real human reviewer performance.

---

## RQ5

> Can traceability be maintained from stakeholder concerns through requirements, architecture, implementation and evaluation?

### Motivation
Traceability is claimed frequently but degrades as artefacts evolve. If a concern cannot be followed to a test and metric, its satisfaction cannot be argued.

### Scope
Chain: Stakeholder → Trust Concern → Requirement → Quality Attribute → Architecture Driver → AI/ML Mechanism → Architecture Decision → Component → Test → Metric, for this repository only.

### Sub-questions
- RQ5.1 What share of requirements have complete forward links to a test and metric?
- RQ5.2 What share of components/tests/metrics link back to a requirement (no orphans)?
- RQ5.3 Can link integrity be checked automatically (e.g. in CI) as artefacts change?
- RQ5.4 What effort does maintaining the trace chain add?

### How it will be investigated
Machine-readable artefacts (YAML/CSV) with automated consistency checks in later phases; manual review for semantic correctness of links.

### Twelve-point rule
1. **What:** a verifiable trace chain.
2. **Why:** support auditability and accountability claims.
3. **RQ:** RQ5.
4. **Trust requirement:** traceability, accountability, transparency.
5. **Why appropriate:** structural link checks are cheap and objective.
6. **Baseline:** prose documentation with no explicit links.
7. **Alternatives:** requirements-management tools, model-based engineering, issue-tracker links.
8. **Assumptions:** artefacts remain in-repo and machine-readable.
9. **Failure modes:** links exist but are semantically wrong; link rot; effort too high.
10. **Evaluation:** coverage, orphan counts, automated link-check pass/fail.
11. **Trade-off:** rigor vs. maintenance burden.
12. **Can conclude:** structural completeness of links. **Cannot conclude:** that linked requirements are correctly implemented or sufficient.

---

## Relationship between questions

RQ1 is the umbrella. RQ2 supplies evidence on mechanism choice, RQ3 on conflicts among drivers, RQ4 on one concrete mechanism (oversight) and RQ5 on whether the whole chain remains verifiable. Hypotheses are in `research/hypotheses.md`.
