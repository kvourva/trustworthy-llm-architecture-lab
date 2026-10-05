# Trustworthy LLM Architecture Lab

## Abstract

An independently installable research repository for tracing trust concerns
through requirements, AI mechanisms, architecture, tests, and evaluation in an
AI-assisted logistics incident-management scenario. It includes deterministic
synthetic data, classical NLP/ML baselines, retrieval, a provider-neutral RAG
prototype, claim-verification heuristics, risk-tiered oversight, privacy
experiments, and research artefacts. The system assists human staff; it is not
an autonomous logistics decision maker.

## Motivation

Trust features should be justified by stakeholder concerns and evaluated
through explicit links rather than added as disconnected checkboxes. The
repository studies a conservative, testable path from concerns to architecture
and makes the costs and limits visible.

## Research Questions

RQ1 asks how concerns translate into requirements and decisions. RQ2 compares
classical ML, transformers, and LLM-based approaches for reliability,
complexity, and transparency. RQ3 studies conflicting drivers; RQ4 investigates
risk-tiered oversight and latency; RQ5 examines traceability. See
[`research/research_questions.md`](research/research_questions.md) and
[`research/hypotheses.md`](research/hypotheses.md).

## Domain

The scenario covers delays, supplier disruption, customs, route changes,
damage, dangerous goods, warehouse events, customer-data incidents, and
regulatory questions. Output is advisory; humans remain responsible for
consequential decisions.

## Stakeholders

Role profiles and hypothesised concerns are in
[`requirements/stakeholders.md`](requirements/stakeholders.md). They are not
validated interview findings.

## Trustworthiness Requirements

Eight attributes are mapped in
[`requirements/trust_taxonomy.md`](requirements/trust_taxonomy.md). Machine
readable requirements and concern-to-metric links are in
`requirements/trust_requirements.yaml` and
`requirements/traceability_matrix.csv`. Structural links do not prove semantic
correctness or requirement satisfaction.

## AI/ML Pipeline

`Incident → privacy filter → risk estimate → retrieval → provider draft →
claim verification → policy routing → audit`. Each stage can fail; missing or
uncertain evidence is not silently treated as fact. The interfaces and views
are described under [`architecture/`](architecture/).

## Classical ML

The `DummyClassifier`, class-weighted LogisticRegression, and LinearSVC models
use word unigram/bigram TF-IDF. Macro-F1 gives each risk class equal weight;
per-class HIGH/CRITICAL recall and false negatives are reported separately.
Conservative normalization is for classical features only; transformer inputs
are not lowercased or stemmed by this pipeline. See ADR-001.

## Transformers

`TransformerRiskClassifier` is isolated and optional. It fine-tunes a small
Hugging Face sequence-classification model, uses local files by default, and
does not enable remote model code. Run it only with compatible PyTorch and
Transformers installed and an explicit download opt-in. No transformer result
is included or claimed. Added dependency risk and training/memory costs are
part of the comparison, not hidden by the baseline.

## Retrieval

Core retrieval is TF-IDF cosine similarity with evidence IDs, source metadata,
and ranking scores. Dense Sentence Transformer retrieval is an optional adapter
and is not a core dependency; model downloads are excluded from routine tests.
Lexical matching can retain exact regulatory terms, while dense matching may
help paraphrases; both need evaluation on labelled queries.

## RAG

`RAGPipeline` preserves retrieved evidence IDs and returns
`INSUFFICIENT_EVIDENCE`, `LLM_FAILURE`, or `REVIEW_REQUIRED` when appropriate.
`LLMProvider` isolates provider calls and `MockLLMProvider` makes offline tests
possible. The mock is a contract test double, not evidence about real LLM
grounding. Citations establish source provenance, not truth.

## Verification

The default verifier is a token-overlap/negation heuristic with
SUPPORTED/CONTRADICTED/UNKNOWN outcomes. It is not semantic proof. An NLI model
could be evaluated as another predictive model but is not included in the core
dependencies.

## Architecture

The design separates API Gateway, Incident Service, ML/Transformer Risk
Services, Retrieval, LLM, Verification, Policy, Privacy, Human Approval, Audit,
and Decision Store responsibilities. This codebase provides small research
primitives rather than a deployed network service or production database.

## Experiments

E1–E6 have parameterized deterministic scaffolding; each output must be
generated explicitly. See [`research/experimental_design.md`](research/experimental_design.md)
and [`experiments/README.md`](experiments/README.md). E1's transformer arm and
E2's dense arm are opt-in and require compatible external model packages and
weights.

## Results

No empirical results are checked in. `results/` is intentionally empty apart
from its usage note. Experiment output is synthetic, generated when run, and
must not be described as real-world evidence.

## Trade-offs

Sparse linear models are inspectable and inexpensive but vocabulary-bound.
Retrieval provenance improves reviewability but does not establish correctness.
Verification adds latency and can be wrong. Redaction can miss or over-redact.
Risk-based oversight raises review load, and a risk-estimator false negative
can still bypass escalation. Auditability competes with data minimisation.

## Threats to Validity

Synthetic data use fixed lexical templates and artificial class balance.
Role-based concerns have not been elicited from people. The mock provider and
heuristic verifier do not represent production LLMs or NLI models. Results are
method demonstrations only. Full discussion: `research/threats_to_validity.md`.

## Limitations

The repository is a reproducible research prototype, not a validated logistics
tool, regulatory interpretation service, security assessment, or operational
PII detector. No real operational data or human approval timings are included.

## Reproducibility

Python 3.12+ is required. Core model dependency is scikit-learn; tests use
pytest. Transformer/dense integrations are isolated optional paths.

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]'
python -m pytest
trustworthy-llm-generate-data --count 200 --seed 42
trustworthy-llm-experiment --experiment E1 --seed 42 --output results/e1-seed-42.json
```

Keep seed, split, optional model identifier, software/hardware environment, and
all generated result files with any reported experiment. Read the learning
notes and ADRs before interpreting outputs.
