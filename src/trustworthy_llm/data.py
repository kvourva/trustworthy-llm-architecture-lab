"""Deterministic synthetic incident generation; generated records are not real data."""

from __future__ import annotations

import random

from trustworthy_llm.domain import Incident, RiskLevel

CATEGORIES = (
    "shipment delay",
    "supplier disruption",
    "customs problem",
    "route change",
    "damaged shipment",
    "dangerous goods",
    "warehouse incident",
    "customer-data incident",
    "regulatory question",
)
RISK_LEVELS = tuple(RiskLevel)

_DESCRIPTORS = {
    RiskLevel.LOW: ("minor", "no service impact", "routine", "resolved locally"),
    RiskLevel.MEDIUM: ("moderate", "delivery may slip", "needs monitoring", "limited disruption"),
    RiskLevel.HIGH: ("urgent", "multiple shipments affected", "significant delay", "escalation requested"),
    RiskLevel.CRITICAL: ("critical", "immediate safety concern", "dangerous goods exposure", "regulatory stop required"),
}


def generate_incidents(count: int = 100, seed: int = 42) -> list[Incident]:
    """Create a reproducible, near-balanced labelled dataset from fixed templates."""
    if count < 0:
        raise ValueError("count must be non-negative")
    rng = random.Random(seed)
    incidents = []
    for index in range(count):
        risk = RISK_LEVELS[index % len(RISK_LEVELS)]
        category = CATEGORIES[(index // len(RISK_LEVELS)) % len(CATEGORIES)]
        descriptor = rng.choice(_DESCRIPTORS[risk])
        description = f"Synthetic {category}: {descriptor}; reference case {index:04d}."
        incidents.append(
            Incident(
                incident_id=f"SYN-{index:06d}",
                category=category,
                description=description,
                risk_level=risk,
            )
        )
    rng.shuffle(incidents)
    return incidents
