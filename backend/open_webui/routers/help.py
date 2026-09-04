from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from open_webui.utils.auth import get_verified_user

router = APIRouter()

DOCUMENT_NAME = '项目说明文档.md'
DOCUMENT_TITLE = 'Open WebUI 项目说明文档'


class SystemDocumentationResponse(BaseModel):
    title: str
    content: str
    source: str
    updated_at: str


def get_project_document_path() -> Path:
    return Path(__file__).resolve().parents[3] / DOCUMENT_NAME


def read_system_documentation() -> SystemDocumentationResponse:
    document_path = get_project_document_path()
    try:
        content = document_path.read_text(encoding='utf-8')
        updated_at = document_path.stat().st_mtime_ns
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{DOCUMENT_NAME} not found',
        ) from exc
    except (OSError, UnicodeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Unable to read system documentation',
        ) from exc

    return SystemDocumentationResponse(
        title=DOCUMENT_TITLE,
        content=content,
        source=DOCUMENT_NAME,
        updated_at=str(updated_at),
    )


@router.get('/system-documentation', response_model=SystemDocumentationResponse)
async def get_system_documentation(user=Depends(get_verified_user)):
    return read_system_documentation()
