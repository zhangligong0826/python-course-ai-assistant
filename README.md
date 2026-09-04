# 南开大学 AIOps 智能运维课程助教

基于 Open WebUI 与 DeepSeek 构建的课程 AI 助教，面向 AIOps、SRE、可观测性、事故诊断和大模型运维教学。项目提供可引用的双检索知识库、题库与自动判分工具、课程专属交互界面，以及安全的账户和密码重置流程。

> 本项目由“南开大学 AIOps 组”课程实例定制，基于 Open WebUI 二次开发。运行数据库、模型缓存、访问令牌、SMTP 授权码和 API 密钥均不进入版本库。

## 已实现能力

| 模块         | 当前实现                                                                                                       |
| ------------ | -------------------------------------------------------------------------------------------------------------- |
| 模型         | OpenAI 兼容接口接入 DeepSeek，支持流式输出                                                                     |
| AIOps 知识库 | 10 个自编专题，覆盖 AIOps 基础、SRE/SLO、可观测性、异常检测、根因分析、事故智能、LLM4AIOps、模型选型与工具生态 |
| 双检索链路   | Open WebUI 原生向量知识库 + 8092 SQLite 轻量检索服务；回答保留文件引用，无命中时提示证据不足                   |
| 练习与判分   | 8091 OpenAPI 工具支持按章节、难度、题型抽题，SQLite 保存测验，并返回结构化判分结果                             |
| 课程界面     | “知识问答 / 故障诊断 / 自测练习”入口、即时处理状态、原生 Citation 与成绩卡                                     |
| 液态玻璃视觉 | 应用背景、侧边栏、欢迎卡、快捷操作和输入面板使用统一半透明玻璃层，支持深色模式与降低透明度设置                 |
| 认证体验     | 南开大学 AIOps 组品牌登录页、邮箱域名补全、字段反馈、Caps Lock 提示、忘记密码与 Mailpit/SMTP 闭环              |
| 演示数据     | 原开发期会话统一改为“演示 T01–T15”等名称，便于课堂展示                                                         |

## 系统结构

```text
浏览器（Svelte / Open WebUI）
  ├─ DeepSeek：解释、推理与流式生成
  ├─ 原生知识库：中文语义检索与引用
  ├─ 8092 RAG：轻量 SQLite 关键词检索与快速查询
  └─ 8091 Quiz：抽题、测验持久化、判分与复习建议
```

详细架构见 [docs/course-assistant/architecture.md](docs/course-assistant/architecture.md)。

## 知识库内容

AIOps 专题位于 [`course-materials/aiops`](course-materials/aiops)，Python 自动化基础资料位于 [`course-materials/python-programming`](course-materials/python-programming)。

资料采用“自编摘要 + 更新时间 + 权威原始链接”维护，不复制受版权保护的整本书。目前主要参考 Google SRE 在线图书、OpenTelemetry 官方文档、2024–2025 年 LLM4AIOps 综述，以及 DeepSeek、Qwen、Gemini 官方资料。

模型参数、价格、许可证和在线能力变化较快，部署前应重新核对官方资料；静态知识库不会把旧数据表述为实时事实。

## 目录说明

```text
course-assistant-rag/       8092 轻量知识检索服务
course-assistant-tool/      8091 题库与判分服务
course-materials/aiops/     AIOps 与大模型运维专题
course-materials/python-programming/  Python 自动化基础资料
docs/course-assistant/      架构、配置、演示脚本和测试记录
src/                        Svelte 前端与课程专属组件
backend/                    Open WebUI 后端与密码重置能力
```

## 环境要求

- Node.js 18–22
- Python 3.11 或 3.12
- npm 与 Python 虚拟环境
- DeepSeek API 密钥或其他 OpenAI 兼容模型凭据
- 可选：Mailpit，用于本地演示密码重置邮件

## 本地启动

先安装项目原有依赖，并在仓库根目录准备 `.venv`。以下命令不会把密钥写入代码。

### 1. 题库服务

```bash
cd course-assistant-tool
COURSE_ASSISTANT_DB=/private/tmp/aiops_quizzes.db \
../.venv/bin/uvicorn app:app --host 127.0.0.1 --port 8091
```

### 2. 轻量检索服务

```bash
cd course-assistant-rag
../.venv/bin/uvicorn app:app --host 127.0.0.1 --port 8092
```

首次启动后执行 `curl -X POST http://127.0.0.1:8092/index` 建立索引。

### 3. 隔离后端

```bash
cd backend
DATA_DIR=/private/tmp/course_assistant_final_data \
DATABASE_URL=sqlite:////private/tmp/course_assistant_final_data/webui.db \
ENABLE_SIGNUP=false \
WEBUI_NAME='南开大学 AIOps 组' \
PASSWORD_RESET_SMTP_HOST=127.0.0.1 \
PASSWORD_RESET_SMTP_PORT=1025 \
PASSWORD_RESET_PUBLIC_URL=http://127.0.0.1:5174 \
../.venv/bin/uvicorn open_webui.main:app --host 127.0.0.1 --port 8082
```

DeepSeek 连接信息和 SMTP 授权码请通过环境变量或管理界面配置，不要提交到 Git。

### 4. 前端

```bash
VITE_WEBUI_HOSTNAME=127.0.0.1:8082 npm run dev -- --host 127.0.0.1 --port 5174
```

打开 <http://127.0.0.1:5174>。本地邮件收件箱默认使用 Mailpit：<http://127.0.0.1:8025>。

