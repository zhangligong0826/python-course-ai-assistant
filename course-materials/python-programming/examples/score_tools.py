"""可运行的成绩统计示例。"""

from __future__ import annotations


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


if __name__ == "__main__":
    samples = [parse_score(item) for item in ("72", "88", "95")]
    print(summarize(samples))

