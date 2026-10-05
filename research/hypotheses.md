# Hypotheses (Phase 1)

> Status: **pre-registered expectations, not results.** No experiment has been run. Directions are conservative expectations based on general literature and reasoning, and are explicitly allowed to be refuted. Metric values/thresholds are deliberately left to be fixed in `research/experimental_design.md` *before* running experiments.

## How to read this document

Each hypothesis states: statement, expected direction, supporting evidence, refuting evidence, metrics/artefacts, and the planned experiment. Hypotheses are falsifiable because each names a measurable comparison and the outcome that would contradict it. Conventions:
- "Held-out" = test split unseen during training/tuning, fixed by a deterministic seed.
- Comparisons use multiple seeds and report spread; "differs" requires the difference to exceed seed-to-seed variation (exact statistical procedure to be set in the experimental design).
- All data are synthetic initially; all hypotheses concern the *method on synthetic data*.
- The system assists humans; no hypothesis concerns autonomous decision making.

---

## RQ1 – Translation of concerns

### H1.1 Operationalisability
- **Statement:** Every trust concern in the taxonomy can be expressed as at least one requirement that has a verification method and an evaluation metric.
- **Direction:** Majority operationalisable; some (e.g. "accountability") only partially.
- **Supports:** ≥ a pre-set share of requirements carry both a verification method and a metric; remaining ones are documented with reason.
- **Refutes:** a substantial share of concerns can only be stated as non-verifiable prose.
- **Metrics/artefacts:** `requirements/trust_requirements.yaml` field completeness; proportion with verification_method and evaluation_metric.
- **Experiment/analysis:** requirement completeness check.

### H1.2 Mechanism coverage
- **Statement:** Not all trust requirements are satisfied by AI mechanisms; a non-trivial share requires conventional architectural measures (audit log, access control, policy engine).
- **Direction:** Mixed (AI and non-AI) mapping.
- **Supports:** requirements map to both categories in the traceability matrix.
- **Refutes:** nearly all requirements map to a single mechanism type.
- **Metrics/artefacts:** `requirements/traceability_matrix.csv`; ADR set.