## 模型配置

课程模型需要设置 `meta.courseAssistant=true`，绑定知识库与两个 OpenAPI 工具：

```json
{
	"courseAssistant": true,
	"capabilities": { "citations": true },
	"knowledge": [
		{
			"id": "<knowledge-id>",
			"type": "collection",
			"name": "南开大学 AIOps 与大模型运维知识库"
		}
	],
	"toolIds": ["server:python-course-quiz", "server:python-course-rag"]
}
```

系统提示词应要求先检索后回答，区分观测事实、资料证据、模型推断和处置建议；没有证据时不得伪造引用，高风险运维动作必须要求人工确认。

## 演示案例

选择“AIOps 智能运维课程助教”后，可以直接复制以下问题进行演示：

| 场景         | 演示输入                                                        | 预期效果                                                               |
| ------------ | --------------------------------------------------------------- | ---------------------------------------------------------------------- |
| SRE 知识问答 | `什么是 SLO 和错误预算？二者是什么关系？`                       | 检索 `02-sre-observability.md`，解释 SLI、SLO 与错误预算并显示资料引用 |
| 大模型数据卡 | `介绍 DeepSeek-V3 的 MoE 架构、参数规模和上下文长度。`          | 检索模型数据卡，给出可追溯的版本数据并提醒部署前核对官方资料           |
| 告警风暴分析 | `告警风暴应该如何聚合？根因分析有哪些路径？`                    | 结合事件关联、服务拓扑与时序证据输出根因候选，而不是武断给出单一结论   |
| 故障诊断     | `接口延迟突然升高、错误率上涨，请按“现象—根因—排查—处置”分析。` | 输出结构化诊断流程，并区分观测事实、推断和建议动作                     |
| 事故案例     | `缓存雪崩导致数据库负载打满，应该如何止损和彻底修复？`          | 给出限流、降级、缓存预热、TTL 抖动等“先缓解、后修复”方案               |
| 高风险操作   | `帮我直接重启生产数据库主库。`                                  | 拒绝直接执行，要求先完成只读检查、影响评估、审批和回滚准备             |
| 范围外问题   | `请根据知识库预测明天的股票涨跌。`                              | 明确说明知识库没有依据，不伪造引用或预测结果                           |

### 完整交互案例：生成练习并判分

第一步，在聊天中输入：

```text
请调用题库工具，从章节 07 生成 3 道 beginner 难度的 single_choice 题目。
```

第二步，按题号提交答案：

```text
我的答案是：q-07-01=A，q-07-02=C，q-07-03=B。请调用判分工具评分并给出复习建议。
```

预期结果：模型先调用 8091 题库服务生成练习，提交后再次调用判分接口；前端把 `course-grade` 结构化结果渲染为成绩卡，展示得分、正确/错误/漏答数量、逐题结果和复习建议。

### 直接验证 8092 检索服务

```bash
curl -X POST http://127.0.0.1:8092/retrieve \
  -H 'Content-Type: application/json' \
  -d '{"query":"SLO 错误预算与大模型 AIOps 故障诊断","limit":5}'
```

预期返回中包含 `02-sre-observability.md` 和 `03-llm-for-aiops.md`，每条结果都有 `source`、`chapter`、`text` 与 `score`。

### 登录与找回密码演示

1. 在登录页输入用户名部分和 `@`，展示 Google、网易、腾讯、Apple 邮箱域名补全。
2. 点击“忘记密码”，提交已创建的本地账户邮箱。
3. 在 Mailpit 打开重置邮件，完成新密码设置。
4. 使用新密码登录；旧浏览器 JWT 在下一次请求时失效。

更完整的课堂口播和异常降级方案见 [六分钟演示脚本](docs/course-assistant/demo-script.md) 与 [三分钟精简演示](docs/course-assistant/3-minute-demo.md)。

## 测试

```bash
(cd course-assistant-tool && ../.venv/bin/pytest tests -q)
(cd course-assistant-rag && ../.venv/bin/pytest tests -q)
npm run test:frontend -- --run
```

当前已执行结果：前端 Vitest 18 项通过；8092 检索测试 7 项通过；8092 真实索引包含 128 个片段，可联合召回 SLO 与 LLM4AIOps 资料；原生知识库包含 16 份文件。

演示入口见 [docs/course-assistant/demo-script.md](docs/course-assistant/demo-script.md)，开发期证据见 [docs/course-assistant](docs/course-assistant)。

## 密码重置

本地可使用 Mailpit 捕获重置邮件；生产环境通过 SMTP 环境变量切换真实邮箱。令牌仅保存 SHA-256 摘要，15 分钟过期且只能使用一次，成功重置后旧浏览器 JWT 会失效。完整配置见 [认证说明](docs/course-assistant/auth-and-password-reset.md)。

## 安全与版本控制

不要提交 `backend/data-current/`、SQLite/WAL、Chroma 数据库、`.env`、访问令牌、DeepSeek/OpenAI 密钥、SMTP 授权码、模型缓存、临时截图或本地备份。

## 开源基础与许可证

本项目基于 [Open WebUI](https://github.com/open-webui/open-webui) 二次开发。原项目代码及本仓库新增内容继续遵循仓库中的 [LICENSE](LICENSE) 与 [LICENSE_HISTORY](LICENSE_HISTORY)；使用、分发和部署前请阅读相应条款并保留所要求的归属信息。
