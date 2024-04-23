from jinja2 import Template
from promptflow import tool
from promptflow.connections import CustomStrongTypeConnection
from promptflow.contracts.types import PromptTemplate, Secret

from promptflow.tools.common import render_jinja_template, parse_chat

import anthropic

class ClaudeConnection(CustomStrongTypeConnection):
    """My custom strong type connection.

    :param api_key: The api key get from "https://xxx.com".
    :type api_key: Secret
    :param api_base: The api base.
    :type api_base: String
    """
    api_key: Secret
    api_base: str = "This is a fake api base."

@tool
def generate(
    connection: ClaudeConnection,
    prompt: PromptTemplate,
    model: str = "claude-3-opus-20240229",
    temperature: float  = 1,
    top_p: float = 1.0,
    max_tokens: int = 1024,
    **kwargs
) -> str:
    
    # Replace with your tool code, customise your own code to handle and use the prompt here.
    # Usually connection contains configs to connect to an API.
    # Not all tools need a connection. You can remove it if you don't need it.
    prompt = render_jinja_template(prompt, trim_blocks=True, keep_trailing_newline=True, **kwargs)
    messages = parse_chat(prompt)

    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=connection.api_key,
    )

    system = ''
    updatedMessages = []

    for i in messages:
        if i['role'] == 'system':
            system = i['content']
        else:
            updatedMessages.append(i)

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        system=system,
        messages=updatedMessages
    )

    response = ''
    for txt in message.content:
        response = response + txt.text

    return response