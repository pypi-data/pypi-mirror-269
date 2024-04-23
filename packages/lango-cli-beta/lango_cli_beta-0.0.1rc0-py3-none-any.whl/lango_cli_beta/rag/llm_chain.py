from typing import List, Union

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable, RunnablePassthrough

from lango_cli_beta.rag.types import ChatInputType


def format_messages(
    input: List[Union[HumanMessage, AIMessage, SystemMessage]], context: str
) -> List[Union[HumanMessage, AIMessage, SystemMessage]]:
    new_input = input[:-1]  # Create a new list without the last item
    last_message = input[-1]
    last_message.content = (
        f"<context>\n{context}\n</context>\n<query>\n{last_message.content}\n</query>"
    )
    new_input.append(last_message)
    return new_input


def construct_llm_chain(
    llm: BaseChatModel, system_message: SystemMessage
) -> Runnable[ChatInputType, str]:
    prompt = ChatPromptTemplate.from_messages(
        [
            system_message,
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    chain = (
        RunnablePassthrough.assign(
            messages=lambda x: format_messages(x["input"], x["context"])
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain.with_config(config={"run_name": "llm_chain"})
