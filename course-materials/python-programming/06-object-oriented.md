# 第 6 章 面向对象

## 学习目标

理解类、对象、属性和方法；能够用封装和继承组织具有共同状态与行为的代码。

## 类与对象

类是对象的模板，\`__init__\` 初始化实例属性，实例方法的第一个参数通常是 \`self\`。类属性由所有实例共享，实例属性属于具体对象。

    class Student:
        def __init__(self, name: str, score: int):
            self.name = name
            self.score = score

        def passed(self) -> bool:
            return self.score >= 60

    alice = Student("Alice", 88)
    print(alice.name, alice.passed())

属性应保持有效状态。可以通过方法限制修改方式，也可以使用 \`@property\` 暴露计算属性。对象方法修改自身状态，纯计算逻辑可设计为不改变对象的函数。

## 继承与多态

子类可以复用父类行为并覆盖方法。调用 \`super()\` 可执行父类实现。多态强调“只要支持所需方法即可使用”，调用方不必依赖具体子类名称。

    class GraduateStudent(Student):
        def passed(self) -> bool:
            return self.score >= 70

继承应表达稳定的“是一种”关系；如果只是共享少量工具逻辑，组合通常比深层继承更简单。

## 易错点

- 忘记在实例方法中写 \`self\`。
- 把实例属性误写成类属性，导致对象之间意外共享状态。
- 子类覆盖方法时参数契约不一致。
- 为了复用代码创建过深的继承层级。

## 小结

先识别对象负责的数据和行为，再决定是否需要类。面向对象不是必须使用的语法，而是帮助管理复杂状态和变化的一种组织方式。
