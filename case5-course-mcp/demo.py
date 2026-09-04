"""不启动 MCP 服务时的本地查询演示。"""

from __future__ import annotations

import json

from server import get_course, list_assignments, query_course_information


def show(title: str, data: object) -> None:
    print(f"\n=== {title} ===")
    print(json.dumps(data, ensure_ascii=False, indent=2))


show("自然语言：张伟老师教什么课", query_course_information("张伟老师教什么课"))
show("课程详情：CS205", get_course("CS205"))
show("作业查询：CS205", list_assignments("CS205"))
