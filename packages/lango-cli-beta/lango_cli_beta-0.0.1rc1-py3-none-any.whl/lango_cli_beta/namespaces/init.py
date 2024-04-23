"""
CLI commands
"""

import json
import shutil
from pathlib import Path
from typing import Optional

import typer
from rich import print as rich_print

from lango_cli_beta.constants import (
    CLI_INVOKE_NAME,
    DEFAULT_CONFIG_FILE_NAME,
    DEFAULT_RAG_CONFIG,
    GET_IP_AND_START_FILE_NAME,
    GET_IP_AND_START_SCRIPT,
    SAMPLE_DATA_FOLDER_NAME,
)


def init_cli(
    project_name: str,
    no_sample_data: Optional[bool] = typer.Option(
        None,
        help="Pass this flag to skip copying the sample data folder.",
    ),
):
    # strip all non-alphanumeric characters from the project name, and make lowercase
    clean_project_name = "".join(e for e in project_name if e.isalnum()).lower()
    # Create a new directory with the project name
    project_dir = Path(clean_project_name)
    project_dir.mkdir(exist_ok=False)

    # write a new config file with the default RAG config
    with open(project_dir / DEFAULT_CONFIG_FILE_NAME, "w") as f:
        f.write(json.dumps(DEFAULT_RAG_CONFIG))

    # write the get IP & start script
    with open(project_dir / GET_IP_AND_START_FILE_NAME, "w") as f:
        f.write(GET_IP_AND_START_SCRIPT)

    if no_sample_data is None or not no_sample_data:
        sample_data_dir = project_dir / SAMPLE_DATA_FOLDER_NAME
        sample_data_dir.mkdir(exist_ok=True)
        # Copy a folder with sample data into the new project directory
        project_template_dir = Path(__file__).parents[1] / SAMPLE_DATA_FOLDER_NAME
        shutil.copytree(project_template_dir, sample_data_dir, dirs_exist_ok=True)
        rich_print(
            f"Created sample data directory at [bold]{clean_project_name}/{SAMPLE_DATA_FOLDER_NAME}[/bold]"
        )

    rich_print(
        f"Initialized new project: [#2ae84d]{project_name}[/#2ae84d]"
        + "\n"
        + f"Config file created at [bold]{clean_project_name}/{DEFAULT_CONFIG_FILE_NAME}[/bold]"
    )
    rich_print(
        f"""Navigate to the project directory ("[bold italic]cd ./{clean_project_name}[/bold italic]") and run "[bold italic]{CLI_INVOKE_NAME} config[/bold italic]" to configure."""
    )
