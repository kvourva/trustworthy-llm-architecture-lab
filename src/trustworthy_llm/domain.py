"""Small domain objects shared by the research components."""

from dataclasses import dataclass, field
from enum import Enum


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class Incident:
    incident_id: str
    category: str
    description: str
    risk_level: RiskLevel
    synthetic: bool = True


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    text: str
    source: str
    synthetic: bool = True


@dataclass
class Recommendation:
    status: str
    text: str
    claims: list[str] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)
    verification: list[str] = field(default_factory=list)
