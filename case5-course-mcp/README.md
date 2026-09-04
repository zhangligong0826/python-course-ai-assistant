# 课程信息 MCP Server

本项目使用 Python、SQLite 和 MCP Python SDK 实现本地课程信息查询服务。首次导入 `server.py` 时会自动创建 `courses.db`，其中包含课程表、教师表和作业表及示例数据。

## MCP Tools

| Tool | 用途 |
| --- | --- |
| `list_courses` | 按课程、教师或学院查询课程 |
| `get_course` | 按课程代码查询课程详情 |
| `list_teachers` | 查询教师信息 |
| `list_assignments` | 查询课程作业 |
| `query_course_information` | 接收中文自然语言问题并返回匹配课程信息 |

## 使用 uv 运行

```bash
uv sync
uv run python demo.py
uv run pytest -q
uv run python server.py
```

最后一条命令以 stdio MCP Server 方式运行，不能直接在终端输入聊天文本；应由 Codex 等 MCP 客户端调用。

## 接入 Codex

1. 打开 `mcp_config.toml`，确认 `cwd` 是本项目的实际绝对路径。
2. 将该文件中的 `[mcp_servers.course_information]` 配置合并进 `~/.codex/config.toml`。
3. 重启 Codex。
4. 在 Codex 对话中输入：`张伟老师教什么课？` 或 `CS205 有什么作业？`。

## 示例查询

```text
张伟老师教什么课？
CS205 有什么作业？
查询计算机科学学院的课程
MA201 的上课时间是什么？
```
