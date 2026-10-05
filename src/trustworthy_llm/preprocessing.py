"""Conservative text preparation for sparse classical models only."""

import re


def preprocess_classical(text: str) -> str:
    """Normalize whitespace and case without stemming or dropping negation."""
    return re.sub(r"\s+", " ", text.strip().lower())
