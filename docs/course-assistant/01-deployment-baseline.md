# W101 Open WebUI 部署基线

验证日期：2026-09-03  
任务：W101  
结论：通过（隔离临时数据目录）

## 启动配置

- Python：`.venv/bin/python`，版本 3.12.13。
- 后端：`uvicorn open_webui.main:app --host 127.0.0.1 --port 8082`。
- 前端：`npx vite dev --host 127.0.0.1 --port 5174`。
- 临时数据库：`/private/tmp/course_assistant_webui_data2/webui.db`。
- `BYPASS_EMBEDDING_AND_RETRIEVAL=true` 仅用于部署基线，不能作为最终知识库验收配置。
- `WEBUI_SECRET_KEY` 使用临时开发值，未写入仓库。

## 验证结果

1. 后端首次使用显式 `DATABASE_URL=sqlite:////private/tmp/course_assistant_webui_data2/webui.db` 启动。
2. Alembic 从空库完成全部迁移，数据库文件生成且大小约 644 KB。
3. `curl --noproxy '*' http://127.0.0.1:8082/health` 返回 `{"status":true}`。
4. 前端 Vite 输出 `VITE v5.4.21 ready`，并在本机访问 5174 返回 `HTTP/1.1 200 OK`。
5. 后端和前端验证结束后已停止，避免留下后台进程。

## 失败与修正

第一次启动只设置 `DATA_DIR`，迁移阶段出现 SQLite `unable to open database file`，随后启动阶段出现 `no such table: config`。原因是初始化过程没有使用明确的数据库 URL。改用新的临时目录并显式设置 `DATABASE_URL` 后通过。

受限沙箱禁止直接绑定本机端口；经授权在本机环境完成了 8082 和 5174 的验证。该授权只用于本地启动和健康检查。

## 限制

- 当前没有发现本地 Ollama 服务（11434 无响应）。
- 环境变量中没有可复用的 OpenAI 兼容模型凭据。
- 当前前端没有仓库 `build/` 目录，后端以 API-only 模式启动；Vite 开发服务器可正常提供前端。
- 因此 W102（接入真实大模型）需要用户提供模型端点/凭据，或启动本地 Ollama 并准备一个模型。
