from __future__ import annotations

import asyncio
import hashlib
import logging
import os
import smtplib
from email.message import EmailMessage
from urllib.parse import quote

log = logging.getLogger(__name__)


def hash_reset_token(token: str) -> str:
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


def build_reset_url(origin: str, token: str) -> str:
    return f"{origin.rstrip('/')}/auth/reset-password?token={quote(token, safe='')}"


def _send_reset_email_sync(recipient: str, reset_url: str) -> None:
    host = os.getenv('PASSWORD_RESET_SMTP_HOST', '127.0.0.1')
    port = int(os.getenv('PASSWORD_RESET_SMTP_PORT', '1025'))
    username = os.getenv('PASSWORD_RESET_SMTP_USERNAME', '')
    password = os.getenv('PASSWORD_RESET_SMTP_PASSWORD', '')
    use_tls = os.getenv('PASSWORD_RESET_SMTP_TLS', 'False').lower() == 'true'

    message = EmailMessage()
    message['Subject'] = '南开大学 AIOps 组 · 重置密码'
    message['From'] = os.getenv('PASSWORD_RESET_EMAIL_FROM', 'aiops@nankai.local')
    message['To'] = recipient
    message.set_content(
        '你正在重置 Python 程序设计 AI 助教的登录密码。\n\n'
        f'请在 15 分钟内打开以下链接：\n{reset_url}\n\n'
        '如果这不是你的操作，请忽略此邮件。'
    )

    with smtplib.SMTP(host, port, timeout=10) as client:
        if use_tls:
            client.starttls()
        if username:
            client.login(username, password)
        client.send_message(message)


async def send_reset_email(recipient: str, token: str) -> None:
    origin = os.getenv('PASSWORD_RESET_PUBLIC_URL', 'http://127.0.0.1:5174')
    try:
        await asyncio.to_thread(_send_reset_email_sync, recipient, build_reset_url(origin, token))
    except Exception:
        log.exception('Unable to send password reset email')
