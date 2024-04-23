"""
CLI commands
"""

from typing import Optional, Union

import typer
from rich import print as rich_print

from lango_cli_beta.constants import (
    DEFAULT_CONFIG_PATH,
    JSON_SCHEMA_REQUIRED_MESSAGE,
)
from lango_cli_beta.namespaces.config import (
    _is_json_str_or_file,
    _is_only_txt_files,
    _load_json,
    ingest_data,
)
from lango_cli_beta.rag.ingest import Ingester
from lango_cli_beta.rag_config import RagConfig


def process_fast_entry(
    typer: typer,
    ingest_data_path: Union[str, None] = None,
    metadata: Union[str, None] = None,
    chunk_size: int = 500,
    chunk_overlap: int = 75,
    user_config: RagConfig = None,
    json_schema: Optional[str] = None,
) -> None:
    """Processes the user's fast entry, skipping the interacive prompts.

    Args:
        typer (typer): The typer instance to use for prompting.
        ingest_data_path (str): The path to the data file, or folder with files to ingest.
        metadata (Union[str, None]): The path to the metadata JSON file, or a JSON string.
        chunk_size (int): The size of the chunks to split the data into.
        chunk_overlap (int): The overlap between chunks.
    Returns: None
    """

    if ingest_data_path is None:
        typer.echo("The '--data-path' flag is required when ingesting.")
        raise typer.Exit(1)
    ingest_data_path = ingest_data_path.strip()

    if _is_only_txt_files(ingest_data_path) is False:
        typer.echo("Invalid file type. Please provide a .txt file.")
        raise typer.Exit(1)

    if user_config.rag_type == "query_construction" and json_schema is None:
        typer.echo(JSON_SCHEMA_REQUIRED_MESSAGE)
        raise typer.Exit(1)

    if metadata is not None and _is_json_str_or_file(metadata) is False:
        typer.echo(
            "Invalid metadata input. Please provide a valid JSON file path, or stringified JSON."
        )
        raise typer.Exit(1)

    if json_schema is not None and _is_json_str_or_file(json_schema) is False:
        typer.echo(
            "Invalid JSONSchema input. Please provide a valid JSON file path, or stringified JSON."
        )
        raise typer.Exit(1)

    # Parse the metadata JSON string, or read the JSON file if provided
    if metadata is not None:
        metadata = _load_json(metadata)
    if json_schema is not None:
        json_schema = _load_json(json_schema)

    user_config.ingest_path = ingest_data_path
    user_config.metadata = metadata
    user_config.chunk_size = int(chunk_size)
    user_config.chunk_overlap = int(chunk_overlap)
    user_config.json_schema = json_schema

    user_config.save_config(DEFAULT_CONFIG_PATH)

    rich_print("[bold #00FF00]Ingesting data now.[/bold #00FF00]")
    ingest = Ingester(user_config)
    ingest.ingest_data()


def upsert_cli(
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
    user_config = RagConfig(path_or_config=DEFAULT_CONFIG_PATH)

    if fast:
        # Skip interactive prompt, use provided values
        process_fast_entry(
            typer,
            ingest_data_path=data_path,
            metadata=metadata,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            user_config=user_config,
            json_schema=json_schema,
        )
        return

    rich_print(
        "[bold]Welcome to the [#d3e0e0]Lang[/#d3e0e0][#beb4fd]Chain[/#beb4fd] [#00ed64]MongoDB[/#00ed64] RAG CLI.[/bold]\n\n"
        + "[bold]Let's start [italic]indexing[/italic].[/bold]\n\n"
    )

    # Ingester data now, or later
    user_config = ingest_data(typer, user_config)
    # Save the config file
    user_config.save_config(DEFAULT_CONFIG_PATH)
    rich_print(
        f"[bold #0af2b0]Successfully created new RAG config.[/bold #0af2b0]\nSaved to [italic]{DEFAULT_CONFIG_PATH}[/italic]"
    )
