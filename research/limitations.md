# Limitations

- Incident records and evidence fixtures are entirely synthetic and
  non-representative; their templates can make classification artificially
  easy.
- Stakeholder profiles are hypotheses, not empirical elicitation.
- The TF-IDF verifier is lexical, not semantic entailment. NLI is not included.
- Dense retrieval and transformer classification require optional dependencies
  and externally available weights; no results are claimed for them.
- MockLLMProvider does not model real LLM behavior, hallucination, calibration,
  safety, or latency.
- Oversight timing is an explicit assumption; the scaffold does not include
  real reviewers, fatigue, automation bias, or organizational workflow.
- Regex PII handling is a synthetic experiment, not a detector validated on
  real personal data.
- Audit and decision storage are prototypes; persistence, access control,
  retention, integrity, and availability controls are not production-ready.
- No operational, legal, safety, or security certification follows from passing
  this repository's tests.
