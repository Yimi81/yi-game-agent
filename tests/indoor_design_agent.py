import json
from typing import Sequence, List

from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.agent.openai import OpenAIAgent


aoai_api_key = "3d97a348a4a24119ac590d12a4751509"
aoai_endpoint = "https://ai2team.openai.azure.com/"
aoai_api_version = "2024-06-01"


def add(a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    return a + b


add_tool = FunctionTool.from_defaults(fn=add)


def useless_tool() -> int:
    """This is a useless tool."""
    return "This is a useless output."


useless_tool = FunctionTool.from_defaults(fn=useless_tool)


def create_agent() -> OpenAIAgent:
    llm = AzureOpenAI(
        engine="ai2team-gpt4o-standard",
        model="gpt-4o",
        api_key=aoai_api_key,
        azure_endpoint=aoai_endpoint,
        api_version=aoai_api_version,
    )

    agent = OpenAIAgent.from_tools([useless_tool, add_tool], llm=llm, verbose=True)
    return agent


if __name__ == "__main__":
    agent = create_agent()

    response = agent.chat("What is 5 + 2?", tool_choice="auto")

    print(response)
