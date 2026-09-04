# W001 仓库规则与工作树审计

审计日期：2026-09-03  
审计任务：W001  
目标：在不覆盖用户已有工作的前提下，确认 Python 程序设计 AI 助教的实现基线。

## 1. 项目与规则

- 项目：Open WebUI，当前 `package.json` 版本为 `0.11.0`。
- 分支：`main`。
- 远程：`origin` 指向 `https://github.com/open-webui/open-webui`。
- 未发现仓库根目录或父目录的 `AGENTS.md`。
- 前端：Svelte 5、SvelteKit 2、Vite 5、TypeScript。
- 后端：FastAPI、Uvicorn、SQLAlchemy、SQLite/PostgreSQL。
- AI/RAG：已有知识库、文件解析、向量检索和工具/MCP/OpenAPI 扩展能力。
- 项目文档允许使用 `npm run check`、`npm run test:frontend`、后端 pytest 和 ruff 等检查。

## 2. 相关实现入口

- 模型编辑器已支持系统提示词、知识库、工具、技能和模型元数据：`src/lib/components/workspace/Models/ModelEditor.svelte`。
- 知识库选择和文件上传：`src/lib/components/workspace/Models/Knowledge.svelte`。
- 工具选择：`src/lib/components/workspace/Models/ToolsSelector.svelte`。
- 知识库后端：`backend/open_webui/routers/knowledge.py`、`backend/open_webui/models/knowledge.py`。
- 当前课程信息原型：`case5-course-mcp/server.py`，已有 SQLite 和 MCP 工具测试，但它面向课程/教师/作业查询，不是本作业最终的课程知识助教。

## 3. 可用命令和已知环境限制

| 检查项 | 结果 |
| --- | --- |
| Node | `v25.9.0`，超出项目声明的 `>=18.13.0 <=22.x.x`，后续优先使用 Node 22 |
| npm | `11.12.1` |
| Python | `3.14.4`，超出 `pyproject.toml` 的 `<3.13.0a1`，后端优先使用已有 Python 3.11/3.12 虚拟环境 |
| 前端静态检查 | `npm run check`，后续聚焦运行；项目已有类型问题需单独记录 |
| 前端测试 | `npm run test:frontend` |
| 后端测试 | `.venv/bin/python -m pytest ... -q` 或项目可用 Python 环境 |
| 后端健康检查 | 本次审计时 `127.0.0.1:8082` 未监听 |
| 前端健康检查 | 本次审计时 `127.0.0.1:5174` 未监听 |
| `npm run dev` | 文档记录会先运行 Pyodide 准备，可能受本机代理 `127.0.0.1:7890` 影响；需要时直接运行 Vite |

当前没有在 W001 中启动服务、安装依赖、下载模型或执行修改性命令。

## 4. 启动前用户既有改动（不得覆盖或顺手提交）

以下状态来自 W001 开始前的 `git status --porcelain=v1`。新增课程项目只能使用自己的目录和明确批准的配置文件。

### 已修改

- `backend/open_webui/main.py`
- `src/app.html`
- `src/lib/components/chat/ChatPlaceholder.svelte`
- `src/lib/components/chat/MessageInput.svelte`
- `src/lib/components/layout/Sidebar.svelte`
- `src/lib/constants.ts`
- `src/lib/i18n/locales/en-US/translation.json`
- `src/lib/i18n/locales/zh-CN/translation.json`

### 已暂存删除

- `backend/open_webui/static/apple-touch-icon.png`
- `backend/open_webui/static/custom.css`
- `backend/open_webui/static/favicon-96x96.png`
- `backend/open_webui/static/favicon.ico`
- `backend/open_webui/static/favicon.png`
- `backend/open_webui/static/favicon.svg`
- `backend/open_webui/static/loader.js`
- `backend/open_webui/static/logo.png`
- `backend/open_webui/static/site.webmanifest`
- `backend/open_webui/static/splash-dark.png`
- `backend/open_webui/static/splash.png`
- `backend/open_webui/static/user-import.csv`
- `backend/open_webui/static/user.png`
- `backend/open_webui/static/web-app-manifest-192x192.png`
- `backend/open_webui/static/web-app-manifest-512x512.png`

### 已存在的未跟踪内容

- `.codex/`
- `Codex分析过程记录.md`
- `backend/data-current/`
- `backend/open_webui/routers/help.py`
- `backend/tests/`
- `case5-course-mcp/`
- `src/lib/apis/help.test.ts`
- `src/lib/apis/help.ts`
- `src/lib/components/chat/MessageInput/QuickActions.svelte`
- `src/lib/components/chat/MessageInput/quickActions.test.ts`
- `src/lib/components/chat/MessageInput/quickActions.ts`
- `src/routes/(app)/help/`
- `作业4-Codex交互过程.md`
- `作业4实现报告.md`
- `作业4接口说明.md`
- `作业4测试记录.md`
- `快捷提示词测试记录.md`
- `项目说明文档.md`
- 本次新增的 `GPT单智能体完整实现工作流.md`

本次课程项目不得恢复、删除、重命名或提交以上内容，除非用户另行明确授权。

## 5. 新项目的文件边界

允许优先新增：

```text
course-assistant-tool/
course-materials/python-programming/
tests/course-assistant/
docs/course-assistant/
```

暂不修改：

```text
src/lib/components/workspace/Models/ModelEditor.svelte
backend/open_webui/main.py
backend/open_webui/models/
backend/open_webui/retrieval/
backend/data-current/
```

只有在真实端到端验证证明现有能力不足，并完成影响分析和测试后，才能扩大修改范围。

## 6. W001 结论

- 需求可以通过现有 Open WebUI 的模型配置、知识库、RAG 和 OpenAPI Tool Server 能力完成。
- `case5-course-mcp` 可参考其 SQLite 和测试结构，但不直接作为最终工具接入。
- 当前环境的 Node/Python 版本不符合项目声明，后续应使用已有兼容虚拟环境或先请求用户批准切换环境。
- 工作树有大量用户既有改动，所有新增文件必须严格隔离。
- W001 审计完成；下一项为 W002：创建实施状态、证据目录和忽略规则。
