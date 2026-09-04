from __future__ import annotations

import time
import uuid

from open_webui.internal.db import Base, get_async_db_context
from sqlalchemy import BigInteger, Column, String, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class PasswordResetToken(Base):
    __tablename__ = 'password_reset_token'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    token_hash = Column(String(64), nullable=False, unique=True, index=True)
    expires_at = Column(BigInteger, nullable=False)
    used_at = Column(BigInteger, nullable=True)
    created_at = Column(BigInteger, nullable=False)


class PasswordResetTokensTable:
    async def issue(self, user_id: str, token_hash: str, ttl_seconds: int = 900, db: AsyncSession | None = None):
        now = int(time.time())
        async with get_async_db_context(db) as session:
            await session.execute(
                update(PasswordResetToken)
                .where(PasswordResetToken.user_id == user_id, PasswordResetToken.used_at.is_(None))
                .values(used_at=now)
            )
            row = PasswordResetToken(
                id=str(uuid.uuid4()),
                user_id=user_id,
                token_hash=token_hash,
                expires_at=now + ttl_seconds,
                created_at=now,
            )
            session.add(row)
            await session.commit()
            return row

    async def consume(self, token_hash: str, db: AsyncSession | None = None) -> str | None:
        now = int(time.time())
        async with get_async_db_context(db) as session:
            query = select(PasswordResetToken).where(
                PasswordResetToken.token_hash == token_hash,
                PasswordResetToken.used_at.is_(None),
                PasswordResetToken.expires_at >= now,
            )
            row = (await session.execute(query)).scalar_one_or_none()
            if row is None:
                return None
            row.used_at = now
            await session.commit()
            return row.user_id


PasswordResetTokens = PasswordResetTokensTable()
