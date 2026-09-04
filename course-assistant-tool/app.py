"""Python 课程助教题库工具的 API 合约与服务入口。"""

from __future__ import annotations

import json
import os
import random
import sqlite3
import tempfile
import uuid
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field


Difficulty = Literal["beginner", "intermediate", "advanced"]
QuestionType = Literal["single_choice", "true_false", "mixed"]


class GenerateQuizRequest(BaseModel):
    """按课程章节、难度和题型抽取不泄露答案的练习题。"""

    model_config = ConfigDict(extra="forbid")

    chapter: str = Field(min_length=1, max_length=32)
    difficulty: Difficulty = "beginner"
    count: int = Field(default=5, ge=1, le=20)
    question_type: QuestionType = "mixed"
    seed: int | None = Field(default=None, ge=0)


class AnswerSubmission(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: str = Field(min_length=1, max_length=64)
    answer: str = Field(min_length=1, max_length=32)


class GradeQuizRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quiz_id: str = Field(min_length=1, max_length=64)
    answers: list[AnswerSubmission] = Field(min_length=1, max_length=20)


app = FastAPI(
    title="Python Course Assistant Tool",
    version="1.0.0",
    description="为 Open WebUI 提供章节抽题和客观题判分。",
)

QUESTION_BANK_PATH = Path(__file__).parent / "data" / "question_bank.json"
DB_PATH = Path(os.getenv("COURSE_ASSISTANT_DB", Path(tempfile.gettempdir()) / "course_assistant_quizzes.db"))
QUIZ_STORE: dict[str, list[dict]] = {}


def load_question_bank() -> list[dict]:
    return json.loads(QUESTION_BANK_PATH.read_text(encoding="utf-8"))


def initialize_database() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS quizzes (id TEXT PRIMARY KEY, questions_json TEXT NOT NULL)"
        )
        connection.commit()


def save_quiz(quiz_id: str, questions: list[dict]) -> None:
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            "INSERT INTO quizzes (id, questions_json) VALUES (?, ?)",
            (quiz_id, json.dumps(questions, ensure_ascii=False)),
        )
        connection.commit()


def load_quiz(quiz_id: str) -> list[dict] | None:
    with sqlite3.connect(DB_PATH) as connection:
        row = connection.execute("SELECT questions_json FROM quizzes WHERE id = ?", (quiz_id,)).fetchone()
    return json.loads(row[0]) if row else None


initialize_database()


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/quiz/generate", tags=["quiz"])
def generate_quiz(request: GenerateQuizRequest) -> dict:
    questions = [
        item
        for item in load_question_bank()
        if item["chapter"] == request.chapter and item["difficulty"] == request.difficulty
    ]
    if not questions:
        raise HTTPException(status_code=404, detail=f"chapter or difficulty not found: {request.chapter}")
    if request.question_type != "mixed":
        questions = [item for item in questions if item["type"] == request.question_type]
    if len(questions) < request.count:
        raise HTTPException(
            status_code=422,
            detail=f"not enough questions for requested filters: available={len(questions)}, requested={request.count}",
        )

    rng = random.Random(request.seed) if request.seed is not None else random.SystemRandom()
    selected = rng.sample(questions, request.count)
    quiz_id = f"quiz-{uuid.uuid4().hex[:12]}"
    QUIZ_STORE[quiz_id] = selected
    save_quiz(quiz_id, selected)
    return {
        "quiz_id": quiz_id,
        "chapter": request.chapter,
        "difficulty": request.difficulty,
        "question_type": request.question_type,
        "questions": [
            {
                "question_id": item["id"],
                "type": item["type"],
                "stem": item["stem"],
                "options": item["options"],
                "concept": item["concept"],
                "source": item["source"],
            }
            for item in selected
        ],
    }


@app.post("/quiz/grade", tags=["quiz"])
def grade_quiz(request: GradeQuizRequest) -> dict:
    selected = QUIZ_STORE.get(request.quiz_id) or load_quiz(request.quiz_id)
    if selected is None:
        raise HTTPException(status_code=404, detail=f"quiz not found: {request.quiz_id}")

    submitted = {item.question_id: item.answer.strip().upper() for item in request.answers}
    selected_by_id = {item["id"]: item for item in selected}
    unknown_ids = sorted(set(submitted) - set(selected_by_id))
    if unknown_ids:
        raise HTTPException(status_code=422, detail=f"answers contain unknown question ids: {unknown_ids}")

    results = []
    recommendations = []
    for item in selected:
        question_id = item["id"]
        answer = submitted.get(question_id)
        status = "missing" if answer is None else ("correct" if answer == item["answer"] else "wrong")
        correct = status == "correct"
        results.append(
            {
                "question_id": question_id,
                "status": status,
                "correct": correct,
                "selected_answer": answer,
                "correct_answer": item["answer"],
                "explanation": item["explanation"],
                "concept": item["concept"],
                "source": item["source"],
            }
        )
        if not correct:
            recommendations.append(f"复习 {item['concept']}，参考 {item['source']}。")

    return {
        "quiz_id": request.quiz_id,
        "score": sum(item["correct"] for item in results),
        "max_score": len(selected),
        "results": results,
        "recommendations": recommendations,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8091)
