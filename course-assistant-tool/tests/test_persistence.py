from __future__ import annotations

from fastapi.testclient import TestClient

from app import DB_PATH, QUIZ_STORE, app


def test_generated_quiz_survives_in_memory_store_reset() -> None:
    client = TestClient(app)
    generated = client.post(
        "/quiz/generate",
        json={"chapter": "05", "difficulty": "intermediate", "count": 1, "question_type": "mixed", "seed": 4},
    ).json()
    question = generated["questions"][0]
    stored = QUIZ_STORE.pop(generated["quiz_id"])
    assert stored
    response = client.post(
        "/quiz/grade",
        json={
            "quiz_id": generated["quiz_id"],
            "answers": [{"question_id": question["question_id"], "answer": "A"}],
        },
    )
    assert response.status_code == 200
    assert DB_PATH.exists()


def test_health_is_structured() -> None:
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
