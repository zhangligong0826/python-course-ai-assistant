# 实现报告（阶段性交付）

已完成：DeepSeek 模型链路、六章十份课程材料、48 道题库、抽题与判分 FastAPI 工具、SQLite 会话持久化、轻量 SQLite 课程 RAG 检索、OpenAPI 接入、课程模型绑定、v1/v2 系统提示词、15 条验收矩阵和 20 个自动化回归测试。

质量证据：`course-assistant-tool/tests` 全部 16 passed；Open WebUI 工具注册与 DeepSeek 函数选择均 HTTP 200；密钥和运行时数据库未写入仓库。

RAG 进展（2026-09-04 更新）：原生知识库 RAG 已完成。使用 Ollama 嵌入模型建立索引（12/12 资料），六章定向检索最终 7/7 通过（bge-m3 优化后），带引用对话验证通过（行内引用 [1]）。早期版本使用本地 SQLite 词法检索作为无嵌入期间的替代方案，现已被原生 RAG 替代。详见 `03-rag-blocker.md` 解除记录与 `08-retrieval-analysis.md`。

可选升级：配置重排模型（如 bge-reranker）进一步提升混合检索的最终排序质量；补充 15 条固定测试集的人工输出评估。
