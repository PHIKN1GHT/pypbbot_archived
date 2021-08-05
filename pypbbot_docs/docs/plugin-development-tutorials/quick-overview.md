
# 快速上手

## 一个简单例程

首先，让我们从一个足够简单但具有代表性的例程开始：

!!! example "例程：simple_class_driver.py" 

    ```python linenums="1"
    from pypbbot import app, run_server, BaseDriver
    from pypbbot.utils import sendBackClipsToAndWait


    class SimpleDriver(BaseDriver):
        def onPrivateMessage(self, event):
            message = event.raw_message
            if message.startswith('#echo '):
                sendBackClipsToAndWait(event, message.replace('#echo ', ""))


    app.driver_builder = SimpleDriver

    if __name__ == '__main__':
        run_server(app='__main__:app', host='localhost', port=8082, reload=True)
    ```


在正确安装或克隆本项目后，将上述代码保存为.py 后缀的源代码文件并执行（记得也要按照上一章节的说明启动协议客户端程序），我们就启动了一个对话式 QQ 机器人。试着通过 QQ 对其发送`#echo`加上空格再加上任意字符串的私聊消息后，它就会回复我们相同的内容。

!!! note "提示"

    在克隆本项目后，亦可直接在根目录执行下述命令以运行该例程：

    ```shell
    python -m pypbbot_examples.simple_class_driver
    ```

    本文档的所有例程均保存于`pypbbot_examples`文件夹内，并且都可使用类似上述指令的方式直接执行，稍后不再赘述。

## 发生了什么？

在此例程中，类`SimpleDriver`描述了机器人的全部行为：在收到私聊消息后，对消息文本的前缀进行判断，如果前缀以`"#echo "`字符串开头，那么向事件的发起者进行私聊回复，回复的内容是去掉了这个前缀字符串的消息文本。

在第12行中，脚本程序向 PyPbBot 注册了[驱动器](/getting-started/basic-concepts/#_4)类`SimpleDriver`。稍后只需要调用`run_server`函数即可启动服务。

这个例程仅展示了 PyPbBot 的基本使用方法之一，也即类驱动器法。相信有经验的读者会发现，这种方法固然清晰直观，却难以胜任项目的扩展。因此，实际开发过程中，通常使用更灵活的事务驱动器法。不过，这需要读者对[事务](/getting-started/basic-concepts/#_5)等基本概念有所认知。因此，在开始文档的主体部分前，不妨先阅读下一章节以了解本框架的基本的概念和抽象方法。
