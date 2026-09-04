# 第 4 章 容器

## 学习目标

根据数据关系选择列表、元组、字典或集合；掌握索引、切片、遍历和推导式。

## 列表与元组

列表有序且可变，支持 \`append\`、\`extend\`、\`pop\` 和切片。索引从 0 开始，负索引从末尾开始。元组有序但不可变，适合表示不应被修改的固定记录。

    scores = [72, 88, 95]
    scores.append(81)
    print(scores[1:3])  # [88, 95]
    point = (3, 4)

切片 \`items[start:stop:step]\` 不会包含 \`stop\`。对空列表访问 \`items[0]\` 会产生 \`IndexError\`，需要先判断长度或使用迭代。

## 字典与集合

字典存储键值映射，键必须可哈希。\`mapping.get(key, default)\` 可避免访问不存在键时抛出 \`KeyError\`。集合无序且元素不重复，适合去重和集合运算。

    counts = {}
    for word in ["a", "b", "a"]:
        counts[word] = counts.get(word, 0) + 1
    unique = set(["a", "b", "a"])
    print(counts, unique)

## 推导式

推导式适合简单的映射或筛选；逻辑复杂时应改写为普通循环或函数，以保持可读性。

    even_squares = [n * n for n in range(6) if n % 2 == 0]

## 易错点

- 混淆列表的 \`append\`（添加一个元素）和 \`extend\`（添加多个元素）。
- 遍历字典时直接修改其键集合。
- 假定集合保持输入顺序。
- 复制嵌套列表时误用浅拷贝造成共享内部对象。

## 小结

先问“是否有顺序”“是否允许重复”“是否按键查找”“是否需要修改”，再选择容器。
