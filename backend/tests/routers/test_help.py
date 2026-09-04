from pathlib import Path

import pytest
from fastapi import HTTPException

from open_webui.routers import help as help_router


def test_document_path_is_fixed_to_project_document():
    assert help_router.get_project_document_path().name == '项目说明文档.md'


def test_read_system_documentation_returns_document_metadata(tmp_path, monkeypatch):
    document = tmp_path / '项目说明文档.md'
    document.write_text('# 测试项目说明\n', encoding='utf-8')
    monkeypatch.setattr(help_router, 'get_project_document_path', lambda: Path(document))

    result = help_router.read_system_documentation()

    assert result.title == 'Open WebUI 项目说明文档'
    assert result.content == '# 测试项目说明\n'
    assert result.source == '项目说明文档.md'
    assert result.updated_at.isdigit()


def test_read_system_documentation_returns_404_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(help_router, 'get_project_document_path', lambda: tmp_path / 'missing.md')

    with pytest.raises(HTTPException) as raised:
        help_router.read_system_documentation()

    assert raised.value.status_code == 404
