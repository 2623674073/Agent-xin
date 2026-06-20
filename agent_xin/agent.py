from __future__ import annotations

from dataclasses import dataclass

from .model import MockProvider
from .tools import ToolRegistry


@dataclass
class AgentResult:
    """Agent 运行结束后交给 CLI 展示的结果。"""

    # final 是最终回复；trace 记录中间步骤，便于学习 agent 如何调用工具。
    final: str
    trace: list[str]


def run_agent(prompt: str, provider: MockProvider, tools: ToolRegistry) -> AgentResult:
    """执行一个最小 agent 循环：模型决定工具调用，工具结果再交回模型。"""

    # messages 是模型上下文。每次工具执行后的 observation 都会追加进来。
    messages = [{"role": "user", "content": prompt}]
    trace: list[str] = []

    response = provider.complete(messages=messages)

    for call in response.tool_calls or []:
        trace.append(f"tool_call:{call.name} {call.arguments}")

        result = tools.run(call)
        trace.append(f"observation: {result.content}")
        # 工具结果会成为下一轮模型调用的 observation
        messages.append(
            {
                "role": "tool",
                "tool_call_id": result.tool_call_id,
                "content": result.content,
            }
        )

        response = provider.complete(messages=messages)

    final = response.text or ""
    trace.append(f"final: {final}")

    return AgentResult(final=final, trace=trace)
