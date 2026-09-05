# AIOps 智能运维课程助教交付说明

这是一个仅对课程助教模型（`courseAssistant=true`，当前为 `course-aiops-assistant`）生效的 Open WebUI 课程助教增强：课程问答优先检索已绑定知识库，练习由题库 OpenAPI 工具生成，提交答案后将稳定的 `course-grade` 块渲染为成绩卡。其他模型继续使用原有欢迎页和通用 Quick Actions。

> 定位说明：本项目对外统一使用**演示**口径（见 [3-minute-demo.md](3-minute-demo.md)）。早期开发过程中形成的 10/11/12 号"验收"文档作为内部测试记录保留，演示底稿以演示脚本与演示记录为准。

## 知识库方向

- **当前课程方向：AIOps 智能运维**。知识库为"AIOps 智能运维知识库"，资料位于 `course-materials/aiops/`（10 份正文：AIOps 基础、SRE 与可观测性、LLM4Ops、模型选型数据卡、事故管理、异常检测、根因分析、大模型基础与主流模型数据卡、工具生态、故障案例），隔离实例使用嵌入模型 `bge-m3`。
- `course-materials/python-programming/`（Python 程序设计资料）保留在仓库中，作为题库练习工具的配套资料，不删除。
- 前端课程入口文案已同步为 AIOps 方向（"知识问答 / 故障诊断 / 自测练习"三张卡片）。

## 交付内容

| 能力 | 实现位置 | 演示/验证方式 |
| --- | --- | --- |
| AIOps 专精知识库 | 11 份 `course-materials/aiops/` 资料；隔离实例使用 `bge-m3` | 11 个定向检索用例全部命中（见 `evidence/aiops-rag-retrieval.txt`）；引用对话见 `evidence/aiops-citation-chat.txt` |
| 题库工具 | `course-assistant-tool/` | 17 个 pytest；抽题、判分真实模型调用 |
| 轻量检索工具 | `course-assistant-rag/` | 8 个 pytest；检索真实模型调用 |
| 课程欢迎页与快捷入口 | `CourseWelcome.svelte`、`ChatPlaceholder.svelte`、`MessageInput.svelte` | 8 个 Vitest；只对 `meta.courseAssistant=true` 生效 |
| 成绩卡 | `CourseGradeCard.svelte`、`courseAssistant.ts` | 兼容数值及题号数组两种 `course-grade` 格式；异常时保留 Markdown |
| 液态玻璃界面 | `src/app.css`、`MessageInput.svelte`、`QuickActions.svelte` 等 | 玻璃化侧栏、输入面板、卡片、浮层；浏览器目视确认 |
| 演示材料 | 本目录 | 完整讲稿见 [demo-script.md](demo-script.md)（约 6 分钟），精简版见 [3-minute-demo.md](3-minute-demo.md)，架构见 `architecture.md` |

## 安全边界

- 使用隔离 `DATA_DIR` 和 SQLite 数据库；不改写 `backend/data-current`。
- 不提交模型缓存、临时数据库、截图、JWT 或 DeepSeek 凭据。
- 嵌入模型缓存由运行环境管理在仓库外。

## 本地启动

以下命令只展示变量名；请从你已有的隔离配置提供 DeepSeek 凭据。

```bash
# 终端 1：题库 OpenAPI（默认 8091）
cd course-assistant-tool
COURSE_ASSISTANT_QUIZ_TTL_SECONDS=3600 \
../.venv/bin/uvicorn app:app --host 127.0.0.1 --port 8091

# 终端 2：轻量检索 OpenAPI（默认 8092）
cd course-assistant-rag
COURSE_ASSISTANT_RAG_DB=/private/tmp/aiops_course_rag.db ../.venv/bin/python app.py --build-index
COURSE_ASSISTANT_RAG_DB=/private/tmp/aiops_course_rag.db \
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

架构见 [architecture.md](architecture.md)，**演示流程见 [3-minute-demo.md](3-minute-demo.md)**，完整讲稿见 [demo-script.md](demo-script.md)；课程开发要求逐条自查见 [13-requirements-checklist.md](13-requirements-checklist.md)；11-final-acceptance.md 为开发期内部测试记录。

登录品牌与 Mailpit/SMTP 密码重置配置见 [auth-and-password-reset.md](auth-and-password-reset.md)。
12-auth-acceptance.md 为认证功能的内部验证记录。
