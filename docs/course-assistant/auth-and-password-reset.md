# 南开大学 AIOps 组登录与密码重置

## 本地演示

登录页、侧边栏和密码重置页使用“南开大学 AIOps 组 / NK AIOps”文字品牌，不包含官方校徽素材。课程实例关闭公开注册，账户由管理员创建。

Mailpit 默认监听 SMTP `127.0.0.1:1025`，收件箱位于 `http://127.0.0.1:8025`。启动后为后端提供：

```bash
ENABLE_SIGNUP=false \
WEBUI_NAME='南开大学 AIOps 组' \
PASSWORD_RESET_SMTP_HOST=127.0.0.1 \
PASSWORD_RESET_SMTP_PORT=1025 \
PASSWORD_RESET_PUBLIC_URL=http://127.0.0.1:5174 \
PASSWORD_RESET_EMAIL_FROM=aiops@nankai.local \
../.venv/bin/uvicorn open_webui.main:app --host 127.0.0.1 --port 8082
```

## 正式 SMTP

生产环境仅通过部署环境设置以下变量，不将授权码写入仓库：

- `PASSWORD_RESET_SMTP_HOST`
- `PASSWORD_RESET_SMTP_PORT`
- `PASSWORD_RESET_SMTP_USERNAME`
- `PASSWORD_RESET_SMTP_PASSWORD`
- `PASSWORD_RESET_SMTP_TLS=true`
- `PASSWORD_RESET_EMAIL_FROM`
- `PASSWORD_RESET_PUBLIC_URL`

重置令牌只以 SHA-256 摘要保存，15 分钟过期且只能使用一次。成功重置会递增账户会话版本，使重置前签发的浏览器 JWT 失效，但不撤销用户 API Key。
