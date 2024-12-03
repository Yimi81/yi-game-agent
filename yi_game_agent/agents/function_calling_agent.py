from typing import Optional, Union, Sequence

from yi_game_agent.agents import AgentBase
from yi_game_agent.message import Msg
from yi_game_agent.tools import ServiceToolkit, ServiceResponse, ServiceExecStatus


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

    def reply(self, x: Optional[Union[Msg, Sequence[Msg]]] = None) -> Msg:
        """The reply method of the agent"""
        self.memory.add(x)

        prompt = self.model.format(
            Msg("system", self.sys_prompt, role="system"),
            self.memory and self.memory.get_memory() or x,  # type: ignore[arg-type]
        )

        tools = []
        for tool in self.service_toolkit.service_funcs.keys():
            tools.append(self.service_toolkit.json_schemas[tool])

        response = self.model(self.name, prompt, tools=tools)

        # msg = Msg(self.name, response.text, role="assistant")
        
        msg = response.message
        if self.memory:
            self.memory.add(msg)
        
        tool_calls = self.model.get_tool_calls_from_response(response, error_on_no_tool_call=False)

        if self.verbose:
            self.speak(response.stream or response.text)
        return msg
