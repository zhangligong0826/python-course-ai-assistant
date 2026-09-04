from __future__ import annotations

import json
from pathlib import Path


BANK = Path(__file__).parents[1] / "data" / "question_bank.json"


def load_questions() -> list[dict]:
    return json.loads(BANK.read_text(encoding="utf-8"))


def test_bank_has_required_size_and_unique_ids() -> None:
    questions = load_questions()
    assert len(questions) == 60
    ids = [item["id"] for item in questions]
    assert len(ids) == len(set(ids))


def test_bank_covers_python_and_aiops_chapters_with_three_difficulties() -> None:
    questions = load_questions()
    assert {item["chapter"] for item in questions} == {
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
    }
    for chapter in {item["chapter"] for item in questions}:
        chapter_questions = [item for item in questions if item["chapter"] == chapter]
        assert {item["difficulty"] for item in chapter_questions} == {
            "beginner",
            "intermediate",
            "advanced",
        }


def test_question_shape_and_sources_are_valid() -> None:
    questions = load_questions()
    assert {item["type"] for item in questions} == {"single_choice", "true_false"}
    for item in questions:
        assert item["source"].startswith(
            ("01-", "02-", "03-", "04-", "05-", "06-", "07-")
        )
        assert item["answer"] in {"A", "B", "C", "D", "T", "F"}
        assert item["stem"] and item["explanation"] and item["concept"]
        if item["type"] == "single_choice":
            assert set(item["options"]) == {"A", "B", "C", "D"}
            assert item["answer"] in item["options"]
        else:
            assert item["options"] == {"T": "正确", "F": "错误"}
