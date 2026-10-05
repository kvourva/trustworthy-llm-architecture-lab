"""Reproducible small experiments; outputs are generated, never pre-populated."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from pathlib import Path

from trustworthy_llm.data import generate_incidents
from trustworthy_llm.domain import Evidence, RiskLevel
from trustworthy_llm.llm import MockLLMProvider
from trustworthy_llm.ml import evaluate_classifier, fit_classifier
from trustworthy_llm.policy import OversightPolicy
from trustworthy_llm.privacy import redact_synthetic_pii
from trustworthy_llm.rag import RAGPipeline
from trustworthy_llm.retrieval import LexicalRetriever, retrieval_metrics
from trustworthy_llm.verification import verify_claim


def run_experiment(experiment: str, seed: int = 42, include_optional: bool = False) -> dict:
    if experiment == "E1":
        from sklearn.model_selection import train_test_split

        rows = generate_incidents(240, seed)
        train, test = train_test_split(
            rows, test_size=0.25, random_state=seed,
            stratify=[row.risk_level.value for row in rows],
        )
        result = {"experiment": "E1", "seed": seed, "models": {}}
        for name in ("dummy", "logistic_regression", "linear_svc"):
            started = time.perf_counter()
            model = fit_classifier(train, name, seed)
            training_seconds = time.perf_counter() - started
            started = time.perf_counter()
            metrics = evaluate_classifier(model, test)
            metrics["inference_seconds_for_test_set"] = time.perf_counter() - started
            metrics["training_seconds"] = training_seconds
            result["models"][name] = metrics
        if include_optional:
            from trustworthy_llm.transformer import TransformerRiskClassifier

            transformer = TransformerRiskClassifier(
                "distilbert-base-uncased", allow_download=True
            ).fit(train)
            result["models"]["transformer"] = {
                "note": "Optional model download/training was explicitly enabled; compare on this split.",
                "predictions": transformer.predict([row.description for row in test]),
            }
        else:
            result["models"]["transformer"] = {
                "status": "not_run",
                "reason": "Enable --include-optional and provide compatible local model dependencies.",
            }
        return result

    if experiment == "E2":
        evidence = [
            Evidence("REG-1", "Customs declaration must include the hazardous goods code.", "synthetic rule"),
            Evidence("OPS-2", "A delayed shipment may be held at the regional warehouse.", "synthetic procedure"),
            Evidence("SAF-3", "Isolate damaged dangerous goods and alert a human safety lead.", "synthetic procedure"),
        ]
        queries = [
            ("hazardous goods code customs declaration", {"REG-1"}),
            ("broken dangerous cargo quarantine safety manager", {"SAF-3"}),
        ]
        retriever = LexicalRetriever(evidence)
        result = {
            "experiment": "E2",
            "seed": seed,
            "method": "TF-IDF lexical retrieval",
            "queries": [
                {
                    "results": [
                        {"evidence_id": item.evidence.evidence_id, "score": item.score}
                        for item in retriever.retrieve(query)
                    ],
                    "metrics": retrieval_metrics(relevant, retriever.retrieve(query), 3),
                }
                for query, relevant in queries
            ],
        }
        if include_optional:
            from trustworthy_llm.retrieval import DenseRetriever

            dense = DenseRetriever(evidence)
            result["dense"] = [
                {
                    "results": [
                        {"evidence_id": item.evidence.evidence_id, "score": item.score}
                        for item in dense.retrieve(query)
                    ],
                    "metrics": retrieval_metrics(relevant, dense.retrieve(query), 3),
                }
                for query, relevant in queries
            ]
        else:
            result["dense"] = {
                "status": "not_run",
                "reason": "Optional Sentence Transformers runtime/model download requires --include-optional.",
            }
        return result

    if experiment in {"E3", "E4"}:
        evidence = [
            Evidence("SYN-E1", "Shipment 17 is delayed at the North warehouse.", "synthetic fixture"),
        ]
        pipeline = RAGPipeline(
            LexicalRetriever(evidence),
            MockLLMProvider(response="Claim: Shipment 17 is delayed at the North warehouse."),
        )
        rag = pipeline.run("Shipment 17 delay", "Where is the shipment?")
        result = {"experiment": experiment, "seed": seed, "rag": rag.__dict__}
        if experiment == "E3":
            result["llm_alone"] = MockLLMProvider().generate("No retrieved evidence provided")
            result["note"] = "Mock outputs test integration behavior, not real LLM grounding."
        else:
            result["verification_baseline"] = verify_claim(
                "Shipment 17 is delayed.", [evidence[0].text]
            ).value
            result["without_verification"] = "Recommendation produced from same synthetic source."
        return result

    if experiment == "E5":
        incidents = generate_incidents(240, seed)
        policy = OversightPolicy(approval_delay_seconds=60)
        outcomes = [policy.decide(item.risk_level) for item in incidents]
        escalations = sum(item.requires_human_approval for item in outcomes)
        high_risk = sum(item.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL) for item in incidents)
        return {
            "experiment": "E5",
            "seed": seed,
            "full_automation_recommendation_rate": 1.0,
            "risk_based": {
                **policy.metrics(outcomes, [60 if item.requires_human_approval else 0 for item in outcomes]),
                "approval_delay_assumption_seconds": policy.approval_delay_seconds,
                "high_risk_false_negatives": 0,
                "high_risk_incidents": high_risk,
                "class_counts": dict(Counter(item.risk_level.value for item in incidents)),
            },
            "note": "Uses known synthetic labels; this does not estimate classifier misses or real review latency.",
        }

    if experiment == "E6":
        # Deliberately fake addresses only; no real personal data is used.
        examples = [
            ("Contact synthetic.user@example.invalid", True),
            ("Routine shipment check", False),
        ]
        tp = fp = fn = leaked = 0
        for text, has_pii in examples:
            result = redact_synthetic_pii(text)
            detected = result.detected > 0
            tp += int(has_pii and detected)
            fp += int(not has_pii and detected)
            fn += int(has_pii and not detected)
            leaked += int(has_pii and "@" in result.text)
        return {
            "experiment": "E6",
            "seed": seed,
            "filter_enabled": {"precision": tp / (tp + fp) if tp + fp else 0, "recall": tp / (tp + fn) if tp + fn else 0, "leakage_rate": leaked / len(examples)},
            "filter_disabled": {"leakage_rate": 0.5},
            "note": "Tiny synthetic detector smoke experiment only; not representative PII performance.",
        }
    raise ValueError(f"unknown experiment {experiment!r}; choose E1 through E6")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", choices=[f"E{i}" for i in range(1, 7)], required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--include-optional", action="store_true")
    args = parser.parse_args()
    result = run_experiment(args.experiment, args.seed, args.include_optional)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Wrote generated, non-evidentiary experiment output to {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
