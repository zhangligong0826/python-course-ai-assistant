"""无需外部模型的轻量本地课程检索服务。

使用 SQLite 保存课程片段，查询采用确定性的词/中文字符匹配；它是 RAG 的检索层，
DeepSeek 仍负责生成回答。资料规模较小时，这比下载和维护独立向量数据库更轻。
"""

from __future__ import annotations

import re
import sqlite3
import tempfile
from collections.abc import Iterable
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATERIALS = (
    ROOT / "course-materials" / "python-programming",
    ROOT / "course-materials" / "aiops",
)
DB_PATH = Path(tempfile.gettempdir()) / "python_course_rag.db"

app = FastAPI(title="Python Course Lightweight RAG", version="1.0.0")


class RetrieveRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    limit: int = Field(default=3, ge=1, le=10)


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute(
        "CREATE TABLE IF NOT EXISTS chunks (id INTEGER PRIMARY KEY, source TEXT, chapter TEXT, text TEXT)"
    )
    return connection


def _split_text(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    blocks = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    return blocks


def build_index(materials_dir: Path | Iterable[Path] = DEFAULT_MATERIALS) -> int:
    rows: list[tuple[str, str, str]] = []
    directories = [materials_dir] if isinstance(materials_dir, Path) else list(materials_dir)
    paths = sorted(path for directory in directories for path in directory.glob("*.md"))
    for path in paths:
        chapter = next((line.lstrip("# ").strip() for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("#")), path.stem)
        for block in _split_text(path):
            if len(block) >= 20:
                rows.append((path.name, chapter, block[:1600]))
    if not rows:
        return 0
    with _connect() as connection:
        connection.execute("DELETE FROM chunks")
        connection.executemany("INSERT INTO chunks(source, chapter, text) VALUES (?, ?, ?)", rows)
        connection.commit()
    return len(rows)


def _terms(query: str) -> set[str]:
    terms = set(re.findall(r"[A-Za-z_][A-Za-z_0-9]*", query.lower()))
    for sequence in re.findall(r"[\u4e00-\u9fff]+", query):
        if len(sequence) == 1:
            terms.add(sequence)
        else:
            terms.update(sequence[index : index + 2] for index in range(len(sequence) - 1))
    return {term for term in terms if term.strip()}


def search_chunks(query: str, limit: int = 3) -> list[dict]:
    terms = _terms(query)
    if not terms:
        return []
    with _connect() as connection:
        rows = connection.execute("SELECT source, chapter, text FROM chunks").fetchall()
    scored: list[tuple[int, sqlite3.Row]] = []
    for row in rows:
        haystack = f"{row['source']} {row['chapter']} {row['text']}".lower()
        score = sum(haystack.count(term) for term in terms)
        if score:
            scored.append((score, row))
    scored.sort(key=lambda item: (-item[0], item[1]["source"]))
    return [
        {"source": row["source"], "chapter": row["chapter"], "text": row["text"], "score": score}
        for score, row in scored[:limit]
    ]


@app.get("/health", operation_id="rag_health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/index")
def index_materials() -> dict[str, int]:
    return {"chunks": build_index()}


@app.post("/retrieve")
def retrieve(request: RetrieveRequest) -> dict[str, list[dict]]:
    with _connect() as connection:
        count = connection.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    if count == 0:
        build_index()
    return {"results": search_chunks(request.query, request.limit)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8092)
