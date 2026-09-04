from __future__ import annotations

from fastapi.testclient import TestClient

from app import app, load_question_bank


client = TestClient(app)


def make_quiz() -> tuple[str, list[dict]]:
    response = client.post(
        "/quiz/generate",
        json={"chapter": "02", "difficulty": "beginner", "count": 2, "question_type": "mixed", "seed": 3},
    )
    assert response.status_code == 200
    payload = response.json()
    bank = {item["id"]: item for item in load_question_bank()}
    return payload["quiz_id"], [bank[item["question_id"]] for item in payload["questions"]]


def test_grade_returns_score_and_per_question_feedback() -> None:
    quiz_id, questions = make_quiz()
    response = client.post(
        "/quiz/grade",
        json={
            "quiz_id": quiz_id,
            "answers": [{"question_id": item["id"], "answer": item["answer"]} for item in questions],
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["score"] == payload["max_score"] == len(questions)
    assert all(item["correct"] for item in payload["results"])
    assert all(item["source"] for item in payload["results"])


def test_grade_handles_wrong_and_missing_answers() -> None:
    quiz_id, questions = make_quiz()
    wrong = "A" if questions[0]["answer"] != "A" else "B"
    response = client.post(
        "/quiz/grade",
        json={"quiz_id": quiz_id, "answers": [{"question_id": questions[0]["id"], "answer": wrong}]},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["score"] == 0
    assert len(payload["results"]) == len(questions)
    assert any(item["status"] == "missing" for item in payload["results"])
    assert payload["recommendations"]


def test_grade_rejects_unknown_quiz() -> None:
    response = client.post(
        "/quiz/grade",
        json={"quiz_id": "quiz-missing", "answers": [{"question_id": "q-01-01", "answer": "A"}]},
    )
    assert response.status_code == 404
