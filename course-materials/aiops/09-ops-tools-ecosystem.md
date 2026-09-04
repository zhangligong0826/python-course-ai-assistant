# 运维可观测性工具生态

更新时间：2026-09-04。按数据链路"采集→存储→可视化→告警→编排"梳理主流开源工具，均以官方文档概念为准。

## 指标（Metrics）

- **Prometheus**：事实标准的时序指标系统。拉取（pull）模式，PromQL 查询，Exporter 生态覆盖主机（node_exporter）、数据库、中间件。告警规则声明式定义，由 Alertmanager 负责分组、抑制、路由。
- **Grafana**：可视化与仪表盘事实标准，数据源可接 Prometheus、Loki、Tempo、ES 等；也支持统一告警。
- 关键实践：指标命名遵循 `<子系统>_<对象>_<度量>_<单位>`；标签基数（label cardinality）必须受控，避免把 user_id、request_id 打成标签导致时序爆炸。

## 日志（Logs）

- **ELK/EFK**：Elasticsearch 存查、Logstash/Fluentd/Fluent Bit 采集、Kibana 可视化。适合全文检索与复杂分析，资源成本较高。
- **Loki**：Grafana 生态日志系统，只索引标签不索引全文，成本低，与 Prometheus 标签体系对齐，适合与指标联动排查。
- 关键实践：**结构化日志**（JSON、稳定字段）、日志带 trace_id/span_id、日志级别有明确使用规范（DEBUG 不进生产、ERROR 表示需要人介入）。

## 链路追踪（Traces）

- **OpenTelemetry（OTel）**：CNCF 厂商中立标准，统一 traces/metrics/logs 的采集 SDK 与语义约定（semantic conventions，如 service.name、deployment.environment）。新项目应优先用 OTel 埋点，后端可自由切换。
- **Jaeger / Tempo / Zipkin**：链路后端。追踪的核心价值是跨服务延迟分解（哪个 span 慢）和错误传播路径。

## 编排与云原生

- **Kubernetes**：容器编排事实标准。运维重点关注 Pod 状态（CrashLoopBackOff、OOMKilled）、事件（events）、资源 requests/limits、探针（liveness/readiness/startup）。
- **Helm**：K8s 应用打包；**Argo CD**：GitOps 持续部署，变更可追溯、可回滚——事故复盘时变更记录是关键数据源。
- **IaC（Terraform 等）**：基础设施即代码，环境漂移可检测。

## 工具链与 AIOps 的关系

工具产生的是"原料"：指标、日志、链路、事件、拓扑、变更。AIOps 是在原料之上做检测、关联、定位与建议。常见失败模式是"工具堆了很多但数据不通"：服务名在三套系统里三种写法、时间戳时区不统一、标签维度不一致，导致跨源关联无法进行。**数据治理先行于算法**。

## 参考资料

- Prometheus 文档，https://prometheus.io/docs/
- OpenTelemetry 文档，https://opentelemetry.io/docs/
- Grafana/Loki 文档，https://grafana.com/docs/
- Kubernetes 文档，https://kubernetes.io/docs/