### H1.3 Mapping reproducibility
- **Statement:** Two independent analysts, given the same concerns and taxonomy, produce substantially agreeing concern→attribute and requirement→driver mappings.
- **Direction:** Moderate-to-high agreement for attributes, lower for drivers.
- **Supports:** agreement (e.g. Cohen's kappa) above a threshold fixed in advance.
- **Refutes:** agreement near chance.
- **Metrics/artefacts:** kappa on a sampled mapping. *Requires a second analyst; otherwise reported as untested.*

---

## RQ2 – Classical ML vs. transformers vs. LLM

### H2.1 Classical baseline is competitive
- **Statement:** TF-IDF + LinearSVC achieves macro-F1 within a small margin of a small fine-tuned transformer encoder on lexically regular synthetic incident text.
- **Direction:** Small or no gap (risk: synthetic data saturation).
- **Supports:** gap below a pre-set margin, within seed variance.
- **Refutes:** transformer exceeds baseline by more than the margin consistently across seeds.
- **Metrics:** macro-F1, per-class recall (HIGH, CRITICAL), accuracy, confusion matrix.
- **Experiment:** E1.

### H2.2 Transformer robustness to paraphrase
- **Statement:** On held-out paraphrased incidents that share little vocabulary with training text, the transformer degrades less than TF-IDF models.
- **Direction:** Transformer advantage grows with lexical shift.
- **Supports:** smaller macro-F1 drop for the transformer on the paraphrase subset.
- **Refutes:** equal or larger drop.
- **Metrics:** macro-F1 delta between standard and paraphrase test sets. *Requires a paraphrase set to be constructed and labelled as such.*
- **Experiment:** E1.

### H2.3 Cost of complexity
- **Statement:** The transformer has materially higher inference latency, memory footprint and training cost than TF-IDF + LinearSVC.
- **Direction:** Higher by at least an order of magnitude on CPU for latency.
- **Supports:** measured values on the same hardware.
- **Refutes:** comparable resource use.
- **Metrics:** ms/incident (median, p95), peak memory, training wall-time, parameter count.
- **Experiment:** E1.

### H2.4 Transparency gap
- **Statement:** Linear TF-IDF models offer more directly inspectable explanations (top weighted terms) than the transformer or an LLM; whether such explanations are *faithful* is separate.
- **Direction:** Linear > transformer ≥ LLM in inspectability.
- **Supports:** higher rubric rating for the linear model, and removing its top-weighted terms changes its prediction more than removing random terms.
- **Refutes:** the linear model's top terms are no more influential than random terms (explanations unfaithful), or the rubric rates the transformer/LLM equal or higher.
- **Metrics/artefacts:** explanation rubric; deletion test effect size.

### H2.5 LLM alone is less grounded than RAG
- **Statement:** A mock/optional LLM recommendation without retrieved evidence contains a larger share of unsupported claims than the same recommendation with retrieved evidence.
- **Direction:** Unsupported-claim rate lower with RAG.
- **Supports:** lower unsupported-claim rate with RAG on identical questions.
- **Refutes:** no difference or higher rate.
- **Metrics:** unsupported-claim rate, citation validity, INSUFFICIENT_EVIDENCE rate.
- **Experiment:** E3. **Caveat:** the default `MockLLMProvider` is deterministic and not representative of real LLM behaviour; this hypothesis can only be tested meaningfully with an optional real provider, otherwise it tests the pipeline mechanics only.

---

## RQ3 – Conflicting drivers

### H3.1 Verification adds latency
- **Statement:** Adding claim verification (E4) increases end-to-end processing latency relative to RAG alone.
- **Direction:** Latency increases.
- **Supports:** measured latency increase beyond measurement noise.
- **Refutes:** no measurable increase.
- **Metrics:** end-to-end latency (median, p95), per-stage latency.
- **Experiment:** E4.

### H3.2 Privacy filtering trades off against utility
- **Statement:** Enabling PII redaction reduces PII leakage but may reduce downstream classification or retrieval quality through over-redaction.
- **Direction:** Leakage ↓, utility slightly ↓ or unchanged.
- **Supports:** lower leakage rate with a measurable (possibly small) utility change.
- **Refutes:** leakage unchanged, or utility drop negligible and leakage not reduced (the trade-off does not materialise).
- **Metrics:** PII precision/recall, leakage rate, false positives, macro-F1 and retrieval metrics with/without filtering.
- **Experiment:** E6. **Note:** synthetic PII only.

### H3.3 Auditability vs. data minimisation
- **Statement:** Full audit logging (traceability, accountability) conflicts with data minimisation (privacy) unless logs store redacted or referenced content.
- **Direction:** Conflict present; resolvable through redaction/reference design.
- **Supports:** conflict-matrix entry confirmed by ADR analysis and by inspecting log contents for PII in later phases.
- **Refutes:** a design with full logging and no residual PII exposure is trivially achievable without any trade-off.
- **Artefacts:** conflict matrix; ADR-006 and ADR-007; audit-log leakage check.

---

## RQ4 – Risk-based oversight

### H4.1 Automation reduction
- **Statement:** Risk-based oversight lowers the automation rate compared with full automation, by an amount that depends on the share of HIGH/CRITICAL incidents.
- **Direction:** Automation ↓; escalation ↑.
- **Supports:** measured automation/escalation rates differ as predicted by class mix.
- **Refutes:** automation rate unchanged.
- **Metrics:** automation rate, escalation rate.
- **Experiment:** E5.

### H4.2 Latency cost is dominated by approval delay
- **Statement:** Under risk-based oversight, mean end-to-end latency is dominated by the assumed human approval delay, not by model compute.
- **Direction:** Approval delay ≫ compute time.
- **Supports:** sensitivity analysis shows latency tracks approval delay.
- **Refutes:** compute stages dominate.
- **Metrics:** latency decomposition per stage. **Caveat:** approval delay is an assumed parameter; this hypothesis is about structure of cost, not real approver speed.
- **Experiment:** E5.

### H4.3 Oversight is bounded by risk-estimator quality
- **Statement:** The number of HIGH/CRITICAL incidents that bypass oversight (high-risk false negatives) is determined by the upstream classifier's recall on those classes; oversight does not remove this risk.
- **Direction:** Residual bypass rate ≈ classifier miss rate on HIGH/CRITICAL.
- **Supports:** high-risk false negatives under policy match classifier misses; lowering thresholds for escalation reduces them at the cost of automation.
- **Refutes:** bypass rate substantially differs from classifier misses without an explanation in the design.
- **Metrics:** high-risk false negatives, recall for HIGH/CRITICAL, escalation rate.
- **Experiment:** E5 (with E1 outputs).

---

## RQ5 – Traceability

### H5.1 Forward completeness
- **Statement:** Every requirement can be linked forward to at least one component, test and metric.
- **Direction:** Achievable for the full requirement set at the end of the project; gaps visible earlier.
- **Supports:** link-check reports 100% forward links, or lists explained exceptions.
- **Refutes:** persistent requirements with no feasible test or metric.
- **Metrics/artefacts:** coverage percentage from traceability matrix check.

### H5.2 Backward completeness (no orphans)
- **Statement:** Every component, test and metric links back to at least one requirement.
- **Direction:** Few orphans; those remaining indicate scope creep or missing requirements.
- **Supports:** orphan count ≈ 0 or justified.
- **Refutes:** many unexplained orphans.
- **Metrics/artefacts:** orphan count.

### H5.3 Automated checking prevents drift
- **Statement:** An automated link-integrity check detects broken links introduced by artefact changes.
- **Direction:** Detects injected breakages.
- **Supports:** deliberately injected broken links are all flagged (mutation-style test).
- **Refutes:** injected breaks go undetected.
- **Metrics:** detection rate of injected faults. **Limitation:** detects structural, not semantic, errors.

---

## Summary table

| ID | RQ | Direction | Experiment / analysis | Status |
|---|---|---|---|---|
| H1.1 | RQ1 | most operationalisable | requirements completeness | untested |
| H1.2 | RQ1 | mixed AI/non-AI | traceability matrix | untested |
| H1.3 | RQ1 | moderate-high agreement | second-analyst mapping | untested |
| H2.1 | RQ2 | small gap | E1 | untested |
| H2.2 | RQ2 | transformer more robust | E1 | untested |
| H2.3 | RQ2 | transformer costlier | E1 | untested |
| H2.4 | RQ2 | linear most inspectable | rubric + deletion test | untested |
| H2.5 | RQ2 | RAG more grounded | E3 | untested |
| H3.1 | RQ3 | latency ↑ | E4 | untested |
| H3.2 | RQ3 | leakage ↓, utility ↓/= | E6 | untested |
| H3.3 | RQ3 | conflict exists | ADR/conflict matrix | untested |
| H4.1 | RQ4 | automation ↓ | E5 | untested |
| H4.2 | RQ4 | approval delay dominates | E5 | untested |
| H4.3 | RQ4 | bounded by classifier recall | E5 | untested |
| H5.1 | RQ5 | complete forward links | link check | untested |
| H5.2 | RQ5 | few orphans | link check | untested |
| H5.3 | RQ5 | detects drift | mutation test | untested |

## What these hypotheses cannot show
Confirmation on synthetic data does not demonstrate real-world trustworthiness. Refutation is informative and will be reported, not hidden.
