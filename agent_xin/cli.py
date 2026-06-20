from __future__ import annotations # 导入未来版本的注解功能，允许在函数定义中使用类型提示

import typer    # 用于构建命令行界面（CLI）的库
from rich.console import Console    # 用于在终端中美化输出的库

from .agent import run_agent
from .model import MockProvider
from .tools import default_tools


console = Console() # 创建一个Rich Console实例，用于在终端中输出美化的文本

app = typer.Typer(add_completion=False) # 创建一个Typer应用实例，add_completion=False表示不添加自动补全功能


@app.callback(invoke_without_command=True)  # 装饰器，表示这个函数是一个可调用的命令    
def main_command(prompt: str = typer.Argument("hi")) -> None:
    """
    Main command for the CLI. It takes a prompt as input and sends it to the agent.
    """

    # 这里可以添加代码将提示发送给代理并处理响应
    # provider = MockProvider()
    # response = provider.complete(prompt=prompt)
    # console.print(f"输出：{response.text}")

    result = run_agent(prompt=prompt, provider=MockProvider(), tools=default_tools())
    for line in result.trace:
        console.print(line)

def main():
    app() # 启动Typer应用，等待用户输入命令 