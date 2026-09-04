# W102 DeepSeek 模型连接记录

验证日期：2026-09-03  
任务：W102  
结论：通过

## 已复用配置

- 配置来源：启动前已有 `backend/data-current/webui.db`，仅读取其连接配置。
- OpenAI 兼容地址：`https://api.deepseek.com`。
- 密钥：存在且启用；未打印、未写入本仓库、未写入报告。
- 实际选择模型：`deepseek-v4-flash`。

## 验证证据

1. DeepSeek `GET /models` 返回 HTTP 200；发现 `deepseek-v4-flash`、`deepseek-v4-pro` 和 `deepseek-v4-flash-vision-exp`。
2. 使用 Open WebUI 隔离实例的 JWT 调用 `/api/models` 返回 HTTP 200，模型列表包含上述 DeepSeek 模型。
3. 使用 Open WebUI `/api/chat/completions` 发送最小请求：`请只回复：WebUI连接成功。`，返回 HTTP 200，模型为 `deepseek-v4-flash`，响应正文以 `WebUI连接` 开头。
4. 请求限制为 16 tokens，未保存响应中的敏感数据。

## 隔离实例

- 后端端口：127.0.0.1:8082。
- 前端端口：127.0.0.1:5174。
- 数据库副本：`/private/tmp/deepseek_webui_data/webui.db`。
- 原始 `backend/data-current/` 未被修改。
- 当前实例保留运行，供后续知识库和工具接入使用；若结束本轮工作，应主动停止进程。

## 限制

- DeepSeek 是聊天模型，不自动提供课程资料嵌入模型。
- 当前隔离实例启动时暂时设置了 `BYPASS_EMBEDDING_AND_RETRIEVAL=true`，只能证明模型链路，不能作为最终 RAG 验收。
- W205 前必须准备可用嵌入模型（优先已有 Ollama `nomic-embed-text`，或用户批准配置其他兼容嵌入服务）。
