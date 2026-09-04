from pathlib import Path
import sqlite3

from fastapi.testclient import TestClient

from app import DB_PATH, app, build_index, search_chunks


MATERIALS = Path(__file__).parents[2] / "course-materials" / "python-programming"


def _chunk_count() -> int:
    with sqlite3.connect(DB_PATH) as connection:
        return connection.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]


def test_index_contains_all_course_materials() -> None:
    count = build_index(MATERIALS)
    assert count >= 10


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


def test_build_index_with_empty_dir_does_not_wipe_existing_index(tmp_path) -> None:
    build_index(MATERIALS)
    before = _chunk_count()
    assert before > 0
    assert build_index(tmp_path) == 0
    assert _chunk_count() == before
