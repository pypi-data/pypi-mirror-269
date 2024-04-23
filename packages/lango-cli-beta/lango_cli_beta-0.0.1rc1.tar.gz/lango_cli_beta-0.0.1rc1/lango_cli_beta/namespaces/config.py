"""
CLI commands
"""

from typing import Optional, Union

import typer
from rich import print as rich_print
from rich.prompt import Confirm as RichConfirm
from rich.prompt import Prompt as RichPrompt

from lango_cli_beta.constants import (
    CLI_INVOKE_NAME,
    DEFAULT_CONFIG_PATH,
    JSON_SCHEMA_REQUIRED_MESSAGE,
)
from lango_cli_beta.namespaces.utils import (
    _is_json_str_or_file,
    _is_only_txt_files,
    _load_json,
    ingest_data,
)
from lango_cli_beta.rag.ingest import Ingester
from lango_cli_beta.rag_config import RagConfig

DEFAULT_CONFIG = {
    "rag_type": "basic",
    "llm": "anthropic",
    "chunk_size": 500,
    "chunk_overlap": 75,
}
RAG_CANDIDATE_OPTIONS = [
    {
        "name": "Basic RAG",
        "value": "basic",
    },
    {
        "name": "Query Construction RAG",
        "value": "query_construction",
    },
]
LLM_OPTIONS = [
    {
        "name": "Anthropic (Claude 3 Opus)",
        "value": "claude_3_opus",
    },
    {
        "name": "OpenAI (GPT-4 Turbo)",
        "value": "gpt_4_turbo",
    },
    {
        "name": "Cohere (Command R)",
        "value": "command_r",
    },
    {
        "name": "Mistral (Mistral-Large)",
        "value": "mistral_large",
    },
    {
        "name": "Google (Gemini Pro)",
        "value": "gemini_pro",
    },
    {
        "name": "Mixtral-8x7b",
        "value": "fireworks_mixtral_8x7b",
    },
]


def get_llm(typer: typer) -> dict:
    """Prompts the user for the LLM to use.

    Args:
        typer (typer): The typer instance to use for prompting.
    Returns:
        str: The LLM to use.
    """

    llm_options_prompt = "\n".join(
        f"  [bold][{i}]: {option['name']}[/bold]"
        for i, option in enumerate(LLM_OPTIONS, start=1)
    )
    llm_choice = RichPrompt.ask(
        f"What LLM do you want to use?\n\n{llm_options_prompt}\n\nEnter the number of the LLM provider to use. E.g. '[bold]1[/bold]' for anthropic"
    )
    selected_llm = LLM_OPTIONS[int(llm_choice.strip()) - 1]
    rich_print(f"Selected LLM: [bold]{selected_llm['name']}[/bold]")
    typer.echo("\n")
    return selected_llm


