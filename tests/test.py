import yi_game_agent
from yi_game_agent.agents import DialogAgent
from yi_game_agent.message import Msg

qwen_model_config = {
    "config_name": "qwen2.5-14b-chat",
    "model_type": "openai_chat",
    "model_name": "qwen2.5-14b",
    "api_key": "test",
    "client_args": {
        "base_url": "http://localhost:8000/v1",
    },
    "stream": True
}

yi_game_agent.init(model_configs=[qwen_model_config])

agent1 = DialogAgent(name="Guofeng Yi", model_config_name="qwen2.5-14b-chat", sys_prompt="You are a new student in Anhui University.")

response = agent1(Msg(name="user", role="user", content="你好，你是谁"))
