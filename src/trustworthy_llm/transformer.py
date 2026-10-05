"""Optional fine-tuned Hugging Face sequence classifier.

This module is isolated from the core dependencies. Loading uses the standard
library model classes without enabling custom remote code; model files must
already be local unless the caller explicitly opts into a download.
"""

from __future__ import annotations

from trustworthy_llm.domain import Incident, RiskLevel
from trustworthy_llm.ml import LABELS


class TransformerRiskClassifier:
    def __init__(self, model_name: str, allow_download: bool = False, device: str | None = None):
        try:
            import torch
            from transformers import AutoModelForSequenceClassification, AutoTokenizer
        except ImportError as error:
            raise RuntimeError(
                "Install compatible torch and transformers packages to enable this optional classifier"
            ) from error
        local_files_only = not allow_download
        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, local_files_only=local_files_only, trust_remote_code=False
        )
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=len(LABELS),
            local_files_only=local_files_only,
            trust_remote_code=False,
        )
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def fit(self, incidents: list[Incident], epochs: int = 2, batch_size: int = 8, learning_rate: float = 2e-5):
        if not incidents:
            raise ValueError("training data must not be empty")
        if epochs < 1 or batch_size < 1:
            raise ValueError("epochs and batch_size must be positive")
        torch = self.torch
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=learning_rate)
        self.model.train()
        for _ in range(epochs):
            for start in range(0, len(incidents), batch_size):
                batch = incidents[start : start + batch_size]
                encoded = self.tokenizer(
                    [item.description for item in batch],
                    truncation=True,
                    padding=True,
                    return_tensors="pt",
                )
                encoded = {key: value.to(self.device) for key, value in encoded.items()}
                labels = torch.tensor(
                    [LABELS.index(item.risk_level.value) for item in batch],
                    dtype=torch.long,
                    device=self.device,
                )
                optimizer.zero_grad()
                loss = self.model(**encoded, labels=labels).loss
                loss.backward()
                optimizer.step()
        self.model.eval()
        return self

    def predict(self, texts: list[str]) -> list[str]:
        if not texts:
            return []
        self.model.eval()
        with self.torch.no_grad():
            encoded = self.tokenizer(texts, truncation=True, padding=True, return_tensors="pt")
            encoded = {key: value.to(self.device) for key, value in encoded.items()}
            predicted = self.model(**encoded).logits.argmax(dim=1).cpu().tolist()
        return [LABELS[index] for index in predicted]

    def predict_incidents(self, incidents: list[Incident]) -> list[RiskLevel]:
        return [RiskLevel(label) for label in self.predict([item.description for item in incidents])]
