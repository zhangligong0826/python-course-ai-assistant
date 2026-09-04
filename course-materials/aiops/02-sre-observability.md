# SRE 与可观测性：SLI、SLO、错误预算和遥测信号

更新时间：2026-09-04。本文依据 Google SRE 在线图书与 OpenTelemetry 官方概念编写。

## SLI、SLO 与错误预算

SLI 是用户可感知服务行为的量化指标，例如成功请求比例或延迟低于阈值的比例。SLO 是一个时间窗口内对 SLI 的目标。错误预算等于允许的不可靠比例，例如 99.9% 可用性目标对应 0.1% 的预算。预算充足时可以提高发布速度；预算持续耗尽时应暂停高风险变更并优先处理可靠性。

## 四类黄金信号与 RED

黄金信号包括延迟、流量、错误和饱和度。面向请求的服务常使用 RED：Rate、Errors、Duration。告警应尽量基于用户影响和错误预算消耗率，而不是单一 CPU 阈值；仪表盘用于探索，告警用于触发行动，每条告警都应有负责人、严重级别和运行手册。

## 日志、指标、链路和拓扑

OpenTelemetry 的核心信号是 traces、metrics、logs 和 baggage。结构化日志需要稳定字段，而不只是合法 JSON；trace_id 和 span_id 可把日志与分布式链路关联。AIOps 数据层应统一 service.name、deployment.environment、版本与资源属性，避免同一服务在不同平台使用不可对齐的名称。

## 参考资料

- Google，《Site Reliability Engineering》《The Site Reliability Workbook》《Building Secure & Reliable Systems》，均可在线阅读：https://sre.google/books/
- OpenTelemetry Observability Primer，https://opentelemetry.io/docs/concepts/observability-primer/
- OpenTelemetry Semantic Conventions，https://opentelemetry.io/docs/concepts/semantic-conventions/
