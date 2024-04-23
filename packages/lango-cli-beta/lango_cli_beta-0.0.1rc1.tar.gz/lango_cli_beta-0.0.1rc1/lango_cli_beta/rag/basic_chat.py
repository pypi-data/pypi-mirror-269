"""Class containing logic for the chat interface"""

from typing import List, Union

import typer as TyperType
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import (
    Runnable,
    RunnableLambda,
    RunnablePassthrough,
)
from rich import print as rich_print
from rich.prompt import Prompt as RichPrompt

from lango_cli_beta.constants import SYSTEM_MESSAGE
from lango_cli_beta.rag.llm_chain import construct_llm_chain
from lango_cli_beta.rag.types import ChatInputType
from lango_cli_beta.rag.utils import (
    _clean_mongo_docs,
    _get_llm,
)
from lango_cli_beta.rag_config import RagConfig
from lango_cli_beta.utils import initialize_vectorstore


def construct_basic_chat_chain(
    llm_chain: Runnable[ChatInputType, str],
    retrieval_chain: Runnable[ChatInputType, str],
) -> Runnable:
    chain = (
        RunnablePassthrough.assign(
            context=lambda x: x["input"][-1]["content"] | retrieval_chain,
        ).with_config(config={"run_name": "retrieval_chain_passthrough"})
        | llm_chain
    )
    return chain


def documents_to_str(docs: List[Document]) -> str:
    """Convert a list of documents into a single string."""

    return "\n".join([doc.page_content for doc in docs])


def clean_and_retrieve_docs(x):
    vectorstore = initialize_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
    input_human_message = x["input"][-1]
    return _clean_mongo_docs(retriever.invoke(input_human_message.content))


def simple_chat_retrieval() -> Runnable[ChatInputType, str]:
    chain = RunnablePassthrough.assign(
        documents=RunnableLambda(lambda x: clean_and_retrieve_docs(x)).with_config(
            config={"run_name": "retrieve_and_clean"}
        )
    ).with_config(config={"run_name": "assign_documents"}) | RunnablePassthrough.assign(
        context=RunnableLambda(lambda x: documents_to_str(x["documents"])).with_config(
            config={"run_name": "documents_to_str"}
        )
    ).with_config(config={"run_name": "assign_context_passthrough"})
    return chain


class BasicChat:
    typer: TyperType

    chat_chain: Runnable

    def __init__(
        self,
        config: RagConfig = None,
        typer: TyperType = None,
    ) -> None:
        self.typer = typer

        llm = _get_llm(config.llm)
        basic_retrieval_chain = simple_chat_retrieval()
        llm_chain = construct_llm_chain(llm, SYSTEM_MESSAGE)

        self.chat_chain = basic_retrieval_chain | llm_chain

    def chat_loop(self):
        first_iter = True
        history: List[Union[HumanMessage, AIMessage, SystemMessage]] = []

        while True:
            prompt_message = (
                "Start chatting here.\nType 'exit' to quit.\n[bold #fce8fc]Human[/bold #fce8fc]"
                if first_iter
                else "\n\n[bold]Human[/bold]"
            )
            if first_iter:
                first_iter = False

            input = RichPrompt.ask(prompt_message)
            self.typer.echo("\n")

            if input == "exit":
                self.typer.echo("Aborting chat.")
                raise self.typer.Exit(0)
            history.append(HumanMessage(content=input))

            final_message = ""
            first_chunk = False
            for message in self.chat_chain.stream({"input": history}):
                if first_chunk is False:
                    first_chunk = True
                    rich_print("[bold]Assistant:[/bold]", end=" ")
                final_message += message
                rich_print(message, end="")

            # Update the message history
            history.append(AIMessage(content=final_message))
