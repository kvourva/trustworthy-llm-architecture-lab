"""Inspectable risk-tiered human oversight policy."""

from dataclasses import dataclass

from trustworthy_llm.domain import RiskLevel


@dataclass(frozen=True)
class PolicyOutcome:
    route: str
    warning: bool
    requires_human_approval: bool
    automatic_execution_allowed: bool


class OversightPolicy:
    def __init__(self, approval_delay_seconds: float = 0.0):
        if approval_delay_seconds < 0:
            raise ValueError("approval delay cannot be negative")
        self.approval_delay_seconds = approval_delay_seconds

    def decide(self, risk: RiskLevel) -> PolicyOutcome:
        if risk == RiskLevel.LOW:
            return PolicyOutcome("ADVISORY", False, False, False)
        if risk == RiskLevel.MEDIUM:
            return PolicyOutcome("ADVISORY_WITH_WARNING", True, False, False)
        if risk == RiskLevel.HIGH:
            return PolicyOutcome("HUMAN_APPROVAL_REQUIRED", True, True, False)
        return PolicyOutcome("CRITICAL_HUMAN_ESCALATION", True, True, False)

    @staticmethod
    def metrics(outcomes: list[PolicyOutcome], latency_seconds: list[float]) -> dict:
        count = len(outcomes)
        return {
            # "Automation" here is recommendation drafting/routing only, never action.
            "automation_rate": sum(not item.requires_human_approval for item in outcomes) / count if count else 0.0,
            "escalation_rate": sum(item.requires_human_approval for item in outcomes) / count if count else 0.0,
            "mean_latency_seconds": sum(latency_seconds) / len(latency_seconds) if latency_seconds else 0.0,
        }
