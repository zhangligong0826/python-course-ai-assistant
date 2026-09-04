# AIOps 智能运维知识库

本目录是"AIOps 智能运维 AI 助教"的知识库源资料，围绕**智能运维（AIOps）**组织，并纳入**当下流行的大语言模型（LLM）**基础知识与工程实践，帮助学习者理解可观测性、异常检测、根因分析、故障响应以及"LLM + 运维"的最新工程模式。

## 资料组织（10 份正文）

| 文件 | 主题 | 参考来源 |
| --- | --- | --- |
| 01-aiops-foundations.md | AIOps 核心闭环、典型任务、质量评价（MTTD/MTTA/MTTR） | AIOps in LLM Era 综述、Google SRE |
| 02-sre-observability.md | SLI/SLO/错误预算、黄金信号、OTel 遥测信号 | Google SRE Books、OpenTelemetry |
| 03-llm-for-aiops.md | LLM 用于运维的能力边界、RAG 数据结构、Agent 安全护栏 | LLM4AIOps 综述（183 篇论文） |
| 04-model-landscape.md | 大模型选型维度、开放权重 vs 托管、DeepSeek-V3 数据卡 | 官方仓库与模型卡 |
| 05-incident-intelligence.md | 事故时间线、根因候选输出、处置与无责复盘 | Google SRE 事故管理 |
| 06-anomaly-detection.md | 异常类型、检测方法阶梯（阈值→EWMA→STL→IF→LSTM）、评估 | AIOps 综述异常检测章节 |
| 07-root-cause-analysis.md | 告警风暴聚合、拓扑/时序/案例三类 RCA 路径、LLM 的正确位置 | Failure Management 综述 |
| 08-llm-fundamentals.md | Transformer/Token/上下文窗口/函数调用/MCP/RAG/Agent + 主流模型数据卡 | 2024–2025 公开模型资料 |
| 09-ops-tools-ecosystem.md | Prometheus/Grafana/Loki/ELK/OTel/K8s/Helm/Argo 工具生态 | 各项目官方文档 |
| 10-incident-case-studies.md | 5 个教学故障案例（慢查询、缓存雪崩、告警风暴、内存泄漏、LLM 误判） | 课程自编，SRE 复盘体例 |

## 使用方式

- 资料面向知识库 RAG 检索：每个主题独立成文，章节标题清晰，便于 Markdown 分块命中。
- 模型回答应基于检索片段给出引用；区分"观测事实、检索证据、模型推断、建议动作"；证据不足时明确拒答。
- 模型版本数据变化快，08/04 中的数字仅作坐标系，实际部署前以官方模型卡为准。
