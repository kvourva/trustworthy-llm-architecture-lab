# Synthetic dataset

The generator creates labelled logistics incident descriptions from a fixed
template vocabulary. IDs and output ordering are deterministic for a given
seed. The default 200-row dataset is near-balanced across risk labels; counts
that are not divisible by four differ by at most one. This dataset is wholly
synthetic, not representative of real operations, and contains no real
personal data.

## Generate

```sh
pip install -e .
trustworthy-llm-generate-data --count 200 --seed 42
# or: python -m trustworthy_llm.generate --count 200 --seed 42
```

Schema: `incident_id` (stable synthetic ID), `category` (one of nine incident
categories), `description` (synthetic scenario text), `risk_level` (LOW,
MEDIUM, HIGH, CRITICAL), and `synthetic` (always true). The scenario templates
are illustrative labels; they do not encode an empirically validated risk
policy.

The controlled vocabulary makes tests reproducible but risks lexical leakage
and overly easy classification. There is no operational volume, temporal
structure, class prevalence, causal relation, or stakeholder validation. Do
not train or evaluate a deployed system from these records. For retrieval
experiments, create synthetic `Evidence` fixtures and label relevance
explicitly; source IDs are retained in every retrieval result.
