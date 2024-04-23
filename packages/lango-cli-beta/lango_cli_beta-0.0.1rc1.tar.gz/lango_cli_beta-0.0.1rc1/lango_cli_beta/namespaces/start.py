"""
CLI commands
"""

import uvicorn
from fastapi import FastAPI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableLambda, RunnablePassthrough
from langserve import add_routes

from lango_cli_beta.constants import (
    DEFAULT_CONFIG_PATH,
    SYSTEM_MESSAGE,
)
from lango_cli_beta.rag.basic_chat import (
    construct_llm_chain,
    simple_chat_retrieval,
)
from lango_cli_beta.rag.query_construction import (
    construct_query_construction_graph,
)
from lango_cli_beta.rag.types import ChatInputType
from lango_cli_beta.rag.utils import _get_llm
from lango_cli_beta.rag_config import RagConfig


def construct_basic_rag_runnable(llm: str) -> Runnable[ChatInputType, str]:
    llm = _get_llm(llm)
    basic_retrieval_chain = simple_chat_retrieval()
    llm_chain = construct_llm_chain(llm, SYSTEM_MESSAGE)
    chat_chain = basic_retrieval_chain | llm_chain
    return chat_chain.with_types(input_type=ChatInputType)


def construct_query_construction_runnable(
    llm: str, json_schema: dict
) -> Runnable[ChatInputType, str]:
    model = _get_llm(llm)
    query_construction_graph = construct_query_construction_graph()
    llm_chain = construct_llm_chain(model, SYSTEM_MESSAGE)

    chain = (
        RunnableLambda(
            lambda x: query_construction_graph.invoke(
                {"input": x["input"], "json_schema": json_schema},
                {
                    "configurable": {
                        "llm": model,
                    }
                },
            )
        ).with_config(config={"run_name": "query_construction_graph"})
        | RunnablePassthrough.assign(
            input=lambda x: [HumanMessage(content=x["input"])]
        ).with_config(config={"run_name": "convert_str_human_message"})
        | llm_chain
        | StrOutputParser()
    ).with_types(input_type=ChatInputType)
    return chain


def create_runnable(rag_config: RagConfig) -> Runnable[ChatInputType, str]:
    rag_type = rag_config.rag_type
    llm = rag_config.llm
    json_schema = rag_config.json_schema
    if rag_type == "query_construction":
        return construct_query_construction_runnable(llm, json_schema)
    else:
        return construct_basic_rag_runnable(llm)


def start_cli():
    user_config = RagConfig(path_or_config=DEFAULT_CONFIG_PATH)
    app = FastAPI(
        title="LangChain Server",
        version="1.0",
        description="A simple api server using Langchain's Runnable interfaces",
    )

    add_routes(app, create_runnable(user_config), path="/chat", playground_type="chat")
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
