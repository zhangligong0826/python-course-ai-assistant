from __future__ import annotations

import server


def test_database_contains_three_required_tables():
    with server.connection() as conn:
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"courses", "teachers", "assignments"}.issubset(tables)


def test_get_course_returns_teacher_and_schedule():
    course = server.get_course("CS101")
    assert course["name"] == "Python 程序设计"
    assert course["teacher"] == "张伟"
    assert "周一" in course["schedule"]


def test_natural_language_assignment_query():
    result = server.query_course_information("CS205 有什么作业？")
    assert result["assignments"][0]["title"] == "课程数据库设计"


def test_natural_language_query_without_space_still_finds_course():
    result = server.query_course_information("CS205有什么作业")
    assert [item["course_code"] for item in result["assignments"]] == ["CS205"]


def test_natural_language_query_with_chinese_punctuation():
    result = server.query_course_information("MA201的上课时间是什么？")
    assert result["course"]["code"] == "MA201"


def test_single_character_surname_teacher_query():
    result = server.query_course_information("张老师教什么课")
    assert any(course["teacher"] == "张伟" for course in result["courses"])


def test_assignment_query_for_unknown_course_returns_message():
    result = server.query_course_information("CS999 有什么作业？")
    assert "未找到课程" in result["message"]
