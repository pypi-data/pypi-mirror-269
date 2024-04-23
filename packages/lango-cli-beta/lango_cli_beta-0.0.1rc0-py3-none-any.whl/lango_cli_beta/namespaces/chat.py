"""
CLI commands
"""

import typer
from rich import print as rich_print

from lango_cli_beta.constants import DEFAULT_CONFIG_PATH
from lango_cli_beta.rag.chat import Chat
from lango_cli_beta.rag_config import RagConfig


def chat_cli():
    rich_print(
        "[bold]Welcome to the [#d3e0e0]Lang[/#d3e0e0][#beb4fd]Chain[/#beb4fd] [#00ed64]MongoDB[/#00ed64] RAG CLI.[/bold]\n\n"
        + "[bold]Let's start [italic]chatting[/italic].[/bold]\n\n"
    )
    user_config = RagConfig(path_or_config=DEFAULT_CONFIG_PATH)
    chat = Chat(config=user_config, typer=typer)
    chat.chat_loop()
