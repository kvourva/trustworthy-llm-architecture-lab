"""Minimal append-only JSONL audit sink and in-memory decision store."""

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    requirement_id: str
    component: str
    outcome: str
    timestamp: str

    @classmethod
    def create(cls, event_type: str, requirement_id: str, component: str, outcome: str):
        return cls(event_type, requirement_id, component, outcome, datetime.now(timezone.utc).isoformat())


class AuditLogger:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def log(self, event: AuditEvent) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(asdict(event), sort_keys=True) + "\n")


class DecisionStore:
    def __init__(self):
        self._decisions: dict[str, dict] = {}

    def save(self, decision_id: str, decision: dict) -> None:
        self._decisions[decision_id] = dict(decision)

    def get(self, decision_id: str) -> dict | None:
        value = self._decisions.get(decision_id)
        return dict(value) if value is not None else None
