# Learning Note – Phase 1: Research Questions and Hypotheses

## What was built
Documentation only: `research/research_questions.md`, `research/hypotheses.md`, this note, and a short README status section. A small structural test checks the Phase 1 documents exist and keep their required sections. No dataset, model, retrieval, RAG, verification, oversight or experiment code exists.

## Why
Research software needs falsifiable questions fixed *before* implementation; otherwise metrics and experiments get chosen after seeing results. Writing hypotheses first (pre-registration in spirit) limits post-hoc rationalisation.

## How the research questions are structured
- **RQ1** (primary) is a method question: how concerns become requirements, mechanisms and decisions.
- **RQ2–RQ5** each probe one aspect: mechanism comparison, conflicting drivers, oversight cost, traceability integrity.
- Each RQ lists motivation, scope, sub-questions, investigation approach and the 12-point scientific working rule (what, why, RQ, trust requirement, appropriateness, baseline, alternatives, assumptions, failure modes, evaluation, trade-off, conclusions that can/cannot be drawn).

## Why the hypotheses are testable
Each names (a) a comparison, (b) an expected direction, (c) evidence that would support and refute it, and (d) metrics/artefacts and an experiment (E1–E6) or analysis. Thresholds are deliberately deferred to the experimental design, to be fixed before running. Hypotheses that depend on resources not yet available (second analyst, real LLM provider, paraphrase set) say so explicitly.

## Assumptions and limitations
- Synthetic data only; no claim about real logistics operations.
- Stakeholder concerns are role-modelled, not elicited by interview.
- Risk classes are a modelling choice, not a legal classification.
- Approval delays in oversight experiments are assumed parameters.
- The default mock LLM is not representative of real LLMs.
- Directions are expectations, not findings. No results exist.

## Trustworthiness implications
Explicit hypotheses and stated refutation criteria support transparency and accountability of the research itself. The system is framed as human-assisting: oversight hypotheses (H4.x) address that accountability stays with people, and that oversight is only as strong as the risk estimate that triggers it.

## How to explain this in a PhD interview
- "I separated a design-science question (RQ1) from four empirical/analytic questions, so each claim has its own evidence type."
- "Every hypothesis can fail: I wrote down what would refute it, and I expect some to fail, e.g. the classical baseline may be competitive (H2.1)."
- "I do not claim trustworthiness from passing tests; traceability shows *structure*, not correctness (H5.x limitation)."
- "Synthetic data lets me test mechanisms and trade-offs, not real-world performance; I state this as a limit rather than hiding it."
- Likely challenges: *Why these metrics?* (they map to stated requirements); *Why not simply use an LLM?* (RQ2 baseline comparison); *How is this not circular?* (hypotheses precede implementation, thresholds fixed before running).
