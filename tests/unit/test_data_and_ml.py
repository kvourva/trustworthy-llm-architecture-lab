from trustworthy_llm.data import generate_incidents
from trustworthy_llm.domain import RiskLevel
from trustworthy_llm.ml import evaluate_classifier, fit_classifier
from trustworthy_llm.preprocessing import preprocess_classical


def test_synthetic_generation_is_reproducible_and_covers_risks():
    first = generate_incidents(40, seed=17)
    second = generate_incidents(40, seed=17)
    assert first == second
    assert {item.risk_level for item in first} == set(RiskLevel)
    assert all(item.synthetic for item in first)


def test_classical_preprocessing_preserves_negation():
    assert preprocess_classical("  Shipment is NOT delayed \n ") == "shipment is not delayed"


def test_baseline_inference_reports_class_sensitive_metrics():
    train = generate_incidents(80, seed=4)
    model = fit_classifier(train, "linear_svc", seed=4)
    metrics = evaluate_classifier(model, train[:16])
    assert 0 <= metrics["macro_f1"] <= 1
    assert set(metrics["per_class"]) == {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
    assert len(metrics["confusion_matrix"]) == 4
    assert "high_risk_false_negatives" in metrics
