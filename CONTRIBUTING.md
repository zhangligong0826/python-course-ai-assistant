# 贡献指南

感谢你为南开大学 AIOps 智能运维课程助教做出贡献。仓库已公开；请通过 Fork 后提交 Pull Request（PR），不要向默认分支直接推送。

## 开始之前

1. 从默认分支 `feat/python-course-ai-assistant` 创建一个语义明确的分支，例如 `fix/quiz-expiration`。
2. 只提交与当前 PR 有关的代码和文档；不要提交 `.env`、JWT、DeepSeek/OpenAI 密钥、SMTP 授权码、SQLite 数据库、模型缓存或本地截图。
3. 涉及课程资料时，请提供自编摘要和权威来源链接，避免复制受版权保护的整本书或长篇内容。

## 本地验证

Python 服务使用项目根目录的 `.venv`，前端使用 npm 依赖。提交 PR 前至少运行与改动范围对应的检查：

```bash
# 8091：题库、测验持久化、TTL 和判分统计
(cd course-assistant-tool && ../.venv/bin/pytest tests -q)

# 8092：离线索引、检索及空索引保护
(cd course-assistant-rag && ../.venv/bin/pytest tests -q)

# 前端：课程模型判断和成绩卡数据契约
npx vitest run src/lib/components/chat/courseAssistant.test.ts
```

首次使用 8092 时，必须显式建立本地索引：

```bash
cd course-assistant-rag
COURSE_ASSISTANT_RAG_DB=/private/tmp/aiops_course_rag.db \
  ../.venv/bin/python app.py --build-index
```

服务端 `/retrieve` 不会隐式建索引：索引为空时应返回 HTTP 503，并提示先运行 `--build-index`。这是为了避免模型工具调用中意外重建或清空索引。

## 课程功能契约

- 8091 的 `quiz/grade` 响应必须保留 `score`、`max_score`、`correct`、`wrong`、`missing`、`results` 与 `recommendations`。前端成绩卡依赖这些字段。
- 测验由 `COURSE_ASSISTANT_QUIZ_TTL_SECONDS` 控制有效期；该值必须为正数。过期测验应从内存和 SQLite 中清除，并返回“未找到”。
- 8092 的 OpenAPI 仅提供只读检索；索引构建只能由离线命令执行。
- 课程专属界面只应在 `meta.courseAssistant=true` 的模型上生效，不得影响普通模型的欢迎页或快捷操作。
- 课程回答必须区分资料证据与模型推断；没有依据时不得伪造 Citation，高风险运维操作必须保留人工确认边界。

## Pull Request 要求

PR 描述请包含：

1. 改动目的与影响范围；
2. 已执行的测试命令和结果；
3. 如修改 UI，附上脱敏截图，并说明桌面端或移动端覆盖情况；
4. 如修改 API、知识库或题库，说明兼容性及迁移方式。

GitHub Actions 会在涉及课程服务或课程前端契约的 PR 上执行上述关键测试。维护者审核通过后再合并。
