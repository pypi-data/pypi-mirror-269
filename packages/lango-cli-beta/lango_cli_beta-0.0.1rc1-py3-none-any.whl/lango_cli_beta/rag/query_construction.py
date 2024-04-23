"""Class containing logic for the chat interface"""

from typing import List, Optional, Union

import typer as TyperType
from langchain_cohere import CohereRerank
from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_mongodb import MongoDBAtlasVectorSearch
from langgraph.graph import StateGraph
from langgraph.graph.graph import CompiledGraph
from rich import print as rich_print
from rich.prompt import Prompt as RichPrompt
from typing_extensions import TypedDict

from lango_cli_beta.constants import SYSTEM_MESSAGE
from lango_cli_beta.rag.llm_chain import construct_llm_chain
from lango_cli_beta.rag.utils import _clean_mongo_docs, _get_llm
from lango_cli_beta.rag_config import RagConfig
from lango_cli_beta.utils import initialize_vectorstore


class QueryConstructionState(TypedDict):
    input: HumanMessage
    """The input from the user"""
    json_schema: dict
    # """The JSON schema for the structured output. Provided by the RagConfig"""
    llm: BaseChatModel
    # llm: str1
    """The language model to use"""
    documents: Union[list[Document], None]
    """The raw documents returned from the retrieval step"""
    context: Union[str, None]
    """Stringified documents"""
    filters: Union[dict, None]
    """Filters extracted from the input"""
    system_message: SystemMessage
    """The system message to use for the final generation"""


def graph_documents_to_str(state: QueryConstructionState) -> str:
    """Convert a list of documents into a single string."""

    docs = state["documents"]
    context = "\n".join([doc.page_content for doc in docs])
    return {"context": context}


def rerank_docs(state: QueryConstructionState):
    """Rerank a list of documents using Cohere's 'rerank-english-v3.0'."""
    docs = state["documents"]
    rephrased_query = state["input"]
    reranker = CohereRerank(model="rerank-english-v3.0")

    reranked_docs_output = reranker.rerank(docs, rephrased_query, top_n=10)
    reranked_docs = [docs[doc["index"]] for doc in reranked_docs_output]

    return {"documents": reranked_docs}


def _convert_openai_filters_to_mongo(filters: Union[dict, None]) -> Union[dict, None]:
    """
    Converts filters returned from an OpenAI function call into filters MongoDB can accept.

    Args:
        filters (Union[dict, None]): The filters returned from an OpenAI function call.

    Returns:
        Union[dict, None]: The converted filters that MongoDB can accept, or None if the input filters are None.
    """
    if filters is None:
        return None

    mongo_filters = {}
    for key, value in filters.items():
        mongo_filters[key] = {"$eq": value}

    return mongo_filters


def extract_filters_chain(
    state: QueryConstructionState, config: Optional[RunnableConfig]
):
    llm: BaseChatModel = config["configurable"]["llm"]
    json_schema = state["json_schema"]
    model_with_tools = llm.with_structured_output(json_schema)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant.\n"
                + "You are provided with a given query by the user, along with a tool you"
                + "can use to extract specific information from the query.\n"
                + "Do not make information up.",
            ),
            ("human", "<query>{input}</query>"),
        ]
    )
    extract_filters_chain = prompt | model_with_tools
    filters = extract_filters_chain.invoke({"input": state["input"]})
    return {
        "filters": filters,
    }


def retrieve_docs(state: QueryConstructionState):
    vectorstore = initialize_vectorstore()
    input = state["input"]
    filters = state["filters"]

    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 30,
            "pre_filter": _convert_openai_filters_to_mongo(filters),
        }
    )
    documents = retriever.invoke(input)
    # Remove the _id field inserted by MongoDB from the metadata
    cleaned_documents = _clean_mongo_docs(documents)
    return {"documents": cleaned_documents}


def rephrase_query_chain(
    state: QueryConstructionState, config: Optional[RunnableConfig]
):
    """Given an original query and any filters which are applied to the
    retrieval step, rephrase the query to not include any mention of the filters."""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an advanced question asker.\n"
                + "You are presented with a query from a user which was used to perform a semantic search. The query mentioned some specifics which were used to filter results in the semantic search."
                + "Your task is to rephrase the users query without any mention of the filters.\n"
                + "Here is a list of filters that were applied to the query:\n"
                + "<filters>\n{raw_filters}\n</filters>\n"
                + "Respond with ONLY a string containing the rephrased query, and no other content.",
            ),
            ("human", "<query>{input}</query>"),
        ]
    )

    input = state["input"]
    llm: BaseChatModel = config["configurable"]["llm"]
    raw_filters = state["filters"]
    rephrase_query_chain = prompt | llm | StrOutputParser()
    rephrased_query = rephrase_query_chain.invoke(
        {"input": input, "raw_filters": raw_filters}
    )
    return {"input": rephrased_query}


