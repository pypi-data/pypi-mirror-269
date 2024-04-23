"""Class containing logic for the chat interface"""

from typing import Union

import typer as TyperType

from lango_cli_beta.rag.basic_chat import BasicChat
from lango_cli_beta.rag.query_construction import QueryConstruction
from lango_cli_beta.rag_config import RagConfig


class Chat:
    config: RagConfig

    typer: TyperType

    basic_chat_chain: Union[BasicChat, None] = None

    query_construction: Union[QueryConstruction, None] = None

    def __init__(
        self,
        config: RagConfig = None,
        typer: TyperType = None,
    ) -> None:
        self.config = config
        self.typer = typer

        if config.rag_type == "query_construction":
            self.query_construction = QueryConstruction(config=config, typer=typer)
        else:
            self.basic_chat_chain = BasicChat(config=config, typer=typer)

    def chat_loop(self):
        if self.query_construction is not None:
            self.query_construction.chat_loop()
        elif self.basic_chat_chain is not None:
            self.basic_chat_chain.chat_loop()
        else:
            raise ValueError("No chat chain found.")
