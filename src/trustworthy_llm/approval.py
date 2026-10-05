"""Explicit human approval state for recommendation routing."""

from dataclasses import dataclass

from trustworthy_llm.policy import PolicyOutcome


@dataclass
class ApprovalRequest:
    decision_id: str
    status: str
    reviewer: str | None = None
    note: str | None = None


class HumanApprovalGateway:
    def __init__(self):
        self._requests: dict[str, ApprovalRequest] = {}

    def submit(self, decision_id: str, outcome: PolicyOutcome) -> ApprovalRequest:
        status = "PENDING" if outcome.requires_human_approval else "ADVISORY_ONLY"
        request = ApprovalRequest(decision_id, status)
        self._requests[decision_id] = request
        return request

    def resolve(self, decision_id: str, reviewer: str, approved: bool, note: str = "") -> ApprovalRequest:
        if not reviewer.strip():
            raise ValueError("reviewer identity is required")
        request = self._requests.get(decision_id)
        if request is None or request.status != "PENDING":
            raise ValueError("no pending human approval request")
        request.status = "APPROVED" if approved else "REJECTED"
        request.reviewer = reviewer
        request.note = note
        return request
