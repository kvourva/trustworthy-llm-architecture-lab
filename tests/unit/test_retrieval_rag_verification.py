from trustworthy_llm.domain import Evidence
from trustworthy_llm.llm import MockLLMProvider
from trustworthy_llm.rag import RAGPipeline
from trustworthy_llm.retrieval import LexicalRetriever
from trustworthy_llm.verification import VerificationLabel, verify_claim


def test_retrieval_preserves_provenance_and_ranks_relevant_evidence():
    relevant = Evidence("E-1", "Customs declaration requires a hazardous goods code.", "synthetic policy")
    other = Evidence("E-2", "Warehouse reports routine parcel handling.", "synthetic procedure")
    results = LexicalRetriever([relevant, other]).retrieve("hazardous goods code customs", k=2)
    assert results[0].evidence.evidence_id == "E-1"
    assert results[0].evidence.source == "synthetic policy"
    assert results[0].rank == 1


def test_retrieval_failure_and_empty_corpus_return_no_fabricated_results():
    assert LexicalRetriever([]).retrieve("customs") == []
    retriever = LexicalRetriever([Evidence("E-1", "Warehouse loading schedule.", "fixture")])
    assert retriever.retrieve("unrelated customs declaration") == []


def test_verifier_supported_contradicted_and_unknown():
    assert verify_claim("Shipment is delayed", ["Shipment is delayed at the warehouse."]) == VerificationLabel.SUPPORTED
    assert verify_claim("Shipment is delayed", ["Shipment is not delayed at the warehouse."]) == VerificationLabel.CONTRADICTED
    assert verify_claim("Route is closed", ["Supplier confirmed the invoice."]) == VerificationLabel.UNKNOWN


def test_rag_returns_insufficient_evidence_on_retrieval_failure():
    result = RAGPipeline(
        LexicalRetriever([Evidence("E-1", "Warehouse loading.", "fixture")]),
        MockLLMProvider(),
    ).run("shipment incident", "customs seizure")
    assert result.status == "INSUFFICIENT_EVIDENCE"
    assert result.citations == []


def test_rag_marks_unsupported_claim_for_review_without_inventing_ids():
    result = RAGPipeline(
        LexicalRetriever([Evidence("E-1", "Shipment 9 is delayed.", "fixture")]),
        MockLLMProvider(response="Claim: Shipment 9 was delivered on time."),
    ).run("Shipment 9 delay", "What is the status?")
    assert result.status == "REVIEW_REQUIRED"
    assert result.citations == ["E-1"]
    assert result.verification == ["UNKNOWN"]


def test_rag_marks_contradicted_claim_for_review():
    result = RAGPipeline(
        LexicalRetriever([Evidence("E-1", "Shipment 9 is not delayed.", "fixture")]),
        MockLLMProvider(response="Claim: Shipment 9 is delayed."),
    ).run("Shipment 9 delay", "What is the status?")
    assert result.status == "REVIEW_REQUIRED"
    assert result.verification == ["CONTRADICTED"]


def test_provider_failure_is_contained():
    result = RAGPipeline(
        LexicalRetriever([Evidence("E-1", "Shipment 9 is delayed.", "fixture")]),
        MockLLMProvider(fail=True),
    ).run("Shipment 9 delay", "What is the status?")
    assert result.status == "LLM_FAILURE"
    assert result.citations == []
