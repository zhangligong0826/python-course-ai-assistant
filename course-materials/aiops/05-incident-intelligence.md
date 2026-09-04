# 智能事故管理：检测、定位、处置与复盘

更新时间：2026-09-04。本文提供一套适合课程实验的 AIOps 事故分析模板。

## 事故时间线

先按统一时区排列发布、配置变更、告警、用户报障和处置动作，标记每条记录的来源与置信度。相关不代表因果：最近一次变更是强线索，但只有当故障时间、影响组件和回滚结果一致时，才能提高根因置信度。

## 根因候选输出

模型应输出最多三个候选，每个候选包含支持证据、反证、还需查询的数据和置信度，不得只给一个确定结论。诊断顺序可按影响面、变更相关性、依赖拓扑、资源饱和、错误模式和历史相似事故展开，优先执行低风险的只读验证。

## 处置与复盘

缓解动作和永久修复必须分开。缓解目标是尽快恢复用户体验，永久修复关注触发条件、逃逸控制和系统性改进。复盘应无责，记录影响、时间线、根因、促成因素、有效与无效动作，并把改进项落实为有负责人和截止时间的任务。

## 推荐阅读

- Google SRE，Monitoring Distributed Systems，https://sre.google/resources/book-update/monitoring-distributed-systems/
- Google SRE，Anatomy of an Incident，https://sre.google/static/pdf/Anatomy_Of_An_Incident.pdf
