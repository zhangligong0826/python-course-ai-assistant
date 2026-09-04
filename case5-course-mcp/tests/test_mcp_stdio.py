from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

PROJECT_DIR = Path(__file__).resolve().parents[1]


async def verify_mcp_tools() -> None:
    parameters = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(PROJECT_DIR))
    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            names = {tool.name for tool in tools.tools}
            assert {"list_courses", "get_course", "list_teachers", "list_assignments", "query_course_information"}.issubset(names)

            response = await session.call_tool("get_course", {"course_code": "CS205"})
            assert "数据库系统" in response.content[0].text


def test_mcp_server_exposes_and_runs_tools():
    asyncio.run(verify_mcp_tools())
