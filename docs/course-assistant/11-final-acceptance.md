# 最终验收记录（2026-09-04）

本记录只声明本轮实际执行的结果，覆盖旧报告中的历史环境说明不作为本次结论依据。

## 环境与隔离

- Open WebUI：隔离 SQLite / `DATA_DIR`，未改写 `backend/data-current`。
- 知识库：`Python 程序设计知识库`，原生 collection 内 **10/10** 资料；嵌入模型 `BAAI/bge-small-zh-v1.5`。
- 模型：`python-course-assistant`，基座 `deepseek-v4-flash`，绑定 collection、Citation、8091 题库和 8092 检索工具。
- 服务：FastAPI 题库与检索工具均提供 `/health`、`/openapi.json`；健康检查 operationId 分别为 `quiz_health`、`rag_health`。

## 自动化与接口验收

| 项目 | 实际结果 | 结论 |
| --- | --- | --- |
| 题库服务测试 | `16 passed` | 通过 |
| 轻量检索服务测试 | `6 passed` | 通过 |
| 课程前端聚焦 Vitest | `8 passed` | 通过 |
| 原生 collection 查询 | 返回 `04-containers.md` 等来源片段 | 通过 |
| 保存会话知识库调用 | `query_knowledge_files`、`kb_exec` 后生成回答 | 通过 |
| 保存会话抽题调用 | `generate_quiz_quiz_generate_post` 完成 | 通过 |
| 保存会话判分调用 | `grade_quiz_quiz_grade_post` + `course-grade` 完成 | 通过 |
| 工具性能（20 次） | 8091 P95 **3.0 ms**；8092 P95 **2.9 ms** | 通过（目标 ≤300 ms） |

固定 15 条保存会话的完整输入、工具轨迹、输出摘要和通过结论在隔离运行报告 `/private/tmp/course_assistant_15_scenarios.json` 生成；本轮为 **15/15 通过**。其摘要见 `evidence/2026-09-04-15-scenarios.md`。

## 同题集优化前后对比

| 版本 | 输入 | 可验证课程证据 | 结果 |
| --- | --- | --- | --- |
| 基线：未配置的 `deepseek-v4-flash` | 同一固定 15 条 | 0/15：请求不含课程提示词、知识库、Citation 或 `tool_ids` | 15/15 有普通文本响应，但不能验证资料依据、工具调用或判分结构 |
| 优化后：`python-course-assistant` | 同一固定 15 条 | 15/15：保存会话中有检索/工具/范围或诚信证据 | 15/15 通过 |

这项比较衡量的是课程增强带来的**可验证性与工作流覆盖**，不把它解释为基座模型的一般知识能力高低。

## 前端验收

- 课程入口严格由 `meta.courseAssistant=true` 开关；无该标记继续走既有 `Suggestions` 与通用 Quick Actions。
- 三张卡分别注入检索问答、题库抽题、提交答案提示词。
- 生成期间按提示词显示“检索课程资料 / 生成练习题 / 判分并生成复习建议”状态。
- 真实判分回复中的 `correct/wrong/missing` 题号数组已被归一化为统计数与逐题标签；数值格式也受支持；格式异常则 Markdown 原样回退。

本机未提供可供自动化控制的浏览器（Computer Use 返回“无可用浏览器”），因此没有伪造页面截图。`evidence/screenshots.md` 记录了这一限制及可复现截图步骤；组件级验收与开发服务器编译已完成。生产 `npm run build` 会在本仓库既有大体积构建阶段因 Node 堆内存耗尽而中止，未伪报为通过。部署到可登录的浏览器后，按 `3-minute-demo.md` 可在约 3 分钟完成三张截图复核。

## 已修复缺陷

两个 OpenAPI 服务均有 `/health`，FastAPI 默认会生成相同的 `health_health_get` operationId。DeepSeek 会因此拒绝整个工具列表（“Tool names must be unique”）。现已固定为 `quiz_health` 和 `rag_health`，并在两套服务测试中加回归断言；修复后 15 条真实会话全部通过。

## 非阻塞基线问题

全仓 `npm run check` 仍报告大量既有类型错误（主要分布在无关的富文本、鉴权等目录），不能作为本次改动的有效质量门禁；本次新增/修改文件经过聚焦 Vitest 与 Prettier 检查。未将这一基线问题伪报为通过。
