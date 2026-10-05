"""Evidence-grounded advisory pipeline with provenance-preserving citations."""

from __future__ import annotations

import re

from trustworthy_llm.domain import Evidence, Recommendation
from trustworthy_llm.llm import LLMProvider
from trustworthy_llm.retrieval import LexicalRetriever
from trustworthy_llm.verification import VerificationLabel, verify_claim


class RAGPipeline:
    def __init__(self, retriever: LexicalRetriever, provider: LLMProvider):
        self.retriever = retriever
        self.provider = provider

    def run(self, incident: str, question: str, k: int = 3) -> Recommendation:
        retrieved = self.retriever.retrieve(f"{incident} {question}", k=k)
        if not retrieved:
            return Recommendation("INSUFFICIENT_EVIDENCE", "No relevant evidence was retrieved.")
        evidence: list[Evidence] = [item.evidence for item in retrieved]
        context = "\n".join(f"[{item.evidence_id}] {item.text}" for item in evidence)
        prompt = f"Incident: {incident}\nQuestion: {question}\nEvidence:\n{context}"
        try:
            generated = self.provider.generate(prompt)
        except Exception as error:
            return Recommendation("LLM_FAILURE", f"Recommendation unavailable ({type(error).__name__}).")
        claims = [
            match.strip()
            for match in re.findall(r"(?:Claim|Recommendation):\s*([^\n]+)", generated, flags=re.I)
        ]
        if not claims:
            claims = [generated.strip()] if generated.strip() else []
        labels = [
            verify_claim(claim, [item.text for item in evidence]).value
            for claim in claims
        ]
        citations = [item.evidence_id for item in evidence]
        if any(label != VerificationLabel.SUPPORTED.value for label in labels):
            return Recommendation("REVIEW_REQUIRED", generated, claims, citations, labels)
        return Recommendation("EVIDENCE_LINKED", generated, claims, citations, labels)
