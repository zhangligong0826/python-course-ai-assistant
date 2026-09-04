"""课程信息 SQLite MCP Server。通过 stdio 提供给 Codex 或其他 MCP 客户端。"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

PROJECT_DIR = Path(__file__).resolve().parent
DB_PATH = PROJECT_DIR / "courses.db"

mcp = FastMCP(
    "Course Information MCP",
    instructions="Use the course tools to answer questions about courses, teachers, and assignments. Return only data found in courses.db.",
)


def connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    """Create the fixed schema and seed a small, repeatable teaching dataset."""
    with connection() as conn:
        conn.executescript(
            """
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                department TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                teacher_id INTEGER NOT NULL REFERENCES teachers(id),
                credits INTEGER NOT NULL CHECK (credits > 0),
                schedule TEXT NOT NULL,
                capacity INTEGER NOT NULL CHECK (capacity > 0)
            );
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY,
                course_id INTEGER NOT NULL REFERENCES courses(id),
                title TEXT NOT NULL,
                due_date TEXT NOT NULL,
                description TEXT NOT NULL
            );
            """
        )
        conn.executemany(
            "INSERT OR IGNORE INTO teachers (id, name, department, email) VALUES (?, ?, ?, ?)",
            [
                (1, "张伟", "计算机科学学院", "zhang.wei@example.edu"),
                (2, "李娜", "外国语学院", "li.na@example.edu"),
                (3, "王强", "数学学院", "wang.qiang@example.edu"),
            ],
        )
        conn.executemany(
            "INSERT OR IGNORE INTO courses (id, code, name, teacher_id, credits, schedule, capacity) VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                (1, "CS101", "Python 程序设计", 1, 3, "周一 1-2 节 / 周三 3-4 节", 60),
                (2, "CS205", "数据库系统", 1, 3, "周二 1-2 节 / 周四 3-4 节", 45),
                (3, "EN102", "学术英语写作", 2, 2, "周三 5-6 节", 40),
                (4, "MA201", "线性代数", 3, 4, "周一 5-6 节 / 周五 1-2 节", 80),
            ],
        )
        conn.executemany(
            "INSERT OR IGNORE INTO assignments (id, course_id, title, due_date, description) VALUES (?, ?, ?, ?, ?)",
            [
                (1, 1, "Python 成绩管理程序", "2026-09-20", "使用函数和文件读写完成学生成绩管理。"),
                (2, 2, "课程数据库设计", "2026-09-25", "绘制 ER 图并实现课程选课相关表。"),
                (3, 3, "英文摘要改写", "2026-09-18", "将指定研究摘要改写为 200 词学术英语。"),
                (4, 4, "矩阵运算练习", "2026-09-22", "完成矩阵秩、逆矩阵和线性方程组题目。"),
            ],
        )


def rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict[str, Any]]:
    return [dict(row) for row in rows]


def find_courses(keyword: str = "") -> list[dict[str, Any]]:
    keyword = keyword.strip()
    query = """
        SELECT c.code, c.name, c.credits, c.schedule, c.capacity,
               t.name AS teacher, t.department
        FROM courses c JOIN teachers t ON t.id = c.teacher_id
    """
    params: tuple[str, ...] = ()
    if keyword:
        query += " WHERE c.code LIKE ? OR c.name LIKE ? OR t.name LIKE ? OR t.department LIKE ?"
        value = f"%{keyword}%"
        params = (value, value, value, value)
    query += " ORDER BY c.code"
    with connection() as conn:
        return rows_to_dicts(conn.execute(query, params).fetchall())


@mcp.tool()
def list_courses(keyword: str = "") -> list[dict[str, Any]]:
    """列出课程；keyword 可使用课程代码、课程名、教师名或学院名称进行筛选。"""
    return find_courses(keyword)


@mcp.tool()
def get_course(course_code: str) -> dict[str, Any]:
    """按课程代码查询一门课程的详细信息，例如 CS101 或 MA201。"""
    with connection() as conn:
        row = conn.execute(
            """
            SELECT c.code, c.name, c.credits, c.schedule, c.capacity,
                   t.name AS teacher, t.department, t.email AS teacher_email
            FROM courses c JOIN teachers t ON t.id = c.teacher_id
            WHERE UPPER(c.code) = UPPER(?)
            """,
            (course_code.strip(),),
        ).fetchone()
    return dict(row) if row else {"message": f"未找到课程：{course_code}"}


@mcp.tool()
def list_teachers(keyword: str = "") -> list[dict[str, Any]]:
    """查询教师信息；keyword 可使用教师姓名或学院名称筛选。"""
    query = "SELECT name, department, email FROM teachers"
    params: tuple[str, ...] = ()
    if keyword.strip():
        query += " WHERE name LIKE ? OR department LIKE ?"
        value = f"%{keyword.strip()}%"
        params = (value, value)
    query += " ORDER BY name"
    with connection() as conn:
        return rows_to_dicts(conn.execute(query, params).fetchall())


@mcp.tool()
def list_assignments(course_code: str = "") -> list[dict[str, Any]]:
    """查询作业；不传 course_code 返回全部作业，传入代码如 CS205 则只返回该课程作业。"""
    query = """
        SELECT c.code AS course_code, c.name AS course_name, a.title, a.due_date, a.description
        FROM assignments a JOIN courses c ON c.id = a.course_id
    """
    params: tuple[str, ...] = ()
    if course_code.strip():
        query += " WHERE UPPER(c.code) = UPPER(?)"
        params = (course_code.strip(),)
    query += " ORDER BY a.due_date"
    with connection() as conn:
        return rows_to_dicts(conn.execute(query, params).fetchall())


@mcp.tool()
def query_course_information(question: str) -> dict[str, Any]:
    """接收自然语言课程问题，如“张伟老师教什么课”“CS205 有什么作业”“查询计算机学院课程”。"""
    question = question.strip()
    if not question:
        return {"message": "请输入课程、教师或作业相关问题。"}

    code_match = re.search(r"[A-Za-z]{2,}\d{2,}", question)
    code = code_match.group(0) if code_match else ""
    if "作业" in question:
        if code:
            course = get_course(code)
            if "message" in course:
                return {"question": question, "message": course["message"]}
        return {"question": question, "assignments": list_assignments(code)}
    if code:
        return {"question": question, "course": get_course(code), "assignments": list_assignments(code)}

    teacher_match = re.search(r"([\u4e00-\u9fff]{1,4})(?:老师|教师)", question)
    if teacher_match:
        keyword = teacher_match.group(1)
    else:
        keyword = question
        for term in (
            "课程",
            "查询",
            "有哪些",
            "什么",
            "信息",
            "请",
            "帮我",
            "的",
            "学院",
            "老师",
            "教",
        ):
            keyword = keyword.replace(term, "")
        keyword = keyword.strip()
    return {
        "question": question,
        "courses": find_courses(keyword),
        "teachers": list_teachers(keyword),
    }


@mcp.prompt()
def course_assistant() -> str:
    """为智能体提供课程信息查询的使用说明。"""
    return "你是课程信息助手。先根据用户问题调用合适的课程工具，再用中文清晰概括查询结果；不要编造数据库中不存在的信息。"


initialize_database()

if __name__ == "__main__":
    mcp.run(transport="stdio")
