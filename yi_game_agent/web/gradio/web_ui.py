import os
from argparse import ArgumentParser
import gradio as gr

import yi_game_agent
from yi_game_agent.message import Msg
from yi_game_agent.agents import FnCallAgent

from yi_game_agent.tools import ServiceToolkit, ServiceResponse, ServiceExecStatus

def web_serarch(query: str, engine: str, api_key: str, num_results: int = 10) -> ServiceResponse:
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
    data = f"Searching the web using {engine} with query: {query} and API key: {api_key}"

    return ServiceResponse(ServiceExecStatus.SUCCESS, data)
def get_weather(location, unit) -> ServiceResponse:
    """
    Get the weather information for a specified location.

    Args:
        location (str): The location for which to get the weather.
        unit (str): The temperature unit, 'c' for Celsius, 'f' for Fahrenheit.

    Returns:
        dict: A dictionary containing weather information.
    """
    # Validate parameters
    if not isinstance(location, str):
        raise TypeError("location must be a string")
    if unit not in ['c', 'f']:
        raise ValueError("unit must be 'c' or 'f'")

    # Simulate getting weather information
    # In practice, you would call a real weather API here
    sample_weather_data = {
        "location": location,
        "temperature": 20 if unit == 'c' else 68,
        "unit": unit,
        "description": "Clear"
    }

    return ServiceResponse(ServiceExecStatus.SUCCESS, sample_weather_data)


def respond(
    message,
    history,
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    # history_openai_format = []
    # for human, assistant in history:
    #     history_openai_format.append(ChatMessage(role="user", content=human))
    #     history_openai_format.append(ChatMessage(role="assistant", content=assistant))

    response = bot(Msg(name="user", role="user", content=message))

    return response.content


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
        "--server-port", type=int, default=8233, help="Demo server port."
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

    yi_game_agent.init(model_configs=[deepseek_model_config])



    service_toolkit = ServiceToolkit()

    service_toolkit.add(
        web_serarch,
        api_key="xxx",
        num_results=3
    )

    service_toolkit.add(
        get_weather
    )
    bot = FnCallAgent(name="Guofeng Yi", model_config_name="deepseek-chat", sys_prompt="You are a new student in Anhui University.", service_toolkit=service_toolkit)

    demo.launch(
        server_name=args.server_name,
        server_port=args.server_port,
        inbrowser=args.inbrowser,
        share=args.share,
    )
