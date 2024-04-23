import json
import os
from typing import Literal

import typer
from rich import print as rich_print
from rich.prompt import Prompt as RichPrompt

from lango_cli_beta.rag.ingest import Ingester
from lango_cli_beta.rag_config import RagConfig


def _is_only_txt_files(path: str) -> bool:
    """Whether or not a given file is .txt, or all files in a folder
    are .txt files."""
    if os.path.isfile(path):
        return path.endswith(".txt")
    elif os.path.isdir(path):
        return all(file.endswith(".txt") for file in os.listdir(path))


def _is_json_str_or_file(path: str) -> bool:
    """Whether or not a given file is a .json file, or a JSON string."""
    if path.endswith(".json"):
        return True
    try:
        json.loads(path)
        return True
    except json.JSONDecodeError:
        return False


def _does_file_exist(file_path: str) -> bool:
    """Whether or not a given file exists."""
    return os.path.exists(file_path)


def _load_json(metadata_or_path: str) -> dict:
    """Load metadata from a JSON file, or a JSON string."""
    if metadata_or_path.endswith(".json"):
        with open(metadata_or_path, "r") as f:
            metadata = json.load(f)
    else:
        metadata = json.loads(metadata_or_path)
    return metadata


def get_chunking_data(typer: typer) -> dict:
    chunk_size = RichPrompt.ask(
        "What chunk size do you want to use?\nPress enter to use the default [bold #d5b6f0][500][/bold #d5b6f0]",
        default=500,
    )
    rich_print(f"Selected chunk size: [bold]{chunk_size}[/bold]")
    typer.echo("\n")
    chunk_overlap = RichPrompt.ask(
        "What chunk overlap do you want to use?\nPress enter to use the default [bold #d5b6f0][75][/bold #d5b6f0]",
        default=75,
    )
    rich_print(f"Selected chunk overlap: [bold]{chunk_overlap}[/bold]")
    typer.echo("\n")
    return {
        "chunk_size": int(chunk_size),
        "chunk_overlap": int(chunk_overlap),
    }


def recursive_verify_or_prompt_json(
    typer: typer, json_or_path: str, is_metadata: bool = None
) -> str:
    prompt_str = "metadata" if is_metadata else "JSONSchema"
    is_valid = _is_json_str_or_file(json_or_path)

    if is_valid is False:
        json_or_path = typer.prompt(
            f"Invalid file type(s)/{prompt_str} string.\nPlease enter either the path to the .json file containing {prompt_str}, or valid stringified JSON with {prompt_str}",
            default=None,
        )
        return recursive_verify_or_prompt_json(typer, json_or_path)
    else:
        return _load_json(json_or_path)


def get_ingest_path_and_json(
    typer: typer, rag_type: Literal["basic", "query_construction"]
) -> dict:
    """Prompts the user for the path to the data file they want to ingest,
    along with any metadata and JSONSchema, if required.

    Args:
        typer (typer): The typer instance to use for prompting.
        rag_type (Literal["basic", "query_construction"]): The RAG type.
    Returns:
        dict: A dictionary containing the ingest path, metadata and JSONSchema.
    """

    ingest_data_path = typer.prompt(
        "Enter the path to the data file, or folder you want to ingest"
    )
    ingest_data_path = ingest_data_path.strip()

    # Verify file exists & is a .txt file
    if _is_only_txt_files(ingest_data_path) is False:
        typer.echo(
            "Invalid file type(s).\nPlease provide either a single .txt file path, or a folder containing only .txt files."
        )
        raise typer.Exit(1)

    if _does_file_exist(ingest_data_path) is False:
        typer.echo("File does not exist. Please provide a valid path.")
        raise typer.Exit(1)

    typer.echo("\n")

    metadata_or_path = typer.prompt(
        "Enter either the path to the .json file containing metadata, or valid stringified JSON with metadata. (optional)",
        default="",
    )
    metadata_or_path = None if metadata_or_path == "" else metadata_or_path
    # Pre-instantiate metadata variable
    metadata = None
    if metadata_or_path is not None:
        metadata = recursive_verify_or_prompt_json(
            typer, metadata_or_path, is_metadata=True
        )

    typer.echo("\n")

    # Pre-instantiate JSONSchema variable
    json_schema = None
    if rag_type == "query_construction" and metadata is not None:
        # Only request JSONSchema if metadata is provided, and RAG type is query_construction
        json_schema_or_path = typer.prompt(
            "Enter either the path to the .json file containing JSONSchema, or valid stringified JSON with JSONSchema. (required)",
        )
        json_schema = recursive_verify_or_prompt_json(
            typer, json_schema_or_path, is_metadata=False
        )

        typer.echo("\n")

    return {
        "ingest_data_path": ingest_data_path,
        "metadata": metadata,
        "json_schema": json_schema,
    }


def ingest_data(typer: typer, user_config: RagConfig) -> RagConfig:
    """Ingests data into the MongoDB vector store.

    Args:
        typer (typer): The typer instance to use for prompting.
        user_config (dict): The user's configuration.
    Returns:
        dict: The updated user configuration.
    """

    # Optionally prompt for chunking data
    chunking_data = get_chunking_data(typer)
    user_config.chunk_size = int(chunking_data["chunk_size"])
    user_config.chunk_overlap = int(chunking_data["chunk_overlap"])
    # Prompt for the path to the data file
    ingest_and_json = get_ingest_path_and_json(typer, user_config.rag_type)
    user_config.ingest_path = ingest_and_json["ingest_data_path"]
    user_config.metadata = ingest_and_json["metadata"]
    user_config.json_schema = ingest_and_json["json_schema"]

    rich_print("[bold #00FF00]Ingesting data now.[/bold #00FF00]")
    ingest = Ingester(user_config)
    ingest.ingest_data()

    return user_config
