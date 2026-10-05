"""Provider abstraction and deterministic local mock used by the RAG pipeline."""

from __future__ import annotations

from typing import Protocol


class LLMProvider(Protocol):
    def generate(self, prompt: str) -> str: ...


class MockLLMProvider:
    """A deterministic test double; it does not model real LLM quality."""

    def __init__(self, response: str | None = None, fail: bool = False):
        self.response = response
        self.fail = fail

    def generate(self, prompt: str) -> str:
        if self.fail:
            raise RuntimeError("mock LLM failure")
        if self.response is not None:
            return self.response
        return "Recommendation: review the incident against the retrieved evidence."
