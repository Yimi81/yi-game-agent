import os
from argparse import ArgumentParser
import gradio as gr
from yi_game_agent.indoor_design_agent import create_agent
from llama_index.core.llms import ChatMessage

def respond(
    message,
    history,
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append(ChatMessage(role="user", content=human))
        history_openai_format.append(ChatMessage(role="assistant", content=assistant))

    response = bot.stream_chat(message, chat_history=history_openai_format)

    output = ""
    for new_token in response.response_gen:
        if new_token != "":
            output += new_token
            yield output


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

    bot = create_agent()

    demo.launch(
        server_name=args.server_name,
        server_port=args.server_port,
        inbrowser=args.inbrowser,
        share=args.share,
    )
