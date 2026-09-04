# 第 3 章 函数

## 学习目标

理解函数定义、参数、返回值和局部作用域；能够把重复逻辑拆成可测试的小函数。

## 定义与调用

使用 \`def\` 定义函数，参数是输入，\`return\` 是输出。没有显式 \`return\` 时函数返回 \`None\`。

    def rectangle_area(width: float, height: float) -> float:
        """返回矩形面积。"""
        return width * height

    print(rectangle_area(3, 4))

参数可以设置默认值，也可以使用关键字参数。可变对象作为默认参数会在多次调用间共享，不应写成 \`def f(items=[]):\`；应使用 \`None\` 后在函数体内创建新列表。

## 作用域

函数内部创建的名称默认是局部变量。函数可以读取外层变量，但修改外层变量需要 \`global\` 或 \`nonlocal\`。课程练习中应优先通过参数和返回值传递数据，减少隐式状态。

    def mean(values: list[float]) -> float:
        if not values:
            raise ValueError("values cannot be empty")
        return sum(values) / len(values)

函数应尽量保持单一职责，并为边界输入定义行为。递归函数必须有明确的基准条件和规模缩小步骤。

## 易错点

- 忘记调用括号，写成 \`result = mean\` 而不是 \`mean(values)\`。
- 计算完成后只 \`print\` 不 \`return\`，导致调用者拿到 \`None\`。
- 修改列表参数造成调用方数据被意外改变。
- 递归缺少基准条件，导致 \`RecursionError\`。

## 小结

把函数看成“输入到输出的契约”：先写参数、返回值和异常条件，再实现内部步骤。这样更容易单元测试和复用。
