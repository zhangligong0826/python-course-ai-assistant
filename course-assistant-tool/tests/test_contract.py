from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app import (
    AnswerSubmission,
    GenerateQuizRequest,
    GradeQuizRequest,
    app,
)


def test_generate_request_accepts_supported_filters() -> None:
    request = GenerateQuizRequest(
        chapter="01",
        difficulty="beginner",
        count=5,
        question_type="mixed",
        seed=7,
    )
    assert request.count == 5
    assert request.question_type == "mixed"


@pytest.mark.parametrize("field", ["count", "seed"])
def test_generate_request_rejects_invalid_ranges(field: str) -> None:
    values = {"chapter": "01", "difficulty": "beginner", "count": 5, "question_type": "mixed", "seed": 7}
    values[field] = 0 if field == "count" else -1
    with pytest.raises(ValidationError):
        GenerateQuizRequest(**values)


def test_grade_request_requires_question_id_and_answer() -> None:
    request = GradeQuizRequest(
        quiz_id="quiz-001",
        answers=[AnswerSubmission(question_id="q-001", answer="A")],
    )
    assert request.answers[0].answer == "A"


def test_openapi_contract_exposes_health_and_quiz_routes() -> None:
    client = TestClient(app)
    schema = client.get("/openapi.json").json()
    assert "/health" in schema["paths"]
    assert "/quiz/generate" in schema["paths"]
    assert "/quiz/grade" in schema["paths"]
