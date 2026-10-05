"""Classical TF-IDF incident-risk baselines."""

from __future__ import annotations

from typing import Iterable

from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from trustworthy_llm.domain import Incident, RiskLevel
from trustworthy_llm.preprocessing import preprocess_classical

LABELS = [risk.value for risk in RiskLevel]


def _classifier(name: str, seed: int):
    if name == "dummy":
        return DummyClassifier(strategy="most_frequent", random_state=seed)
    if name == "logistic_regression":
        return LogisticRegression(max_iter=1000, class_weight="balanced", random_state=seed)
    if name == "linear_svc":
        return LinearSVC(class_weight="balanced", random_state=seed)
    raise ValueError(f"unknown classifier: {name}")


def build_classifier(name: str = "linear_svc", seed: int = 42) -> Pipeline:
    """Build a word unigram/bigram TF-IDF pipeline without transformer preprocessing."""
    return Pipeline(
        [
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ("classifier", _classifier(name, seed)),
        ]
    )


def fit_classifier(incidents: Iterable[Incident], name: str = "linear_svc", seed: int = 42):
    items = list(incidents)
    if not items:
        raise ValueError("training data must not be empty")
    model = build_classifier(name=name, seed=seed)
    model.fit(
        [preprocess_classical(item.description) for item in items],
        [item.risk_level.value for item in items],
    )
    return model


def evaluate_classifier(model, incidents: Iterable[Incident]) -> dict:
    items = list(incidents)
    if not items:
        raise ValueError("evaluation data must not be empty")
    actual = [item.risk_level.value for item in items]
    predicted = model.predict([preprocess_classical(item.description) for item in items])
    precision, recall, f1, support = precision_recall_fscore_support(
        actual, predicted, labels=LABELS, zero_division=0
    )
    return {
        "accuracy": float(accuracy_score(actual, predicted)),
        "macro_precision": float(precision.mean()),
        "macro_recall": float(recall.mean()),
        "macro_f1": float(f1.mean()),
        "per_class": {
            label: {
                "precision": float(precision[i]),
                "recall": float(recall[i]),
                "f1": float(f1[i]),
                "support": int(support[i]),
            }
            for i, label in enumerate(LABELS)
        },
        "confusion_matrix": confusion_matrix(actual, predicted, labels=LABELS).tolist(),
        "high_risk_false_negatives": int(
            sum(
                (truth == "HIGH" and guess != "HIGH")
                or (truth == "CRITICAL" and guess != "CRITICAL")
                for truth, guess in zip(actual, predicted)
            )
        ),
        "high_risk_escalation_bypasses": int(
            sum(
                truth in ("HIGH", "CRITICAL") and guess not in ("HIGH", "CRITICAL")
                for truth, guess in zip(actual, predicted)
            )
        ),
    }
