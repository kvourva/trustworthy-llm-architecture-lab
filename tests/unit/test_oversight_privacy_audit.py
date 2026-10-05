import json

import pytest

from trustworthy_llm.approval import HumanApprovalGateway
from trustworthy_llm.audit import AuditEvent, AuditLogger, DecisionStore
from trustworthy_llm.domain import RiskLevel
from trustworthy_llm.policy import OversightPolicy
from trustworthy_llm.privacy import pii_metrics, redact_synthetic_pii


def test_policy_requires_human_approval_for_high_and_critical():
    policy = OversightPolicy()
    assert policy.decide(RiskLevel.LOW).route == "ADVISORY"
    assert policy.decide(RiskLevel.MEDIUM).warning
    for risk in (RiskLevel.HIGH, RiskLevel.CRITICAL):
        outcome = policy.decide(risk)
        assert outcome.requires_human_approval
        assert not outcome.automatic_execution_allowed
        assert HumanApprovalGateway().submit("D-1", outcome).status == "PENDING"


def test_approval_requires_named_reviewer_and_pending_request():
    gateway = HumanApprovalGateway()
    gateway.submit("D-1", OversightPolicy().decide(RiskLevel.CRITICAL))
    with pytest.raises(ValueError):
        gateway.resolve("D-1", "", approved=True)
    assert gateway.resolve("D-1", "compliance-officer", approved=False).status == "REJECTED"


def test_synthetic_pii_is_redacted_and_metrics_are_available():
    result = redact_synthetic_pii("Contact test.user@example.invalid about the shipment")
    assert result.detected == 1
    assert "test.user@example.invalid" not in result.text
    assert "[REDACTED_EMAIL]" in result.text
    metrics = pii_metrics(1, 1, 0, 0, 2)
    assert metrics["precision"] == 0.5
    assert metrics["recall"] == 1.0


def test_audit_logs_minimal_event_without_raw_text(tmp_path):
    logger = AuditLogger(tmp_path / "audit" / "events.jsonl")
    event = AuditEvent.create("routing", "TR-03", "Policy Engine", "HUMAN_APPROVAL_REQUIRED")
    logger.log(event)
    stored = json.loads((tmp_path / "audit" / "events.jsonl").read_text())
    assert stored["requirement_id"] == "TR-03"
    assert "incident_text" not in stored
    assert "prompt" not in stored


def test_decision_store_returns_defensive_copy():
    store = DecisionStore()
    store.save("D-1", {"status": "REVIEW"})
    result = store.get("D-1")
    result["status"] = "CHANGED"
    assert store.get("D-1") == {"status": "REVIEW"}
