from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .model import ToolCall, ToolResult

# 所有工具都接收模型传来的参数字典，并返回可写进 observation 的字符串。
ToolFunc = Callable[[dict[str, Any]], str]


@dataclass
class Tool:
    """注册到 agent harness 的一个可调用工具。"""

    name: str
    description: str
    run: ToolFunc


def echo(args: dict[str, Any]) -> str:
    """最小示例工具：原样返回 text 参数。"""

    return str(args.get("text", ""))


class ToolRegistry:
    """管理工具名到 Python 函数的映射。"""

    def __init__(self) -> None:
        # 注册表是模型工具名和本地 Python 函数之间的边界。
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """把一个工具加入注册表，供后续模型调用。"""

        self._tools[tool.name] = tool

    def run(self, call: ToolCall) -> ToolResult:
        """根据模型给出的 ToolCall 查找并执行对应工具。"""

        tool = self._tools.get(call.name)
        if tool is None:
            return ToolResult(
                tool_call_id="not_found_1",
                content="查无此函数",
                is_error=True,
            )

        return ToolResult(tool_call_id=call.id, content=tool.run(call.arguments))


def default_tools() -> ToolRegistry:
    """创建默认工具集合。当前只注册 echo，方便理解完整调用链。"""

    registry = ToolRegistry()
    registry.register(tool=Tool(name="echo", description="返回当前输入内容", run=echo))

    return registry
