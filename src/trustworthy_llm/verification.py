"""Conservative lexical claim/evidence verifier and uncertainty signals."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class VerificationLabel(str, Enum):
    SUPPORTED = "SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    UNKNOWN = "UNKNOWN"


_NEGATIONS = {"not", "no", "never", "without", "isn't", "wasn't", "cannot"}
_STOP = {"the", "a", "an", "is", "are", "was", "were", "to", "of", "and", "in", "on"}


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower())) - _STOP


def verify_claim(claim: str, evidence: list[str], threshold: float = 0.7) -> VerificationLabel:
    """Token-overlap baseline; a predictive heuristic, not factual proof."""
    claim_tokens = _tokens(claim)
    if not claim_tokens or not evidence:
        return VerificationLabel.UNKNOWN
    claim_negated = bool(claim_tokens & _NEGATIONS)
    relationships = set()
    for statement in evidence:
        tokens = _tokens(statement)
        overlap = claim_tokens & tokens
        denominator = max(1, len(claim_tokens - _NEGATIONS))
        similarity = len(overlap - _NEGATIONS) / denominator
        if similarity >= threshold:
            relationships.add(
                VerificationLabel.CONTRADICTED
                if bool(tokens & _NEGATIONS) != claim_negated
                else VerificationLabel.SUPPORTED
            )
    if relationships == {VerificationLabel.SUPPORTED, VerificationLabel.CONTRADICTED}:
        return VerificationLabel.UNKNOWN
    if relationships:
        return next(iter(relationships))
    return VerificationLabel.UNKNOWN


@dataclass(frozen=True)
class UncertaintySignals:
    classifier_probability: float | None = None
    decision_margin: float | None = None
    retrieval_similarity: float | None = None
    evidence_coverage: float | None = None
    model_disagreement: bool = False
    verifier_label: VerificationLabel = VerificationLabel.UNKNOWN
