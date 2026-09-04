# Codex 接入说明

本机 Codex 配置已新增以下 MCP Server：

```toml
[mcp_servers.course_information]
command = ".venv/bin/python"
args = ["server.py"]
cwd = "/Users/zhangligong/Downloads/李老师作业/Case5/课程信息MCP项目"
startup_timeout_sec = 30
```

配置同时保存在 `mcp_config.toml`，便于提交和复现。将项目移动到其他位置时，需要同步修改 `cwd`。

重启 Codex 后，可以用自然语言发起查询，例如：

```text
张伟老师教什么课？
CS205 有什么作业？
查询计算机科学学院的课程。
```

Codex 会根据工具描述选择 `query_course_information`、`get_course` 或 `list_assignments` 等 MCP Tools，再基于数据库返回结果作答。
