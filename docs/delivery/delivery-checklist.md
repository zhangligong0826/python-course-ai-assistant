# AIOps 课程助教最终交付清单

## 一、核心交付材料

| 材料 | 路径 | 状态 |
| --- | --- | --- |
| 项目总结报告 | docs/delivery/project-summary-report.md | 已完成 |
| 系统测试与评价报告 | docs/delivery/system-test-report.md | 已完成 |
| 优化后 T01–T15 原始输出 | docs/delivery/evidence/T01-T15-actual-evidence.md | 已完成 |
| 优化前 T01–T05 基线输出 | docs/delivery/evidence/baseline-T01-T05-actual-evidence.md | 已完成 |
| 代表性 Open-WebUI 截图 | docs/images/ | 已完成 |
| 测试过程截图 | docs/delivery/evidence/ | 已完成 |

## 二、项目功能核对

| 检查项 | 结论 | 依据 |
| --- | --- | --- |
| AIOps 知识库 | 已完成 | course-materials/aiops/ |
| DeepSeek 模型接入 | 已完成 | Open WebUI 模型配置 |
| 课程系统提示词 | 已完成 | AIOps 课程提示词 |
| Citation 引用 | 已验证 | T01–T06、T14 等记录 |
| 题库生成 | 已验证 | T09 |
| 题库判分 | 已验证 | T10 |
| RAG 检索 | 已接入 | python-course-rag |
| 异常输入处理 | 已验证 | T07 |
| 知识库范围外处理 | 已验证 | T14 |
| 高风险运维边界 | 已验证 | T15 |

## 三、测试材料核对

- [x] T01–T15 均有真实 AI 输出原文；
- [x] 六类测试维度均有覆盖；
- [x] T01–T05 已完成优化前基线对比；
- [x] 已记录通过、部分通过和不通过判定；
- [x] 已记录 T05 的资料覆盖限制；
- [x] 已保留 docs/images/ 下的项目演示用 Open-WebUI 截图；
- [x] 已保留 docs/delivery/evidence/ 下的 T03、T14 测试过程截图；
- [ ] 补齐测试时间；
- [ ] 补齐测试人员；
- [ ] 如学校要求，补充 T09/T10 原始工具日志；
- [ ] 如学校要求，补充更多 Citation 展开截图。

## 四、提交前注意事项

1. 提交正式报告、项目总结报告和 evidence 目录，不提交已删除的中间草稿。
2. 不要把 T01–T05 基线输出与优化后 T01–T15 输出混在同一结论表中。
3. 报告中使用“14 条通过、1 条部分通过、0 条不通过”的统一结论。
4. 不要把 T05 写成完全基于课程资料的 PromQL 语法教学。
5. 检查截图和文本证据中不包含账号密码、API 密钥或其他敏感信息。
