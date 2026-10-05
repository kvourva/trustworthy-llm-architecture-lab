import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def test_research_questions_cover_all_rqs():
    text = _read("research/research_questions.md")
    for rq in ("RQ1", "RQ2", "RQ3", "RQ4", "RQ5"):
        assert re.search(rf"^## {rq}\b", text, re.M), rq
    assert "not an autonomous logistics decision maker" in text


def test_hypotheses_have_required_fields_and_cover_all_rqs():
    text = _read("research/hypotheses.md")
    blocks = re.split(r"^### ", text, flags=re.M)[1:]
    assert blocks
    for block in blocks:
        for field in ("Statement", "Direction", "Supports", "Refutes"):
            assert f"**{field}" in block, (block.splitlines()[0], field)
    for rq in range(1, 6):
        assert re.search(rf"^### H{rq}\.\d", text, re.M), rq


def test_learning_note_exists():
    text = _read("docs/learning-notes/phase-1-research-questions-and-hypotheses.md")
    assert "PhD interview" in text
