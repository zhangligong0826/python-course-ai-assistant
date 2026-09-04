# Python 课程 AI 助教交付说明

这是一个仅对 `python-course-assistant` 生效的 Open WebUI 课程助教增强：课程问答优先检索已绑定知识库，练习由题库 OpenAPI 工具生成，提交答案后将稳定的 `course-grade` 块渲染为成绩卡。其他模型继续使用原有欢迎页和通用 Quick Actions。

## 交付内容

| 能力 | 实现位置 | 验收方式 |
| --- | --- | --- |
| 原生中文语义知识库 | 10 份 `course-materials/python-programming/` 资料；隔离实例使用 `BAAI/bge-small-zh-v1.5` | 原生 `query/collection` 与真实保存会话检索通过 |
| 题库工具 | `course-assistant-tool/` | 16 个 pytest；抽题、判分真实模型调用 |
| 轻量检索工具 | `course-assistant-rag/` | 6 个 pytest；检索真实模型调用 |
| 课程欢迎页与快捷入口 | `CourseWelcome.svelte`、`ChatPlaceholder.svelte`、`MessageInput.svelte` | 8 个 Vitest；只对 `meta.courseAssistant=true` 生效 |
| 成绩卡 | `CourseGradeCard.svelte`、`courseAssistant.ts` | 兼容数值及题号数组两种 `course-grade` 格式；异常时保留 Markdown |
| 交付与验收 | 本目录 | 见 `11-final-acceptance.md`、`architecture.md`、`3-minute-demo.md` |

## 安全边界

- 使用隔离 `DATA_DIR` 和 SQLite 数据库；不改写 `backend/data-current`。
- 不提交模型缓存、临时数据库、截图、JWT 或 DeepSeek 凭据。
- 嵌入模型缓存由运行环境管理在仓库外。

## 本地启动

以下命令只展示变量名；请从你已有的隔离配置提供 DeepSeek 凭据。

```bash
# 终端 1：题库 OpenAPI（默认 8091）
cd course-assistant-tool
../.venv/bin/uvicorn app:app --host 127.0.0.1 --port 8091

# 终端 2：轻量检索 OpenAPI（默认 8092）
cd course-assistant-rag
../.venv/bin/uvicorn app:app --host 127.0.0.1 --port 8092

# 终端 3：隔离 Open WebUI（示例端口 8082）
cd backend
DATABASE_URL=sqlite:////private/tmp/course_assistant/webui.db \
DATA_DIR=/private/tmp/course_assistant \
RAG_EMBEDDING_MODEL=BAAI/bge-small-zh-v1.5 \
ENABLE_KB_EXEC=true \
../.venv/bin/uvicorn open_webui.main:app --host 127.0.0.1 --port 8082

# 终端 4：前端开发预览
VITE_WEBUI_HOSTNAME=127.0.0.1:8082 npm run dev -- --host 127.0.0.1 --port 5174
```

在工作区创建模型时，设置 `id=python-course-assistant`、基座模型为现有 DeepSeek 模型，并在 `meta` 中包含：

```json
{
  "courseAssistant": true,
  "capabilities": { "citations": true },
  "knowledge": [{ "id": "<知识库 ID>", "type": "collection", "name": "Python 程序设计知识库" }],
  "toolIds": ["server:python-course-quiz", "server:python-course-rag"]
}
```

两个 OpenAPI 服务的 `/health` operationId 已分别固定为 `quiz_health` 与 `rag_health`；不要恢复为同名默认 operationId，否则部分模型会拒绝重复工具名。

## 快速验证

```bash
(cd course-assistant-tool && ../.venv/bin/python -m pytest tests -q)
(cd course-assistant-rag && ../.venv/bin/python -m pytest tests -q)
npx vitest run src/lib/components/chat/courseAssistant.test.ts src/lib/components/chat/MessageInput/quickActions.test.ts
```

架构见 [architecture.md](architecture.md)，演示流程见 [3-minute-demo.md](3-minute-demo.md)，最终验收见 [11-final-acceptance.md](11-final-acceptance.md)。
