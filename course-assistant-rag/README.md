# 轻量课程 RAG 检索服务

该服务不依赖 Ollama、GPU 或在线嵌入 API，使用标准库 SQLite 保存课程片段，并用词/中文双字匹配完成本地检索。它会同时索引 `course-materials/python-programming/` 和 `course-materials/aiops/`，提供可复现的检索与文件引用；DeepSeek 仍作为生成模型。

```bash
.venv/bin/python course-assistant-rag/app.py
```

启动服务后调用 `POST /index` 建立索引，再调用：

```json
{ "query": "文件读取异常处理", "limit": 3 }
```

`POST /retrieve` 返回 `source`、`chapter`、`text`、`score`，无命中时返回空数组，提示词即可据此拒答并避免编造引用。
