from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ToolCall:
    """模型请求 agent harness 执行的工具调用。"""

    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class ToolResult:
    """工具执行完成后返回给模型的 observation。"""

    tool_call_id: str
    content: str
    is_error: bool = False


@dataclass
class ModelResponse:
    """一次模型响应：可以是最终文本，也可以是下一步工具调用。"""

    text: str | None = None
    tool_calls: list[ToolCall] | None = None
    stop_reason: str = "end_trun"


class MockProvider:
    """用于演示的假模型，让项目不依赖真实 LLM 也能跑通 agent 流程。"""

    def complete(self, messages: list[dict[str, str]]) -> ModelResponse:
        """根据最后一条消息模拟模型回复。"""

        last = messages[-1]
        if last["role"] == "user":
            # 第一次看到用户输入时，模型选择调用 echo 工具。
            text = last["content"].replace("用 echo 工具说", "").strip() or last["content"]
            return ModelResponse(
                tool_calls=[
                    ToolCall(
                        id="tool_1",
                        name="echo",
                        arguments={"text": text},
                    )
                ],
                stop_reason="tool_use",
            )

        if last["role"] == "tool":
            # 收到工具 observation 后，模型产出最终文本。
            return ModelResponse(text=f"echo 工具返回：{last['content']}")

        return ModelResponse(text="我现在只能演示 echo 工具。")
