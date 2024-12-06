from typing import Optional, Union, Sequence, Generator

from yi_game_agent.agents import AgentBase
from yi_game_agent.message import Msg
from yi_game_agent.tools import ServiceToolkit, ServiceResponse, ServiceExecStatus
from yi_game_agent.llm.base import ModelResponse

class FnCallAgent(AgentBase):
    def __init__(
        self,
        name: str,
        model_config_name: str,
        service_toolkit: ServiceToolkit,
        sys_prompt: str = "You're a helpful assistant named {name}.",
        max_iters: int = 10,
        verbose: bool = True,
    ) -> None:
        super().__init__(
            name=name, sys_prompt=sys_prompt, model_config_name=model_config_name
        )

        self.service_toolkit = service_toolkit
        self.verbose = verbose
        self.max_iters = max_iters

        if not sys_prompt.endswith("\n"):
            sys_prompt = sys_prompt + "\n"

        self.sys_prompt = sys_prompt.format(name=self.name)
        self.memory.add(Msg("system", self.sys_prompt, role="system"))

    def reply(self, x: Optional[Union[Msg, Sequence[Msg]]] = None) -> Union[Msg, Generator[Msg, None, None]]:
        """Agent reply method, now supporting streaming output."""
        self.memory.add(x)

        for _ in range(self.max_iters):
            prompt = self.model.format(
                self.memory and self.memory.get_memory() or x,  # type: ignore[arg-type]
            )

            tools = []
            for tool in self.service_toolkit.service_funcs.keys():
                tools.append(self.service_toolkit.json_schemas[tool])

            response = self.model(self.name, prompt, tools=tools)

            # 如果是流式输出（response是一个生成器）
            if isinstance(response, Generator):
                # 流式处理
                return self._handle_stream(response)
            else:
                # 非流式输出，直接处理工具调用并返回最终消息
                msg = response.message
                self.memory.add(msg)
                tool_calls = response.get_tool_calls()
                if tool_calls:
                    for tool_call in tool_calls:
                        tool_output = self.service_toolkit._call_tool(
                            tool_call=tool_call, verbose=True
                        )
                        function_message = Msg(
                            name=self.name,
                            content=tool_output,
                            role="tool",
                            additional_kwargs={
                                "name": tool_call["function"]["name"],
                                "tool_call_id": tool_call["id"],
                            },
                        )
                        self.memory.add(function_message)
                    # 工具调用后可考虑继续迭代，如果需要
                else:
                    if self.verbose:
                        self.speak(msg.content)
                    return msg

    def _handle_stream(
        self, response_gen: Generator[ModelResponse, None, None]
    ) -> Generator[Msg, None, None]:
        """处理流式输出的生成器。对每块输出检查是否有工具调用，有则执行并将结果回流。"""
        final_message = None
        for chunk_response in response_gen:
            msg = chunk_response.message
            tool_calls = msg.additional_kwargs.get("tool_calls", [])

            # if self.verbose:
            #     self.speak(msg.content)
            yield msg
            final_message = msg

        self.memory.add(final_message)

        return final_message
