from __future__ import annotations

from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_generate_returns_requested_questions_without_answers() -> None:
    response = client.post(
        "/quiz/generate",
        json={"chapter": "01", "difficulty": "beginner", "count": 2, "question_type": "mixed", "seed": 42},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["chapter"] == "01"
    assert len(payload["questions"]) == 2
    assert all("answer" not in question for question in payload["questions"])
    assert all("question_id" in question for question in payload["questions"])


def test_generate_is_reproducible_with_same_seed() -> None:
    request = {"chapter": "04", "difficulty": "advanced", "count": 2, "question_type": "single_choice", "seed": 9}
    first = client.post("/quiz/generate", json=request)
    second = client.post("/quiz/generate", json=request)
    assert first.status_code == second.status_code == 200
    assert [q["question_id"] for q in first.json()["questions"]] == [
        q["question_id"] for q in second.json()["questions"]
    ]
    assert first.json()["quiz_id"] != second.json()["quiz_id"]


def test_generate_rejects_unknown_chapter() -> None:
    response = client.post(
        "/quiz/generate",
        json={"chapter": "99", "difficulty": "beginner", "count": 1, "question_type": "mixed"},
    )
    assert response.status_code == 404
    assert "chapter" in response.json()["detail"].lower()
