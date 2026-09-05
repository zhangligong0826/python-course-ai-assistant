from __future__ import annotations

from fastapi.testclient import TestClient

import sqlite3

from app import DB_PATH, QUIZ_STORE, app, delete_expired_quizzes


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


def test_expired_quiz_is_removed_from_memory_and_database() -> None:
    quiz_id = "quiz-expired"
    QUIZ_STORE[quiz_id] = ([{"id": "q-expired"}], 1.0)
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            "INSERT OR REPLACE INTO quizzes (id, questions_json, expires_at) VALUES (?, ?, ?)",
            (quiz_id, "[]", 1.0),
        )
        connection.commit()

    delete_expired_quizzes(now=2.0)

    assert quiz_id not in QUIZ_STORE
    with sqlite3.connect(DB_PATH) as connection:
        assert connection.execute("SELECT id FROM quizzes WHERE id = ?", (quiz_id,)).fetchone() is None
