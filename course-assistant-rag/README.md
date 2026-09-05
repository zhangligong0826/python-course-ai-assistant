# 轻量课程 RAG 检索服务

该服务不依赖 Ollama、GPU 或在线嵌入 API，使用标准库 SQLite 保存课程片段，并用词/中文双字匹配完成本地检索。它会同时索引 `course-materials/python-programming/` 和 `course-materials/aiops/`，提供可复现的检索与文件引用；DeepSeek 仍作为生成模型。

```bash
cd course-assistant-rag
COURSE_ASSISTANT_RAG_DB=/private/tmp/aiops_course_rag.db .venv/bin/python app.py --build-index
COURSE_ASSISTANT_RAG_DB=/private/tmp/aiops_course_rag.db .venv/bin/python app.py
```

索引由离线命令显式构建，服务的 OpenAPI 仅暴露只读的 `POST /retrieve`：

```json
{ "query": "文件读取异常处理", "limit": 3 }
```

`POST /retrieve` 返回 `source`、`chapter`、`text`、`score`，无命中时返回空数组，提示词即可据此拒答并避免编造引用。
