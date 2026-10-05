# Threats to validity

## Construct validity

Risk tiers and role concerns are analyst-defined constructs. Macro-F1,
retrieval scores, latency, and redaction metrics measure narrow observable
behaviors; none is equivalent to trust, safety, privacy compliance, or
accountability.

## Internal validity

Synthetic templates intentionally associate words and risk labels, creating
lexical leakage. Small runs, hyperparameter choices, split variance, and
optional model initialization can confound comparisons. Fix seeds/splits and
record versions and hardware; inspect HIGH/CRITICAL false negatives.

## External validity

No real incidents, operational prevalence, languages, regulations, provider
outputs, or human-review times are represented. Generalisation to logistics
organizations or other domains is unsupported.

## Conclusion validity

Small synthetic samples have limited power. Avoid treating a single seed or
point estimate as a stable difference. Use repeated runs, report spread and
confusion patterns, and predeclare comparison procedures before inference.

## Mitigations and residual gaps

Reproducible generation and explicit metric definitions reduce some
ambiguity. They do not address missing stakeholder validation, scenario
coverage, synthetic distribution shift, or model calibration. These remain
limitations rather than solved threats.
