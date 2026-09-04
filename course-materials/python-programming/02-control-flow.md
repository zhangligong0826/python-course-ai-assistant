# 第 2 章 流程控制

## 学习目标

使用条件分支和循环表达程序的选择与重复；能够处理边界条件，并避免死循环。

## 条件分支

\`if\`、\`elif\`、\`else\` 根据布尔表达式选择路径。代码块由缩进表示，建议统一使用 4 个空格。多个条件可用 \`and\`、\`or\` 组合。

    score = 86
    if score >= 90:
        level = "A"
    elif score >= 60:
        level = "B"
    else:
        level = "C"
    print(level)

空字符串、空容器、\`0\` 和 \`None\` 在条件中会被视为假；其他对象通常为真。需要表达“等于某值”时使用 \`==\`。

## 循环

\`for\` 适合遍历可迭代对象，\`range(start, stop, step)\` 的 \`stop\` 不包含在范围内。 \`while\` 在条件为真时重复执行，循环体必须改变相关状态。

    total = 0
    for number in range(1, 6):
        total += number
    print(total)  # 15

    count = 3
    while count > 0:
        print(count)
        count -= 1

\`break\` 立即结束当前循环，\`continue\` 跳过本轮剩余代码。嵌套循环中的 \`break\` 只结束最近的一层。

## 易错点

- 忘记 \`range\` 的右边界不包含。
- \`while\` 中不更新计数器造成死循环。
- 把 \`break\` 误认为结束所有嵌套循环。
- 条件顺序不合理，导致分支永远无法到达。

## 小结

先写清楚循环不变量和终止条件，再实现循环体。边界值、空输入和只有一项的情况必须单独思考。
