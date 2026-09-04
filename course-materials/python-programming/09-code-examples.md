# Python 示例代码集

## 示例 1：成绩统计

文件：examples/score_tools.py。该示例展示输入校验、列表统计和格式化输出。

    def parse_score(text: str) -> int:
        value = int(text.strip())
        if not 0 <= value <= 100:
            raise ValueError("score out of range")
        return value

    def summarize(scores: list[int]) -> dict[str, float]:
        if not scores:
            return {"count": 0, "average": 0.0, "maximum": 0, "minimum": 0}
        return {
            "count": len(scores),
            "average": sum(scores) / len(scores),
            "maximum": max(scores),
            "minimum": min(scores),
        }

## 示例 2：单词计数

    def count_words(text: str) -> dict[str, int]:
        result: dict[str, int] = {}
        for word in text.lower().split():
            result[word] = result.get(word, 0) + 1
        return result

## 示例 3：安全读取

    from pathlib import Path

    def read_nonempty_lines(path: str) -> list[str]:
        file_path = Path(path)
        with file_path.open(encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]

## 示例说明

每个示例都可以单独导入测试。输入校验函数负责拒绝不合法数据，统计函数负责纯计算，文件函数负责资源管理。助教应先解释调用关系，再根据学生水平决定是否展示完整代码。
