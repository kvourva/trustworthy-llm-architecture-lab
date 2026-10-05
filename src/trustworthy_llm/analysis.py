"""Cautious error-analysis helpers for labelled experiment outputs."""

from __future__ import annotations

import random

from sklearn.metrics import accuracy_score, f1_score

from trustworthy_llm.ml import LABELS


def high_risk_false_negatives(incident_ids: list[str], actual: list[str], predicted: list[str]) -> list[dict]:
    if not (len(incident_ids) == len(actual) == len(predicted)):
        raise ValueError("IDs, actual labels, and predictions must have equal length")
    return [
        {"incident_id": identifier, "actual": truth, "predicted": guess}
        for identifier, truth, guess in zip(incident_ids, actual, predicted)
        if (truth == "HIGH" and guess != "HIGH")
        or (truth == "CRITICAL" and guess != "CRITICAL")
    ]


def disagreement_ids(
    incident_ids: list[str], first_predictions: list[str], second_predictions: list[str]
) -> list[str]:
    if not (len(incident_ids) == len(first_predictions) == len(second_predictions)):
        raise ValueError("IDs and prediction lists must have equal length")
    return [
        identifier
        for identifier, first, second in zip(incident_ids, first_predictions, second_predictions)
        if first != second
    ]


def bootstrap_metric_difference(
    actual: list[str],
    first_predictions: list[str],
    second_predictions: list[str],
    metric: str = "macro_f1",
    resamples: int = 1000,
    seed: int = 42,
) -> dict:
    """Paired percentile interval; descriptive only, not a significance test."""
    if not actual or not (len(actual) == len(first_predictions) == len(second_predictions)):
        raise ValueError("non-empty aligned labels and predictions are required")
    if resamples < 1:
        raise ValueError("resamples must be positive")
    if metric not in {"accuracy", "macro_f1"}:
        raise ValueError("metric must be accuracy or macro_f1")

    def score(truth, predictions):
        if metric == "accuracy":
            return accuracy_score(truth, predictions)
        return f1_score(truth, predictions, labels=LABELS, average="macro", zero_division=0)

    rng = random.Random(seed)
    size = len(actual)
    differences = []
    for _ in range(resamples):
        indices = [rng.randrange(size) for _ in range(size)]
        truth = [actual[index] for index in indices]
        first = [first_predictions[index] for index in indices]
        second = [second_predictions[index] for index in indices]
        differences.append(float(score(truth, second) - score(truth, first)))
    differences.sort()
    return {
        "metric": metric,
        "difference_second_minus_first": float(score(actual, second_predictions) - score(actual, first_predictions)),
        "percentile_interval_95": [
            differences[int(0.025 * (resamples - 1))],
            differences[int(0.975 * (resamples - 1))],
        ],
        "resamples": resamples,
        "seed": seed,
        "interpretation": "Descriptive paired bootstrap interval; not a p-value or proof of general superiority.",
    }
