# 第 5 章 文件与异常

## 学习目标

安全读写文本文件，理解编码和上下文管理器；能够捕获预期异常并给出有用反馈。

## 文件读写

使用 \`with open(...)\` 可在代码块结束时自动关闭文件。文本文件应显式指定编码，课程示例统一使用 UTF-8。\`"r"\` 读取、\`"w"\` 覆盖写入、\`"a"\` 追加写入。

    from pathlib import Path

    path = Path("scores.txt")
    path.write_text("Alice,90\nBob,82\n", encoding="utf-8")
    with path.open(encoding="utf-8") as file:
        rows = [line.strip().split(",") for line in file if line.strip()]
    print(rows)

写入前要确认是否允许覆盖原文件。对于大文件，优先逐行处理，而不是一次性 \`read()\` 载入全部内容。

## 异常处理

\`try\` 放可能失败的代码，\`except\` 只捕获能够处理的异常类型；\`else\` 在没有异常时执行，\`finally\` 无论是否异常都会执行。不要使用裸 \`except:\` 隐藏程序错误。必要时用 \`raise ValueError(...) from exc\` 补充业务语义。

    def parse_score(text: str) -> int:
        try:
            score = int(text)
        except ValueError as exc:
            raise ValueError("score must be an integer") from exc
        if not 0 <= score <= 100:
            raise ValueError("score must be between 0 and 100")
        return score

## 易错点

- 相对路径基于当前工作目录，不一定是脚本所在目录。
- 使用 \`w\` 模式误覆盖已有内容。
- 捕获 \`Exception\` 后不记录上下文。
- 忘记处理文件不存在、权限不足和编码错误。

## 小结

文件操作应包含路径、编码、模式和异常策略。异常处理的目标是恢复或清晰报告，而不是让错误静默消失。
