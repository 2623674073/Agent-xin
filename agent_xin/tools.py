from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .model import ToolCall, ToolResult

ToolFunc = Callable[[dict[str, Any]], str]      # Callable表示可调用对象，[[dict[str, Any]]：参数列表，接受一个字典，键是字符串，值是任意类型，最后的str]是返回值类型

@dataclass
class Tool:
    name: str
    description: str
    run: ToolFunc


def echo(args:dict[str, Any])->str:
    return str(args.get("text", ""))


class ToolRegistry:
    def __init__(self) ->None:
        # 注册表是工具名和 Python 函数之间的 harness 边界。
        self._tools:dict[str,Tool] = {}
    
    def register(self,tool:Tool)->None:
        self._tools[tool.name] = tool
    
    def run(self, call:ToolCall):
        tool = self._tools.get(call.name)
        if tool is None:
            return ToolResult(
                tool_call_id="not_found_1",
                content="查无此函数",
                is_error=True,
            )
        return ToolResult(tool_call_id=call.id,content=tool.run(call.arguments))    # tool.run 就是取到函数对象本身


def default_tools() -> ToolRegistry:

    registry = ToolRegistry()
    registry.register(tool=Tool(name="echo",description="返回当前输入内容",run=echo))

    return registry
