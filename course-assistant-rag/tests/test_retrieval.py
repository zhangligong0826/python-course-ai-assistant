from pathlib import Path
import sqlite3

from fastapi.testclient import TestClient

import app as rag_app
from app import DB_PATH, app, build_index, search_chunks


MATERIALS = Path(__file__).parents[2] / "course-materials" / "python-programming"
AIOPS_MATERIALS = Path(__file__).parents[2] / "course-materials" / "aiops"


def _chunk_count() -> int:
    with sqlite3.connect(DB_PATH) as connection:
        return connection.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]


def test_index_contains_all_course_materials() -> None:
    count = build_index(MATERIALS)
    assert count >= 10


def test_default_index_contains_aiops_and_llm_materials() -> None:
    count = build_index()
    assert count >= 20
    assert any("SLO" in item["text"] for item in search_chunks("SLO 错误预算", limit=5))
    assert any(
        "LLM" in item["text"] or "大模型" in item["text"]
        for item in search_chunks("大模型如何用于 AIOps 故障诊断", limit=5)
    )


def test_search_returns_citation_and_relevant_text() -> None:
    build_index(MATERIALS)
    results = search_chunks("文件读取异常处理", limit=3)
    assert results
    assert any("05-files-exceptions.md" in item["source"] for item in results)
    assert all(item["text"] and item["score"] > 0 for item in results)


def test_unknown_query_returns_empty_for_refusal() -> None:
    build_index(MATERIALS)
    assert search_chunks("量子纠缠时空曲率", limit=3) == []


def test_http_retrieve_contract() -> None:
    client = TestClient(app)
    response = client.post("/retrieve", json={"query": "Python 函数参数", "limit": 2})
    assert response.status_code == 200
    body = response.json()
    assert body["results"]
    assert {"source", "chapter", "text", "score"} <= body["results"][0].keys()


def test_openapi_uses_a_service_specific_health_operation_id() -> None:
    client = TestClient(app)
    schema = client.get("/openapi.json").json()
    assert schema["paths"]["/health"]["get"]["operationId"] == "rag_health"
    assert "/index" not in schema["paths"]


def test_retrieve_requires_an_offline_index(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(rag_app, "DB_PATH", tmp_path / "empty.db")
    response = TestClient(app).post("/retrieve", json={"query": "SLO", "limit": 2})
    assert response.status_code == 503
    assert "--build-index" in response.json()["detail"]


def test_build_index_with_empty_dir_does_not_wipe_existing_index(tmp_path) -> None:
    build_index(MATERIALS)
    before = _chunk_count()
    assert before > 0
    assert build_index(tmp_path) == 0
    assert _chunk_count() == before