def process_fast_entry(
    typer: typer,
    rag_type: str = "",
    llm: str = "",
    ingest_data_path: Union[str, None] = None,
    metadata: Union[str, None] = None,
    chunk_size: int = 500,
    chunk_overlap: int = 75,
    json_schema: Optional[str] = None,
) -> None:
    """Processes the user's fast entry, skipping the interactive prompts.

    Args:
        typer (typer): The typer instance to use for prompting.
        rag_type (str): The RAG type.
        llm (str): The LLM to use.
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

    if (rag_type not in [option["value"] for option in RAG_CANDIDATE_OPTIONS]) or (
        LLM_OPTIONS[int(llm) - 1] is None
    ):
        typer.echo("Invalid input. Please provide valid values.")
        raise typer.Exit(1)

    if rag_type == "query_construction" and json_schema is None:
        typer.echo(JSON_SCHEMA_REQUIRED_MESSAGE)
        raise typer.Exit(1)

    if _is_only_txt_files(ingest_data_path) is False:
        typer.echo("Invalid file type. Please provide a .txt file.")
        raise typer.Exit(1)

    if metadata is not None and _is_json_str_or_file(metadata) is False:
        typer.echo(
            "Invalid metadata input. Please provide either a .json file, or a JSON string."
        )
        raise typer.Exit(1)

    if json_schema is not None and _is_json_str_or_file(json_schema) is False:
        typer.echo(
            "Invalid metadata input. Please provide either a .json file, or a JSON string."
        )
        raise typer.Exit(1)

    # Parse the metadata/JSONSchema JSON string, or read the JSON file if provided
    if metadata is not None:
        metadata = _load_json(metadata)
    if json_schema is not None:
        json_schema = _load_json(json_schema)

    user_config = RagConfig(
        path_or_config={
            "rag_type": rag_type,
            "llm": LLM_OPTIONS[int(llm)]["value"],
            "ingest_path": ingest_data_path,
            "metadata": metadata,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "json_schema": json_schema,
        }
    )
    user_config.save_config(DEFAULT_CONFIG_PATH)

    # Ingest data from file/folder
    ingest = Ingester(user_config)
    ingest.ingest_data()
    rich_print(
        f"[bold #0af2b0]Successfully created new RAG config.[/bold #0af2b0]\nSaved to [italic]{DEFAULT_CONFIG_PATH}[/italic]"
    )


def _get_llm_prompt() -> str:
    llm_options_prompt = "\n".join(
        f"[{i}]: {option['name']}" for i, option in enumerate(LLM_OPTIONS, start=1)
    )
    return llm_options_prompt


def config_cli(
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
    if fast:
        # Skip interactive prompt, use provided values
        process_fast_entry(
            typer,
            ingest_data_path=data_path,
            rag_type=rag_type,
            llm=llm,
            metadata=metadata,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            json_schema=json_schema,
        )
        return

    rich_print(
        "[bold]Welcome to the [#d3e0e0]Lang[/#d3e0e0][#beb4fd]Chain[/#beb4fd] [#00ed64]MongoDB[/#00ed64] RAG CLI.[/bold]\n\n"
        + "[bold]Let's [italic]get started[/italic].[/bold]\n\n"
    )

    user_config = RagConfig(path_or_config=DEFAULT_CONFIG)

    candidate_choice = RichPrompt.ask(
        "What candidate config do you want?\n"
        + f"\n  [bold][1]: {RAG_CANDIDATE_OPTIONS[0]['name']}[/bold]"
        + f"\n  [bold][2]: {RAG_CANDIDATE_OPTIONS[1]['name']}[/bold]\n\nEnter 1, or 2",
    )

    int_candidate_choice = int(candidate_choice.strip()) - 1
    if int_candidate_choice != 0 and int_candidate_choice != 1:
        typer.echo("Invalid choice. Please select a valid option.")
        raise typer.Exit(1)

    # Assign the user selection to the user_config
    user_config.rag_type = RAG_CANDIDATE_OPTIONS[int_candidate_choice]["value"]
    # Print the user selection
    rich_print(
        f"Using: [bold]{RAG_CANDIDATE_OPTIONS[int_candidate_choice]['name']}[bold]"
    )
    typer.echo("\n")

    # Query Construction RAG selected, prompt for LLM
    user_config.llm = get_llm(typer)["value"]

    # Save config before ingesting data
    user_config.save_config(DEFAULT_CONFIG_PATH)

    # Ingest data now, or later
    ingest_now = RichConfirm.ask("Do you want to ingest the data now?")
    if ingest_now:
        typer.echo("\n")
        user_config = ingest_data(typer, user_config)
    else:
        rich_print(
            f"""Data can be ingested later via "[bold #00FF00]{CLI_INVOKE_NAME} upsert[/bold #00FF00]".\n"""
        )
    # Save the config file
    user_config.save_config(DEFAULT_CONFIG_PATH)
    rich_print(
        f"[bold #0af2b0]Successfully created new RAG config.[/bold #0af2b0]\nSaved to [italic]{DEFAULT_CONFIG_PATH}[/italic]"
    )
