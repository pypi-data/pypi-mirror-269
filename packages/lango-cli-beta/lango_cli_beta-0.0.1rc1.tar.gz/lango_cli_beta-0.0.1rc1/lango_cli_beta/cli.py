# File containing logic for CLI
from typing import Optional

import typer
from dotenv import load_dotenv

from lango_cli_beta.constants import CLI_INVOKE_NAME
from lango_cli_beta.namespaces.chat import chat_cli
from lango_cli_beta.namespaces.config import _get_llm_prompt, config_cli
from lango_cli_beta.namespaces.export import export_cli
from lango_cli_beta.namespaces.ingest import upsert_cli
from lango_cli_beta.namespaces.init import init_cli
from lango_cli_beta.namespaces.start import start_cli

__version__ = "0.0.1"

__app_name__ = CLI_INVOKE_NAME

# Load environment variables from .env file
load_dotenv()

app = typer.Typer(no_args_is_help=True, add_completion=False)


def version_callback(show_version: bool) -> None:
    if show_version:
        typer.echo(f"lango-cli {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Print the current CLI version.",
        callback=version_callback,
        is_eager=True,
    ),
):
    pass


@app.command()
def config(
    fast: Optional[bool] = typer.Option(
        False, help="Pass this flag to skip the interactive prompts."
    ),
    data_path: Optional[str] = typer.Option(
        None, help="The path to the data folder or file to ingest."
    ),
    rag_type: Optional[str] = typer.Option(
        "basic",
        help="The type of RAG to create. Options: 'basic', 'query_construction'",
    ),
    llm: Optional[str] = typer.Option(
        "1", help=f"The LLM to use. Options: {_get_llm_prompt()}"
    ),
    metadata: Optional[str] = typer.Option(
        None,
        help="The path to the metadata JSON file, or a JSON string.",
    ),
    json_schema: Optional[str] = typer.Option(
        None,
        help="Valid JSONSchema to be used in query construction. Either a path to a .json file, or a stringified version. All fields should be optional. Required if using 'query_construction' RAG.",
    ),
    chunk_size: Optional[int] = typer.Option(
        500, help="The size of the chunks to split the data into."
    ),
    chunk_overlap: Optional[int] = typer.Option(75, help="The overlap between chunks."),
):
    config_cli(
        fast, data_path, rag_type, llm, metadata, json_schema, chunk_size, chunk_overlap
    )


@app.command()
def upsert(
    fast: Optional[bool] = typer.Option(
        False, help="Pass this flag to skip the interactive prompts."
    ),
    data_path: str = typer.Option(
        None, help="The path to the data folder or file to ingest."
    ),
    metadata: Optional[str] = typer.Option(
        None,
        help="The path to the metadata JSON file, or a JSON string.",
    ),
    json_schema: Optional[str] = typer.Option(
        None,
        help="Valid JSONSchema to be used in query construction. Either a path to a .json file, or a stringified version. All fields should be optional. Required if using 'query_construction' RAG.",
    ),
    chunk_size: Optional[int] = typer.Option(
        500, help="The size of the chunks to split the data into."
    ),
    chunk_overlap: Optional[int] = typer.Option(75, help="The overlap between chunks."),
):
    upsert_cli(fast, data_path, metadata, json_schema, chunk_size, chunk_overlap)


@app.command()
def chat():
    chat_cli()


@app.command()
def start():
    start_cli()


@app.command()
def export():
    export_cli()


@app.command()
def init(
    project_name: str = typer.Argument(..., help="Name of the project"),
    no_sample_data: Optional[bool] = typer.Option(
        None,
        help="Pass this flag to skip copying the sample data folder.",
    ),
):
    init_cli(project_name, no_sample_data)


if __name__ == "__main__":
    app()
