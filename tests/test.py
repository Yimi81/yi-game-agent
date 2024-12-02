import yi_game_agent
from yi_game_agent.agents import DialogAgent
from yi_game_agent.message import Msg

from yi_game_agent.tools import ServiceToolkit, ServiceResponse

def web_serarch(query: str, engine: str, api_key: str, num_results: int = 10):
    """
    Search the web using the given search engine.

    Args:
        query: The query string.
        engine: The search engine to use.
        api_key: The API key for the search engine.
        num_results: The number of results to return.

    Returns:
        List[str]: The search results.
    """
    # Search the web using the given search engine
    print(f"Searching the web using {engine} with query: {query} and API key: {api_key}")

service_toolkit = ServiceToolkit()

service_toolkit.add(
    web_serarch,
    api_key="xxx",
    num_results=3
)

# print(service_toolkit.json_schemas)
tools = []

for tool in service_toolkit.service_funcs.keys():
    tools.append(service_toolkit.json_schemas[tool])
print(tools)
# qwen_model_config = {
#     "config_name": "qwen2.5-14b-chat",
#     "model_type": "openai_chat",
#     "model_name": "qwen2.5-14b",
#     "api_key": "test",
#     "client_args": {
#         "base_url": "http://localhost:8000/v1",
#     },
#     "stream": True
# }

# azure_model_config = {
#     "api_base": "https://ai2team.openai.azure.com/",
#     "api_key": "3d97a348a4a24119ac590d12a4751509",
#     "api_version": "2024-06-01",
#     "config_name": "gpt4o-mini",
#     "model_type": "litellm_chat",
#     "model_name": "azure/ai2team-gpt4o",
#     "stream": True
# }

# yi_game_agent.init(model_configs=[qwen_model_config, azure_model_config])

# agent1 = DialogAgent(name="Guofeng Yi", model_config_name="gpt4o-mini", sys_prompt="You are a new student in Anhui University.")

# response = agent1(Msg(name="user", role="user", content="你好，你是谁, 谁开发的你"))
# print(response.id)