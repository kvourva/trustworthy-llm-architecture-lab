import csv
import re
from pathlib import Path

from trustworthy_llm.analysis import (
    bootstrap_metric_difference,
    disagreement_ids,
    high_risk_false_negatives,
)

ROOT = Path(__file__).resolve().parents[2]


def test_error_analysis_finds_severe_misses_and_disagreement():
    ids = ["A", "B", "C"]
    actual = ["LOW", "HIGH", "CRITICAL"]
    first = ["LOW", "MEDIUM", "HIGH"]
    second = ["LOW", "HIGH", "CRITICAL"]
    assert high_risk_false_negatives(ids, actual, first) == [
        {"incident_id": "B", "actual": "HIGH", "predicted": "MEDIUM"},
        {"incident_id": "C", "actual": "CRITICAL", "predicted": "HIGH"},
    ]
    assert disagreement_ids(ids, first, second) == ["B", "C"]


def test_bootstrap_comparison_is_reproducible_and_descriptive():
    actual = ["LOW", "HIGH", "LOW", "CRITICAL"]
    first = ["LOW", "LOW", "LOW", "HIGH"]
    second = ["LOW", "HIGH", "LOW", "CRITICAL"]
    result = bootstrap_metric_difference(actual, first, second, resamples=50, seed=9)
    assert result == bootstrap_metric_difference(actual, first, second, resamples=50, seed=9)
    assert "not a p-value" in result["interpretation"]


def test_traceability_matrix_has_requirement_component_test_and_metric_links():
    with (ROOT / "requirements/traceability_matrix.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    requirements = (ROOT / "requirements/trust_requirements.yaml").read_text(encoding="utf-8")
    assert rows
    for row in rows:
        assert row["requirement"] in requirements
        for field in ("stakeholder", "trust_concern", "architecture_driver", "component", "test", "metric"):
            assert row[field].strip()
    for key in ("id", "stakeholder", "trust_attribute", "description", "rationale", "priority",
                "risk_level", "architecture_driver", "implementation_component",
                "verification_method", "evaluation_metric"):
        assert re.search(rf"^\s+-?\s*{key}:", requirements, re.M)
