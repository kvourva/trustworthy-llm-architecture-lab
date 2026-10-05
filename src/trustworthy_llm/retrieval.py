"""Evidence retrieval with inspectable provenance."""

from __future__ import annotations

from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from trustworthy_llm.domain import Evidence
from trustworthy_llm.preprocessing import preprocess_classical


@dataclass(frozen=True)
class RetrievedEvidence:
    evidence: Evidence
    score: float
    rank: int


class LexicalRetriever:
    """TF-IDF cosine retrieval; exact terminology remains visible in the representation."""

    def __init__(self, evidence: list[Evidence]):
        self.evidence = list(evidence)
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.matrix = (
            self.vectorizer.fit_transform([preprocess_classical(item.text) for item in evidence])
            if evidence
            else None
        )

    def retrieve(self, query: str, k: int = 3) -> list[RetrievedEvidence]:
        if k < 1:
            raise ValueError("k must be positive")
        if not query.strip() or self.matrix is None:
            return []
        query_vector = self.vectorizer.transform([preprocess_classical(query)])
        scores = cosine_similarity(query_vector, self.matrix).ravel()
        ranked = sorted(enumerate(scores), key=lambda pair: (-pair[1], pair[0]))
        return [
            RetrievedEvidence(self.evidence[index], float(score), rank)
            for rank, (index, score) in enumerate(ranked[:k], start=1)
            if score > 0
        ]


def retrieval_metrics(relevant_ids: set[str], results: list[RetrievedEvidence], k: int = 3) -> dict:
    """Compute Precision@k, Recall@k, reciprocal rank, and hit rate for one query."""
    top = results[:k]
    hits = [position for position, item in enumerate(top, start=1) if item.evidence.evidence_id in relevant_ids]
    return {
        "precision_at_k": len(hits) / k,
        "recall_at_k": len(hits) / len(relevant_ids) if relevant_ids else 0.0,
        "mrr": 1 / hits[0] if hits else 0.0,
        "hit_rate_at_k": float(bool(hits)),
    }


class DenseRetriever:
    """Optional Sentence Transformer adapter; model downloads are never implicit in core use."""

    def __init__(self, evidence: list[Evidence], model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as error:
            raise RuntimeError("Install the 'dense' extra to use DenseRetriever") from error
        self.evidence = list(evidence)
        self.model = SentenceTransformer(model_name)
        self.embeddings = self.model.encode([item.text for item in evidence], normalize_embeddings=True)

    def retrieve(self, query: str, k: int = 3) -> list[RetrievedEvidence]:
        if not query.strip() or not self.evidence:
            return []
        scores = self.model.encode([query], normalize_embeddings=True) @ self.embeddings.T
        ranked = sorted(enumerate(scores[0]), key=lambda pair: (-float(pair[1]), pair[0]))
        return [
            RetrievedEvidence(self.evidence[index], float(score), rank)
            for rank, (index, score) in enumerate(ranked[:k], start=1)
        ]
