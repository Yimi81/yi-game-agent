import os
from argparse import ArgumentParser
import gradio as gr

import yi_game_agent
from yi_game_agent.message import Msg
from yi_game_agent.agents import FnCallAgent

from yi_game_agent.tools import (
    ServiceToolkit,
    ServiceResponse,
    ServiceExecStatus,
    get_weather,
)


def respond(
    message,
    history,
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    # 调用代理，获取响应。可能是单一消息，也可能是一个流式生成器。
    response_or_gen = bot(Msg(name="user", role="user", content=message))

    # 如果返回的不是生成器，说明是一次性输出
    if isinstance(response_or_gen, Msg):
        yield response_or_gen.content
    else:
        for msg_chunk in response_or_gen:
            yield msg_chunk.content


"""
For information on how to customize the ChatInterface, peruse the gradio docs: https://www.gradio.app/docs/chatinterface
"""
demo = gr.ChatInterface(
    respond,
    additional_inputs=[
        gr.Textbox(value="You are a friendly Chatbot.", label="System message"),
        gr.Slider(minimum=1, maximum=8192, value=4096, step=1, label="Max new tokens"),
        gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(
            minimum=0.1,
            maximum=1.0,
            value=0.95,
            step=0.05,
            label="Top-p (nucleus sampling)",
        ),
    ],
)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--share",
        action="store_true",
        default=False,
        help="Create a publicly shareable link for the interface.",
    )
    parser.add_argument(
        "--inbrowser",
        action="store_true",
        default=True,
        help="Automatically launch the interface in a new tab on the default browser.",
    )
    parser.add_argument(
        "--server-port", type=int, default=8333, help="Demo server port."
    )
    parser.add_argument(
        "--server-name", type=str, default="0.0.0.0", help="Demo server name."
    )

    args = parser.parse_args()

    qwen_model_config = {
        "config_name": "qwen2.5-14b-chat",
        "model_type": "openai_chat",
        "model_name": "qwen2.5-14b",
        "api_key": "test",
        "stream": True,
        "client_args": {
            "base_url": "http://localhost:8000/v1",
        },
    }

    deepseek_model_config = {
        "config_name": "deepseek-chat",
        "model_type": "openai_chat",
        "model_name": "deepseek-chat",
        "api_key": "sk-90bb5d4f19cb40008658523cc58ea7f5",
        "client_args": {
            "base_url": "https://api.deepseek.com",
        },
        "stream": False,
    }

    kimi_model_config = {
        "config_name": "kimi-chat",
        "model_type": "openai_chat",
        "model_name": "moonshot-v1-8k",
        "api_key": "sk-Z2oDnJORljxciPYHj45taQ8obz18uM5y0X9SWD3b3YmgsaTk",
        "client_args": {
            "base_url": "https://api.moonshot.cn/v1",
        },
        "stream": False,
    }

    yi_model_config = {
        "config_name": "yi-chat",
        "model_type": "openai_chat",
        "model_name": "yi-large-fc",
        "api_key": "f72a48de1f8d45cebd88c16273af6b4d",
        "client_args": {
            "base_url": "https://api.lingyiwanwu.com/v1",
        },
        "stream": False,
    }

    qwen_office_model_config = {
        "config_name": "qwen-office-chat",
        "model_type": "openai_chat",
        "model_name": "qwen-plus",
        "api_key": "sk-fc0300ba2aef4a48ab9bb9474d6b7077",
        "stream": False,
        "client_args": {
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        },
    }

    yi_game_agent.init(model_configs=[qwen_office_model_config, deepseek_model_config, yi_model_config])

    service_toolkit = ServiceToolkit()

    service_toolkit.add(get_weather)

    bot = FnCallAgent(
        name="Guofeng Yi",
        model_config_name="qwen-office-chat",
        sys_prompt="You are a helpful assistant",
        service_toolkit=service_toolkit,
    )

    demo.launch(
        server_name=args.server_name,
        server_port=args.server_port,
        inbrowser=args.inbrowser,
        share=args.share,
    )
