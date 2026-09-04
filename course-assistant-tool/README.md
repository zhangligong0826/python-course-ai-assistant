# Python 课程题库工具

这是一个独立的 FastAPI OpenAPI 工具服务，供 Open WebUI 的课程模型调用。

```bash
COURSE_ASSISTANT_DB=/tmp/course_assistant_quizzes.db \
  .venv/bin/python course-assistant-tool/app.py
```

- `GET /health`：健康检查
- `POST /quiz/generate`：按章节、难度和题型抽题（章节 `01`–`06` 为 Python 课程章节，`07` 为 AIOps 基础与可观测性，`08` 为大模型与智能运维）
- `POST /quiz/grade`：提交答案并返回得分、逐题反馈与建议
- `GET /docs`、`GET /openapi.json`：接口文档

题库为仓库内种子数据；测验会话使用 SQLite 持久化，数据库路径通过
`COURSE_ASSISTANT_DB` 指定，默认位于系统临时目录，不写入仓库。
