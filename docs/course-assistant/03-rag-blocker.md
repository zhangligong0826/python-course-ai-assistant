# W205 RAG 索引阻塞记录

记录日期：2026-09-03  
结论：BLOCKED，资料文件已准备但尚未声称完成索引。  
**状态更新（2026-09-04）：已解除阻塞并完成验证**，见文末"解除记录"。

## 已确认

- `course-materials/python-programming/` 已有 10 项清单对应的资料文件。
- Open WebUI 后端和 DeepSeek 聊天链路可用。
- 原配置中的嵌入设置为 Ollama `nomic-embed-text`，但本机 11434 没有 Ollama 服务。
- sentence-transformers/all-MiniLM-L6-v2 的本地缓存目录没有模型文件。
- 当前隔离服务启动时设置了 `BYPASS_EMBEDDING_AND_RETRIEVAL=true`，因此只能进行部署/聊天验证，不能用于知识库检索验收。

## 恢复条件

满足任一条件后恢复 W205：

1. 用户启动 Ollama 并准备 `nomic-embed-text`，将地址配置为 `http://127.0.0.1:11434`；或
2. 用户批准下载并缓存一个兼容的 sentence-transformers 嵌入模型；或
3. 用户提供可调用的 OpenAI 兼容 `/embeddings` 服务及模型名。

恢复后必须：取消旁路配置，导入全部资料，等待索引完成，并对六章各执行一次定向检索，保存命中文件和片段。

## 当前策略

不修改核心 RAG 代码，不把无索引的文件当成知识库通过。题库工具 W301—W305 不依赖嵌入，可以先行实现。

## 解除记录（2026-09-04）

恢复条件采用第 1 条：用户启动 Ollama（11434），拉取 `nomic-embed-text` 完成索引与验证。

1. 取消旁路：新隔离实例以 `BYPASS_EMBEDDING_AND_RETRIEVAL=False` 启动，`GET /api/v1/retrieval/config` 确认为 `false`。
2. 导入全部资料：12/12 同步上传并加入知识库（`process_in_background=false` + 轮询 `status=completed`，规避上次竞态问题）。
3. 六章定向检索：首轮 5/7 通过（第 3、6 章未命中），证据 `evidence/native-rag-retrieval.txt`。
4. 优化迭代：混合检索（BM25+向量）无提升（5/7），根因分析见 `08-retrieval-analysis.md`；切换嵌入模型为 `bge-m3` 后重嵌入，7/7 全部通过，证据 `evidence/native-rag-retrieval-bgem3.txt`。
5. 带引用对话验证：课程模型 + 知识库 + DeepSeek，返回行内引用 [1]，证据 `evidence/citation-chat.txt`。