def retrieve_or_rephrase_conditional(state: QueryConstructionState) -> str:
    if state["filters"] is not None:
        return "rephrase_query"
    return "retrieval"


def construct_query_construction_graph():
    workflow = StateGraph(QueryConstructionState)

    workflow.add_node("extract_filters", extract_filters_chain)
    workflow.add_node("retrieval", retrieve_docs)
    workflow.add_node("rephrase_query", rephrase_query_chain)

    workflow.add_conditional_edges("extract_filters", retrieve_or_rephrase_conditional)
    workflow.add_edge("rephrase_query", "retrieval")

    workflow.add_node("rerank_docs", rerank_docs)
    workflow.add_edge("retrieval", "rerank_docs")

    workflow.add_node("docs_to_str", graph_documents_to_str)
    workflow.add_edge("rerank_docs", "docs_to_str")

    workflow.set_entry_point("extract_filters")
    workflow.set_finish_point("docs_to_str")

    app = workflow.compile()
    return app


def prettify_graph_output(output: dict) -> str:
    if "extract_filters" in output and len(output["extract_filters"].keys()) != 0:
        filters = output["extract_filters"]["filters"]
        return f"[bold]Step: [#ff6e5e]Extract Filters[/#ff6e5e][/bold]\n[bold #fcd63a]Filters:[/bold #fcd63a] {filters}\n"
    if "rephrase_query" in output:
        return f"[bold]Step: [#ff6e5e]Rephrase Query[/#ff6e5e][/bold]\n[bold #fcd63a]Rephrased Query:[/bold #fcd63a] {output['rephrase_query']['input']}\n"
    if "retrieval" in output:
        docs_len = len(output["retrieval"]["documents"])
        return f"[bold]Step: [#ff6e5e]Retrieved Documents[/#ff6e5e][/bold]\n[bold #fcd63a]Num docs:[/bold #fcd63a] {docs_len}\n"
    if "rerank_docs" in output:
        docs_len = len(output["rerank_docs"]["documents"])
        return f"[bold]Step: [#ff6e5e]Reranked Documents[/#ff6e5e][/bold]\n[bold #fcd63a]Num docs:[/bold #fcd63a] {docs_len}\n"
    if "docs_to_str" in output:
        return "[bold]Step: [#ff6e5e]Convert Docs to String[/#ff6e5e][/bold]\n"


def update_final_graph_output(output: dict, final_graph_output: dict) -> dict:
    if "rephrase_query" in output:
        final_graph_output["input"] = [
            HumanMessage(content=output["rephrase_query"]["input"])
        ]
    if "docs_to_str" in output:
        final_graph_output["context"] = output["docs_to_str"]["context"]
    return final_graph_output


class QueryConstruction:
    config: RagConfig

    typer: TyperType

    query_construction_graph: CompiledGraph

    llm_chain: Runnable

    llm: BaseChatModel

    vectorstore: MongoDBAtlasVectorSearch

    def __init__(
        self,
        config: RagConfig = None,
        typer: TyperType = None,
    ) -> None:
        self.config = config
        self.typer = typer

        self.vectorstore = initialize_vectorstore()
        self.llm = _get_llm(config.llm)
        self.query_construction_graph = construct_query_construction_graph()
        self.llm_chain = construct_llm_chain(self.llm, SYSTEM_MESSAGE)

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
            input_human_message = HumanMessage(content=input)

            final_message = ""
            final_graph_output = {
                "history": history,
                "input": [input_human_message],
                "context": "",
            }
            first_chunk = False
            for message in self.query_construction_graph.stream(
                {
                    "input": input_human_message,
                    "json_schema": self.config.json_schema,
                },
                {"configurable": {"llm": self.llm}},
            ):
                rich_print(prettify_graph_output(message))
                final_graph_output = update_final_graph_output(
                    message, final_graph_output
                )

            for stream_item in self.llm_chain.stream(final_graph_output):
                if first_chunk is False:
                    first_chunk = True
                    rich_print("[bold]Assistant:[/bold]", end=" ")
                final_message += stream_item
                rich_print(stream_item, end="")

            # Update the message history
            new_messages = [
                input_human_message,
                AIMessage(content=final_message),
            ]
            history.extend(new_messages)
