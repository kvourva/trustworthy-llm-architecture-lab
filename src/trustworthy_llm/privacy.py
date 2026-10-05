"""Synthetic-only PII redaction experiment helpers."""

import re
from dataclasses import dataclass

_PATTERNS = {
    "EMAIL": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "PHONE": re.compile(r"(?<!\w)(?:\+?\d[\d(). -]{7,}\d)(?!\w)"),
}


@dataclass(frozen=True)
class RedactionResult:
    text: str
    detected: int


def redact_synthetic_pii(text: str) -> RedactionResult:
    redacted = text
    detected = 0
    for kind, pattern in _PATTERNS.items():
        redacted, count = pattern.subn(f"[REDACTED_{kind}]", redacted)
        detected += count
    return RedactionResult(redacted, detected)


def pii_metrics(true_positive: int, false_positive: int, false_negative: int, leaked: int, total_records: int) -> dict:
    precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
    recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
    return {
        "precision": precision,
        "recall": recall,
        "false_positives": false_positive,
        "leakage_rate": leaked / total_records if total_records else 0.0,
    }
