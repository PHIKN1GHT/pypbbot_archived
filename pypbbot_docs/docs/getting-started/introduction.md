# 概览

  [PyProtobufBot](https://github.com/PHIKN1GHT/pypbbot)（简称 PyPbBot）是一个使用[Python 语言](https://www.python.org/)实现的，以面向大规模应用为目标的，易于上手与扩展且具有良好效率的[ProtobufBot](https://github.com/ProtobufBot/onebot_idl)协议[服务端](#clientandserver)实现。

!!! 注意 note
    尽管 Python 是一门易于上手的编程语言，使用 PyProtobufBot 进行对话式机器人开发仍需要你对相关基本概念有所了解。建议读者在阅读本文档前，熟悉[Python 语言参考手册](https://docs.python.org/zh-cn/3/reference/index.html)中的全部内容。

PyPbBot 是一个以[FastAPI](https://fastapi.tiangolo.com/)为基础的[异步](https://www.ibm.com/developerworks/cn/linux/l-async/)服务端框架，这意味着在源代码的执行过程中，你可以灵活地创建[协程](https://docs.python.org/zh-cn/3/glossary.html#term-coroutine)以提高效率。（当然，如果你不熟悉异步编程，你也可以像编写普通单线程程序那样使用本框架。）

此外，PyPbBot 针对不同的抽象层次的开发需求分别设计了三种不同的运行模式，其中包括了一个简单而强大的插件引擎，能够支持以插件化的形式对功能进行渐进式扩展，而且支持热重载。

未来，PyPbBot 还将会引入权限控制机制与会话机制，以进一步减轻开发者的抽象负担。

受限于底层实现，PyPbBot 仅支持 Python 3.7 或更高版本。


!!! warning "警告"
    **目前，本项目仍处于早期开发阶段，缺乏文档与测试用例，暂不建议应用于生产环境。**

!!! note "TODOLIST"
    - 测试组件 -> 0.5
    - pypbbot.serve 命令解释器 -> 0.5
    - .env文件解析 -> 0.6
    - 插件市场
    - 权限系统
    - 基础插件
    - 打包分发帮助工具
    - 快照
    - 日志调用