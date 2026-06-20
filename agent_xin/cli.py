from __future__ import annotations

import typer
from rich.console import Console

from .agent import run_agent
from .model import MockProvider
from .tools import default_tools


console = Console()

# 这个 CLI 只有一个默认命令；关闭 shell completion 可以让示例保持简单。
app = typer.Typer(add_completion=False)


@app.callback(invoke_without_command=True)
def main_command(prompt: str = typer.Argument("hi")) -> None:
    """把命令行输入交给 agent，并逐行打印运行轨迹。"""

    result = run_agent(prompt=prompt, provider=MockProvider(), tools=default_tools())
    for line in result.trace:
        console.print(line)


def main() -> None:
    """project.scripts 的入口函数。"""

    app()
